# III. RESULTADOS

> Los resultados provienen de una corrida real del pipeline sobre datos públicos (FRED y Yahoo
> Finance). Conservan un carácter preliminar en cuanto a que restan incorporar el EMBI y los
> controles a nivel de empresa; el grueso del aparato econométrico, no obstante, está ejecutado.

## 3.1 Presentación de Resultados

### 3.1.1 Análisis descriptivo y propiedades de las series

La estadística descriptiva muestra retornos mensuales con media en torno a cero, asimetría negativa
y exceso de curtosis, rasgos típicos de los retornos financieros. La distribución por muestra
confirma colas más pesadas que la normal y una mayor dispersión en la muestra internacional de cobre
puro que en el sector minero local.

![Distribución de los retornos mensuales de las carteras de cada muestra.](outputs/figures/fig_distribucion.png)

La matriz de correlación revela que el retorno del sector se asocia positivamente con el precio del
cobre y negativamente con el VIX y el tipo de cambio, con correlaciones bajas entre los regresores,
lo que mitiga la multicolinealidad.

![Matriz de correlación entre el retorno del sector y los factores macro-financieros.](outputs/figures/fig_correlacion.png)

Las pruebas de raíz unitaria confirman el patrón esperado y validan la estrategia de doble vía. El
logaritmo del precio del cobre resulta no estacionario en nivel —integrado de orden uno, I(1)—
mientras que su retorno, obtenido como primera diferencia logarítmica, es estacionario —I(0)—. El
tipo de cambio arroja un resultado ambiguo en las pruebas convencionales, que la prueba de
Zivot-Andrews resuelve al admitir un quiebre estructural: el nivel no es estacionario y su diferencia
sí lo es, de modo que se concluye que es I(1); la clasificación dudosa inicial respondía a la pérdida
de potencia de las pruebas estándar ante los quiebres del período. Dado que el panel exhibe
dependencia de sección cruzada, se aplica la prueba de raíz unitaria de panel de segunda generación
CIPS, robusta a dicha dependencia, que ratifica de manera contundente la estructura supuesta: el
panel de log-precios no rechaza la raíz unitaria (CIPS = −2,29), comportándose como I(1), mientras que
el panel de retornos la rechaza con holgura (CIPS = −16,32), confirmándose como I(0). La doble vía del
diseño —retornos para el corto plazo, niveles para el largo plazo— queda así validada también con
métodos apropiados para la dependencia transversal.

### 3.1.2 Determinantes de los retornos: factores globales y locales

El modelo de panel de efectos fijos con errores Driscoll-Kraay (muestra B; R² within = 0,245) entrega
los siguientes coeficientes.

| Factor | Coeficiente | Significancia |
|---|---|---|
| Precio del cobre (Δ) | **+0,571** | *** |
| VIX (Δ) | −0,008 | * |
| Fed Funds (Δ) | +0,020 | n.s. |
| Treasury 10Y (Δ) | +0,023 | n.s. |
| Tipo de cambio CLP (Δ) | **−1,574** | *** |
| Tasa local (Δ) | −0,007 | n.s. |
| Actividad local (Δ) | −0,523 | n.s. |

El precio del cobre es el determinante central, con efecto positivo y significativo al 1%: un
incremento del precio del metal se traduce de manera directa en mayores retornos, consistente con el
canal de ingresos y con el apalancamiento operativo del sector. El tipo de cambio presenta un efecto
negativo y de magnitud considerable, que capta simultáneamente los canales de competitividad y de
riesgo, en línea con la naturaleza de empresas que valoran sus flujos en dólares. El VIX es negativo
y significativo, reflejando que los episodios de aversión al riesgo global deprimen la valoración de
un sector cíclico y expuesto. En contraste, los factores locales de tasa de interés y de actividad no
resultan significativos en esta especificación, resultado esperable a la luz de la ausencia, por
ahora, del EMBI y de un indicador de actividad más amplio, y del carácter internacional de las
empresas de la muestra B, menos sensibles al ciclo estrictamente doméstico. La lectura conjunta es
que los factores internacionales —cobre y riesgo global— dominan a los locales, primera evidencia a
favor de la hipótesis de dominancia global.

