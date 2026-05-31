"""
make_figures.py
==============
Genera figuras de calidad de publicación (PNG, 300 dpi) a partir de los datos reales,
para incrustar en el documento de tesis (Word/PDF). Lee web/data.json.
"""

from __future__ import annotations
import json
import numpy as np
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


def construir():
    d = _data()
    fig_ciclo(d); fig_coef(d); fig_fevd(d); fig_tri(d)
    print("[ok] figuras en", C.FIGURES)


if __name__ == "__main__":
    construir()
