"""
data_acquisition.py
===================
Funciones para descargar / cargar las series del proyecto.

Fuentes:
- Yahoo Finance (yfinance): precios accionarios, VIX, IPSA.
- FRED (pandas_datareader): macro global y algunos proxies locales.
- BCCh / Cochilco / CMF: descarga MANUAL a data/raw/ y carga vía load_local_csv().

Todas las funciones devuelven DataFrames con DatetimeIndex.
NINGUNA función inventa datos: si una descarga falla, lo informa y devuelve None/parcial.
"""

from __future__ import annotations
import pandas as pd

from . import config as C


# ------------------------------------------------------------------
# Yahoo Finance
# ------------------------------------------------------------------
def descargar_precios_yahoo(tickers, inicio=C.FECHA_INICIO, fin=C.FECHA_FIN,
                            campo="Adj Close"):
    """
    Descarga precios desde Yahoo Finance.

    Parameters
    ----------
    tickers : list[str] | str
    campo   : 'Adj Close' (recomendado: ajustado por dividendos/splits) o 'Close'

    Returns
    -------
    pd.DataFrame con columnas = tickers, index = fechas.
    """
    import yfinance as yf
    if isinstance(tickers, str):
        tickers = [tickers]

    df = yf.download(tickers, start=inicio, end=fin, auto_adjust=False,
                     progress=False)
    # yfinance devuelve MultiIndex de columnas cuando hay >1 ticker
    if isinstance(df.columns, pd.MultiIndex):
        if campo not in df.columns.get_level_values(0):
            raise KeyError(f"Campo '{campo}' no disponible. Campos: "
                           f"{df.columns.get_level_values(0).unique().tolist()}")
        df = df[campo]
    else:
        df = df[[campo]]
        df.columns = tickers

    faltantes = [t for t in tickers if t not in df.columns or df[t].dropna().empty]
    if faltantes:
        print(f"[AVISO] Sin datos para: {faltantes}. Verifica el ticker en Yahoo.")
    return df


# ------------------------------------------------------------------
# FRED
# ------------------------------------------------------------------
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={codigo}"


def _descargar_serie_fred(codigo: str) -> pd.Series | None:
    """
    Descarga una serie de FRED por su endpoint CSV público (sin API key ni
    pandas_datareader, que está roto con pandas>=3.0).
    """
    import requests
    from io import StringIO
    url = FRED_CSV.format(codigo=codigo)
    try:
        r = requests.get(url, timeout=30,
                         headers={"User-Agent": "Mozilla/5.0 (tesis-academica)"})
        r.raise_for_status()
        df = pd.read_csv(StringIO(r.text))
        # FRED entrega columnas: 'observation_date' (o 'DATE') y el código de la serie
        col_fecha = df.columns[0]
        df[col_fecha] = pd.to_datetime(df[col_fecha], errors="coerce")
        df = df.set_index(col_fecha)
        s = pd.to_numeric(df.iloc[:, 0], errors="coerce")  # '.' (faltante) -> NaN
        return s
    except Exception as e:
        print(f"[FALLA] FRED {codigo}: {e}")
        return None


def descargar_fred(series_dict, inicio=C.FECHA_INICIO, fin=C.FECHA_FIN):
    """
    Descarga series de FRED vía endpoint CSV público.

    Parameters
    ----------
    series_dict : dict {clave_interna: (codigo_fred, fuente, freq, desc)}
                  (se usa solo el codigo_fred; se ignoran filas cuya fuente != 'FRED')

    Returns
    -------
    pd.DataFrame con columnas = claves internas, recortado a [inicio, fin].
    """
    frames = {}
    for clave, meta in series_dict.items():
        codigo, fuente = meta[0], meta[1]
        if fuente != "FRED":
            continue
        s = _descargar_serie_fred(codigo)
        if s is not None and not s.dropna().empty:
            frames[clave] = s
            print(f"[OK]   FRED {codigo:12s} -> '{clave}'  "
                  f"({s.dropna().index.min().date()} a {s.dropna().index.max().date()}, "
                  f"{s.dropna().shape[0]} obs)")
    if not frames:
        return None
    df = pd.DataFrame(frames).sort_index()
    return df.loc[inicio:fin]


# ------------------------------------------------------------------
# Carga de archivos locales (BCCh / Cochilco / CMF descargados a mano)
# ------------------------------------------------------------------
def load_local_csv(nombre_archivo, col_fecha=0, sep=",", decimal=".",
                   carpeta=C.DATA_RAW, **kwargs):
    """
    Carga un CSV/Excel ubicado en data/raw/ (descarga manual).

    Maneja el formato típico del BCCh (fecha en primera columna).
    Ajusta sep/decimal según el export (BCCh suele usar ';' y decimal ',').
    """
    ruta = carpeta / nombre_archivo
    if not ruta.exists():
        print(f"[FALTA] No existe {ruta}. Descárgalo manualmente desde la fuente.")
        return None

    if ruta.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(ruta, **kwargs)
    else:
        df = pd.read_csv(ruta, sep=sep, decimal=decimal, **kwargs)

    df = df.rename(columns={df.columns[col_fecha]: "fecha"})
    df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["fecha"]).set_index("fecha").sort_index()
    return df


# ------------------------------------------------------------------
# Orquestador
# ------------------------------------------------------------------
def adquirir_todo(guardar=True):
    """
    Descarga lo automatizable (Yahoo + FRED) y reporta lo que falta cargar a mano.
    Devuelve un dict de DataFrames crudos.
    """
    print("=" * 60)
    print("ADQUISICIÓN DE DATOS")
    print("=" * 60)

    bundle = {}

    print("\n--- Precios accionarios (Yahoo) ---")
    bundle["precios"] = descargar_precios_yahoo(list(C.UNIVERSO_ACTIVO.keys()))

    print("\n--- Macro global (FRED) ---")
    bundle["macro_global"] = descargar_fred(C.MACRO_GLOBAL)

    print("\n--- Macro local en FRED (proxies) ---")
    bundle["macro_local_fred"] = descargar_fred(C.MACRO_LOCAL_FRED)

    # IPSA: el ticker de Yahoo '^IPSA' se trunca en 2019 (verificado) -> usar BCCh.
    print("\n--- IPSA: descargar del BCCh/Bolsa a data/raw/ (Yahoo se corta en 2019) ---")

    print("\n--- PENDIENTE de descarga MANUAL a data/raw/ ---")
    for clave, meta in C.MACRO_LOCAL_BCCH.items():
        if not str(meta[0]).startswith("^"):
            print(f"    [ ] {clave:8s} -> {meta[0]:18s} ({meta[1]})")

    if guardar:
        for nombre, df in bundle.items():
            if df is not None:
                ruta = C.DATA_INTERIM / f"raw_{nombre}.parquet"
                df.to_parquet(ruta)
                print(f"[guardado] {ruta}")

    return bundle


if __name__ == "__main__":
    adquirir_todo()
