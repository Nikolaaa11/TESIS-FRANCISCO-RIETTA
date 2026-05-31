"""
cointegration.py
===============
Análisis de largo plazo (OE3): cointegración y mecanismo de corrección de error.

Estrategia (Frente 3):
- ARDL bounds (Pesaran-Shin-Smith 2001): caballo de batalla. Funciona con mezcla I(0)/I(1).
- Johansen (1988): contraste de robustez sobre el subconjunto claramente I(1); da el VECM.
- VECM: estima el vector de largo plazo y la velocidad de ajuste (alpha).

Aplica a las variables en NIVEL (log): valor de la cartera del sector, cobre, TC, tasa.
Requiere: statsmodels.
"""

from __future__ import annotations
import numpy as np
import pandas as pd

from statsmodels.tsa.vector_ar.vecm import coint_johansen, VECM, select_coint_rank


# ------------------------------------------------------------------
# ARDL bounds test
# ------------------------------------------------------------------
# Correspondencia trend (statsmodels) -> caso de Pesaran-Shin-Smith para el bounds test.
_TREND_A_CASE = {"n": 1, "c": 3, "ct": 5}


def ardl_bounds(y: pd.Series, X: pd.DataFrame, maxlag: int = 6, trend: str = "c",
                case: int | None = None):
    """
    Test de cointegración por bordes (ARDL bounds) de Pesaran-Shin-Smith.

    Parameters
    ----------
    y : variable dependiente en NIVEL (p. ej. log valor de la cartera).
    X : regresores en NIVEL (cobre, TC, tasa).
    maxlag : rezago máximo a explorar en la selección de orden.
    trend  : 'n' (sin), 'c' (constante, caso 3), 'ct' (const+tend, caso 5).
    case   : caso 1-5 de Pesaran-Shin-Smith; si None se deriva de 'trend'.

    Returns
    -------
    dict con el orden seleccionado, el estadístico F de bordes y el objeto bounds.
    Interpretación: si F > cota superior I(1) => hay cointegración (rechaza H0 'no nivel').
    """
    from statsmodels.tsa.ardl import ardl_select_order

    case = case or _TREND_A_CASE.get(trend, 3)
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    sel = ardl_select_order(df["y"], maxlag, df.drop(columns="y"), maxlag,
                            trend=trend, ic="aic")
    res = sel.model.fit()

    # UECM (modelo de corrección de error no restringido) -> bounds_test.
    # from_ardl convierte el ARDL seleccionado al UECM correspondiente.
    from statsmodels.tsa.ardl import UECM
    uecm = UECM.from_ardl(sel.model).fit()
    bt = uecm.bounds_test(case=case)

    return {
        "ar_lags": sel.model.ar_lags,
        "dl_lags": sel.model.dl_lags,
        "F_stat": float(np.asarray(bt.stat)),
        "bounds_test": bt,
        "ardl_res": res,
        "uecm_res": uecm,
    }


# ------------------------------------------------------------------
# Johansen
# ------------------------------------------------------------------
def johansen(df_niveles: pd.DataFrame, det_order: int = 0, k_ar_diff: int = 1) -> pd.DataFrame:
    """
    Test de cointegración de Johansen (traza y máximo autovalor).

    det_order : -1 sin constante, 0 constante en la cointegración, 1 con tendencia.
    k_ar_diff : rezagos en diferencias.

    Returns
    -------
    DataFrame con estadístico de traza y valores críticos (90/95/99%).
    """
    datos = df_niveles.dropna()
    jo = coint_johansen(datos, det_order, k_ar_diff)
    out = pd.DataFrame({
        "r<=": [f"r<={i}" for i in range(len(jo.lr1))],
        "traza_stat": jo.lr1,
        "cv_90": jo.cvt[:, 0],
        "cv_95": jo.cvt[:, 1],
        "cv_99": jo.cvt[:, 2],
        "maxeig_stat": jo.lr2,
        "cvm_95": jo.cvm[:, 1],
    })
    out["coint_traza_95"] = out["traza_stat"] > out["cv_95"]
    return out


def rango_cointegracion(df_niveles: pd.DataFrame, det_order: int = 0, k_ar_diff: int = 1):
    """Selección automática del rango de cointegración (traza, 95%)."""
    datos = df_niveles.dropna()
    return select_coint_rank(datos, det_order, k_ar_diff, method="trace", signif=0.05)


# ------------------------------------------------------------------
# VECM
# ------------------------------------------------------------------
def estimar_vecm(df_niveles: pd.DataFrame, k_ar_diff: int = 1, coint_rank: int = 1,
                 deterministic: str = "ci"):
    """
    Estima un VECM y devuelve el resultado.

    deterministic : 'ci' = constante en la cointegración (caso típico).
    El atributo .alpha del resultado = velocidad de ajuste (corrección de error).
    El atributo .beta = vector(es) de cointegración (relación de largo plazo).
    """
    datos = df_niveles.dropna()
    modelo = VECM(datos, k_ar_diff=k_ar_diff, coint_rank=coint_rank,
                  deterministic=deterministic)
    return modelo.fit()


if __name__ == "__main__":
    # Smoke test: dos series cointegradas (comparten una tendencia estocástica común).
    rng = np.random.default_rng(3)
    n = 250
    comun = rng.standard_normal(n).cumsum()          # tendencia estocástica común I(1)
    y1 = comun + rng.standard_normal(n) * 0.5
    y2 = 0.7 * comun + rng.standard_normal(n) * 0.5  # cointegrada con y1
    idx = pd.period_range("2004-01", periods=n, freq="M").to_timestamp("M")
    datos = pd.DataFrame({"y1": y1, "y2": y2}, index=idx)

    print("=== Johansen ===")
    print(johansen(datos)[["r<=", "traza_stat", "cv_95", "coint_traza_95"]].round(2))

    print("\n=== VECM (alpha = velocidad de ajuste) ===")
    vecm = estimar_vecm(datos, coint_rank=1)
    print("alpha:\n", np.round(vecm.alpha, 4))
    print("beta (long-run):\n", np.round(vecm.beta, 4))
