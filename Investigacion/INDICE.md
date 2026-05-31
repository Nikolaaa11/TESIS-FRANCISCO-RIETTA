# Carpeta de Investigación — Tesis Francisco Rietta

**Tema:** Impacto de las variables macroeconómicas sobre los retornos accionarios de las empresas de
extracción de cobre con exposición a Chile (2004–2024). Comparación entre el mercado internacional y
el chileno.

Esta carpeta reúne **todo el material de investigación** que sustenta la tesis: estado del arte,
historia del cobre, revisión de literatura, mejoras metodológicas, referencias, y datos/hallazgos.
Cada subcarpeta es autocontenida y está en formato Markdown (texto plano, fácil de leer y citar).

---

## Estructura

### 01_estado_del_arte/
- **estado_del_arte.md** — Síntesis del estado del arte: qué se sabe, qué vacío llena la tesis y
  cómo se posiciona frente a la literatura internacional y regional.

### 02_historia_del_cobre/
- **historia_del_cobre.md** — Historia económica del cobre y de la minería en Chile, el súper-ciclo
  de precios, los principales hitos (2004–2024) y 22 fuentes documentadas.

### 03_literatura/
- **revision_literatura.md** — Revisión de literatura estructurada (marco de antecedentes).
- **lit_chilena.md** — Literatura chilena y latinoamericana (tipo de cambio, cobre, mercado local).
- **lit_emergentes.md** — Literatura de mercados emergentes y de commodities.
- **busqueda_literatura.md** — Estrategia de búsqueda bibliográfica (términos, fuentes, criterios).

### 04_metodologia_y_mejoras/
- **mejoras_metodologicas.md** — Batería econométrica de segunda generación y mejoras propuestas
  (raíz unitaria en panel, cointegración con quiebre, GARCH, pruebas de igualdad de coeficientes).
- **diseno_triangulacion.md** — Diseño de triangulación por muestras (A: Pucobre; B: cobre
  internacional; C: sector minero chileno).
- **matriz_consistencia.md** — Matriz de consistencia (problema–objetivos–hipótesis–variables–método).

### 05_referencias/
- **referencias.md** — Listado completo de referencias en formato APA 7 (~47 fuentes).

### 06_datos_y_hallazgos/
- **hallazgos_datos.md** — Hallazgos de los datos descargados (FRED + Yahoo Finance).
- **guia_descarga_bcch.md** — Guía para descargar el EMBI desde el Banco Central de Chile.
- **reproducibilidad.md** — Flujo de trabajo reproducible (código, entorno, pasos).

---

## Relación con el documento final

El documento de tesis (`outputs/Tesis_Francisco_Rietta.docx` y `.pdf`, 75 páginas, formato USS + APA 7)
se construye a partir de las fuentes de `docs/uss_01_introduccion.md`, `uss_02_metodo.md`,
`uss_03_resultados.md`, `uss_04_conclusiones.md`, `referencias.md` y `anexos.md`. Esta carpeta
`Investigacion/` es el **respaldo de investigación** detrás de ese documento.

> Nota: el material original también vive en `docs/investigacion/`. Esta carpeta `Investigacion/`
> consolida y organiza ese material, agregando la literatura, la matriz de consistencia, las
> referencias y los hallazgos de datos en una sola ubicación de fácil navegación.
