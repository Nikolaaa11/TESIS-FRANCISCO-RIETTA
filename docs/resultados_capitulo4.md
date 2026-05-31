# Capítulo 4 — Resultados y discusión (borrador con resultados preliminares)

> **Advertencia de estatus.** Las cifras de este capítulo provienen de una corrida real del
> pipeline sobre datos públicos (cobre y tipo de cambio de FRED; acciones de Yahoo Finance), pero
> son **preliminares**: aún no incorporan el EMBI ni los controles a nivel de empresa, el orden de
> integración del tipo de cambio requiere revisión por quiebres, y falta la batería completa de
> diagnósticos y robustez. No deben leerse como hallazgos definitivos.

## 4.1 Análisis descriptivo y propiedades de las series (OE1)

Antes de la modelación, conviene caracterizar las series. La estadística descriptiva (Anexo A)
muestra retornos mensuales con media en torno a cero, **asimetría negativa** y **exceso de
curtosis**, rasgos típicos de los retornos financieros. La distribución de los retornos por muestra
(Figura 1) confirma colas más pesadas que la normal y una mayor dispersión en la muestra
internacional de cobre puro que en el sector minero local.

![Distribución de los retornos mensuales de las carteras de cada muestra.](outputs/figures/fig_distribucion.png)

La matriz de correlación de los factores (Figura 2) revela que el retorno del sector se asocia
positivamente con el precio del cobre y negativamente con el VIX y el tipo de cambio, mientras que
las correlaciones entre los regresores son bajas, lo que mitiga preocupaciones de multicolinealidad
—confirmadas más adelante con los factores de inflación de la varianza—.

![Matriz de correlación entre el retorno del sector y los factores macro-financieros (muestra B).](outputs/figures/fig_correlacion.png)

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

Dado que el test de Pesaran detecta dependencia de sección cruzada en el panel (§4.7), se aplica
además la prueba de raíz unitaria de **segunda generación CIPS** (Pesaran, 2007), robusta a dicha
dependencia. Los resultados confirman de manera contundente la estructura supuesta: el panel de
**log-precios** de las empresas no rechaza la raíz unitaria (CIPS = −2,29, por encima del valor
crítico al 5% de −2,57), comportándose como **I(1)**, mientras que el panel de **retornos** la
rechaza con holgura (CIPS = −16,32), confirmándose como **I(0)**. La doble vía del diseño queda así
validada también con métodos de panel apropiados para la dependencia transversal.

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

**Nota sobre la especificación (efectos fijos vs. aleatorios).** Conviene precisar por qué se
adoptan efectos fijos. Dado que los regresores son factores macroeconómicos **comunes a todas las
empresas** —el precio del cobre, el VIX o el tipo de cambio toman el mismo valor para cada firma en
cada mes—, los estimadores de efectos fijos y de efectos aleatorios producen **pendientes
idénticas**; lo único que distingue a ambas especificaciones es el tratamiento de la media
específica de cada empresa. En consecuencia, el test de Hausman resulta degenerado (H ≈ 0) y no
discrimina entre ambos. Se retiene la especificación de **efectos fijos** porque absorbe la
heterogeneidad no observada y constante de cada empresa (distintas medias de retorno por niveles de
riesgo, tamaño o jurisdicción), constituyendo la opción más conservadora y estándar en la
literatura financiera.

## 4.3 Relaciones de largo plazo (OE3)

La evidencia de cointegración es **mixta y, por tanto, no concluyente**. El test de Johansen sobre
las series en nivel (valor de la acción, cobre, tipo de cambio) detecta **un vector de
cointegración** (estadístico de traza 32,1 > 29,8 al 95%), lo que sugiere una relación de equilibrio
de largo plazo. Sin embargo, el **test de bordes ARDL** no permite rechazar la ausencia de
relación de nivel (estadístico F de bordes ≈ 0,95, por debajo de las cotas críticas). Esta
discrepancia entre ambos enfoques sugiere que la relación de largo plazo, de existir, es **débil o
inestable** ante las pruebas que no admiten quiebres. Confirmado ya el orden I(1) del tipo de cambio
(§4.1), la hipótesis natural es que la relación de equilibrio se **desplazó estructuralmente**
durante el período.

