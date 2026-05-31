"""
hausman_test.py
==============
Test de Hausman (efectos fijos vs. efectos aleatorios) para justificar formalmente
la especificación de panel adoptada en OE2.

H0: el estimador de efectos aleatorios (RE) es consistente y eficiente (no hay
correlación entre los efectos individuales y los regresores).
H1: solo el estimador de efectos fijos (FE) es consistente.

Rechazar H0 (p<0.05) => se prefiere EFECTOS FIJOS, que es la especificación principal de la tesis.

Estadístico: H = (b_FE - b_RE)' [V(b_FE) - V(b_RE)]^{-1} (b_FE - b_RE) ~ chi2(k).
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

from . import config as C

REGS = ["d_cobre", "d_vix", "d_fed_funds", "d_treasury10",
        "d_usdclp", "d_tasa_local", "d_actividad_local"]


def hausman(suf="_B"):
    from linearmodels.panel import PanelOLS, RandomEffects
    panel = pd.read_parquet(C.DATA_PROCESSED / f"panel{suf}.parquet")
    regs = [r for r in REGS if r in panel.columns]
    df = panel[["retorno"] + regs].dropna()
    if df.index.get_level_values(0).nunique() < 2:
        return None
    y = df["retorno"]; X = sm.add_constant(df[regs])

    fe = PanelOLS(y, X, entity_effects=True, drop_absorbed=True).fit()
    re = RandomEffects(y, X).fit()

    comunes = [c for c in regs if c in fe.params.index and c in re.params.index]
    b_fe = fe.params[comunes].values
    b_re = re.params[comunes].values
    v_fe = fe.cov.loc[comunes, comunes].values
    v_re = re.cov.loc[comunes, comunes].values
    vdiff = v_fe - v_re
    diff = b_fe - b_re
    H = float(diff.T @ np.linalg.pinv(vdiff) @ diff)
    k = len(comunes)
    p = float(1 - stats.chi2.cdf(H, k))
    # Caso degenerado: con regresores macro COMUNES a todas las empresas (no varían entre
    # unidades), FE y RE entregan pendientes idénticas (b_FE = b_RE) y H ~ 0. En ese caso el
    # test no discrimina; se retiene FE para absorber la heterogeneidad de medias por empresa.
    degenerado = abs(H) < 1e-6
    if degenerado:
        prefiere = "FE = RE en pendientes (regresores comunes); se retiene FE por heterogeneidad"
    else:
        prefiere = "Efectos fijos" if p < 0.05 else "Efectos aleatorios"
    return {"H": round(H, 3), "gl": k, "p": round(p, 4),
            "degenerado": degenerado, "prefiere": prefiere}


def analizar():
    out = {}
    for suf, lab in [("_B", "Muestra B"), ("_C", "Muestra C")]:
        r = hausman(suf)
        if r:
            out[lab] = r
            print(f"  {lab}: H={r['H']} (gl={r['gl']})  p={r['p']}  -> {r['prefiere']}")
    return out


if __name__ == "__main__":
    print("=== Test de Hausman (FE vs RE) ===")
    analizar()
