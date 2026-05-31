"""
triangulation.py
===============
OE6: ejecuta el análisis sobre las TRES muestras (B global, A local-cobre, C local-minería)
y consolida una tabla comparativa para contrastar PI6/H7 (mercado global vs mercado chileno).

Para cada muestra reporta:
- Coeficiente del cobre (Δcobre) y su significancia  -> sensibilidad (H1, comparada).
- R² del modelo de retornos.
- Fracción de la varianza del retorno explicada por shocks GLOBALES (FEVD, OE4) -> H6/H7.

Maneja el caso N=1 (muestra A): usa serie de tiempo (OLS-HAC) en vez de panel FE.
Requiere: pandas, statsmodels, linearmodels.
"""

from __future__ import annotations
import numpy as np
import pandas as pd

from . import config as C
from . import panel_models as pm
from . import var_irf as vi

# Muestras: (sufijo de archivo, etiqueta legible, mercado)
MUESTRAS = [
    ("_B", "B: cobre global", "global"),
    ("_A", "A: cobre Chile", "chileno"),
    ("_C", "C: minería Chile", "chileno"),
]

REGRESORES_DEFECTO = ["d_cobre", "d_vix", "d_fed_funds", "d_treasury10",
                      "d_usdclp", "d_tasa_local", "d_actividad_local"]
GLOBALES = ["d_cobre", "d_vix", "d_fed_funds", "d_treasury10"]
LOCALES = ["d_usdclp", "d_tasa_local", "d_actividad_local"]


def _modelo_retornos(panel: pd.DataFrame, regresores: list[str]):
    """
    Estima el modelo de retornos. Si hay >1 empresa -> Panel FE Driscoll-Kraay;
    si hay 1 empresa (muestra A) -> serie de tiempo OLS con errores HAC.
    Devuelve (params, pvalues, r2, n_empresas).
    """
    regs = [r for r in regresores if r in panel.columns]
    n_emp = panel.index.get_level_values(0).nunique()
    if n_emp > 1:
        res = pm.panel_fe_driscoll_kraay(panel, dep="retorno", regresores=regs)
        return res.params, res.pvalues, float(res.rsquared_within), n_emp
    # N = 1: serie de tiempo
    serie = panel.reset_index(level=0, drop=True)
    res = pm.baseline_cartera(serie["retorno"], serie[regs], maxlags=4)
    return res.params, res.pvalues, float(res.rsquared), n_emp


def _fevd_global(series_wide: pd.DataFrame, regresores_var: list[str]) -> float:
    """Fracción de varianza del retorno de la cartera explicada por shocks globales (h=12)."""
    cols = [c for c in ["d_cobre", "d_vix", "d_usdclp"] if c in series_wide.columns]
    datos = series_wide[["retorno_cartera"] + cols].dropna()
    orden = cols + ["retorno_cartera"]  # acción al final
    res = vi.estimar_var(datos[orden], orden=orden, p=2)
    fevd = vi.tabla_fevd_variable(res, "retorno_cartera", periodos=(12,))
    glob = [c for c in ["d_cobre", "d_vix"] if c in fevd.columns]
    return float(fevd.loc[12, glob].sum())


def comparar_muestras(regresores=REGRESORES_DEFECTO) -> pd.DataFrame:
    """
    Carga panel_{B,A,C} y series_{B,A,C} de data/processed/ y arma la tabla comparativa.
    Requiere haber corrido build_panel.construir(sufijo=...) para cada muestra.
    """
    filas = []
    for suf, etiqueta, mercado in MUESTRAS:
        ruta_panel = C.DATA_PROCESSED / f"panel{suf}.parquet"
        ruta_series = C.DATA_PROCESSED / f"series{suf}.parquet"
        if not ruta_panel.exists():
            print(f"[FALTA] {ruta_panel} — corre build_panel con sufijo='{suf}'.")
            continue
        panel = pd.read_parquet(ruta_panel)
        params, pvals, r2, n_emp = _modelo_retornos(panel, regresores)

        fila = {
            "muestra": etiqueta, "mercado": mercado, "n_empresas": n_emp,
            "beta_cobre": params.get("d_cobre", np.nan),
            "p_cobre": pvals.get("d_cobre", np.nan),
            "R2": r2,
        }
        if ruta_series.exists():
            try:
                fila["FEVD_global_h12"] = _fevd_global(pd.read_parquet(ruta_series), regresores)
            except Exception as e:
                fila["FEVD_global_h12"] = np.nan
                print(f"[aviso] FEVD muestra {etiqueta}: {e}")
        filas.append(fila)

    tabla = pd.DataFrame(filas).set_index("muestra")
    return tabla


if __name__ == "__main__":
    tabla = comparar_muestras()
    pd.set_option("display.width", 120)
    print("\n=== TABLA COMPARATIVA OE6 (PI6/H7) ===")
    print(tabla.round(4).to_string())
    tabla.to_csv(C.TABLES / "oe6_comparacion_mercados.csv")
    print(f"\n[guardado] {C.TABLES / 'oe6_comparacion_mercados.csv'}")
