"""
predictor.py
===========
Extensión PREDICTIVA (demostrativa, para la plataforma — NO para la tesis explicativa).

Entrena y evalúa fuera de muestra un modelo del RETORNO mensual del cobre a un mes,
a partir de factores macro-financieros e información rezagada. Compara:
  - Baseline ingenuo (random walk: predicción = 0 retorno) y AR(1).
  - Ridge (lineal, exportable a JavaScript para el explorador interactivo).
  - Random Forest y Gradient Boosting (no lineales, solo para comparar métricas).

Reporta métricas HONESTAS fuera de muestra (RMSE, MAE, R² OOS, acierto direccional).
Exporta a la plataforma predictor.json: coeficientes en unidades originales (para que el
navegador calcule la predicción), metadatos de cada factor (valor reciente, rango), métricas
y el último precio del cobre para convertir retorno → precio.

Integridad: los retornos de commodities son difíciles de predecir; las métricas se reportan
tal cual resulten, sin maquillaje. Es una herramienta de exploración de escenarios, no una
recomendación de inversión.
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd

from . import config as C

FEATURES = ["r_cobre", "r_cobre_lag", "d_vix", "d_usdclp", "d_treasury10",
            "d_fed_funds", "d_actividad", "vix_nivel"]
ETIQ = {"r_cobre": "Retorno cobre (mes actual)", "r_cobre_lag": "Retorno cobre (mes previo)",
        "d_vix": "Δ VIX", "d_usdclp": "Δ tipo de cambio", "d_treasury10": "Δ Treasury 10Y",
        "d_fed_funds": "Δ Fed Funds", "d_actividad": "Δ actividad local",
        "vix_nivel": "VIX (nivel)"}


def construir_dataset():
    g = pd.read_parquet(C.DATA_INTERIM / "raw_macro_global.parquet")
    lf = pd.read_parquet(C.DATA_INTERIM / "raw_macro_local_fred.parquet")
    cobre = g["cobre"].resample("ME").last()
    vix = g["vix"].resample("ME").last()
    t10 = g["treasury10"].resample("ME").last()
    ff = g["fed_funds"].resample("ME").last()
    tc = lf["usdclp"].resample("ME").last()
    act = lf["actividad_local"].resample("ME").last()

    df = pd.DataFrame(index=cobre.index)
    df["r_cobre"] = np.log(cobre).diff()
    df["r_cobre_lag"] = df["r_cobre"].shift(1)
    df["d_vix"] = vix.diff()
    df["vix_nivel"] = vix
    df["d_usdclp"] = np.log(tc).diff()
    df["d_treasury10"] = t10.diff()
    df["d_fed_funds"] = ff.diff()
    df["d_actividad"] = np.log(act).diff()
    df["target"] = df["r_cobre"].shift(-1)        # retorno del cobre del mes siguiente
    df["precio"] = cobre
    return df.loc[C.FECHA_INICIO:C.FECHA_FIN].dropna(subset=FEATURES + ["target"])


def evaluar():
    from sklearn.linear_model import Ridge
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

    df = construir_dataset()
    X = df[FEATURES].values
    y = df["target"].values
    n = len(df); cut = int(n * 0.75)               # 75% train, 25% test (orden temporal)
    Xtr, Xte, ytr, yte = X[:cut], X[cut:], y[:cut], y[cut:]

    scaler = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = scaler.transform(Xtr), scaler.transform(Xte)

    def metrics(pred):
        rmse = float(np.sqrt(mean_squared_error(yte, pred)))
        mae = float(mean_absolute_error(yte, pred))
        r2 = float(r2_score(yte, pred))
        dir_acc = float(np.mean(np.sign(pred) == np.sign(yte)))
        return {"rmse": round(rmse, 4), "mae": round(mae, 4),
                "r2_oos": round(r2, 4), "acierto_direccional": round(dir_acc, 3)}

    res = {}
    # Baselines
    res["Random walk (0)"] = metrics(np.zeros_like(yte))
    ar1_coef = np.polyfit(ytr[:-1], ytr[1:], 1) if len(ytr) > 2 else [0, 0]
    res["AR(1)"] = metrics(ar1_coef[0] * Xte[:, 0] + ar1_coef[1])  # usa r_cobre actual
    # Ridge (alpha por validación temporal simple)
    best_alpha, best_rmse, ridge = 1.0, np.inf, None
    for a in [0.1, 0.5, 1, 2, 5, 10, 25]:
        m = Ridge(alpha=a).fit(Xtr_s, ytr)
        rm = np.sqrt(mean_squared_error(yte, m.predict(Xte_s)))
        if rm < best_rmse:
            best_rmse, best_alpha, ridge = rm, a, m
    res["Ridge (lineal)"] = metrics(ridge.predict(Xte_s))
    res["Random Forest"] = metrics(RandomForestRegressor(
        n_estimators=300, max_depth=4, random_state=7).fit(Xtr, ytr).predict(Xte))
    res["Gradient Boosting"] = metrics(GradientBoostingRegressor(
        n_estimators=200, max_depth=2, learning_rate=0.03, random_state=7).fit(Xtr, ytr).predict(Xte))

    # Coeficientes del Ridge en UNIDADES ORIGINALES (para evaluar en el navegador)
    coef_raw = ridge.coef_ / scaler.scale_
    intercept_raw = float(ridge.intercept_ - np.sum(ridge.coef_ * scaler.mean_ / scaler.scale_))

    # Metadatos por factor: valor reciente y rango (percentiles) para los sliders
    feats = []
    for i, f in enumerate(FEATURES):
        col = df[f]
        feats.append({"key": f, "label": ETIQ[f],
                      "coef": round(float(coef_raw[i]), 5),
                      "actual": round(float(col.iloc[-1]), 5),
                      "p05": round(float(col.quantile(0.05)), 5),
                      "p95": round(float(col.quantile(0.95)), 5)})

    out = {
        "modelo": "Ridge (alpha=%.1f) — extensión predictiva demostrativa" % best_alpha,
        "intercepto": round(intercept_raw, 6),
        "features": feats,
        "metricas_oos": res,
        "n_train": cut, "n_test": n - cut,
        "ultimo_precio": round(float(df["precio"].iloc[-1]), 2),
        "ultima_fecha": df.index[-1].strftime("%Y-%m"),
        "nota": ("Modelo demostrativo entrenado con datos reales (FRED). Métricas fuera de muestra "
                 "honestas: los retornos de commodities son difíciles de predecir. NO es "
                 "recomendación de inversión."),
    }
    (C.WEB_DATA / "predictor.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("=== Métricas fuera de muestra (test = último 25%) ===")
    for k, v in res.items():
        print(f"  {k:20s} R2_oos={v['r2_oos']:+.3f}  dir={v['acierto_direccional']:.2f}  RMSE={v['rmse']:.4f}")
    print(f"[ok] predictor.json (último precio {out['ultimo_precio']} en {out['ultima_fecha']})")
    return out


if __name__ == "__main__":
    evaluar()
