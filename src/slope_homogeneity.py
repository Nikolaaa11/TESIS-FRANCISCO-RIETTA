"""
slope_homogeneity.py
===================
Test de homogeneidad de pendientes de Pesaran y Yamagata (2008), estadísticos Delta y
Delta ajustado por sesgo.

H0: los coeficientes de pendiente son homogéneos entre empresas (mismo efecto de cada factor
para todas) -> justifica estimadores agrupados (pooled / efectos fijos).
H1: las pendientes son heterogéneas -> convendría un estimador de tipo Mean Group.

Δ ~ N(0,1) bajo H0; |Δ| > 1,96 rechaza la homogeneidad al 5%.

Nota: con N pequeño (B = 5, C = 4 empresas) la potencia es limitada; el resultado se interpreta
con cautela, como diagnóstico complementario que respalda la especificación adoptada.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from scipy import stats

from . import config as C

REGS = ["d_cobre", "d_vix", "d_usdclp"]


def pesaran_yamagata(suf="_B", regs=REGS, dep="retorno"):
    panel = pd.read_parquet(C.DATA_PROCESSED / f"panel{suf}.parquet")
    regs = [r for r in regs if r in panel.columns]
    firms = panel.index.get_level_values(0).unique()
    betas, sig2, XtX, Ts = {}, {}, {}, {}
    k = len(regs)
    for f in firms:
        sub = panel.xs(f, level=0)[[dep] + regs].dropna()
        if len(sub) < k + 10:
            continue
        y = sub[dep].values
        X = sub[regs].values
        yd = y - y.mean()
        Xd = X - X.mean(axis=0)
        b, *_ = np.linalg.lstsq(Xd, yd, rcond=None)
        resid = yd - Xd @ b
        Ti = len(yd)
        s2 = float(resid @ resid) / (Ti - k)
        if s2 <= 0:
            continue
        betas[f], sig2[f], XtX[f], Ts[f] = b, s2, Xd.T @ Xd, Ti
    N = len(betas)
    if N < 2:
        return None
    A = sum(XtX[f] / sig2[f] for f in betas)
    rhs = sum((XtX[f] / sig2[f]) @ betas[f] for f in betas)
    b_wfe = np.linalg.solve(A, rhs)
    S = sum(float((betas[f] - b_wfe) @ (XtX[f] / sig2[f]) @ (betas[f] - b_wfe)) for f in betas)
    T = int(np.mean(list(Ts.values())))
    delta = np.sqrt(N) * ((S / N) - k) / np.sqrt(2 * k)
    var_adj = 2 * k * (T - k - 1) / (T + 1)
    delta_adj = np.sqrt(N) * ((S / N) - k) / np.sqrt(var_adj)
    p = float(2 * (1 - stats.norm.cdf(abs(delta_adj))))
    return {"N": N, "k": k, "T": T, "delta": round(float(delta), 3),
            "delta_adj": round(float(delta_adj), 3), "p": round(p, 4),
            "rechaza_homogeneidad_5pct": bool(abs(delta_adj) > 1.96)}


def analizar():
    print("=== Pesaran-Yamagata: homogeneidad de pendientes ===")
    out = {}
    for suf, lab in [("_B", "Muestra B"), ("_C", "Muestra C")]:
        r = pesaran_yamagata(suf)
        if r:
            out[lab] = r
            estado = "rechaza homogeneidad" if r["rechaza_homogeneidad_5pct"] else "no rechaza (pooling justificado)"
            print(f"  {lab}: Delta_adj = {r['delta_adj']} (p={r['p']})  -> {estado}")
    return out


if __name__ == "__main__":
    analizar()
