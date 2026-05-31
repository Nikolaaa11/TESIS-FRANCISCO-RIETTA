"""
stationarity.py
==============
Pruebas de estacionariedad / orden de integración (OE1).

Incluye:
- ADF (H0: raíz unitaria)
- Phillips-Perron (vía arch)  -- robusto a autocorrelación/heterocedasticidad
- KPSS (H0: estacionariedad)  -- complementa a ADF (H0 invertida)
- Zivot-Andrews (raíz unitaria con un quiebre estructural endógeno)
- Resumen de orden de integración por variable: I(0) / I(1)

Convención de lectura:
- ADF/PP: rechazar H0 (p<0.05) => estacionaria.
- KPSS:   NO rechazar H0 (p>0.05) => estacionaria.
- Conclusión robusta cuando ADF/PP y KPSS coinciden.
"""

from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss


def _adf(serie, regression="c"):
    serie = pd.Series(serie).dropna()
    stat, p, *_ = adfuller(serie, regression=regression, autolag="AIC")
    return stat, p


def _kpss(serie, regression="c"):
    serie = pd.Series(serie).dropna()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # KPSS avisa cuando p está fuera de tabla
        stat, p, *_ = kpss(serie, regression=regression, nlags="auto")
    return stat, p


def _pp(serie):
    """Phillips-Perron desde arch (si está instalado)."""
    try:
        from arch.unitroot import PhillipsPerron
    except ImportError:
        return np.nan, np.nan
    serie = pd.Series(serie).dropna()
    pp = PhillipsPerron(serie)
    return pp.stat, pp.pvalue


def _zivot_andrews(serie):
    """Zivot-Andrews: raíz unitaria permitiendo un quiebre endógeno."""
    try:
        from statsmodels.tsa.stattools import zivot_andrews
    except ImportError:
        return np.nan, np.nan
    serie = pd.Series(serie).dropna()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = zivot_andrews(serie)
    return res[0], res[1]


def test_una_serie(serie, nombre="serie", alpha=0.05):
    """Aplica la batería completa a una serie y clasifica I(0)/I(1)."""
    adf_s, adf_p = _adf(serie)
    pp_s, pp_p = _pp(serie)
    kpss_s, kpss_p = _kpss(serie)
    za_s, za_p = _zivot_andrews(serie)

    nivel_estacionario = (adf_p < alpha) and (kpss_p > alpha)

    # Si no es estacionaria en nivel, testear primera diferencia
    if not nivel_estacionario:
        d = pd.Series(serie).diff().dropna()
        d_adf_p = _adf(d)[1]
        d_kpss_p = _kpss(d)[1]
        dif_estacionaria = (d_adf_p < alpha) and (d_kpss_p > alpha)
        orden = "I(1)" if dif_estacionaria else "I(2)?/revisar"
    else:
        orden = "I(0)"

    return {
        "variable": nombre,
        "ADF_stat": adf_s, "ADF_p": adf_p,
        "PP_stat": pp_s, "PP_p": pp_p,
        "KPSS_stat": kpss_s, "KPSS_p": kpss_p,
        "ZA_stat": za_s, "ZA_p": za_p,
        "orden_integracion": orden,
    }


def tabla_estacionariedad(df: pd.DataFrame, alpha=0.05) -> pd.DataFrame:
    """
    Aplica la batería a todas las columnas de un DataFrame.
    Devuelve una tabla resumen ordenada -> lista para el Capítulo 4 (OE1).
    """
    filas = [test_una_serie(df[c], nombre=c, alpha=alpha) for c in df.columns]
    tabla = pd.DataFrame(filas).set_index("variable")
    cols_p = ["ADF_p", "PP_p", "KPSS_p", "ZA_p", "orden_integracion"]
    return tabla[cols_p + [c for c in tabla.columns if c not in cols_p]]


if __name__ == "__main__":
    # Smoke test con ruido blanco (debe salir I(0)) y random walk (debe salir I(1)).
    rng = np.random.default_rng(7)
    ruido = pd.Series(rng.standard_normal(300))
    rw = ruido.cumsum()
    demo = pd.DataFrame({"ruido_blanco_I0": ruido, "random_walk_I1": rw})
    print(tabla_estacionariedad(demo)[["ADF_p", "KPSS_p", "orden_integracion"]])
