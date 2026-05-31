"""
config.py
=========
Configuración central del proyecto de tesis:
- Rutas de carpetas
- Período muestral
- Definición del universo de empresas (anillo 1 / anillo 2)
- Diccionario de variables (dependiente, macro global, macro local, empresa)
  con su fuente, ticker/código y frecuencia nativa.

NOTA IMPORTANTE: los tickers y códigos de abajo son CANDIDATOS de uso estándar.
Debes VERIFICAR la disponibilidad y cobertura temporal real al descargar.
No hay valores ni resultados pre-cargados.
"""

from pathlib import Path

# ------------------------------------------------------------------
# 1. RUTAS
# ------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"
FIGURES = OUTPUTS / "figures"
TABLES = OUTPUTS / "tables"

for _p in (DATA_RAW, DATA_INTERIM, DATA_PROCESSED, FIGURES, TABLES):
    _p.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------
# 2. PERÍODO MUESTRAL (tentativo — ajustar tras verificar disponibilidad)
# ------------------------------------------------------------------
FECHA_INICIO = "2004-01-01"
FECHA_FIN = "2024-12-31"

# Frecuencia de trabajo principal de los modelos (ver Frente 4, sección 6)
FRECUENCIA_BASE = "M"   # 'M' = mensual (fin de mes). Alternativa de robustez: 'W'

# ------------------------------------------------------------------
# 3. UNIVERSO DE EMPRESAS — DISEÑO DE TRIANGULACIÓN POR TRES MUESTRAS
#    (decidido mayo 2026; cobertura Yahoo 2004-2024 verificada en cada ticker)
#
#    La tesis compara cómo el MERCADO GLOBAL y el MERCADO CHILENO precian el
#    impacto macro sobre las mismas materias primas:
#      - Muestra B = cobre puro, cotiza en mercados globales (operación en Chile)
#      - Muestra A = cobre puro, cotiza en el mercado chileno (Bolsa de Santiago)
#      - Muestra C = sector minero chileno (Bolsa de Santiago), N mayor para panel
# ------------------------------------------------------------------

# --- Muestra A: COBRE PURO en el MERCADO CHILENO (Bolsa de Santiago) ---
# Universo casi unitario: las grandes (Codelco, Escondida) no cotizan localmente.
MUESTRA_A_LOCAL_COBRE = {
    "PUCOBRE.SN": "Sociedad Punta del Cobre (Santiago, CLP) — cobre, Atacama",
}

# --- Muestra B: COBRE PURO en MERCADOS GLOBALES, con operación en Chile ---
MUESTRA_B_GLOBAL_COBRE = {
    "ANTO.L": "Antofagasta plc (LSE, GBP) — cobre, activos en Chile",
    "BHP":    "BHP Group (NYSE, USD) — Escondida, Spence",
    "AAL.L":  "Anglo American (LSE, GBP) — Los Bronces, Collahuasi",
    "LUN.TO": "Lundin Mining (TSX, CAD) — Candelaria",
    "TECK":   "Teck Resources (NYSE, USD) — QB2",
}

# --- Muestra C: SECTOR MINERO en el MERCADO CHILENO (Bolsa de Santiago) ---
# Mezcla de commodities: incluir el precio propio de cada uno como control.
MUESTRA_C_LOCAL_MINERIA = {
    "PUCOBRE.SN": "Punta del Cobre — cobre",
    "CAP.SN":     "CAP S.A. — hierro/acero",
    "SQM-B.SN":   "SQM serie B — litio/yodo",
    "MOLYMET.SN": "Molibdenos y Metales — molibdeno (procesamiento)",
}

# Atajos de uso
UNIVERSO_PRINCIPAL = MUESTRA_B_GLOBAL_COBRE      # panel cobre puro (más sólido)
UNIVERSO_LOCAL_COBRE = MUESTRA_A_LOCAL_COBRE     # serie de tiempo, mercado chileno
UNIVERSO_LOCAL_MINERIA = MUESTRA_C_LOCAL_MINERIA # panel sector minero chileno

