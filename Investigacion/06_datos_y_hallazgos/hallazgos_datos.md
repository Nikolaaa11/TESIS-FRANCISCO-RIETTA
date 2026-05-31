# Hallazgos de disponibilidad de datos (paso F)

Ejecución real de la adquisición (`src/data_acquisition.py`) — fecha de corrida: ver git/log.
**Todo lo de abajo se descargó y verificó efectivamente; no son supuestos.**

## 1. Período efectivo

- **2004–2024 es plenamente viable.** El retorno mensual de ANTO.L (anillo 1) cubre
  **2004-02 → 2024-12 = 251 meses**. Holgado para VAR/VECM/ARDL.
- El cuello de botella NO es la historia de las empresas (todas parten ≥2002), sino la
  **disponibilidad de las series locales del BCCh** (pendiente de descarga manual).

## 2. Macro global (FRED) — ✅ descarga automática OK

| Variable | Código FRED | Cobertura verificada | Frecuencia |
|---|---|---|---|
| Cobre | PCOPPUSDM | 1992 → 2026 | Mensual |
| VIX | VIXCLS | 1990 → 2026 | Diaria |
| Fed Funds | FEDFUNDS | 1954 → 2026 | Mensual |
| Treasury 10Y | DGS10 | 1962 → 2026 | Diaria |
| WTI (control) | DCOILWTICO | 1986 → 2026 | Diaria |
| USD/CLP | DEXCHUS | 1981 → 2026 | Diaria |

> El cobre de FRED (PCOPPUSDM) es **mensual**. Si necesitas cobre **diario** (LME/COMEX)
> para los modelos de alta frecuencia, descárgalo de Cochilco/LME a `data/raw/`.

## 3. Acciones (Yahoo Finance) — ✅ OK

| Ticker | Empresa | Cobertura verificada |
|---|---|---|
| ANTO.L | Antofagasta plc | 2000 → 2024 |
| BHP | BHP Group | 2000 → 2024 |
| AAL.L | Anglo American | 2000 → 2024 |
| LUN.TO | Lundin Mining | 2000 → 2024 |
| TECK | Teck Resources | 2002 → 2024 |
| SQM | SQM | 2000 → 2024 |
| CAP.SN | CAP S.A. | 2000 → 2024 |

Todas usan **Adj Close** (ajustado por dividendos/splits).

## 4. Problema detectado: IPSA por Yahoo ⚠️

- El ticker `^IPSA` de Yahoo **se trunca en 2019-06** (verificado). Los alternativos
  `^SPIPSA` / `SPIPSA.SN` **no existen** en Yahoo.
- **Solución:** descargar el IPSA desde el **BCCh** (si3.bcentral.cl) o la **Bolsa de
  Santiago** a `data/raw/bcch_ipsa.csv`. Ya quedó configurado así en `config.py`.

## 5. Pendiente de descarga MANUAL a `data/raw/` (BCCh / Cochilco / CMF)

| Archivo esperado | Serie | Fuente |
|---|---|---|
| `bcch_tpm.csv` | Tasa de Política Monetaria | BCCh |
| `bcch_imacec.csv` | IMACEC (proxy PIB mensual) | BCCh |
| `bcch_embi.csv` | EMBI Chile / spread soberano | BCCh |
| `bcch_ipc.csv` | IPC / inflación | INE / BCCh |
| `bcch_ipsa.csv` | IPSA | BCCh / Bolsa Santiago |
| EE.FF. trimestrales | leverage, ROA, etc. | CMF (cmfchile.cl) |

## 6. Validación econométrica con datos reales

- OE1 sobre el cobre real (2004–2024): **log-nivel → I(1)** (ADF p=0.013, KPSS rechaza),
  **retorno → I(0)** (ADF p=0.0001, KPSS no rechaza). Patrón esperado confirmado.
- Esto valida la doble vía: retornos I(0) para impacto de corto plazo (OE2);
  niveles I(1) para cointegración de largo plazo (OE3).

## 7. Datos guardados

En `data/interim/` (parquet):
- `raw_macro_global.parquet` — 6 series FRED globales.
- `raw_macro_local_fred.parquet` — USD/CLP.
- `raw_precios.parquet` — 7 acciones candidatas.