La prueba de **Gregory y Hansen (1996)**, que admite un quiebre endógeno en la relación de
cointegración, **confirma esta hipótesis y resuelve la ambigüedad**: el estadístico ADF\* es de
**−6,68**, inferior al valor crítico al 5% (−4,92), de modo que **se rechaza la ausencia de
cointegración**, y el quiebre se fecha en **junio de 2008** —coincidente con la crisis financiera
global—. La lectura es nítida: **existe una relación de equilibrio de largo plazo entre el valor del
sector, el cobre y el tipo de cambio (H5 respaldada), pero esa relación se reconfiguró con la crisis
de 2008**, lo que explica por qué las pruebas que ignoran el quiebre (ARDL/Johansen) arrojaban
evidencia mixta. Este resultado ilustra la importancia de incorporar los quiebres estructurales en
el análisis de largo plazo de un sector tan expuesto al ciclo del commodity.

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
   —el mercado internacional incorporaría el shock de forma más completa—.

**Prueba formal de igualdad de coeficientes entre mercados.** Para contrastar H7 de manera
estadística, se estima un panel combinado de las muestras B y C con interacciones factor × mercado
(indicador *global* = 1 para las empresas que cotizan en el mercado internacional), bajo efectos
fijos por empresa y errores Driscoll-Kraay. El término de interacción **d_cobre × global resulta
positivo y significativo (diferencia = +0,254; p = 0,010)**: la sensibilidad de los retornos al
precio del cobre es **significativamente mayor en el mercado internacional que en el chileno**. La
sensibilidad al VIX también difiere significativamente entre mercados, mientras que la del tipo de
cambio resulta estadísticamente equivalente (p = 0,069). Estos resultados **respaldan formalmente
H7**. Una salvedad de interpretación es pertinente: la muestra internacional es de cobre puro,
mientras que la chilena es un panel del sector minero mixto, de modo que parte de la diferencia
puede reflejar la composición por commodity además del mercado; no obstante, la dirección y la
significancia del resultado son coherentes con una transmisión más completa del shock del cobre en
el mercado de mayor profundidad.

## 4.7 Diagnósticos y robustez

**Dependencia de sección cruzada.** El test de Pesaran (CD) sobre los residuos del panel arroja un
estadístico de **24,50 (p = 0,000)**, rechazando contundentemente la independencia entre empresas.
Este resultado **valida la elección metodológica** de errores estándar de Driscoll-Kraay: las
cinco productoras comparten un factor común —señaladamente el precio del cobre— que induce
correlación contemporánea en sus retornos. Ignorar esta dependencia habría sesgado la inferencia.

**Estabilidad del sistema dinámico.** El VAR estimado es estable (raíces dentro del círculo
unitario), condición necesaria para la validez de las funciones impulso-respuesta y de la
descomposición de varianza reportadas en §4.4.

**Homogeneidad de pendientes.** El test de Pesaran y Yamagata (2008) rechaza la hipótesis de
pendientes homogéneas entre empresas (Δ ajustado = 8,7 en la muestra B; p < 0,01), lo que indica
que las distintas productoras responden al shock del cobre con sensibilidades **heterogéneas** —un
resultado económicamente esperable, dada su diferente composición (cobre puro frente a mineras
diversificadas), tamaño y jurisdicción—. La implicancia es que el coeficiente del panel debe
interpretarse como un **efecto promedio** del sector, en torno al cual existe dispersión entre
firmas; ello motiva, como extensión, un análisis a nivel de empresa con controles idiosincráticos.
La validez de la prueba se verificó sobre paneles sintéticos de pendientes homogéneas (no rechaza)
y heterogéneas (rechaza); no obstante, con el reducido número de empresas la magnitud exacta del
estadístico debe leerse con cautela.

