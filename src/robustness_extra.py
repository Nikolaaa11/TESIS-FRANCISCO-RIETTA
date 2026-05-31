"""
robustness_extra.py
==================
Mejoras metodológicas de alto impacto (sugeridas por la revisión de buenas prácticas):

1. Corrección por pruebas múltiples (Benjamini-Hochberg / FDR) sobre los p-valores del panel,
   para controlar falsos positivos al estimar muchos coeficientes.
2. Betas estandarizados / magnitudes económicas: efecto de 1 desviación estándar de cada factor
   sobre el retorno (comparabilidad entre factores y entre mercados).
3. GARCH asimétrico (GJR-GARCH): contrasta el efecto apalancamiento (las malas noticias elevan
   más la volatilidad que las buenas), comparado con el GARCH simétrico vía BIC.
4. Local Projections (Jordà, 2005): IRF alternativa al VAR, robusta a mala especificación.

Datos reales (muestra B). Salida: web/robustness.json + outputs/figures/fig_lp.png
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from . import config as C
from . import panel_models as pm

COPPER = "#c9712d"
REGS = ["d_cobre", "d_vix", "d_fed_funds", "d_treasury10",
        "d_usdclp", "d_tasa_local", "d_actividad_local"]
ET = {"d_cobre": "Cobre", "d_vix": "VIX", "d_fed_funds": "Fed Funds",
      "d_treasury10": "Treasury 10Y", "d_usdclp": "TC CLP",
      "d_tasa_local": "Tasa local", "d_actividad_local": "Actividad local"}


def fdr_panel():
    from statsmodels.stats.multitest import multipletests
    panel = pd.read_parquet(C.DATA_PROCESSED / "panel_B.parquet")
    regs = [r for r in REGS if r in panel.columns]
    res = pm.panel_fe_driscoll_kraay(panel, "retorno", regs)
    p = res.pvalues[regs]
    rej, p_adj, _, _ = multipletests(p.values, alpha=0.05, method="fdr_bh")
    return [{"factor": ET.get(k, k), "p": round(float(p[k]), 4),
             "p_fdr": round(float(pa), 4), "sig_fdr": bool(r)}
            for k, pa, r in zip(regs, p_adj, rej)]


def betas_estandarizados():
    """Efecto en desviaciones estándar: beta_std = beta * sd(x)/sd(y)."""
    panel = pd.read_parquet(C.DATA_PROCESSED / "panel_B.parquet")
    regs = [r for r in REGS if r in panel.columns]
    res = pm.panel_fe_driscoll_kraay(panel, "retorno", regs)
    sd_y = panel["retorno"].std()
    out = []
    for r in regs:
        sd_x = panel[r].std()
        b = float(res.params.get(r, np.nan))
        out.append({"factor": ET.get(r, r), "beta": round(b, 4),
                    "beta_std": round(b * sd_x / sd_y, 4)})
    out.sort(key=lambda x: abs(x["beta_std"]), reverse=True)
    return out


def gjr_garch():
    from arch import arch_model
    s = pd.read_parquet(C.DATA_PROCESSED / "series_B.parquet")["retorno_cartera"].dropna() * 100
    g = arch_model(s, vol="GARCH", p=1, q=1, dist="t").fit(disp="off")
    gjr = arch_model(s, vol="GARCH", p=1, o=1, q=1, dist="t").fit(disp="off")
    gamma = float(gjr.params.get("gamma[1]", np.nan))
    return {"gjr_gamma": round(gamma, 4),
            "gjr_gamma_p": round(float(gjr.pvalues.get("gamma[1]", np.nan)), 4),
            "bic_garch": round(float(g.bic), 1), "bic_gjr": round(float(gjr.bic), 1),
            "prefiere_asimetrico": bool(gjr.bic < g.bic),
            "interpretacion": ("gamma>0 y significativo indica efecto apalancamiento: las caídas "
                               "elevan más la volatilidad futura que las alzas.")}


def local_projections(H=12):
    """Jordà (2005): respuesta del retorno a un shock del cobre por horizonte, con HAC."""
    s = pd.read_parquet(C.DATA_PROCESSED / "series_B.parquet")
    df = s[["retorno_cartera", "d_cobre", "d_vix", "d_usdclp"]].dropna()
    betas, lo, hi = [], [], []
    for h in range(H + 1):
        y = df["retorno_cartera"].shift(-h)
        X = sm.add_constant(df[["d_cobre", "d_vix", "d_usdclp"]])
        d = pd.concat([y.rename("y"), X], axis=1).dropna()
        m = sm.OLS(d["y"], d.drop(columns="y")).fit(cov_type="HAC", cov_kwds={"maxlags": h + 1})
        b = m.params["d_cobre"]; se = m.bse["d_cobre"]
        betas.append(b); lo.append(b - 1.96 * se); hi.append(b + 1.96 * se)
    # figura
    hh = np.arange(H + 1)
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.axhline(0, color="#888", lw=.8)
    ax.plot(hh, betas, color=COPPER, lw=2, marker="o", ms=3)
    ax.fill_between(hh, lo, hi, color=COPPER, alpha=.12)
    ax.set_xlabel("Horizonte (meses)"); ax.set_ylabel("Respuesta del retorno")
    ax.set_title("Local Projections (Jordà): respuesta a un shock del cobre (IC 95%)",
                 fontsize=11, weight="bold", loc="left")
    ax.grid(True, color="#e9e9ec")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig(C.FIGURES / "fig_lp.png", dpi=300); plt.close(fig)
    return {"h": [int(x) for x in hh], "resp": [round(float(b), 5) for b in betas],
            "lo": [round(float(x), 5) for x in lo], "hi": [round(float(x), 5) for x in hi]}


def construir():
    out = {"fdr": fdr_panel(), "betas_estandarizados": betas_estandarizados(),
           "gjr_garch": gjr_garch(), "local_projections": local_projections()}
    (C.WEB_DATA / "robustness.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: (v if not isinstance(v, dict) or "h" not in v else "[serie]")
                      for k, v in out.items()}, ensure_ascii=False, indent=2)[:1500])
    print("[ok] robustness.json + fig_lp.png")
    return out


if __name__ == "__main__":
    construir()