El contraste formal de significancia conjunta por bloque confirma esta lectura: el conjunto de los
factores globales resulta significativo, en tanto que el bloque de los factores locales aporta una
contribución sustancialmente menor a la explicación de la variación de los retornos. El ajuste del
modelo (R² within de 0,245) se encuentra dentro de los valores habituales para regresiones de
retornos mensuales, donde el interés reside en el signo, la significancia y la magnitud económica de
los coeficientes más que en la capacidad de ajuste global.

![Sensibilidad de los retornos a cada factor macro-financiero (muestra B).](outputs/figures/fig_coeficientes.png)

### 3.1.3 Relaciones de largo plazo

La evidencia de cointegración por los métodos que no admiten quiebres es mixta: el test de Johansen
detecta un vector de cointegración, en tanto que el test de bordes ARDL no permite rechazar la
ausencia de una relación de nivel. Esta discrepancia sugiere que la relación de largo plazo, de
existir, es débil o inestable ante pruebas que suponen parámetros constantes. La prueba de
Gregory-Hansen, que admite un quiebre estructural endógeno en la relación de cointegración,
**confirma su existencia** (estadístico ADF\* = −6,68, inferior al valor crítico de −4,92 al 5%) y
fecha el quiebre en **junio de 2008**, coincidente con la crisis financiera global. La lectura es que
existe una relación de equilibrio de largo plazo entre el valor del sector, el cobre y el tipo de
cambio, pero que dicha relación se reconfiguró con la crisis; ello explica por qué las pruebas que
ignoran el quiebre arrojaban evidencia ambigua, y subraya la importancia de incorporar los cambios
estructurales en el análisis de un sector tan expuesto al ciclo del commodity.

### 3.1.4 Dinámica de shocks

La descomposición de la varianza del error de pronóstico del retorno (horizonte de 12 meses, muestra
B) atribuye 62,7% al componente idiosincrático, 18,0% al precio del cobre y 14,0% al VIX, frente a
fracciones marginales de los factores locales (en torno al 3% para la tasa local y al 2% para el tipo
de cambio). Más allá del componente propio, los shocks globales —cobre y riesgo internacional—
explican una fracción muy superior a la de los locales, lo que constituye la evidencia más nítida a
favor de la hipótesis de dominancia global. La causalidad de Granger confirma que el precio del cobre
antecede de manera significativa al retorno del sector (F = 9,11; p = 0,003), y el sistema VAR,
seleccionado por criterio de información, es estable —todas sus raíces se encuentran dentro del
círculo unitario—, condición que valida la lectura de las funciones impulso-respuesta y de la
descomposición de varianza.

![Descomposición de la varianza del error de pronóstico del retorno (FEVD, horizonte 12 meses).](outputs/figures/fig_fevd.png)

La función impulso-respuesta muestra una reacción positiva e inmediata del retorno ante un shock del
cobre, que se disipa en los meses siguientes, resultado cross-validado por las proyecciones locales.

![Impulso-respuesta del retorno del sector ante un shock del precio del cobre (±2 errores estándar).](outputs/figures/fig_irf.png)

### 3.1.5 Estabilidad por fases del ciclo

El algoritmo de Bry-Boschan identifica una secuencia coherente de fases de expansión y contracción
del precio del cobre a lo largo de 2004-2024, capturando el súper-ciclo con auge hasta 2011, la
corrección posterior, el shock de 2020 y la recuperación reciente. La estimación del modelo con un
término de interacción entre el precio del cobre y la fase de expansión arroja una sensibilidad base
—en contracción— de 0,630 y un incremento en expansión de +0,083 que, no obstante, no es
estadísticamente significativo (p = 0,63). La lectura es que, en esta especificación, la sensibilidad
de los retornos al precio del cobre **no difiere de manera significativa entre las fases del ciclo**:
el efecto del cobre es robusto y de magnitud estable a lo largo del régimen, resultado que matiza la
hipótesis de asimetría y constituye en sí mismo un hallazgo de interés.

![Precio del cobre y fases del ciclo fechadas con Bry-Boschan.](outputs/figures/fig_ciclo_cobre.png)

### 3.1.6 Comparación entre mercados

La triangulación entrega la siguiente comparación.

| Muestra | Mercado | β cobre | R² | Varianza por shocks globales |
|---|---|---|---|---|
| B · cobre internacional | global | 0,571 | 0,245 | 0,320 |
| A · cobre Chile | chileno | 0,631 | 0,331 | 0,295 |
| C · minería Chile | chileno | 0,418 | 0,113 | 0,279 |