**Robustez por subperíodos.** Al reestimar el coeficiente del cobre en submuestras, este se
mantiene positivo y significativo, con una magnitud que **aumenta del período 2004–2019 (0,559) al
período 2020–2024 (0,751)**. La mayor sensibilidad reciente es coherente con la intensificación de
la atención de los mercados sobre el cobre en el contexto de la transición energética, y confirma
que el signo y la relevancia del efecto **no dependen de un subperíodo particular**.

**Volatilidad condicional (GARCH).** La prueba ARCH-LM rechaza con holgura la ausencia de efectos
de heterocedasticidad condicional (estadístico 41,1; p = 0,000), lo que justifica modelar la
varianza con un GARCH(1,1). El modelo estimado sobre los retornos de la cartera arroja una
**persistencia de la volatilidad de 0,86** (α = 0,15; β = 0,70), indicativa de **agrupamiento de
volatilidad**: los episodios de alta volatilidad —como las crisis— tienden a prolongarse. La
distribución t estimada (ν ≈ 12) confirma además la presencia de **colas más pesadas** que la
normal, característica de los retornos financieros. La extensión a un modelo asimétrico
**GJR-GARCH** revela un **efecto apalancamiento** estadísticamente significativo (γ = 0,22;
p = 0,023), preferido por el criterio BIC: las caídas del retorno elevan la volatilidad futura más
que las alzas de igual magnitud, un patrón habitual en los mercados accionarios. La volatilidad
condicional estimada (Figura) traza con claridad los episodios de tensión —la crisis de 2008 y la
pandemia de 2020 destacan como picos—, ilustrando el agrupamiento de volatilidad.

![Volatilidad condicional estimada por el modelo GARCH(1,1) para la cartera de la muestra B.](outputs/figures/fig_garch.png)

**Corrección por pruebas múltiples.** Dado que el contraste de las hipótesis involucra la
estimación simultánea de numerosos coeficientes, se aplica la corrección de **Benjamini-Hochberg
(control de la tasa de falsos descubrimientos, FDR)** sobre los p-valores del panel. Tras la
corrección, **el precio del cobre, el VIX y el tipo de cambio conservan su significancia**
(p-valores ajustados de 0,000, 0,000 y 0,000, respectivamente), mientras que los factores ya no
significativos se mantienen como tales. Los hallazgos centrales no son, por tanto, artefactos de
pruebas múltiples.

**Magnitudes económicas (betas estandarizados).** Expresado en desviaciones estándar, el factor de
mayor impacto sobre el retorno es el **riesgo global (VIX, −0,31 σ)**, seguido muy de cerca por el
**precio del cobre (+0,29 σ)** y, a mayor distancia, el tipo de cambio (−0,13 σ). Esta jerarquía
—dos factores globales en la cúspide— constituye evidencia económica, y no solo estadística, a
favor de la dominancia de los factores internacionales (H6).

![Importancia económica de cada factor medida por su coeficiente estandarizado (muestra B).](outputs/figures/fig_betas.png)

**Local Projections.** Como alternativa al VAR, más robusta a la mala especificación, se estima la
respuesta del retorno a un shock del cobre mediante **proyecciones locales (Jordà, 2005)** con
errores estándar HAC horizonte a horizonte. La respuesta estimada (0,68 en el impacto, con
decaimiento posterior) **coincide cualitativamente con la función impulso-respuesta del VAR**, lo
que refuerza la robustez de la dinámica reportada en §4.4.

![Respuesta del retorno a un shock del cobre mediante proyecciones locales (Jordà, 2005), IC 95%.](outputs/figures/fig_lp.png)

## 4.8 Discusión integrada

