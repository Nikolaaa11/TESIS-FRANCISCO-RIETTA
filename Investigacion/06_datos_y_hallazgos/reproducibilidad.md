# Declaración de reproducibilidad

Este proyecto está diseñado para ser **completamente reproducible**. Todos los resultados,
tablas y figuras de la tesis se generan a partir de datos públicos mediante código abierto y
determinista.

## Cómo reproducir

```powershell
# 1. Entorno
python -m venv .venv && .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. (opcional) Volver a descargar los datos de fuentes públicas
python -m src.run_all --descargar

# 3. Regenerar TODO el análisis (paneles, tests, robustez, predictor, figuras, anexos)
python -m src.run_all

# 4. Pruebas unitarias
python -m pytest -q

# 5. Regenerar el documento Word/PDF (requiere Microsoft Word)
python build_thesis.py
```

## Garantías

- **Determinismo:** el pipeline produce exactamente los mismos resultados en cada ejecución
  (semillas fijas donde aplica; sin aleatoriedad no controlada). Una corrida de verificación
  confirmó **0 diferencias** entre ejecuciones sucesivas.
- **Cobertura:** `python -m src.run_all` ejecuta los 12 pasos del análisis (construcción de
  paneles → diagnósticos avanzados → robustez de segunda generación → predictor → exportación de
  datos, figuras y anexos) con reporte de estado por paso.
- **Pruebas:** la suite `tests/` valida las funciones econométricas clave sobre datos sintéticos
  de referencia (estacionariedad I(0)/I(1), fechado del ciclo, transformaciones, panel de efectos
  fijos).
- **Fuentes:** todos los datos provienen de fuentes públicas (FRED, Yahoo Finance) y, donde
  corresponde, del Banco Central de Chile; los códigos y tickers están documentados en
  `src/config.py` y en el Anexo G.

## Estructura del código

| Módulo `src/` | Función |
|---|---|
| `config`, `data_acquisition`, `transformations` | Configuración, descarga y transformación de datos |
| `stationarity`, `panel_unit_root` | Raíz unitaria individual y en panel (ADF/PP/KPSS/ZA, CIPS) |
| `panel_models`, `hausman_test` | Panel de efectos fijos (Driscoll-Kraay), FE vs RE |
| `cointegration`, `extensions` | ARDL/Johansen/VECM, Gregory-Hansen, GARCH |
| `var_irf`, `cycle_dating` | VAR/IRF/FEVD, fechado del ciclo (Bry-Boschan) |
| `robustness_extra`, `variance_ratio`, `market_comparison` | FDR, betas, GJR, Local Projections, Lo-MacKinlay, H7 |
| `predictor` | Extensión predictiva del precio del cobre |
| `make_figures`, `full_tables`, `export_web` | Figuras, anexos y datos para la plataforma |
| `run_all` | Orquestador del pipeline completo |