Se observa que la sensibilidad al cobre es comparable entre el cobre puro internacional (0,571) y el
local de Pucobre (0,631), y menor en el sector minero mixto (0,418), lo que sugiere que la dilución
por otros commodities —hierro, litio y molibdeno— atenúa el coeficiente en la muestra C. La fracción
de varianza atribuida a los shocks globales es, asimismo, algo mayor en el mercado internacional que
en el chileno.

La prueba formal de igualdad de coeficientes (panel combinado de las muestras B y C con interacción
factor × mercado, bajo efectos fijos y errores Driscoll-Kraay) muestra que la sensibilidad al cobre
es **significativamente mayor en el mercado internacional** (diferencia = +0,254; p = 0,010), y que la
sensibilidad al VIX también difiere significativamente, mientras que la del tipo de cambio resulta
estadísticamente equivalente entre mercados. Estos resultados respaldan formalmente la hipótesis de
transmisión diferenciada y constituyen la evidencia central del aporte comparativo de la
investigación.

![Triangulación: sensibilidad al cobre y dominancia global por muestra (B, A, C).](outputs/figures/fig_triangulacion.png)

### 3.1.7 Diagnósticos y robustez

La validez de los resultados se sustenta en una batería de diagnósticos y de pruebas de robustez. El
test de Pesaran (CD = 24,50; p = 0,000) detecta una dependencia de sección cruzada significativa, lo
que valida el uso de errores estándar de Driscoll-Kraay y confirma la presencia del factor común que
representa el cobre. La corrección de Benjamini-Hochberg por pruebas múltiples mantiene la
significancia del cobre, el VIX y el tipo de cambio, de modo que los hallazgos centrales no son
artefactos de la estimación simultánea de numerosos coeficientes. El modelo GJR-GARCH detecta un
efecto apalancamiento estadísticamente significativo (γ = 0,22; p = 0,023): las caídas del retorno
elevan la volatilidad futura más que las alzas de igual magnitud, patrón habitual en los mercados
accionarios. La prueba de Pesaran-Yamagata rechaza la homogeneidad de las pendientes entre empresas,
por lo que el coeficiente del panel debe interpretarse como un efecto promedio en torno al cual existe
dispersión entre firmas, coherente con su distinta composición y tamaño. El efecto del cobre se
mantiene robusto entre subperíodos, intensificándose de 0,56 en 2004-2019 a 0,75 en 2020-2024, en
línea con la creciente atención de los mercados hacia el metal en el contexto de la transición
energética. Finalmente, en términos estandarizados, el VIX (−0,31 σ) y el cobre (+0,29 σ) encabezan la
importancia económica, lo que constituye evidencia económica, y no solo estadística, de la dominancia
de los factores globales. El test de razón de varianzas de Lo y MacKinlay, por su parte, muestra que
los retornos del sector son en gran medida consistentes con un paseo aleatorio, coherente con la
eficiencia de mercado en su forma débil.

![Importancia económica de cada factor (coeficientes estandarizados, muestra B).](outputs/figures/fig_betas.png)

## 3.2 Discusión de Resultados

Los resultados configuran un cuadro coherente con la teoría. La **hipótesis H1** se respalda con
solidez: el cobre es el principal determinante de los retornos, con efecto positivo, significativo,
estable entre fases y robusto entre subperíodos. La **H2** se confirma con signo negativo, reflejo de
los canales de competitividad y de riesgo característicos de las exportadoras de commodities. La
**H3** no encuentra respaldo en la especificación base, donde las tasas no resultan significativas,
lo que sugiere la preeminencia de los factores de commodity y de riesgo global sobre el canal de
descuento. La **H4** se confirma, con el VIX como factor de mayor impacto estandarizado. La **H5** se
respalda una vez que se admite el quiebre de 2008. La **H6** recibe doble respaldo, por la
descomposición de varianza y por los coeficientes estandarizados. Finalmente, la **H7** se confirma
formalmente: la sensibilidad al cobre es mayor en el mercado internacional.

El predominio del precio del cobre como determinante coincide con el canal de flujos de caja
postulado por la teoría y con el apalancamiento operativo del sector, y es consistente con la
evidencia de Zurita et al. (2005), quienes hallaron primas por riesgo significativas asociadas a las
sorpresas del cobre en los retornos accionarios chilenos a nivel agregado. La presente investigación
extiende ese hallazgo al nivel de empresa y lo sitúa en el período 2004-2024, mostrando que el efecto
no solo persiste sino que se intensifica tras 2020, en línea con la creciente atención de los
mercados hacia el cobre en el contexto de la transición energética.

