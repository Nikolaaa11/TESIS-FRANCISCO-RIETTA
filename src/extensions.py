"""
extensions.py
============
Extensiones avanzadas que elevan el rigor de la tesis:

1. GARCH(1,1): modela la volatilidad condicional de los retornos del sector
   (los retornos financieros exhiben agrupamiento de volatilidad / efectos ARCH).
2. Gregory-Hansen (1996): prueba de cointegración con UN quiebre estructural endógeno,
   apropiada cuando la relación de largo plazo puede haberse desplazado (súper-ciclo).

Datos reales (muestra B). Requiere: arch, statsmodels.
Salida: web/extensions.json
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

from . import config as C


# ------------------------------------------------------------------
# 1. GARCH(1,1) sobre la cartera del sector
# ------------------------------------------------------------------
def garch_cartera():
    from arch import arch_model
    from statsmodels.stats.diagnostic import het_arch

    series = pd.read_parquet(C.DATA_PROCESSED / "series_B.parquet")
    r = series["retorno_cartera"].dropna() * 100  # en %

    # Test ARCH-LM (¿hay efectos ARCH que justifiquen GARCH?)
    arch_stat, arch_p, _, _ = het_arch(r, nlags=12)

    am = arch_model(r, mean="Constant", vol="GARCH", p=1, q=1, dist="t")
    res = am.fit(disp="off")
    pr = res.params
    alpha = float(pr.get("alpha[1]", np.nan))
    beta = float(pr.get("beta[1]", np.nan))
    return {
        "arch_lm_stat": round(float(arch_stat), 3),
        "arch_lm_p": round(float(arch_p), 4),
        "omega": round(float(pr.get("omega", np.nan)), 4),
        "alpha": round(alpha, 4),
        "beta": round(beta, 4),
        "persistencia": round(alpha + beta, 4),
        "nu_t": round(float(pr.get("nu", np.nan)), 2),
        "interpretacion": ("Persistencia alta (~alpha+beta cercano a 1) indica que los shocks de "
                           "volatilidad son duraderos; efectos ARCH significativos si arch_lm_p<0.05."),
    }


# ------------------------------------------------------------------
# 2. Gregory-Hansen (cointegración con quiebre, modelo C: cambio de nivel)
# ------------------------------------------------------------------
# Valores críticos del estadístico ADF* (Z_t), Gregory & Hansen (1996), modelo C.
GH_CV_MODELO_C = {1: {"1%": -5.13, "5%": -4.61, "10%": -4.34},
                  2: {"1%": -5.44, "5%": -4.92, "10%": -4.69},
                  3: {"1%": -5.77, "5%": -5.28, "10%": -5.02},
                  4: {"1%": -6.05, "5%": -5.56, "10%": -5.31}}


def gregory_hansen(y: pd.Series, X: pd.DataFrame, trim: float = 0.15):
    """
    Prueba de cointegración con un quiebre endógeno (modelo C, cambio de nivel).
    Para cada posible fecha de quiebre se estima y = mu + mu1*D + beta'X + e y se
    calcula el ADF sobre los residuos; el estadístico GH es el mínimo (más negativo).
    """
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    n = len(df)
    lo, hi = int(trim * n), int((1 - trim) * n)
    Xmat = df.drop(columns="y").values
    yv = df["y"].values
    best = {"adf": np.inf, "idx": None}
    for b in range(lo, hi):
        D = (np.arange(n) > b).astype(float).reshape(-1, 1)
        Z = np.column_stack([np.ones(n), D, Xmat])
        coef, *_ = np.linalg.lstsq(Z, yv, rcond=None)
        resid = yv - Z @ coef
        try:
            adf = adfuller(resid, regression="n", autolag="AIC")[0]
        except Exception:
            continue
        if adf < best["adf"]:
            best = {"adf": adf, "idx": b}
    m = X.shape[1]
    cv = GH_CV_MODELO_C.get(m, GH_CV_MODELO_C[2])
    fecha = df.index[best["idx"]] if best["idx"] is not None else None
    coint = best["adf"] < cv["5%"]
    return {
        "gh_adf_stat": round(float(best["adf"]), 4),
        "fecha_quiebre": fecha.strftime("%Y-%m") if fecha is not None else None,
        "cv_5pct": cv["5%"], "cv_10pct": cv["10%"], "m_regresores": m,
        "cointegra_con_quiebre_5pct": bool(coint),
        "interpretacion": ("Si gh_adf_stat < valor crítico, hay cointegración con un quiebre en la "
                           "fecha estimada; complementa al ARDL/Johansen sin quiebre (H5)."),
    }


def construir():
    out = {}
    out["garch"] = garch_cartera()

    g = pd.read_parquet(C.DATA_INTERIM / "raw_macro_global.parquet")
    lf = pd.read_parquet(C.DATA_INTERIM / "raw_macro_local_fred.parquet")
    px = pd.read_parquet(C.DATA_INTERIM / "raw_precios.parquet")
    valor = np.log(px["ANTO.L"].resample("ME").last())
    cobre = np.log(g["cobre"].resample("ME").last())
    tc = np.log(lf["usdclp"].resample("ME").last())
    niveles = pd.concat([valor, cobre, tc], axis=1).loc[C.FECHA_INICIO:C.FECHA_FIN].dropna()
    niveles.columns = ["valor", "cobre", "tc"]
    out["gregory_hansen"] = gregory_hansen(niveles["valor"], niveles[["cobre", "tc"]])

    (C.ROOT / "web" / "extensions.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return out


if __name__ == "__main__":
    construir()
