"""
market_comparison.py
===================
Prueba FORMAL de la hipótesis de transmisión diferenciada entre mercados (H7 / OE6).

Combina las muestras B (mercado internacional) y C (mercado chileno) en un único panel,
con un indicador 'global' (1 = empresa que cotiza en el mercado internacional) e interacciones
factor × global. Bajo efectos fijos por empresa, el indicador 'global' (invariante en el tiempo)
es absorbido, pero las INTERACCIONES con los factores (que sí varían en el tiempo) son estimables.

El coeficiente de la interacción d_cobre × global mide la DIFERENCIA en la sensibilidad al cobre
entre el mercado internacional y el chileno. Su significancia es la prueba directa de H7 en su
dimensión de sensibilidad: si no es significativa, el cobre se precia de forma estadísticamente
equivalente en ambos mercados.
"""
from __future__ import annotations
import pandas as pd
import numpy as np

from . import config as C
from . import panel_models as pm

FACTORES = ["d_cobre", "d_vix", "d_usdclp"]


def construir_panel_combinado():
    pB = pd.read_parquet(C.DATA_PROCESSED / "panel_B.parquet").copy()
    pC = pd.read_parquet(C.DATA_PROCESSED / "panel_C.parquet").copy()
    pB["global"] = 1
    pC["global"] = 0
    # PUCOBRE.SN está en C; evita duplicar empresas entre paneles
    combinado = pd.concat([pB, pC])
    return combinado


def test_diferencia():
    panel = construir_panel_combinado()
    for f in FACTORES:
        if f in panel.columns:
            panel[f + "_x_global"] = panel[f] * panel["global"]
    regs = [f for f in FACTORES if f in panel.columns] + \
           [f + "_x_global" for f in FACTORES if f in panel.columns]
    res = pm.panel_fe_driscoll_kraay(panel, "retorno", regs)

    out = {}
    for f in FACTORES:
        ix = f + "_x_global"
        if ix in res.params.index:
            out[f] = {"dif_global_vs_local": round(float(res.params[ix]), 4),
                      "p": round(float(res.pvalues[ix]), 4),
                      "difiere_sig": bool(res.pvalues[ix] < 0.05)}
    return out, res


def analizar():
    out, res = test_diferencia()
    print("=== H7: ¿difiere la sensibilidad entre mercado internacional y chileno? ===")
    print(f"   (N={int(res.nobs)}, empresas={res.entity_info.total})")
    for f, v in out.items():
        sig = "SÍ difiere" if v["difiere_sig"] else "no difiere (equivalente)"
        print(f"   {f:10s}: dif (global-local) = {v['dif_global_vs_local']:+.4f}  p={v['p']:.4f}  -> {sig}")
    return out


if __name__ == "__main__":
    analizar()