El efecto negativo del tipo de cambio dialoga con la literatura de las monedas-commodity (Chen y
Rogoff, 2003; Pincheira y Hardy, 2019): dado que el peso chileno se aprecia con las alzas del cobre,
una depreciación tiende a coincidir con caídas del metal y con episodios de aversión al riesgo, de
modo que el signo observado captura simultáneamente el canal de competitividad y el de riesgo, tal
como anticipa la teoría de la exposición cambiaria de Adler y Dumas (1984) y Jorion (1990). La
preeminencia de los factores globales sobre los locales, por su parte, es coherente con la condición
de Chile como economía pequeña, abierta y exportadora de un commodity cuyo precio se determina en
los mercados internacionales.

La confirmación de la cointegración con un quiebre en 2008 ilustra la importancia de incorporar los
cambios estructurales en el análisis de largo plazo de un sector tan expuesto al ciclo del commodity,
y reconcilia la evidencia inicialmente mixta de las pruebas que no admiten quiebres. Finalmente, el
hallazgo de una transmisión diferenciada entre mercados conecta la economía del cobre con la
literatura de integración y segmentación (Bekaert y Harvey, 1995, 2005): el mercado internacional,
de mayor profundidad y liquidez, incorpora el shock del cobre de forma más completa que el mercado
chileno. Una salvedad pertinente es que la muestra chilena corresponde al sector minero mixto, por lo
que parte de la diferencia de sensibilidad puede reflejar la composición por commodity además del
efecto de mercado; el control por el precio de cada commodity mitiga, aunque no elimina por completo,
esta consideración. En conjunto, la evidencia configura un cuadro teóricamente fundamentado en el que
seis de las siete hipótesis encuentran respaldo empírico, con la comparación entre mercados como su
aporte más original.

## 3.3 Aporte práctico

El estudio ofrece aportes concretos en varios planos. Para los **inversionistas**, la evidencia
indica que la diversificación frente al ciclo del cobre y al riesgo global es más determinante para
el riesgo de una posición en el sector que la exposición a las variables macroeconómicas locales; en
consecuencia, las estrategias de cobertura y de construcción de carteras deberían priorizar la
gestión de estos dos factores. La cuantificación de la sensibilidad (β del cobre y betas
estandarizados) ofrece, además, un insumo directo para los modelos de riesgo y de valoración del
sector.

Para la **gestión empresarial**, la exposición cambiaria significativa justifica políticas explícitas
de cobertura, en especial para las empresas con estructura de costos en moneda local; y la
persistencia asimétrica de la volatilidad documentada por el modelo GJR-GARCH —según la cual las
caídas elevan la volatilidad más que las alzas— aconseja contemplar escenarios de tensión prolongada
en la planificación financiera.

Para el **mercado de capitales chileno** y los formuladores de política, la evidencia de una
transmisión más completa del shock en los mercados de mayor profundidad plantea la cuestión de
fortalecer la representación bursátil del sector cuprífero en la bolsa nacional, de modo de mejorar
la incorporación de la información y la formación de precios. Finalmente, en el plano metodológico y
de **transparencia**, el proyecto deja disponible una plataforma web interactiva que comunica los
hallazgos y un conjunto de herramientas reproducibles que permiten replicar y extender el análisis,
contribución alineada con los estándares actuales de ciencia abierta.

A modo de síntesis aplicada, los resultados pueden ordenarse en una jerarquía de acción para el
gestor expuesto al sector: en primer lugar, monitorear y cubrir la exposición al ciclo del cobre, por
ser el determinante de mayor peso y el más estable; en segundo lugar, gestionar la exposición al
riesgo global —aproximado por el VIX—, cuyo impacto estandarizado es el más alto y se intensifica en
los episodios de tensión; en tercer lugar, atender la exposición cambiaria, relevante sobre todo para
las empresas con costos en moneda local; y, por último, tratar las tasas de interés y la actividad
local como factores de segundo orden en el horizonte mensual analizado. Esta jerarquía, sustentada en
la evidencia empírica del estudio y no en supuestos a priori, constituye el aporte práctico central
para la toma de decisiones de inversión y de cobertura en el sector cuprífero con exposición a Chile.
