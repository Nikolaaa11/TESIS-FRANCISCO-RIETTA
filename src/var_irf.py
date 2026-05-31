"""
var_irf.py
=========
Dinámica de shocks (OE4): VAR / VECM, funciones impulso-respuesta (IRF) y
descomposición de varianza (FEVD), más causalidad de Granger.

Decisiones clave (Frente 3):
- Si las series cointegran (OE3) -> usar VECM; si no -> VAR en diferencias/retornos.
- Identificación: ORDEN POR EXOGENEIDAD para Cholesky:
  cobre (global, exógeno) -> riesgo/tasas externas -> locales (TC, tasa) -> ACCIÓN (endógena).
  Robustez: IRF generalizadas (Pesaran-Shin), invariantes al orden.
- FEVD del retorno = evidencia directa para H6 (dominancia global vs local).

Requiere: statsmodels.
"""

from __future__ import annotations
import numpy as np
import pandas as pd

from statsmodels.tsa.api import VAR

# Orden recomendado por exogeneidad (de más exógena a más endógena).
# Ajustar a las columnas reales. La ACCIÓN/cartera va SIEMPRE al final.
ORDEN_CHOLESKY = ["d_cobre", "d_vix", "d_fed_funds", "d_usdclp", "d_tpm", "retorno_cartera"]


def seleccionar_rezagos(datos: pd.DataFrame, maxlags: int = 12) -> pd.DataFrame:
    """Tabla de criterios de información (AIC/BIC/HQIC/FPE) para elegir p."""
    datos = datos.dropna()
    modelo = VAR(datos)
    sel = modelo.select_order(maxlags)
    return pd.DataFrame({
        "AIC": sel.ics["aic"], "BIC": sel.ics["bic"],
        "HQIC": sel.ics["hqic"], "FPE": sel.ics["fpe"],
    })


def estimar_var(datos: pd.DataFrame, orden: list[str] | None = None, p: int = 1):
    """
    Estima un VAR con las columnas reordenadas según exogeneidad (para Cholesky).

    datos : DataFrame de variables ESTACIONARIAS (retornos / diferencias).
    orden : lista de columnas en orden de exogeneidad; si None usa el del DataFrame.
    p     : número de rezagos.
    """
    if orden:
        cols = [c for c in orden if c in datos.columns]
    else:
        cols = list(datos.columns)
    datos = datos[cols].dropna()
    return VAR(datos).fit(p)


def irf(res_var, periodos: int = 24, ortogonal: bool = True):
    """
    Funciones impulso-respuesta. ortogonal=True -> Cholesky (depende del orden);
    usar .plot() en el notebook. Para robustez al orden, ver irf_generalizada().
    """
    return res_var.irf(periodos)


def fevd(res_var, periodos: int = 24):
    """Descomposición de la varianza del error de pronóstico (FEVD)."""
    return res_var.fevd(periodos)


def granger_causalidad(res_var, causa: str, efecto: str):
    """
    Test de causalidad de Granger: ¿'causa' ayuda a predecir 'efecto'?
    Devuelve (estadístico, p_value).
    """
    test = res_var.test_causality(efecto, [causa], kind="f")
    return test.test_statistic, test.pvalue


def tabla_fevd_variable(res_var, variable: str, periodos=(1, 6, 12, 24)) -> pd.DataFrame:
    """
    Extrae la FEVD de UNA variable (p. ej. 'retorno_cartera') en horizontes dados.
    Útil para H6: qué fracción de la varianza del retorno explica cada shock.
    """
    fe = res_var.fevd(max(periodos))
    cols = res_var.names
    idx = cols.index(variable)
    filas = {h: fe.decomp[idx, h - 1, :] for h in periodos}
    return pd.DataFrame(filas, index=cols).T  # filas=horizonte, cols=fuente del shock


if __name__ == "__main__":
    # Smoke test: 'shock_global' causa Granger 'retorno' (con rezago); el local no.
    rng = np.random.default_rng(5)
    n = 240
    g = rng.standard_normal(n)
    loc = rng.standard_normal(n)
    ret = np.empty(n)
    ret[0] = 0
    for t in range(1, n):
        ret[t] = 0.6 * g[t - 1] + 0.2 * ret[t - 1] + rng.standard_normal() * 0.5
    idx = pd.period_range("2004-01", periods=n, freq="M").to_timestamp("M")
    datos = pd.DataFrame({"d_cobre": g, "d_usdclp": loc, "retorno_cartera": ret}, index=idx)

    res = estimar_var(datos, orden=["d_cobre", "d_usdclp", "retorno_cartera"], p=2)
    print("Granger cobre->retorno:", tuple(round(float(x), 4) for x in
          granger_causalidad(res, "d_cobre", "retorno_cartera")))
    print("Granger usdclp->retorno:", tuple(round(float(x), 4) for x in
          granger_causalidad(res, "d_usdclp", "retorno_cartera")))
    print("\nFEVD de retorno_cartera (fracción por fuente de shock):")
    print(tabla_fevd_variable(res, "retorno_cartera").round(3))
