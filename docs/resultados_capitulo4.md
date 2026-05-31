# Capítulo 4 — Resultados y discusión (borrador con resultados preliminares)

> **Advertencia de estatus.** Las cifras de este capítulo provienen de una corrida real del
> pipeline sobre datos públicos (cobre y tipo de cambio de FRED; acciones de Yahoo Finance), pero
> son **preliminares**: aún no incorporan el EMBI ni los controles a nivel de empresa, el orden de
> integración del tipo de cambio requiere revisión por quiebres, y falta la batería completa de
> diagnósticos y robustez. No deben leerse como hallazgos definitivos.

## 4.1 Análisis descriptivo y propiedades de las series (OE1)

Las pruebas de raíz unitaria confirman el patrón esperado y validan la estrategia de doble vía.
El **logaritmo del precio del cobre** resulta no estacionario en nivel —integrado de orden uno,
I(1) (ADF p = 0,013; KPSS rechaza la estacionariedad, p = 0,014)— mientras que su **retorno**
(primera diferencia logarítmica) es estacionario, I(0) (ADF p = 0,0001; KPSS no rechaza, p = 0,10).
Esta dicotomía sustenta el diseño: los **retornos** alimentan los modelos de impacto de corto
plazo (OE2, OE4) y los **niveles I(1)** ingresan al análisis de cointegración (OE3).

El **tipo de cambio USD/CLP** en logaritmo arroja un resultado ambiguo (ADF p = 0,150; KPSS
rechaza), que el algoritmo clasifica como caso a revisar. La explicación más plausible es la
presencia de **quiebres estructurales** (súper-ciclo del cobre, crisis de 2008, pandemia de 2020),
ante los cuales las pruebas estándar pierden potencia. Se recomienda re-evaluar su orden de
integración con pruebas que admitan quiebres (Zivot-Andrews) antes de su uso definitivo.

## 4.2 Determinantes de los retornos: global vs local (OE2)

El modelo de panel de efectos fijos con errores Driscoll-Kraay (muestra B, cinco productoras de
cobre con cotización internacional; R² within = 0,245) entrega los siguientes coeficientes:

| Factor | Coeficiente | Significancia |
|---|---|---|
| Precio del cobre (Δ) | **+0,571** | *** (sig. al 1%) |
| VIX (Δ) | −0,008 | * (sig.) |
| Fed Funds (Δ) | +0,020 | n.s. |
| Treasury 10Y (Δ) | +0,023 | n.s. |
| Tipo de cambio CLP (Δ) | **−1,574** | *** (sig.) |
| Tasa local (Δ) | −0,007 | n.s. |
| Actividad local (Δ) | −0,523 | n.s. |

Tres lecturas se desprenden:

1. **El cobre domina (H1 respaldada).** El coeficiente del cobre es positivo, de magnitud
   económica relevante y altamente significativo: un aumento del precio del cobre se traduce en
   mayores retornos, consistente con el canal de ingresos. Es el determinante central del valor
   del sector.
2. **El tipo de cambio tiene efecto negativo y fuerte.** Una depreciación del peso (↑ USD/CLP) se
   asocia a retornos negativos. Para empresas que cotizan y valoran en dólares, la depreciación
   del peso suele coincidir con episodios de aversión al riesgo y caída del cobre, de modo que el
   signo capta tanto el canal de competitividad como el de riesgo. Este resultado confirma la
   ambigüedad teórica anticipada (H2) y merece un análisis fino por empresa.
3. **El riesgo global (VIX) pesa; los factores locales de tasa y actividad, no (en esta
   especificación).** La no significancia de la tasa y la actividad locales es esperable a la luz
   de la ausencia, por ahora, del EMBI y de un IMACEC propiamente tal, y por tratarse de empresas
   internacionales (muestra B) menos sensibles al ciclo doméstico. Globalmente, los factores
   internacionales (cobre + VIX) dominan a los locales, primera evidencia a favor de H6.

![Sensibilidad de los retornos a cada factor macro-financiero (muestra B).](outputs/figures/fig_coeficientes.png)

## 4.3 Relaciones de largo plazo (OE3)

La evidencia de cointegración es **mixta y, por tanto, no concluyente**. El test de Johansen sobre
las series en nivel (valor de la acción, cobre, tipo de cambio) detecta **un vector de
cointegración** (estadístico de traza 32,1 > 29,8 al 95%), lo que sugiere una relación de equilibrio
de largo plazo. Sin embargo, el **test de bordes ARDL** no permite rechazar la ausencia de
relación de nivel (estadístico F de bordes ≈ 0,95, por debajo de las cotas críticas). Esta
discrepancia es habitual cuando el orden de integración de alguna variable no es nítido —como
ocurre aquí con el tipo de cambio (§4.1)—. La conclusión prudente es **suspender el juicio sobre
H5** hasta resolver el orden de integración del tipo de cambio y reespecificar el vector de largo
plazo (por ejemplo, incorporando quiebres o reconsiderando los regresores).

