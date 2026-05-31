# Guía de descarga de series locales (BCCh / INE / Bolsa) a `data/raw/`

Objetivo: obtener las series que NO están en FRED y dejarlas en `data/raw/` con el formato y
nombre exactos que el código (`src/config.py` → `MACRO_LOCAL_BCCH`) espera.

> ⚠️ Las rutas de menú de los portales cambian con el tiempo. Lo invariable es el **formato de
> archivo** y los **nombres** de abajo. Los códigos de serie debes **verificarlos** al descargar.

---

## 1. Series requeridas y dónde encontrarlas

| Archivo destino (`data/raw/`) | Serie | Fuente principal | Dónde |
|---|---|---|---|
| `bcch_tpm.csv` | Tasa de Política Monetaria (TPM) | Banco Central de Chile | BDE → Tasas de interés → TPM |
| `bcch_imacec.csv` | IMACEC (índice mensual de actividad) | Banco Central de Chile | BDE → Actividad → IMACEC (serie empalmada, desestacionalizada o no — ver §4) |
| `bcch_embi.csv` | EMBI Chile / spread soberano | Banco Central de Chile | BDE → Estadísticas monetarias y financieras → Riesgo soberano / EMBI |
| `bcch_ipc.csv` | IPC / variación mensual | INE (BCCh redistribuye) | ine.gob.cl → IPC, o BDE → Precios → IPC |
| `bcch_ipsa.csv` | Índice IPSA | Bolsa de Santiago / BCCh | BDE → Mercado bursátil → IPSA (NO usar Yahoo: se corta en 2019) |

**Portal BCCh:** Base de Datos Estadísticos (BDE), `si3.bcentral.cl`. Permite seleccionar la
serie, el rango de fechas (pon **2003-01 a 2024-12** para tener margen de un año antes del inicio
muestral) y **exportar a Excel/CSV**.

**Cobre diario (opcional, solo si harás análisis de alta frecuencia):** Cochilco
(`cochilco.cl` → estadísticas → precio del cobre) o LME. Guárdalo como `cobre_diario.csv`.

---

## 2. Formato exacto que espera el código

La función `data_acquisition.load_local_csv()` está configurada para el export típico del BCCh:

- **Separador:** `;` (punto y coma). El BCCh suele exportar así.
- **Decimal:** `,` (coma). Verifícalo abriendo el archivo en un editor de texto.
- **Primera columna = fecha**, en formato día/mes/año o mes/año (la función usa `dayfirst=True`).
- **Una columna de valores** (la serie). Si el export trae varias columnas o metadatos en las
  primeras filas, elimínalas o usa el parámetro `skiprows` al cargar.

Si tu export usa coma como separador y punto decimal (formato anglosajón), cárgalo con
`sep=','` y `decimal='.'` en lugar de los valores por defecto.

### Ejemplo de archivo válido (`bcch_tpm.csv`)
```
fecha;valor
02-01-2004;2,25
05-01-2004;2,25
...
```

---

## 3. Cómo cargar y verificar (en el notebook 01 o una celda nueva)

```python
from src import data_acquisition as da

tpm    = da.load_local_csv('bcch_tpm.csv',    sep=';', decimal=',')
imacec = da.load_local_csv('bcch_imacec.csv', sep=';', decimal=',')
embi   = da.load_local_csv('bcch_embi.csv',   sep=';', decimal=',')
ipc    = da.load_local_csv('bcch_ipc.csv',    sep=';', decimal=',')
ipsa   = da.load_local_csv('bcch_ipsa.csv',   sep=';', decimal=',')

# Verificación mínima por serie:
for nombre, df in [('TPM',tpm),('IMACEC',imacec),('EMBI',embi),('IPC',ipc),('IPSA',ipsa)]:
    if df is not None:
        print(f'{nombre:7s} {df.index.min().date()} -> {df.index.max().date()}  ({len(df)} obs)')
```

Si una serie carga con `NaN` en los valores, casi siempre es por `sep`/`decimal` mal puestos:
abre el CSV en un editor de texto y ajusta los parámetros.

---

## 4. Decisiones de transformación a tomar al descargar

- **IMACEC:** elige la versión **desestacionalizada** si vas a usarlo en nivel/diferencia sin
  dummies de mes; si usas la serie original, incluye control de estacionalidad. Anótalo.
- **TPM:** es una tasa de nivel; el código la diferencia (`d_tpm`). Descárgala diaria o mensual;
  se remuestrea a fin de mes.
- **EMBI:** verifica unidades (puntos base). Entra en diferencia (`d_embi`).
- **IPC:** decide si usas el **índice** (nivel, I(1)) o la **variación mensual** (ya estacionaria).
  El código por defecto diferencia; si bajas la variación, ajústalo en `build_panel.py`.
- **Rango:** descarga desde **2003** para no perder observaciones por los rezagos/diferencias al
  inicio de 2004.

---

## 5. Una vez descargadas las 5 series

```python
# Reconstruir el panel ahora CON las locales:
from src import build_panel as bp
from src import config as C
panel, series = bp.construir(guardar=True, universo=C.UNIVERSO_ROBUSTEZ)
# build_panel detecta automáticamente los CSV en data/raw/ y los incorpora.
```

El log debe pasar de `[AVISO] Sin series BCCh...` a `[OK] BCCh cargado: ['tpm','imacec',...]`,
y la lista "Columnas macro" debe incluir `d_tpm`, `d_imacec`, `d_embi`, etc.

---

## 6. Estados financieros (CMF) — para los controles de empresa (fase posterior)

Para `leverage`, `ROA` y demás ratios contables (trimestrales):
- Fuente: **CMF** (`cmfchile.cl`) → información financiera de cada emisor; o Bloomberg/Refinitiv.
- Guarda un CSV por empresa o uno consolidado en `data/raw/` (p. ej. `eeff_trimestral.csv`)
  con columnas: `empresa, fecha, deuda_patrimonio, roa, ...`.
- El código las incorpora vía `transformations.contable_a_mensual()` (ffill + rezago de
  publicación). Esto es de prioridad menor: parte con los modelos macro y agrega los controles
  de empresa después.

---

### Checklist
- [ ] `bcch_tpm.csv`
- [ ] `bcch_imacec.csv`
- [ ] `bcch_embi.csv`
- [ ] `bcch_ipc.csv`
- [ ] `bcch_ipsa.csv`
- [ ] (opcional) `cobre_diario.csv` — solo si harás alta frecuencia
- [ ] (posterior) EE.FF. trimestrales CMF
