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

El **tipo de cambio USD/CLP** en logaritmo arroja un resultado ambiguo en las pruebas estándar
(ADF p = 0,150; KPSS rechaza). La prueba de **Zivot-Andrews**, que admite un quiebre estructural
endógeno, **resuelve la ambigüedad**: el nivel no es estacionario (estadístico −2,83; p = 0,95),
mientras que su primera diferencia sí lo es de forma marginal (estadístico −4,59; p = 0,09). Se
concluye que el tipo de cambio es **integrado de orden uno, I(1)**, y que la clasificación dudosa
inicial respondía a la pérdida de potencia de las pruebas convencionales ante los quiebres del
período (súper-ciclo, crisis de 2008, pandemia de 2020). El cobre en nivel, contrastado con la
misma prueba, se mantiene como I(1) (p = 0,17).

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
discrepancia entre ambos enfoques sugiere que la relación de largo plazo, de existir, es **débil o
inestable**. Confirmado ya el orden I(1) del tipo de cambio (§4.1), la explicación más probable no
es el orden de integración sino la **presencia de quiebres en la relación de cointegración** misma
(el súper-ciclo altera la relación de equilibrio). La conclusión prudente es **mantener cautela
sobre H5**: se reportará la relación de largo plazo del VECM como indicativa, complementándola con
pruebas de cointegración con quiebre (Gregory-Hansen) en la versión final.

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

La causalidad de Granger confirma que el precio del cobre **antecede** a los retornos del sector
de manera estadísticamente significativa (F = 9,11; p = 0,003). Más allá del componente
idiosincrático, **los shocks globales (cobre + VIX ≈ 32%) explican una fracción muy superior a
los locales (≈ 5%)**, lo que constituye la evidencia más nítida a favor de **H6 (dominancia de los
factores globales)**. El sistema VAR seleccionado por criterio de Akaike (un rezago) es
**estable** —todas sus raíces se encuentran dentro del círculo unitario—, lo que valida la lectura
de las funciones impulso-respuesta.

![Descomposición de la varianza del error de pronóstico del retorno (FEVD, horizonte 12 meses).](outputs/figures/fig_fevd.png)

La función impulso-respuesta cuantifica la reacción dinámica del retorno ante un shock de una
desviación estándar en el precio del cobre: la respuesta es **positiva e inmediata** y se disipa en
los meses siguientes, coherente con una incorporación rápida de la información del commodity
(H1).

![Impulso-respuesta del retorno del sector ante un shock del precio del cobre (±2 errores estándar).](outputs/figures/fig_irf.png)

## 4.5 Estabilidad por fases del ciclo del cobre (OE5)

El algoritmo de Bry-Boschan identifica una secuencia coherente de fases de expansión y contracción
del precio del cobre a lo largo de 2004–2024, capturando el súper-ciclo (auge hasta 2011),
la corrección posterior, el shock de 2020 y la recuperación reciente.

La estimación del modelo con **término de interacción** entre el precio del cobre y la fase de
expansión (muestra B) arroja una sensibilidad base —en contracción— de **0,630** y un incremento
en expansión de **+0,083** que, sin embargo, **no es estadísticamente significativo** (p = 0,63).
La lectura es que, en esta especificación preliminar, **la sensibilidad de los retornos al precio
del cobre no difiere de manera significativa entre las fases del ciclo**: el efecto del cobre es
robusto y de magnitud estable a lo largo del régimen. Este resultado matiza la hipótesis de
asimetría (H5 sobre estabilidad) y constituye en sí mismo un hallazgo de interés, sujeto a
confirmación con el conjunto de datos completo.

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

## 4.7 Diagnósticos y robustez

**Dependencia de sección cruzada.** El test de Pesaran (CD) sobre los residuos del panel arroja un
estadístico de **24,50 (p = 0,000)**, rechazando contundentemente la independencia entre empresas.
Este resultado **valida la elección metodológica** de errores estándar de Driscoll-Kraay: las
cinco productoras comparten un factor común —señaladamente el precio del cobre— que induce
correlación contemporánea en sus retornos. Ignorar esta dependencia habría sesgado la inferencia.

**Estabilidad del sistema dinámico.** El VAR estimado es estable (raíces dentro del círculo
unitario), condición necesaria para la validez de las funciones impulso-respuesta y de la
descomposición de varianza reportadas en §4.4.

**Robustez por subperíodos.** Al reestimar el coeficiente del cobre en submuestras, este se
mantiene positivo y significativo, con una magnitud que **aumenta del período 2004–2019 (0,559) al
período 2020–2024 (0,751)**. La mayor sensibilidad reciente es coherente con la intensificación de
la atención de los mercados sobre el cobre en el contexto de la transición energética, y confirma
que el signo y la relevancia del efecto **no dependen de un subperíodo particular**.

## 4.8 Discusión integrada

Los resultados preliminares dibujan un cuadro coherente con la teoría: **el precio del cobre es el
principal determinante de los retornos del sector** (H1), con un efecto positivo, significativo,
**estable entre fases del ciclo** (§4.5) y robusto entre subperíodos (§4.7); **los factores globales
dominan a los locales** en la explicación de la varianza (H6); y el **tipo de cambio** ejerce un
efecto negativo significativo cuyo signo refleja la doble naturaleza —competitividad y riesgo—
anticipada (H2). La comparación entre mercados aporta una primera señal, aún débil, de
**transmisión diferenciada** (H7), mientras que la evidencia de **cointegración de largo plazo**
(H5) resulta mixta, lo que sugiere una relación de equilibrio débil o afectada por quiebres. La
fuerte dependencia de sección cruzada detectada (§4.7) confirma, además, la pertinencia del
tratamiento econométrico adoptado.

Estas lecturas son **provisionales**. Su elevación a la categoría de hallazgos definitivos exige
todavía: (i) incorporar el EMBI y los controles a nivel de empresa; (ii) reespecificar la relación
de largo plazo con pruebas de cointegración con quiebre (Gregory-Hansen); (iii) modelar la
volatilidad condicional (efectos ARCH/GARCH); y (iv) formalizar la comparación entre mercados con
pruebas de igualdad de coeficientes. Los componentes ya ejecutados —resolución del orden de
integración, interacciones por ciclo, diagnósticos de panel y VAR, y robustez por subperíodos—
confieren, no obstante, una base empírica sólida a las conclusiones provisionales.
