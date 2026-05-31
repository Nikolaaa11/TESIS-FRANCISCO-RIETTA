# II. MATERIAL Y MÉTODO

## 2.1 Tipo y Diseño de Investigación

La investigación es de enfoque **cuantitativo**, de tipo **explicativo o de medición de impacto**
—no predictivo—, orientada a cuantificar la relación entre las variables macroeconómicas y los
retornos accionarios. El diseño es **no experimental** (las variables no se manipulan, se observan
en su contexto natural) y **longitudinal**, pues abarca el período 2004-2024 con frecuencia mensual,
combinando técnicas de series de tiempo y de datos de panel. El alcance es, además, **correlacional-
explicativo y comparativo**, ya que contrasta la transmisión del impacto entre dos mercados
bursátiles.

## 2.2 Población, Muestra y Muestreo

La **población** está constituida por las empresas cuya valoración bursátil depende mayoritariamente
de la producción de cobre y que mantienen exposición a Chile. Dado que las grandes productoras con
operación en Chile no cotizan en la Bolsa de Santiago —por ser estatales (Codelco) o subsidiarias de
empresas extranjeras (Escondida, Los Bronces)—, el **muestreo** es no probabilístico, intencionado,
y adopta un **diseño de triangulación por tres muestras complementarias**:

- **Muestra B (cobre, mercado internacional):** empresas de cobre con operación en Chile que cotizan
  en mercados internacionales (Antofagasta plc, BHP, Anglo American, Lundin Mining, Teck). Constituye
  la referencia de "cobre puro" y, por su tamaño de sección cruzada, el panel principal.
- **Muestra A (cobre, mercado chileno):** empresa de extracción de cobre que cotiza en la Bolsa de
  Santiago (Sociedad Punta del Cobre). De cardinalidad reducida, se analiza mediante técnicas de
  serie de tiempo.
- **Muestra C (sector minero, mercado chileno):** empresas mineras cotizadas en la Bolsa de Santiago
  (Punta del Cobre, CAP, SQM-B, Molibdenos y Metales). Actúa como vehículo del mercado local, con
  control por el precio propio de cada commodity para aislar el efecto del cobre.

La comparación de los resultados entre las tres muestras permite evaluar si el mercado internacional
y el chileno incorporan los shocks macroeconómicos de manera diferenciada.

## 2.3 Variables y Operacionalización

La **variable dependiente** es el retorno logarítmico mensual de cada empresa,
$rᵢₜ = ln(Pᵢₜ) − ln(Pᵢ,ₜ₋₁)$, calculado sobre precios de cierre ajustados por dividendos y splits.
Las **variables independientes** se agrupan en factores macroeconómicos globales (precio del cobre,
VIX, tasa de fondos federales, rendimiento del bono del Tesoro a 10 años, petróleo WTI como control)
y locales (tipo de cambio USD/CLP, tasa de interés local, actividad económica, IPC). La siguiente
tabla resume la operacionalización.

| Bloque | Variable | Indicador (proxy) | Fuente | Transformación |
|---|---|---|---|---|
| Dependiente | Retorno accionario | Δlog precio ajustado | Yahoo Finance | — |
| Global | Precio del cobre | Precio global del cobre | FRED / Cochilco | Δlog |
| Global | Riesgo global | VIX | FRED | Δ |
| Global | Tasa externa | Fed Funds / Treasury 10Y | FRED | Δ |
| Local | Tipo de cambio | USD/CLP | FRED | Δlog |
| Local | Tasa local | Interbancaria 3 meses | FRED | Δ |
| Local | Actividad económica | Producción industrial | FRED | Δlog |
| Empresa | Controles | Tamaño, volatilidad, apalancamiento | Mercado / CMF | nivel |

## 2.4 Técnicas e instrumentos de recolección de datos. Validez y confiabilidad