## 4.4 Dinámica de shocks (OE4)

La descomposición de la varianza del error de pronóstico del retorno (FEVD, horizonte de 12 meses,
muestra B) reparte la varianza así:

| Fuente del shock | Fracción de la varianza |
|---|---|
| Componente propio (idiosincrático) | 62,7% |
| **Precio del cobre** | **18,0%** |
| **VIX (riesgo global)** | **14,0%** |
| Tasa local | 3,1% |
| Tipo de cambio | 2,2% |

La causalidad de Granger confirma que el precio del cobre **antecede** a los retornos del sector.
Más allá del componente idiosincrático, **los shocks globales (cobre + VIX ≈ 32%) explican una
fracción muy superior a los locales (≈ 5%)**, lo que constituye la evidencia más nítida a favor de
**H6 (dominancia de los factores globales)**. La función impulso-respuesta (no tabulada aquí)
muestra una reacción positiva del retorno ante un shock del cobre, coherente con H1.

![Descomposición de la varianza del error de pronóstico del retorno (FEVD, horizonte 12 meses).](outputs/figures/fig_fevd.png)

## 4.5 Estabilidad por fases del ciclo del cobre (OE5)

El algoritmo de Bry-Boschan identifica una secuencia coherente de fases de expansión y contracción
del precio del cobre a lo largo de 2004–2024, capturando el súper-ciclo (auge hasta 2011),
la corrección posterior, el shock de 2020 y la recuperación reciente. La infraestructura para
estimar la **sensibilidad condicional al régimen** (términos de interacción y re-estimación por
subperíodo) está implementada; su estimación definitiva se realizará una vez consolidado el
conjunto de datos. La hipótesis a contrastar es una **mayor sensibilidad al cobre en expansión que
en contracción** (asimetría de régimen).

![Precio del cobre y fases del ciclo (expansión/contracción) fechadas con Bry-Boschan.](outputs/figures/fig_ciclo_cobre.png)

## 4.6 Comparación entre mercados: triangulación (OE6)

La tabla comparativa entre las tres muestras ofrece la primera evidencia sobre la transmisión
diferenciada del impacto macroeconómico:

| Muestra | Mercado | β cobre | R² | Varianza por shocks globales |
|---|---|---|---|---|
| B · cobre internacional | global | 0,571 | 0,245 | 0,320 |
| A · cobre Chile (Pucobre) | chileno | 0,631 | 0,331 | 0,295 |
| C · minería Chile | chileno | 0,418 | 0,113 | 0,279 |

Dos hallazgos preliminares:

1. **La sensibilidad al cobre es similar entre el cobre puro internacional (0,571) y el local
   (0,631), y cae en el sector minero mixto (0,418).** Esto sugiere que el mercado precia la
   exposición al cobre de forma comparable con independencia del lugar de cotización, y que la
   menor sensibilidad de la muestra C se debe a la **dilución por otros commodities** (hierro,
   litio, molibdeno), tal como anticipa el rol de "vehículo" de esa muestra.

![Triangulación: sensibilidad al cobre y dominancia global por muestra (B, A, C).](outputs/figures/fig_triangulacion.png)
2. **La fracción de varianza atribuida a shocks globales es algo mayor en el mercado internacional
   (0,320) que en el chileno (0,295 y 0,279).** Es una señal **direccionalmente consistente con H7**
   —el mercado internacional incorporaría el shock de forma más completa—, aunque la diferencia es
   modesta y requiere confirmación con el conjunto de datos completo y pruebas formales de igualdad
   de coeficientes entre muestras.

## 4.7 Discusión integrada

Los resultados preliminares dibujan un cuadro coherente con la teoría: **el precio del cobre es el
principal determinante de los retornos del sector** (H1), **los factores globales dominan a los
locales** en la explicación de la varianza (H6), y el **tipo de cambio** ejerce un efecto negativo
significativo cuyo signo refleja la doble naturaleza —competitividad y riesgo— anticipada (H2). La
comparación entre mercados aporta una primera señal, aún débil, de **transmisión diferenciada**
(H7), mientras que la evidencia de **cointegración de largo plazo** (H5) permanece inconclusa por
la ambigüedad en el orden de integración del tipo de cambio.

Estas lecturas son **provisionales**. Su confirmación exige: (i) incorporar el EMBI y los controles
a nivel de empresa; (ii) resolver el orden de integración del tipo de cambio con pruebas de
quiebre; (iii) estimar las interacciones por fase del ciclo (OE5); (iv) ejecutar la batería de
diagnósticos (CD de Pesaran, efectos ARCH, estabilidad del VAR) y de robustez (submuestras,
definiciones alternativas, cartera equiponderada vs ponderada). Solo entonces los signos y
magnitudes aquí reportados podrán elevarse a la categoría de hallazgos.
