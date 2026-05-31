"""
advanced_results.py
==================
Completa el análisis empírico con los componentes que faltaban por correr de verdad:
- Zivot-Andrews sobre tipo de cambio y cobre (resuelve el orden de integración con quiebre).
- OE5: modelo de interacción por fase del ciclo (sensibilidad condicional al régimen).
- Diagnósticos: CD de Pesaran (dependencia de sección cruzada), estabilidad del VAR,
  selección de rezagos, causalidad de Granger.
- Robustez: β del cobre en submuestras (pre/post 2020).
- Figura de impulso-respuesta (cobre -> retorno).

Salida: web/advanced.json  +  outputs/figures/fig_irf.png
Todo sobre datos reales (muestra B). Resultados preliminares.
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from . import config as C
from . import panel_models as pm
from . import var_irf as vi
from . import stationarity as st

COPPER, BLUE = "#c9712d", "#0071e3"


def cd_pesaran(resid_wide: pd.DataFrame):
    R = resid_wide.corr()
    N = R.shape[0]
    T = resid_wide.dropna().shape[0]
    rho = R.values[np.triu_indices(N, 1)]
    CD = np.sqrt(2 * T / (N * (N - 1))) * np.nansum(rho)
    from scipy.stats import norm
    return float(CD), float(2 * (1 - norm.cdf(abs(CD))))


def construir():
    out = {}
    panel = pd.read_parquet(C.DATA_PROCESSED / "panel_B.parquet")
    series = pd.read_parquet(C.DATA_PROCESSED / "series_B.parquet")

    # ---- Zivot-Andrews (quiebre endógeno) sobre niveles ----
    g = pd.read_parquet(C.DATA_INTERIM / "raw_macro_global.parquet")
    lf = pd.read_parquet(C.DATA_INTERIM / "raw_macro_local_fred.parquet")
    cobre_lvl = np.log(g["cobre"].resample("ME").last().loc[C.FECHA_INICIO:C.FECHA_FIN]).dropna()
    tc_lvl = np.log(lf["usdclp"].resample("ME").last().loc[C.FECHA_INICIO:C.FECHA_FIN]).dropna()
    za = {}
    for nombre, s in [("cobre_nivel", cobre_lvl), ("tc_nivel", tc_lvl),
                      ("tc_dif", tc_lvl.diff().dropna())]:
        stat, p = st._zivot_andrews(s)
        za[nombre] = {"stat": round(float(stat), 4), "p": round(float(p), 4)}
    out["zivot_andrews"] = za

    # ---- OE5: interacción por fase del ciclo ----
    pB = panel.copy()
    pB["d_cobre_x_exp"] = pB["d_cobre"] * pB["exp"]
    regs5 = ["d_cobre", "d_cobre_x_exp", "d_vix", "d_usdclp", "exp"]
    regs5 = [r for r in regs5 if r in pB.columns]
    res5 = pm.panel_fe_driscoll_kraay(pB, "retorno", regs5)
    out["oe5_interaccion"] = {
        "beta_cobre_base": round(float(res5.params.get("d_cobre", np.nan)), 4),
        "beta_cobre_x_exp": round(float(res5.params.get("d_cobre_x_exp", np.nan)), 4),
        "p_interaccion": round(float(res5.pvalues.get("d_cobre_x_exp", np.nan)), 4),
        "interpretacion": "beta_cobre en contracción = base; en expansión = base + interacción",
    }

    # ---- Diagnósticos panel: CD de Pesaran ----
    regs2 = ["d_cobre", "d_vix", "d_fed_funds", "d_treasury10",
             "d_usdclp", "d_tasa_local", "d_actividad_local"]
    regs2 = [r for r in regs2 if r in panel.columns]
    res2 = pm.panel_fe_driscoll_kraay(panel, "retorno", regs2)
    resid_wide = res2.resids.unstack(level=0)
    cd_stat, cd_p = cd_pesaran(resid_wide)
    out["cd_pesaran"] = {"stat": round(cd_stat, 4), "p": round(cd_p, 4),
                         "conclusion": "dependencia de sección cruzada significativa"
                         if cd_p < 0.05 else "sin evidencia de dependencia cruzada"}

    # ---- VAR: estabilidad, rezagos, Granger ----
    cols = [c for c in ["d_cobre", "d_vix", "d_usdclp", "retorno_cartera"] if c in series.columns]
    datos = series[cols].dropna()
    sel = vi.seleccionar_rezagos(datos, maxlags=12)
    p_opt = int(sel["AIC"].astype(float).idxmin()) if "AIC" in sel else 2
    p_opt = max(1, min(p_opt, 6))
    resV = vi.estimar_var(datos, orden=cols, p=p_opt)
    g_stat, g_p = vi.granger_causalidad(resV, "d_cobre", "retorno_cartera")
    out["var_diag"] = {"rezagos_aic": p_opt, "estable": bool(resV.is_stable()),
                       "granger_cobre_retorno_F": round(float(g_stat), 3),
                       "granger_cobre_retorno_p": round(float(g_p), 4)}

    # ---- Robustez: β cobre pre/post 2020 ----
    rob = {}
    for etiqueta, sl in [("2004-2019", slice("2004", "2019")), ("2020-2024", slice("2020", "2024"))]:
        sub = panel.loc[(slice(None), sl), :]
        try:
            r = pm.panel_fe_driscoll_kraay(sub, "retorno", regs2)
            rob[etiqueta] = round(float(r.params.get("d_cobre", np.nan)), 4)
        except Exception:
            rob[etiqueta] = None
    out["robustez_beta_cobre"] = rob

    # ---- Figura IRF: cobre -> retorno ----
    irf = resV.irf(18)
    idx_c = cols.index("d_cobre"); idx_r = cols.index("retorno_cartera")
    resp = irf.orth_irfs[:, idx_r, idx_c]
    try:
        se = irf.stderr(orth=True)[:, idx_r, idx_c]
    except Exception:
        se = np.zeros_like(resp)
    h = np.arange(len(resp))
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.axhline(0, color="#888", lw=.8)
    ax.plot(h, resp, color=COPPER, lw=2, marker="o", ms=3)
    ax.fill_between(h, resp - 2*se, resp + 2*se, color=COPPER, alpha=.12)
    ax.set_xlabel("Meses tras el shock"); ax.set_ylabel("Respuesta del retorno")
    ax.set_title("Impulso-respuesta: shock del cobre → retorno del sector (±2 e.e.)",
                 fontsize=11, weight="bold", loc="left")
    ax.grid(True, color="#e9e9ec")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig(C.FIGURES / "fig_irf.png", dpi=300)
    plt.close(fig)

    (C.ROOT / "web" / "advanced.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print("[ok] fig_irf.png + advanced.json")
    return out


if __name__ == "__main__":
    construir()
