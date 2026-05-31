"""
build_panel.py
=============
Orquesta la construcción del dataset final a partir de los datos crudos en
data/interim/ (+ las series locales del BCCh en data/raw/ cuando estén disponibles).

Produce:
- data/processed/panel.parquet    -> formato long (empresa, fecha) para OE2/OE5 (panel FE).
- data/processed/series.parquet   -> formato wide a nivel agregado para OE3/OE4 (cartera + macro).

Reglas (Frente 4):
- Frecuencia base mensual (fin de mes).
- Precios -> retorno log. Macro I(1) -> diferencia (Δ o Δlog). Macro I(0) -> nivel.
- Contables trimestrales -> ffill con rezago de publicación (se incorporan si existen).
- Maneja con elegancia la AUSENCIA de series del BCCh: solo incluye lo disponible y avisa.
"""

from __future__ import annotations
import numpy as np
import pandas as pd

from . import config as C
from . import transformations as T
from . import cycle_dating as cd


# Variables macro que entran en DIFERENCIA (son I(1) en nivel; confirmar con OE1).
MACRO_EN_DIFERENCIA_LOG = ["cobre", "usdclp", "actividad_local", "ipc_local"]  # Δlog
MACRO_EN_DIFERENCIA = ["vix", "fed_funds", "treasury10", "tpm", "embi",
                       "tasa_local"]                   # Δ nivel
MACRO_EN_NIVEL = ["imacec"]                            # si resulta I(0); revisar OE1


def _cargar_interim():
    """Carga lo descargado automáticamente (FRED + precios)."""
    out = {}
    for nombre in ["raw_macro_global", "raw_macro_local_fred", "raw_precios"]:
        ruta = C.DATA_INTERIM / f"{nombre}.parquet"
        out[nombre] = pd.read_parquet(ruta) if ruta.exists() else None
        if out[nombre] is None:
            print(f"[FALTA] {ruta} — corre el notebook 01 primero.")
    return out


def _cargar_bcch():
    """Carga las series locales del BCCh si están en data/raw/ (descarga manual)."""
    from . import data_acquisition as da
    series = {}
    for clave, meta in C.MACRO_LOCAL_BCCH.items():
        archivo = meta[0]
        if str(archivo).startswith("^"):
            continue
        df = da.load_local_csv(archivo, sep=";", decimal=",")
        if df is not None:
            # toma la primera columna numérica
            num = df.select_dtypes("number")
            if not num.empty:
                series[clave] = num.iloc[:, 0]
    if series:
        print(f"[OK] BCCh cargado: {list(series.keys())}")
    else:
        print("[AVISO] Sin series BCCh en data/raw/. El panel usará solo FRED+precios.")
    return pd.DataFrame(series) if series else None


def construir_macro_mensual(interim, bcch):
    """Arma la matriz macro mensual ya transformada (diferencias/niveles)."""
    g = interim["raw_macro_global"]
    lf = interim["raw_macro_local_fred"]
    piezas = [df for df in (g, lf, bcch) if df is not None]
    macro_nivel = pd.concat(piezas, axis=1)
    macro_nivel = T.a_fin_de_mes(macro_nivel, metodo="last")

    cols = {}
    for c in macro_nivel.columns:
        if c in MACRO_EN_DIFERENCIA_LOG:
            cols["d_" + c] = np.log(macro_nivel[c]).diff()
        elif c in MACRO_EN_DIFERENCIA:
            cols["d_" + c] = macro_nivel[c].diff()
        elif c in MACRO_EN_NIVEL:
            cols[c] = macro_nivel[c]
        else:
            cols["d_" + c] = macro_nivel[c].diff()  # por defecto, diferenciar
    return pd.DataFrame(cols), macro_nivel


def construir(guardar=True, universo=None, sufijo=""):
    """
    Construye y (opcionalmente) guarda el panel long y las series wide.

    universo : dict de tickers; por defecto C.UNIVERSO_ACTIVO.
    sufijo   : sufijo para el nombre de salida (p. ej. '_B', '_A', '_C' en la
               triangulación por muestras), para no sobrescribir entre muestras.
    """
    print("=" * 60)
    print("CONSTRUCCIÓN DEL PANEL FINAL")
    print("=" * 60)
    universo = universo or C.UNIVERSO_ACTIVO
    interim = _cargar_interim()
    if interim["raw_precios"] is None:
        raise FileNotFoundError("Faltan precios. Corre el notebook 01 de adquisición.")

    bcch = _cargar_bcch()

    # --- Macro mensual transformada ---
    macro, macro_nivel = construir_macro_mensual(interim, bcch)

    # --- Retornos por empresa (solo las del universo presentes en los datos) ---
    px = interim["raw_precios"]
    tickers = [t for t in universo if t in px.columns]
    if not tickers:
        tickers = list(px.columns)
        print(f"[AVISO] Universo activo no presente; uso todos: {tickers}")
    precios_m = T.a_fin_de_mes(px[tickers], "last")
    retornos = T.retorno_log(precios_m)

    # --- Fase del ciclo del cobre (OE5) ---
    cobre_m = T.a_fin_de_mes(interim["raw_macro_global"][["cobre"]], "last")["cobre"]
    fechado = cd.datar_ciclo_cobre(cobre_m.loc[C.FECHA_INICIO:C.FECHA_FIN], k=6)

    # --- Panel long ---
    panel = T.construir_panel(retornos, macro)
    panel = cd.agregar_dummy_fase(panel, fechado)
    panel = panel.loc[(slice(None), slice(C.FECHA_INICIO, C.FECHA_FIN)), :].dropna(how="all")

    # --- Series wide (cartera + macro) para OE3/OE4 ---
    cartera = T.cartera_equiponderada(retornos).rename("retorno_cartera")
    series = pd.concat([cartera, macro], axis=1).loc[C.FECHA_INICIO:C.FECHA_FIN]

    print(f"\nPanel long : {panel.shape}  (empresas={len(tickers)})")
    print(f"Series wide: {series.shape}")
    print(f"Columnas macro: {list(macro.columns)}")

    if guardar:
        ruta_panel = C.DATA_PROCESSED / f"panel{sufijo}.parquet"
        ruta_series = C.DATA_PROCESSED / f"series{sufijo}.parquet"
        panel.to_parquet(ruta_panel)
        series.to_parquet(ruta_series)
        print(f"\n[guardado] {ruta_panel}")
        print(f"[guardado] {ruta_series}")

    return panel, series


if __name__ == "__main__":
    construir(guardar=True)
