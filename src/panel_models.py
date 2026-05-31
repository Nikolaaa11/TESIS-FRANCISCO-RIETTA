"""
panel_models.py
==============
Modelos para el OE2: sensibilidad de los retornos a factores macro-financieros,
con contraste GLOBAL vs LOCAL (H6).

Estrategia (ver Frente 3):
- Baseline: serie de tiempo sobre la cartera del sector (OLS con HAC/Newey-West).
- Principal: Panel de efectos fijos (FE) con errores Driscoll-Kraay
  (robustos a heterocedasticidad, autocorrelación y DEPENDENCIA DE SECCIÓN CRUZADA,
  que es casi segura aquí porque todas las empresas comparten el shock del cobre).

Requiere: linearmodels, statsmodels.
"""

from __future__ import annotations
import numpy as np
import pandas as pd

import statsmodels.api as sm

# Bloques de regresores para el contraste global vs local (H6).
# Ajustar los nombres a las columnas reales de tu panel.
FACTORES_GLOBALES = ["d_cobre", "d_vix", "d_fed_funds", "d_treasury10"]
FACTORES_LOCALES = ["d_usdclp", "d_tpm", "d_imacec", "d_embi"]
CONTROLES_EMPRESA = ["size", "volatilidad", "leverage"]


# ------------------------------------------------------------------
# Baseline: serie de tiempo sobre la cartera del sector
# ------------------------------------------------------------------
def baseline_cartera(cartera_ret: pd.Series, X: pd.DataFrame,
                     maxlags: int = 4) -> sm.regression.linear_model.RegressionResults:
    """
    OLS de la cartera del sector sobre factores macro, con errores HAC (Newey-West).

    cartera_ret : Serie de retornos de la cartera (variable dependiente).
    X           : DataFrame de regresores (ya estacionarios / diferenciados).
    """
    df = pd.concat([cartera_ret.rename("y"), X], axis=1).dropna()
    y = df["y"]
    Xc = sm.add_constant(df.drop(columns="y"))
    modelo = sm.OLS(y, Xc).fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})
    return modelo


# ------------------------------------------------------------------
# Principal: Panel FE con Driscoll-Kraay
# ------------------------------------------------------------------
def panel_fe_driscoll_kraay(panel: pd.DataFrame, dep: str, regresores: list[str],
                            entity_effects: bool = True,
                            time_effects: bool = False,
                            kernel: str = "bartlett", bandwidth=None):
    """
    Panel OLS de efectos fijos con covarianza Driscoll-Kraay.

    panel : DataFrame con MultiIndex (empresa, fecha).
    dep   : nombre de la columna dependiente (p. ej. 'retorno').
    regresores : lista de columnas explicativas.

    Returns
    -------
    PanelEffectsResults de linearmodels.
    """
    from linearmodels.panel import PanelOLS

    df = panel[[dep] + regresores].dropna()
    y = df[dep]
    X = sm.add_constant(df[regresores])

    mod = PanelOLS(y, X, entity_effects=entity_effects, time_effects=time_effects,
                   drop_absorbed=True)
    # cov_type='kernel' con kernel Bartlett == Driscoll-Kraay
    res = mod.fit(cov_type="kernel", kernel=kernel, bandwidth=bandwidth)
    return res


# ------------------------------------------------------------------
# Contraste GLOBAL vs LOCAL (H6)
# ------------------------------------------------------------------
def test_bloque(res, nombres_bloque: list[str]):
    """
    Test de Wald de significancia conjunta de un bloque de coeficientes
    (p. ej. todos los factores globales). Sirve para H6.

    Funciona tanto con resultados de statsmodels (baseline) como de linearmodels.
    Devuelve (estadistico, p_value, gl).
    """
    presentes = [n for n in nombres_bloque if n in list(res.params.index)]
    if not presentes:
        return np.nan, np.nan, 0

    # Construcción de hipótesis lineal "coef = 0" para cada uno del bloque
    restricciones = ", ".join(f"{n} = 0" for n in presentes)
    if "linearmodels" in type(res).__module__:
        # linearmodels: la fórmula como string va en el keyword 'formula'
        wald = res.wald_test(formula=restricciones)
        stat = float(np.asarray(wald.stat))
        pval = float(np.asarray(wald.pval))
    else:
        # statsmodels: acepta el string posicional
        wald = res.wald_test(restricciones, use_f=False, scalar=True)
        stat = float(np.asarray(wald.statistic))
        pval = float(np.asarray(wald.pvalue))
    return stat, pval, len(presentes)


def comparar_global_vs_local(res,
                             globales=FACTORES_GLOBALES,
                             locales=FACTORES_LOCALES) -> pd.DataFrame:
    """
    Resume el contraste H6: significancia conjunta de bloques global vs local.
    Para la magnitud relativa, complementar con descomposición de varianza (OE4, FEVD)
    y/o R^2 incremental por bloque.
    """
    gs, gp, gk = test_bloque(res, globales)
    ls, lp, lk = test_bloque(res, locales)
    return pd.DataFrame({
        "bloque": ["Global", "Local"],
        "n_factores": [gk, lk],
        "wald_stat": [gs, ls],
        "p_value": [gp, lp],
    }).set_index("bloque")


if __name__ == "__main__":
    # Smoke test: panel sintético donde un factor 'global' SÍ explica y otro 'local' NO.
    rng = np.random.default_rng(11)
    empresas = ["A", "B", "C", "D"]
    fechas = pd.period_range("2010-01", periods=120, freq="M").to_timestamp("M")
    d_cobre = pd.Series(rng.standard_normal(len(fechas)), index=fechas)  # factor comun
    filas = []
    for e in empresas:
        ruido = rng.standard_normal(len(fechas)) * 0.5
        d_usdclp = rng.standard_normal(len(fechas))  # local irrelevante
        y = 0.8 * d_cobre.values + 0.0 * d_usdclp + ruido  # solo global importa
        filas.append(pd.DataFrame({
            "empresa": e, "fecha": fechas, "retorno": y,
            "d_cobre": d_cobre.values, "d_usdclp": d_usdclp,
        }))
    panel = pd.concat(filas).set_index(["empresa", "fecha"])

    try:
        res = panel_fe_driscoll_kraay(panel, "retorno", ["d_cobre", "d_usdclp"])
        print(res.params)
        print()
        print(comparar_global_vs_local(res,
              globales=["d_cobre"], locales=["d_usdclp"]))
    except ImportError:
        print("Instala linearmodels para el panel: pip install linearmodels")
