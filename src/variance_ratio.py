"""
variance_ratio.py
================
Test de razón de varianzas de Lo y MacKinlay (1988) para la hipótesis de paseo aleatorio
(eficiencia de mercado en forma débil), con estadístico robusto a heterocedasticidad.

VR(q) = Var(retorno a q períodos) / (q · Var(retorno a 1 período)). Bajo paseo aleatorio,
VR(q) = 1. El estadístico M2(q) ~ N(0,1); |z| > 1,96 rechaza el paseo aleatorio al 5%.

Complementa la extensión predictiva: si no se rechaza el paseo aleatorio, los retornos no son
predecibles linealmente, coherente con que los factores macro expliquen pero no anticipen.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

from . import config as C


def variance_ratio(r: pd.Series, q: int):
    r = pd.Series(r).dropna().values
    T = len(r)
    mu = r.mean()
    # varianza a 1 período (insesgada)
    sa = np.sum((r - mu) ** 2) / (T - 1)
    # varianza a q períodos (solapada, insesgada)
    m = q * (T - q + 1) * (1 - q / T)
    suma = 0.0
    for t in range(q - 1, T):
        suma += (np.sum(r[t - q + 1: t + 1]) - q * mu) ** 2
    sc = suma / m
    vr = sc / sa
    # estadístico robusto a heterocedasticidad (Lo-MacKinlay)
    denom = np.sum((r - mu) ** 2) ** 2
    theta = 0.0
    for j in range(1, q):
        num = np.sum(((r[j:] - mu) ** 2) * ((r[:-j] - mu) ** 2))
        delta = T * num / denom        # factor T (Lo-MacKinlay 1988)
        theta += ((2 * (q - j) / q) ** 2) * delta
    z = np.sqrt(T) * (vr - 1) / np.sqrt(theta) if theta > 0 else np.nan
    from scipy.stats import norm
    p = 2 * (1 - norm.cdf(abs(z)))
    return {"q": q, "VR": round(float(vr), 4), "z_robusto": round(float(z), 3),
            "p": round(float(p), 4), "rechaza_paseo_aleatorio_5pct": bool(abs(z) > 1.96)}


def analizar():
    g = pd.read_parquet(C.DATA_INTERIM / "raw_macro_global.parquet")
    cobre_ret = np.log(g["cobre"].resample("ME").last()).diff().loc[C.FECHA_INICIO:C.FECHA_FIN]
    cartera = pd.read_parquet(C.DATA_PROCESSED / "series_B.parquet")["retorno_cartera"]
    out = {}
    for nombre, serie in [("cobre", cobre_ret), ("cartera_B", cartera)]:
        out[nombre] = [variance_ratio(serie, q) for q in (2, 4, 8, 12)]
        print(f"=== {nombre} ===")
        for r in out[nombre]:
            estado = "rechaza RW" if r["rechaza_paseo_aleatorio_5pct"] else "no rechaza RW"
            print(f"   q={r['q']:2d}  VR={r['VR']:.3f}  z={r['z_robusto']:+.2f}  p={r['p']:.3f}  -> {estado}")
    return out


if __name__ == "__main__":
    analizar()
