"""
test_core.py
===========
Suite de pruebas unitarias de las funciones econométricas clave, con datos SINTÉTICOS
(sin red ni dependencia de los datos descargados). Verifica que el aparato metodológico
se comporta como debe sobre casos de referencia conocidos.

Ejecutar:  python -m pytest -q
"""
import numpy as np
import pandas as pd

from src import stationarity as st
from src import cycle_dating as cd
from src import transformations as T
from src import panel_models as pm


def _rng():
    return np.random.default_rng(42)


# ---------------- Estacionariedad (OE1) ----------------
def test_ruido_blanco_es_I0():
    s = pd.Series(_rng().standard_normal(400))
    r = st.test_una_serie(s, "ruido")
    assert r["orden_integracion"] == "I(0)"


def test_random_walk_es_I1():
    s = pd.Series(_rng().standard_normal(400).cumsum())
    r = st.test_una_serie(s, "rw")
    assert r["orden_integracion"] == "I(1)"


def test_tabla_estacionariedad_columnas():
    rng = _rng()
    df = pd.DataFrame({"a": rng.standard_normal(200), "b": rng.standard_normal(200).cumsum()})
    tabla = st.tabla_estacionariedad(df)
    assert {"ADF_p", "KPSS_p", "orden_integracion"} <= set(tabla.columns)
    assert len(tabla) == 2


# ---------------- Fechado del ciclo (OE5) ----------------
def test_ciclo_detecta_dos_fases():
    n = 180
    t = np.arange(n)
    serie = 100 * np.exp(0.002 * t) * (1 + 0.3 * np.sin(2 * np.pi * t / 48))
    idx = pd.period_range("2008-01", periods=n, freq="M").to_timestamp("M")
    precio = pd.Series(serie, index=idx)
    res = cd.datar_ciclo_cobre(precio, k=6, min_fase=6, min_ciclo=15)
    fases = set(res["fase"].dropna().unique())
    assert fases == {"expansion", "contraccion"}
    # debe haber al menos un pico y un valle
    tp = res["turning_point"].dropna().tolist()
    assert "P" in tp and "V" in tp


# ---------------- Transformaciones ----------------
def test_retorno_log_correcto():
    precios = pd.DataFrame({"x": [100.0, 110.0, 99.0]})
    r = T.retorno_log(precios)["x"].tolist()
    assert np.isnan(r[0])
    assert abs(r[1] - np.log(110 / 100)) < 1e-9
    assert abs(r[2] - np.log(99 / 110)) < 1e-9


def test_cartera_equiponderada_promedia():
    ret = pd.DataFrame({"a": [0.02, -0.01], "b": [0.04, 0.03]})
    cart = T.cartera_equiponderada(ret).tolist()
    assert abs(cart[0] - 0.03) < 1e-12
    assert abs(cart[1] - 0.01) < 1e-12


# ---------------- Panel de efectos fijos (OE2) ----------------
def test_panel_fe_recupera_coeficiente():
    rng = _rng()
    fechas = pd.period_range("2010-01", periods=120, freq="M").to_timestamp("M")
    factor = pd.Series(rng.standard_normal(len(fechas)), index=fechas)
    filas = []
    for e in ["A", "B", "C", "D"]:
        ruido = rng.standard_normal(len(fechas)) * 0.5
        y = 0.8 * factor.values + ruido + (1.0 if e == "A" else 0.0)  # efecto fijo por empresa
        filas.append(pd.DataFrame({"empresa": e, "fecha": fechas, "retorno": y,
                                   "d_cobre": factor.values}))
    panel = pd.concat(filas).set_index(["empresa", "fecha"])
    res = pm.panel_fe_driscoll_kraay(panel, "retorno", ["d_cobre"])
    assert abs(float(res.params["d_cobre"]) - 0.8) < 0.1
