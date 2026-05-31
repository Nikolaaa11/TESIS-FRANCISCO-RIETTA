"""
panel_unit_root.py
=================
Prueba de raíz unitaria en panel de SEGUNDA GENERACIÓN: CIPS de Pesaran (2007),
robusta a la dependencia de sección cruzada (que el test CD detecta en este panel).

Procedimiento: para cada empresa i se estima la regresión CADF aumentada con los
promedios de sección cruzada (nivel y diferencia):
    Δy_it = a_i + b_i y_{i,t-1} + c_i ȳ_{t-1} + d_i Δȳ_t + e_it
y se toma el estadístico t de b_i (CADF_i). El estadístico CIPS es el promedio de
los CADF_i. Si CIPS < valor crítico, se rechaza la raíz unitaria (serie estacionaria).

Valores críticos aproximados (Pesaran 2007, caso con intercepto): se usan como referencia;
la conclusión cualitativa (retornos I(0), precios I(1)) es robusta a su valor exacto.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import statsmodels.api as sm

from . import config as C

# Pesaran (2007), caso con intercepto (sin tendencia), referencia para N pequeño/T grande.
CIPS_CV = {"1%": -2.85, "5%": -2.57, "10%": -2.42}


def cips(panel_wide: pd.DataFrame):
    """panel_wide: DataFrame (fechas x unidades) de UNA variable. Devuelve (CIPS, CADF por unidad)."""
    Y = panel_wide.dropna(how="all")
    ybar = Y.mean(axis=1)
    dybar = ybar.diff()
    cadf = {}
    for col in Y.columns:
        yi = Y[col]
        df = pd.DataFrame({"dy": yi.diff(), "y_lag": yi.shift(1),
                           "ybar_lag": ybar.shift(1), "dybar": dybar}).dropna()
        if len(df) < 20:
            continue
        X = sm.add_constant(df[["y_lag", "ybar_lag", "dybar"]])
        m = sm.OLS(df["dy"], X).fit()
        cadf[col] = float(m.tvalues["y_lag"])
    stat = float(np.mean(list(cadf.values()))) if cadf else np.nan
    return stat, cadf


def analizar():
    px = pd.read_parquet(C.DATA_INTERIM / "raw_precios.parquet")
    tickers = [t for t in C.MUESTRA_B_GLOBAL_COBRE if t in px.columns]
    precios_m = px[tickers].resample("ME").last().loc[C.FECHA_INICIO:C.FECHA_FIN]
    log_px = np.log(precios_m)
    retornos = log_px.diff()

    out = {}
    for nombre, datos in [("log_precios", log_px), ("retornos", retornos)]:
        stat, cadf = cips(datos)
        rechaza = stat < CIPS_CV["5%"]
        out[nombre] = {"cips": round(stat, 4), "cv_5pct": CIPS_CV["5%"],
                       "rechaza_raiz_unitaria_5pct": bool(rechaza),
                       "orden": "I(0)" if rechaza else "I(1)",
                       "n_unidades": len(cadf)}
    print("=== CIPS de Pesaran (2007) — panel muestra B, robusto a dependencia cruzada ===")
    for k, v in out.items():
        print(f"  {k:14s} CIPS={v['cips']:+.3f}  (cv5%={v['cv_5pct']})  -> {v['orden']}")
    return out


if __name__ == "__main__":
    analizar()