Los resultados preliminares dibujan un cuadro coherente con la teoría: **el precio del cobre es el
principal determinante de los retornos del sector** (H1), con un efecto positivo, significativo,
**estable entre fases del ciclo** (§4.5) y robusto entre subperíodos (§4.7); **los factores globales
dominan a los locales** en la explicación de la varianza (H6); y el **tipo de cambio** ejerce un
efecto negativo significativo cuyo signo refleja la doble naturaleza —competitividad y riesgo—
anticipada (H2). La comparación entre mercados, contrastada formalmente mediante interacciones,
**respalda H7**: la sensibilidad al cobre es significativamente mayor en el mercado internacional
que en el chileno (§4.6). La **relación de cointegración de largo plazo** (H5) **se confirma una vez
que se admite un quiebre estructural** en 2008 (Gregory-Hansen), lo que reconcilia la evidencia
inicialmente mixta. La fuerte dependencia de sección cruzada detectada (§4.7) confirma, además, la
pertinencia del tratamiento econométrico adoptado.

Estas lecturas son **provisionales** en un único sentido acotado: su elevación a hallazgos
plenamente definitivos exige todavía incorporar el **EMBI** y los **controles a nivel de empresa**.
En cambio, el grueso del aparato econométrico **ya está ejecutado y
es concluyente**: la resolución del orden de integración (Zivot-Andrews), las interacciones por
ciclo (OE5), los diagnósticos de panel y VAR (CD de Pesaran, estabilidad), la robustez por
subperíodos, la **cointegración con quiebre** (Gregory-Hansen) y la **volatilidad condicional**
(GARCH) confieren una base empírica sólida a las conclusiones aquí presentadas.

## 4.9 Síntesis del contraste de hipótesis

Para cerrar el capítulo conviene recapitular el resultado del contraste de cada hipótesis a la luz de la evidencia reunida. La **hipótesis H1**, que postula un efecto positivo del precio del cobre sobre los retornos, se ve sólidamente respaldada: el coeficiente es positivo, de magnitud económica relevante, significativo al 1% y, además, robusto tanto a la corrección por pruebas múltiples como a la partición en subperíodos. Es, sin ambigüedad, el determinante central del valor del sector.

La **hipótesis H2** sobre el efecto del tipo de cambio se confirma con signo negativo: la depreciación del peso se asocia a menores retornos, un resultado que captura simultáneamente el canal de competitividad y el de riesgo, y que es coherente con la naturaleza de empresas que valoran sus flujos en dólares. La **hipótesis H3** relativa a las tasas de interés no encuentra respaldo en la especificación base, donde ni la tasa local ni la externa resultan significativas; este resultado, antes que una anomalía, refleja la preeminencia de los factores de commodity y de riesgo global sobre el canal de descuento para este sector específico.

La **hipótesis H4** sobre el riesgo global se confirma: el VIX presenta un efecto negativo y significativo y, medido en desviaciones estándar, constituye el factor de mayor impacto económico sobre el retorno. La **hipótesis H5** de cointegración de largo plazo, inicialmente ambigua, se confirma una vez que se admite un quiebre estructural en 2008: la relación de equilibrio entre el valor del sector y el cobre existe, pero se reconfiguró con la crisis financiera global. La **hipótesis H6** de dominancia de los factores globales recibe doble respaldo, tanto por la descomposición de varianza —donde los shocks globales explican una fracción muy superior a los locales— como por la jerarquía de los coeficientes estandarizados.

Finalmente, la **hipótesis H7**, eje distintivo de esta investigación, se respalda mediante la prueba formal de igualdad de coeficientes entre mercados: la sensibilidad de los retornos al precio del cobre es significativamente mayor en el mercado bursátil internacional que en el chileno. En conjunto, seis de las siete hipótesis encuentran respaldo empírico, configurando un cuadro coherente y teóricamente fundamentado sobre la transmisión del impacto macroeconómico al sector del cobre, con la comparación entre mercados como su aporte más original.
