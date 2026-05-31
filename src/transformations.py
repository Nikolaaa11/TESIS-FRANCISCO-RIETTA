"""
transformations.py
==================
Transformaciones de las series:
- Retornos logarítmicos
- Cartera del sector (equiponderada y ponderada por capitalización)
- Remuestreo a frecuencia base (fin de mes) con reglas correctas por tipo de variable
- Construcción del panel 'long' para linearmodels

Reglas clave (ver Frente 4):
- Precios/índices -> último valor del mes (fin de mes).
- Flujos/tasas    -> promedio o fin de mes según naturaleza (declarar).
- Contables trim. -> 'forward fill' con rezago de publicación (NO interpolar).
"""

from __future__ import annotations
import numpy as np
import pandas as pd

from . import config as C


# ------------------------------------------------------------------
# Retornos
# ------------------------------------------------------------------
def retorno_log(precios: pd.DataFrame) -> pd.DataFrame:
    """Retorno logarítmico: r_t = ln(P_t) - ln(P_{t-1})."""
    return np.log(precios).diff()


def diferencia_log(serie: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    """Δlog para variables en nivel I(1) que se quieran estacionarizar."""
    return np.log(serie).diff()


# ------------------------------------------------------------------
# Cartera del sector
# ------------------------------------------------------------------
def cartera_equiponderada(retornos: pd.DataFrame) -> pd.Series:
    """Promedio simple de los retornos de las empresas (rebalanceo cada período)."""
    return retornos.mean(axis=1, skipna=True)


def cartera_ponderada_cap(retornos: pd.DataFrame,
                          capitalizacion: pd.DataFrame) -> pd.Series:
    """
    Cartera ponderada por capitalización bursátil (peso rezagado un período
    para evitar look-ahead). retornos y capitalizacion alineados por columnas/index.
    """
    pesos = capitalizacion.shift(1)
    pesos = pesos.div(pesos.sum(axis=1), axis=0)
    return (retornos * pesos).sum(axis=1, skipna=True)


# ------------------------------------------------------------------
# Remuestreo a frecuencia base
# ------------------------------------------------------------------
def a_fin_de_mes(df: pd.DataFrame, metodo: str = "last") -> pd.DataFrame:
    """
    Remuestrea a fin de mes ('ME').
    metodo: 'last'  -> último dato (precios, índices, tasas de nivel)
            'mean'  -> promedio del mes (tasas, spreads si se prefiere)
    """
    r = df.resample("ME")
    if metodo == "last":
        return r.last()
    elif metodo == "mean":
        return r.mean()
    raise ValueError("metodo debe ser 'last' o 'mean'")


def contable_a_mensual(df_trim: pd.DataFrame, rezago_meses: int = 1) -> pd.DataFrame:
    """
    Lleva datos contables trimestrales a mensual SIN interpolar:
    - forward-fill del último valor conocido
    - rezago de publicación para evitar look-ahead bias (los EE.FF. se publican
      con semanas de desfase). Por defecto 1 mes; ajustar según calendario CMF.
    """
    mensual = df_trim.resample("ME").ffill()
    return mensual.shift(rezago_meses)


# ------------------------------------------------------------------
# Construcción del panel 'long'
# ------------------------------------------------------------------
def construir_panel(retornos: pd.DataFrame,
                    macro: pd.DataFrame,
                    vars_empresa: dict[str, pd.DataFrame] | None = None
                    ) -> pd.DataFrame:
    """
    Une retornos por empresa con variables macro (comunes a todas) y
    variables de empresa, en formato long con MultiIndex (empresa, fecha).

    Parameters
    ----------
    retornos : DataFrame (index=fecha, columns=empresas)
    macro    : DataFrame (index=fecha, columns=variables macro)  -- mismas para todas
    vars_empresa : opcional, dict {nombre_var: DataFrame(index=fecha, columns=empresas)}

    Returns
    -------
    DataFrame long, index=MultiIndex(empresa, fecha), listo para PanelOLS.
    """
    largo = retornos.stack().rename("retorno").to_frame()
    largo.index.names = ["fecha", "empresa"]
    largo = largo.swaplevel().sort_index()  # (empresa, fecha)

    # macro: se replica para cada empresa via join sobre 'fecha'
    largo = largo.join(macro, on="fecha")

    if vars_empresa:
        for nombre, dfv in vars_empresa.items():
            s = dfv.stack().rename(nombre)
            s.index.names = ["fecha", "empresa"]
            s = s.swaplevel()
            largo = largo.join(s)

    return largo


if __name__ == "__main__":
    print("Módulo de transformaciones. Importar desde el notebook.")
