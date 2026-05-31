"""
cycle_dating.py
==============
Fechado de las fases del ciclo del precio del cobre (OE5).

Implementa una versión del algoritmo de puntos de giro tipo
**Bry-Boschan / Harding-Pagan (BBQ)**:
1. Identifica máximos y mínimos locales en una ventana +-k.
2. Fuerza alternancia pico/valle.
3. Impone duración mínima de fase y de ciclo (censura).
El resultado es una serie de FASE: 'expansion' (valle->pico) y 'contraccion' (pico->valle),
que luego se cruza con los modelos (dummies/interacciones) para evaluar estabilidad.

Referencias metodológicas: Bry & Boschan (1971); Harding & Pagan (2002).

IMPORTANTE: el ciclo se fecha sobre el PRECIO DEL COBRE, no sobre las acciones
(evita circularidad). Trabaja sobre el log-nivel del precio.
"""

from __future__ import annotations
import numpy as np
import pandas as pd


def _candidatos_turning_points(x: np.ndarray, k: int):
    """Máximos y mínimos locales en ventana +-k. Devuelve (idx_pico, idx_valle)."""
    n = len(x)
    picos, valles = [], []
    for t in range(k, n - k):
        ventana = x[t - k: t + k + 1]
        if x[t] == ventana.max() and np.argmax(ventana) == k:
            picos.append(t)
        if x[t] == ventana.min() and np.argmin(ventana) == k:
            valles.append(t)
    return picos, valles


def _alternar(picos, valles, x):
    """Fuerza alternancia pico/valle; ante dos consecutivos del mismo tipo,
    conserva el más extremo."""
    marcas = [(t, "P") for t in picos] + [(t, "V") for t in valles]
    marcas.sort()
    limpio = []
    for t, tipo in marcas:
        if not limpio:
            limpio.append((t, tipo))
            continue
        t0, tipo0 = limpio[-1]
        if tipo == tipo0:
            # mismo tipo consecutivo: quedarse con el extremo correcto
            if tipo == "P":
                if x[t] > x[t0]:
                    limpio[-1] = (t, tipo)
            else:
                if x[t] < x[t0]:
                    limpio[-1] = (t, tipo)
        else:
            limpio.append((t, tipo))
    return limpio


def _censura(marcas, min_fase, min_ciclo):
    """Elimina fases más cortas que min_fase y ciclos más cortos que min_ciclo."""
    cambios = True
    while cambios and len(marcas) > 2:
        cambios = False
        for i in range(1, len(marcas)):
            if marcas[i][0] - marcas[i - 1][0] < min_fase:
                # fase demasiado corta -> elimina la marca menos extrema del par
                del marcas[i]
                cambios = True
                break
    return marcas


def datar_ciclo_cobre(precio: pd.Series, k: int = 6,
                      min_fase: int = 6, min_ciclo: int = 15,
                      log: bool = True) -> pd.DataFrame:
    """
    Fecha el ciclo del precio del cobre.

    Parameters
    ----------
    precio : Serie del precio del cobre (index temporal, frecuencia base, p. ej. mensual).
    k      : semiventana para puntos de giro (6 meses es estándar para datos mensuales).
    min_fase  : duración mínima de una fase (en períodos).
    min_ciclo : duración mínima pico-a-pico (en períodos).
    log    : usar log del precio (recomendado).

    Returns
    -------
    DataFrame con columnas:
      - 'precio'
      - 'turning_point': 'P' (pico), 'V' (valle) o NaN
      - 'fase': 'expansion' (valle->pico) | 'contraccion' (pico->valle)
    """
    s = precio.dropna().astype(float)
    x = np.log(s.values) if log else s.values

    picos, valles = _candidatos_turning_points(x, k)
    marcas = _alternar(picos, valles, x)
    marcas = _censura(marcas, min_fase, min_ciclo)

    out = pd.DataFrame({"precio": s})
    out["turning_point"] = pd.Series(np.nan, index=s.index, dtype="object")
    tp_loc = out.columns.get_loc("turning_point")
    for t, tipo in marcas:
        out.iloc[t, tp_loc] = tipo

    # Construir la fase entre puntos de giro
    fase = pd.Series(index=s.index, dtype="object")
    for i in range(1, len(marcas)):
        t0, tipo0 = marcas[i - 1]
        t1, _ = marcas[i]
        etiqueta = "expansion" if tipo0 == "V" else "contraccion"
        fase.iloc[t0:t1] = etiqueta
    # extremos: rellenar bordes con la fase contigua
    fase = fase.ffill().bfill()
    out["fase"] = fase.values
    return out


def agregar_dummy_fase(panel: pd.DataFrame, fechado: pd.DataFrame,
                       col_fecha_level: str = "fecha") -> pd.DataFrame:
    """
    Une la fase del ciclo al panel (MultiIndex empresa, fecha) y crea
    la dummy 'exp' = 1 en expansión, 0 en contracción, lista para interacciones (OE5).
    """
    fase = fechado["fase"]
    panel = panel.copy()
    fechas = panel.index.get_level_values(col_fecha_level)
    panel["fase"] = fase.reindex(fechas).values
    panel["exp"] = (panel["fase"] == "expansion").astype(int)
    return panel


if __name__ == "__main__":
    # Smoke test: precio sintético con un ciclo claro (seno) + tendencia + ruido.
    n = 180
    t = np.arange(n)
    serie = 100 * np.exp(0.002 * t) * (1 + 0.3 * np.sin(2 * np.pi * t / 48))
    idx = pd.period_range("2008-01", periods=n, freq="M").to_timestamp("M")
    precio = pd.Series(serie, index=idx, name="cobre")
    res = datar_ciclo_cobre(precio, k=6, min_fase=6, min_ciclo=15)
    print("Puntos de giro detectados:")
    print(res.loc[res["turning_point"].notna(), ["precio", "turning_point"]])
    print("\nDistribución de fases:")
    print(res["fase"].value_counts())