La **técnica** de recolección es documental, sobre datos secundarios de fuentes públicas y oficiales:
Federal Reserve Economic Data (FRED) para las variables macroeconómicas globales y los proxies
locales, Yahoo Finance para los precios accionarios y la Comisión Chilena del Cobre (Cochilco) y el
Banco Central de Chile como referencias institucionales. Los **instrumentos** son los códigos de
descarga y procesamiento programados en Python, documentados y versionados.

La **validez** se sustenta en el uso de series oficiales, ampliamente empleadas en la literatura, y
en la verificación de su cobertura temporal. La **confiabilidad** se garantiza mediante la
**reproducibilidad** del proceso: el pipeline completo de análisis se regenera con un solo comando y
produce resultados idénticos en cada ejecución, y se acompaña de una suite de pruebas unitarias que
valida las funciones econométricas sobre casos de referencia conocidos.

## 2.5 Procedimiento de análisis de datos

El análisis sigue una secuencia donde el orden de integración de las series bifurca la estrategia:

**Estacionariedad (OE1).** Se aplican pruebas de raíz unitaria de Dickey-Fuller aumentada (ADF),
Phillips-Perron y KPSS, complementadas con Zivot-Andrews para quiebres y con la prueba de panel de
segunda generación CIPS (Pesaran, 2007), robusta a la dependencia de sección cruzada.

**Sensibilidad (OE2).** Se estima un modelo de datos de panel con efectos fijos por empresa:

$$rᵢₜ = αᵢ + β₁ Δcobreₜ + β₂ ΔTCₜ + β₃ Δtasaₜ + β₄ ΔVIXₜ + γ′ Xᵢₜ + εᵢₜ$$

con errores estándar de Driscoll-Kraay, robustos a heterocedasticidad, autocorrelación y dependencia
de sección cruzada. El contraste de dominancia global versus local (H6) se realiza mediante tests de
Wald por bloque.

**Largo plazo (OE3).** Se evalúa la cointegración mediante el test de bordes ARDL (Pesaran, Shin y
Smith, 2001), el test de Johansen y, ante la posibilidad de quiebres, el test de Gregory-Hansen
(1996), del que se obtiene el modelo de corrección de error.

**Dinámica de shocks (OE4).** Se estima un VAR (o VECM) con identificación de Cholesky ordenada por
exogeneidad, del que se reportan funciones impulso-respuesta y descomposición de varianza (FEVD),
complementadas con proyecciones locales (Jordà, 2005).

**Estabilidad y comparación (OE5 y OE6).** Las fases del ciclo se fechan con el algoritmo de
Bry-Boschan, incorporándose mediante interacciones; la comparación entre mercados se contrasta con
una prueba formal de igualdad de coeficientes. Se modela además la volatilidad condicional con
GARCH y GJR-GARCH, y se controla por pruebas múltiples (Benjamini-Hochberg).

## 2.6 Criterios éticos

La investigación se sustenta en **datos públicos y de libre acceso**, sin información personal ni
confidencial, por lo que no requiere consentimiento informado. Se respeta la **propiedad
intelectual** mediante la citación rigurosa de toda fuente conforme a las normas APA. Se observa el
principio de **integridad científica**: no se inventan datos ni resultados, las cifras provienen de
fuentes verificables y los hallazgos se reportan tal como resultan, incluyendo los no significativos.

## 2.7 Criterios de Rigor Científico

El rigor se asegura mediante: (i) la **validez interna**, con una batería completa de diagnósticos
(dependencia de sección cruzada, estabilidad del sistema dinámico, homogeneidad de pendientes); (ii)
la **robustez**, contrastando los resultados en submuestras, con definiciones alternativas de las
variables y con métodos complementarios (proyecciones locales frente a VAR, corrección por pruebas
múltiples); (iii) la **reproducibilidad**, dado que todo resultado puede regenerarse desde el
repositorio del proyecto; y (iv) la **transparencia**, declarando explícitamente las limitaciones y
el carácter de los resultados.
