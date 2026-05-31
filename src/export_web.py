"""
export_web.py
============
Exporta los resultados reales (preliminares) del análisis a `web/data.json`,
para alimentar los gráficos de la plataforma web (Vercel).

NO inventa datos: todo se computa de los paneles en data/processed/.
Marca los resultados como preliminares (faltan EMBI y controles de empresa).
"""

from __future__ import annotations
import json
import numpy as np
import pandas as pd

from . import config as C
from . import panel_models as pm
from . import var_irf as vi
from . import cycle_dating as cd
from . import stationarity as st

MUESTRAS = [("_B", "B · cobre internacional", "global"),
            ("_A", "A · cobre Chile", "chileno"),
            ("_C", "C · minería Chile", "chileno")]

REGS = ["d_cobre", "d_vix", "d_fed_funds", "d_treasury10",
        "d_usdclp", "d_tasa_local", "d_actividad_local"]
ETIQUETAS = {
    "d_cobre": "Cobre", "d_vix": "VIX (riesgo)", "d_fed_funds": "Fed Funds",
    "d_treasury10": "Treasury 10Y", "d_usdclp": "Tipo cambio CLP",
    "d_tasa_local": "Tasa local", "d_actividad_local": "Actividad local",
}


def _modelo(panel):
    regs = [r for r in REGS if r in panel.columns]
    n = panel.index.get_level_values(0).nunique()
    if n > 1:
        res = pm.panel_fe_driscoll_kraay(panel, "retorno", regs)
        return res.params, res.pvalues, float(res.rsquared_within), n
    serie = panel.reset_index(level=0, drop=True)
    res = pm.baseline_cartera(serie["retorno"], serie[regs], maxlags=4)
    return res.params, res.pvalues, float(res.rsquared), n


def _fevd(series_wide):
    cols = [c for c in ["d_cobre", "d_vix", "d_usdclp", "d_tasa_local"]
            if c in series_wide.columns]
    datos = series_wide[["retorno_cartera"] + cols].dropna()
    orden = cols + ["retorno_cartera"]
    res = vi.estimar_var(datos[orden], orden=orden, p=2)
    f = vi.tabla_fevd_variable(res, "retorno_cartera", periodos=(12,)).loc[12]
    return {ETIQUETAS.get(k, k): round(float(v), 4) for k, v in f.items()}


def construir_json():
    out = {"meta": {"periodo": f"{C.FECHA_INICIO[:4]}–{C.FECHA_FIN[:4]}",
                    "nota": "Resultados preliminares: faltan EMBI y controles de empresa.",
                    "n_muestras": len(MUESTRAS)}}

    # 1. Triangulación + coeficientes + FEVD por muestra
    tri, coefs_B, fevd_B = [], None, None
    for suf, etiqueta, mercado in MUESTRAS:
        rp = C.DATA_PROCESSED / f"panel{suf}.parquet"
        rs = C.DATA_PROCESSED / f"series{suf}.parquet"
        if not rp.exists():
            continue
        panel = pd.read_parquet(rp)
        params, pvals, r2, n = _modelo(panel)
        fila = {"muestra": etiqueta, "mercado": mercado, "n": n,
                "beta_cobre": round(float(params.get("d_cobre", np.nan)), 4),
                "p_cobre": round(float(pvals.get("d_cobre", np.nan)), 4),
                "r2": round(r2, 4)}
        if rs.exists():
            fevd = _fevd(pd.read_parquet(rs))
            fila["fevd_global"] = round(sum(v for k, v in fevd.items()
                                            if k in ("Cobre", "VIX (riesgo)")), 4)
            if suf == "_B":
                fevd_B = fevd
        tri.append(fila)
        if suf == "_B":
            coefs_B = [{"factor": ETIQUETAS.get(k, k), "coef": round(float(v), 4),
                        "sig": bool(pvals.get(k, 1) < 0.05)}
                       for k, v in params.items() if k in REGS]
    out["triangulacion"] = tri
    out["coeficientes_B"] = coefs_B
    out["fevd_B"] = fevd_B

    # 2. Ciclo del cobre (precio mensual + fase)
    g = pd.read_parquet(C.DATA_INTERIM / "raw_macro_global.parquet")
    cobre = g["cobre"].resample("ME").last().loc[C.FECHA_INICIO:C.FECHA_FIN].dropna()
    fechado = cd.datar_ciclo_cobre(cobre, k=6)
    out["ciclo_cobre"] = {
        "fechas": [d.strftime("%Y-%m") for d in fechado.index],
        "precio": [round(float(x), 2) for x in fechado["precio"]],
        "fase": list(fechado["fase"]),
    }

    # 3. OE1 estacionariedad (cobre nivel/retorno, TC, VIX)
    serie_niv = pd.DataFrame({
        "Cobre (nivel)": np.log(cobre),
        "Cobre (retorno)": np.log(cobre).diff(),
        "Tipo cambio (nivel)": np.log(pd.read_parquet(
            C.DATA_INTERIM / "raw_macro_local_fred.parquet")["usdclp"]
            .resample("ME").last().loc[C.FECHA_INICIO:C.FECHA_FIN]),
    }).dropna()
    tabla = st.tabla_estacionariedad(serie_niv)
    out["estacionariedad"] = [
        {"variable": idx, "adf_p": round(float(r["ADF_p"]), 4),
         "kpss_p": round(float(r["KPSS_p"]), 4), "orden": r["orden_integracion"]}
        for idx, r in tabla.iterrows()]

    # 4. Fusionar hallazgos avanzados (advanced.json + extensions.json) si existen
    avz = {}
    for nombre in ("advanced.json", "extensions.json"):
        f = C.ROOT / "web" / nombre
        if f.exists():
            try:
                avz.update(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                pass
    if avz:
        out["avanzado"] = avz

    ruta = C.ROOT / "web" / "data.json"
    ruta.parent.mkdir(exist_ok=True)
    ruta.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[guardado] {ruta}  ({len(json.dumps(out))} bytes)")
    return out


if __name__ == "__main__":
    construir_json()
