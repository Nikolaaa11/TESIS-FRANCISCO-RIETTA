"""
make_figures.py
==============
Genera figuras de calidad de publicación (PNG, 300 dpi) a partir de los datos reales,
para incrustar en el documento de tesis (Word/PDF). Lee web/data.json.
"""

from __future__ import annotations
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

from . import config as C

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.edgecolor": "#bbbbbb", "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": "#e9e9ec", "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
})
BLUE, COPPER, GREEN, RED = "#0071e3", "#c9712d", "#34c759", "#ff3b30"


def _data():
    return json.loads((C.WEB_DATA / "data.json").read_text(encoding="utf-8"))


def fig_ciclo(d):
    cc = d["ciclo_cobre"]
    x = np.arange(len(cc["fechas"]))
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(x, cc["precio"], color=COPPER, lw=1.6)
    ax.fill_between(x, min(cc["precio"]), cc["precio"], color=COPPER, alpha=.06)
    # bandas de fase
    for i, f in enumerate(cc["fase"]):
        ax.axvspan(i - .5, i + .5, color=(GREEN if f == "expansion" else RED),
                   alpha=.06, lw=0)
    ticks = list(range(0, len(x), 24))
    ax.set_xticks(ticks)
    ax.set_xticklabels([cc["fechas"][t][:4] for t in ticks])
    ax.set_ylabel("Precio del cobre (USD/ton)")
    ax.set_title("Ciclo del precio del cobre y fases (Bry-Boschan), 2004–2024",
                 fontsize=11, weight="bold", loc="left")
    fig.savefig(C.FIGURES / "fig_ciclo_cobre.png")
    plt.close(fig)


def fig_coef(d):
    cf = d["coeficientes_B"]
    nombres = [c["factor"] for c in cf][::-1]
    vals = [c["coef"] for c in cf][::-1]
    sig = [c["sig"] for c in cf][::-1]
    colores = [(GREEN if v >= 0 else RED) if s else ("#a8e6b4" if v >= 0 else "#ffc1bd")
               for v, s in zip(vals, sig)]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.barh(nombres, vals, color=colores)
    ax.axvline(0, color="#888", lw=.8)
    ax.set_xlabel("Coeficiente (impacto sobre el retorno)")
    ax.set_title("Sensibilidad de los retornos por factor — muestra B\n(panel FE, Driscoll-Kraay)",
                 fontsize=11, weight="bold", loc="left")
    fig.savefig(C.FIGURES / "fig_coeficientes.png")
    plt.close(fig)


def fig_fevd(d):
    fv = d["fevd_B"]
    labels = ["Propio" if k == "retorno_cartera" else k for k in fv]
    vals = [v * 100 for v in fv.values()]
    colors = ["#c7c7cc", COPPER, BLUE, "#5e5ce6", "#ff9f0a"][:len(vals)]
    fig, ax = plt.subplots(figsize=(5.4, 4.2))
    w, _, at = ax.pie(vals, labels=labels, autopct="%1.1f%%", startangle=90,
                      colors=colors, wedgeprops=dict(width=.42, edgecolor="w"),
                      pctdistance=.78, textprops={"fontsize": 9})
    ax.set_title("Descomposición de varianza del retorno (FEVD, h=12)",
                 fontsize=11, weight="bold")
    fig.savefig(C.FIGURES / "fig_fevd.png")
    plt.close(fig)


def fig_tri(d):
    tri = d["triangulacion"]
    et = [t["muestra"].split("·")[0].strip() for t in tri]
    beta = [t["beta_cobre"] for t in tri]
    feg = [t["fevd_global"] for t in tri]
    x = np.arange(len(et)); w = .38
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.bar(x - w/2, beta, w, label="β cobre", color=BLUE)
    ax.bar(x + w/2, feg, w, label="Varianza global (FEVD)", color=COPPER)
    ax.set_xticks(x); ax.set_xticklabels(et)
    ax.legend(frameon=False)
    ax.set_title("Triangulación: sensibilidad al cobre y dominancia global por muestra",
                 fontsize=11, weight="bold", loc="left")
    fig.savefig(C.FIGURES / "fig_triangulacion.png")
    plt.close(fig)


ET = {"d_cobre": "Δ Cobre", "d_vix": "Δ VIX", "d_fed_funds": "Δ FedFunds",
      "d_treasury10": "Δ Tr10Y", "d_usdclp": "Δ TC", "d_tasa_local": "Δ Tasa",
      "d_actividad_local": "Δ Activ.", "retorno_cartera": "Retorno"}
