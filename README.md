# Tesis — Impacto de variables macroeconómicas globales y financieras en la valoración bursátil del sector minería de cobre en Chile

Magíster en Data Science. Enfoque **explicativo / de medición de impacto** (no predictivo),
con econometría de series de tiempo y datos de panel aplicada en Python.

## Estructura del proyecto

```
.
├── README.md
├── requirements.txt
├── data/
│   ├── raw/         # Descargas MANUALES (BCCh, Cochilco, CMF). No versionar datos pesados.
│   ├── interim/     # Series descargadas/limpiadas (parquet)
│   └── processed/   # Panel final listo para modelar
├── src/
│   ├── config.py            # Rutas, período, universo de empresas, diccionario de variables
│   ├── data_acquisition.py  # Descarga Yahoo/FRED + carga de CSV locales
│   ├── transformations.py   # Retornos, cartera del sector, remuestreo, panel long
│   └── stationarity.py      # OE1: ADF, PP, KPSS, Zivot-Andrews
├── notebooks/
│   ├── 01_adquisicion_datos.ipynb
│   └── 02_eda_oe1.ipynb
├── outputs/{figures,tables}
└── docs/
    ├── matriz_consistencia.md   # Objetivo→pregunta→hipótesis→variable→método→prueba
    └── revision_literatura.md   # Mapa de literatura para el Capítulo 2
```

## Puesta en marcha

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

## Flujo de trabajo (mapeo a objetivos específicos)

| Notebook / módulo | Objetivo | Qué produce |
|---|---|---|
| `00_construir_panel` | — | `panel_{B,A,C}.parquet` y `series_{B,A,C}.parquet` por muestra |
| `01_adquisicion_datos` | — | Series crudas, retornos, cartera del sector |
| `02_eda_oe1` | **OE1** | Descriptivos, correlaciones, tabla de estacionariedad I(0)/I(1) |
| `03_oe2_panel` | **OE2** | Panel FE + Driscoll-Kraay, global vs local |
| `04_oe3_cointegracion` | **OE3** | ARDL bounds / Johansen, VECM |
| `05_oe4_var_irf` | **OE4** | VAR/VECM, impulso-respuesta, descomposición de varianza |
| `06_oe5_fases_ciclo` | **OE5** | Fechado BBQ del ciclo, interacciones por fase |
| `07_triangulacion` | **OE6** | Comparación mercado global vs chileno (PI6/H7) |

> Todos los módulos `src/` están probados (smoke tests + corrida end-to-end con datos
> reales). Los notebooks requieren las series locales del BCCh para el análisis definitivo,
> pero el pipeline ya funciona con cobre+TC+acciones.

## Reproducibilidad — un solo comando

```powershell
python -m src.run_all          # regenera todo el análisis (usa datos en caché)
python -m src.run_all --descargar   # vuelve a descargar de FRED/Yahoo primero
python build_thesis.py         # regenera el documento Word/PDF (requiere Word)
```

`run_all` ejecuta el pipeline completo (paneles B/A/C → análisis avanzado, GARCH/Gregory-Hansen,
robustez FDR/GJR/Local Projections, predictor, Hausman, CIPS, comparación de mercados → datos web,
figuras y anexos) con manejo de errores y resumen. Cada resultado de la tesis es reproducible.

**Pruebas unitarias** (datos sintéticos, sin red): `python -m pytest -q` valida las funciones
econométricas clave (estacionariedad, fechado del ciclo, transformaciones, panel de efectos fijos).

## Diseño: triangulación por tres muestras

Ver `docs/diseno_triangulacion.md`. El universo se organiza en tres muestras comparables:
**B** (cobre, mercado global), **A** (cobre, mercado chileno: Pucobre), **C** (sector minero
chileno). Definidas en `config.py` como `UNIVERSO_PRINCIPAL`, `UNIVERSO_LOCAL_COBRE`,
`UNIVERSO_LOCAL_MINERIA`.

## Decisiones pendientes

1. **Descargar series del BCCh** (TPM, IMACEC, EMBI, IPC, IPSA) a `data/raw/` — ver
   `docs/guia_descarga_bcch.md`.
2. **Moneda de trabajo**: USD común vs moneda local + control cambiario.
3. **Logo USS**: depositar `assets/logo_uss.png` — ver `assets/COMO_AGREGAR_LOGO.md`.

## Nota de integridad

El código **no incluye datos ni resultados pre-cargados**. Todas las series deben
descargarse de sus fuentes y su disponibilidad verificarse. Las hipótesis (H1–H7) son
teóricamente fundadas pero su contraste depende de los datos.