# Universo activo por defecto en los scripts:
UNIVERSO_ACTIVO = UNIVERSO_PRINCIPAL

# ------------------------------------------------------------------
# 4. VARIABLES MACRO GLOBALES  (FRED salvo indicación)
#    clave_interna: (codigo_fuente, fuente, frecuencia_nativa, descripcion)
# ------------------------------------------------------------------
MACRO_GLOBAL = {
    "cobre":      ("PCOPPUSDM", "FRED", "M", "Precio cobre USD/MT (Global price of Copper)"),
    "vix":        ("VIXCLS",    "FRED", "D", "CBOE Volatility Index (VIX)"),
    "fed_funds":  ("FEDFUNDS",  "FRED", "M", "Federal Funds Effective Rate"),
    "treasury10": ("DGS10",     "FRED", "D", "10-Year Treasury Yield"),
    "dxy_wti":    ("DCOILWTICO","FRED", "D", "WTI Crude (control factor commodity)"),
    # Nota: el cobre LME diario de alta frecuencia conviene bajarlo de Cochilco/LME
    #       (CSV manual) y dejarlo en data/raw. FRED PCOPPUSDM es mensual.
}

# ------------------------------------------------------------------
# 5. VARIABLES MACRO LOCALES (Chile)
#    El Banco Central (BCCh) y el INE no están en FRED de forma confiable.
#    => Descarga MANUAL (xlsx/csv) a data/raw/ y carga con load_bcch_csv().
#    Algunos proxies SÍ están en FRED (verificar continuidad).
# ------------------------------------------------------------------
MACRO_LOCAL_FRED = {
    "usdclp":         ("DEXCHUS",         "FRED", "D", "Tipo de cambio CLP/USD"),
    # Proxies de variables locales disponibles en FRED (OCDE) — descargables sin credenciales:
    "tasa_local":     ("IR3TIB01CLM156N", "FRED", "M", "Tasa interbancaria 3m Chile (proxy TPM)"),
    "actividad_local":("CHLPROINDMISMEI", "FRED", "M", "Producción industrial Chile (proxy IMACEC)"),
    "ipc_local":      ("CHLCPIALLMINMEI", "FRED", "M", "IPC Chile (índice; cobertura hasta ~2023)"),
    # Para precisión, el IMACEC y la TPM exactos del BCCh pueden reemplazar a estos proxies.
}

MACRO_LOCAL_BCCH = {
    # clave_interna: (nombre_archivo_en_data_raw, descripcion, frecuencia)
    "tpm":    ("bcch_tpm.csv",    "Tasa de Política Monetaria", "D/M"),
    "imacec": ("bcch_imacec.csv", "IMACEC (proxy PIB mensual)", "M"),
    "embi":   ("bcch_embi.csv",   "EMBI Chile / spread soberano", "D/M"),
    "ipc":    ("bcch_ipc.csv",    "IPC / inflación", "M"),
    # OJO: el IPSA por Yahoo ('^IPSA') se TRUNCA en 2019-06 (verificado). No usar Yahoo.
    # Descargar el IPSA desde el BCCh (si3.bcentral.cl) o Bolsa de Santiago a data/raw/.
    "ipsa":   ("bcch_ipsa.csv",   "IPSA (BCCh/Bolsa — NO Yahoo, se corta en 2019)", "D"),
}

# ------------------------------------------------------------------
# 6. VARIABLES FINANCIERAS DE EMPRESA (prioridad: size, vol, leverage)
# ------------------------------------------------------------------
# Las de mercado (size, vol, liquidez) se calculan de precios/volumen.
# Las contables (leverage, ROA...) vienen de EE.FF. trimestrales:
#   fuente: CMF (cmfchile.cl), Bloomberg o Refinitiv -> cargar manual a data/raw.
VARS_EMPRESA_MERCADO = ["retorno", "volatilidad", "size", "liquidez"]
VARS_EMPRESA_CONTABLE = ["leverage", "roa", "roe", "pb"]   # opcionales