REGS = ["retorno_cartera", "d_cobre", "d_vix", "d_fed_funds", "d_treasury10",
        "d_usdclp", "d_tasa_local", "d_actividad_local"]


def fig_correlacion():
    s = pd.read_parquet(C.DATA_PROCESSED / "series_B.parquet")
    cols = [c for c in REGS if c in s.columns]
    corr = s[cols].dropna().corr()
    labs = [ET.get(c, c) for c in cols]
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(labs))); ax.set_yticklabels(labs, fontsize=9)
    for i in range(len(labs)):
        for j in range(len(labs)):
            v = corr.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    color="white" if abs(v) > 0.55 else "#222", fontsize=8)
    ax.set_title("Matriz de correlación de los factores (muestra B)", fontsize=11, weight="bold")
    fig.colorbar(im, fraction=0.046, pad=0.04)
    fig.savefig(C.FIGURES / "fig_correlacion.png"); plt.close(fig)


def fig_distribucion():
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    for suf, lab, col in [("_B", "B · internacional", BLUE), ("_A", "A · Pucobre", COPPER),
                          ("_C", "C · minería", GREEN)]:
        r = pd.read_parquet(C.DATA_PROCESSED / f"series{suf}.parquet")["retorno_cartera"].dropna()
        ax.hist(r, bins=35, alpha=.45, color=col, label=lab, density=True)
    ax.set_xlabel("Retorno mensual"); ax.set_ylabel("Densidad")
    ax.set_title("Distribución de los retornos mensuales por muestra", fontsize=11, weight="bold", loc="left")
    ax.legend(frameon=False)
    fig.savefig(C.FIGURES / "fig_distribucion.png"); plt.close(fig)


def fig_garch():
    from arch import arch_model
    r = pd.read_parquet(C.DATA_PROCESSED / "series_B.parquet")["retorno_cartera"].dropna() * 100
    res = arch_model(r, vol="GARCH", p=1, q=1, dist="t").fit(disp="off")
    cv = res.conditional_volatility
    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    ax.plot(r.index, cv, color=COPPER, lw=1.4)
    ax.fill_between(r.index, 0, cv, color=COPPER, alpha=.08)
    ax.set_ylabel("Volatilidad condicional (%)")
    ax.set_title("Volatilidad condicional estimada (GARCH(1,1)) — cartera B",
                 fontsize=11, weight="bold", loc="left")
    fig.savefig(C.FIGURES / "fig_garch.png"); plt.close(fig)


def fig_betas(d):
    bs = (d.get("avanzado", {}) or {}).get("betas_estandarizados")
    if not bs:
        return
    bs = sorted(bs, key=lambda x: abs(x["beta_std"]))
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.barh([x["factor"] for x in bs], [x["beta_std"] for x in bs],
            color=[GREEN if x["beta_std"] >= 0 else RED for x in bs])
    ax.axvline(0, color="#888", lw=.8)
    ax.set_xlabel("Efecto en desviaciones estándar (σ)")
    ax.set_title("Importancia económica: betas estandarizados (muestra B)",
                 fontsize=11, weight="bold", loc="left")
    fig.savefig(C.FIGURES / "fig_betas.png"); plt.close(fig)


def fig_predictor():
    import json
    f = C.WEB_DATA / "predictor.json"
    if not f.exists():
        return
    m = json.loads(f.read_text(encoding="utf-8"))["metricas_oos"]
    nombres = list(m.keys())
    r2 = [m[k]["r2_oos"] for k in nombres]
    dirn = [m[k]["acierto_direccional"] * 100 for k in nombres]
    x = np.arange(len(nombres)); w = .38
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    ax.bar(x - w/2, r2, w, label="R² fuera de muestra", color=BLUE)
    ax2 = ax.twinx()
    ax2.bar(x + w/2, dirn, w, label="Acierto direccional (%)", color=COPPER)
    ax.axhline(0, color="#888", lw=.8)
    ax.set_xticks(x); ax.set_xticklabels(nombres, rotation=20, ha="right", fontsize=8)
    ax.set_ylabel("R² OOS"); ax2.set_ylabel("Acierto direccional (%)")
    ax.set_title("Desempeño predictivo fuera de muestra por modelo",
                 fontsize=11, weight="bold", loc="left")
    fig.savefig(C.FIGURES / "fig_predictor.png"); plt.close(fig)


def construir():
    d = _data()
    fig_ciclo(d); fig_coef(d); fig_fevd(d); fig_tri(d)
    fig_correlacion(); fig_distribucion(); fig_garch(); fig_betas(d); fig_predictor()
    print("[ok] figuras en", C.FIGURES)


if __name__ == "__main__":
    construir()
