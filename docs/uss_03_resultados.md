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

Las pruebas de raíz unitaria confirman que el logaritmo del precio del cobre es no estacionario en
nivel —I(1)— mientras que su retorno es estacionario —I(0)—. La prueba de Zivot-Andrews resuelve la
ambigüedad del tipo de cambio, confirmándolo como I(1). La prueba de panel CIPS, robusta a la
dependencia de sección cruzada, ratifica que los log-precios son I(1) (CIPS = −2,29) y los retornos
I(0) (CIPS = −16,32).

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

El precio del cobre es el determinante central, con efecto positivo y significativo al 1%. El tipo
de cambio presenta un efecto negativo y fuerte, que capta los canales de competitividad y de riesgo.
El VIX es negativo y significativo, mientras que los factores locales de tasa y actividad no resultan
significativos en esta especificación.

![Sensibilidad de los retornos a cada factor macro-financiero (muestra B).](outputs/figures/fig_coeficientes.png)

### 3.1.3 Relaciones de largo plazo

La evidencia de cointegración por los métodos sin quiebre es mixta (Johansen detecta un vector;
ARDL no rechaza la ausencia de relación de nivel). La prueba de Gregory-Hansen, que admite un quiebre
endógeno, **confirma la cointegración** (estadístico ADF\* = −6,68 < −4,92 al 5%) y fecha el quiebre
en **junio de 2008**, coincidente con la crisis financiera global. Existe, por tanto, una relación de
equilibrio de largo plazo que se reconfiguró con la crisis.

### 3.1.4 Dinámica de shocks

La descomposición de varianza del retorno (horizonte de 12 meses, muestra B) atribuye 62,7% al
componente idiosincrático, 18,0% al precio del cobre y 14,0% al VIX, frente a fracciones marginales
de los factores locales. La causalidad de Granger confirma que el cobre antecede al retorno
(F = 9,11; p = 0,003), y el VAR es estable.

![Descomposición de la varianza del error de pronóstico del retorno (FEVD, horizonte 12 meses).](outputs/figures/fig_fevd.png)

La función impulso-respuesta muestra una reacción positiva e inmediata del retorno ante un shock del
cobre, que se disipa en los meses siguientes, resultado cross-validado por las proyecciones locales.

![Impulso-respuesta del retorno del sector ante un shock del precio del cobre (±2 errores estándar).](outputs/figures/fig_irf.png)

### 3.1.5 Estabilidad por fases del ciclo

El fechado de Bry-Boschan identifica una secuencia coherente de fases de expansión y contracción del
precio del cobre. La estimación con interacción por fase arroja una sensibilidad base de 0,630 y un
incremento en expansión de +0,083 no significativo (p = 0,63): la sensibilidad al cobre **no difiere
significativamente** entre fases.

![Precio del cobre y fases del ciclo fechadas con Bry-Boschan.](outputs/figures/fig_ciclo_cobre.png)

### 3.1.6 Comparación entre mercados

La triangulación entrega la siguiente comparación.

| Muestra | Mercado | β cobre | R² | Varianza por shocks globales |
|---|---|---|---|---|
| B · cobre internacional | global | 0,571 | 0,245 | 0,320 |
| A · cobre Chile | chileno | 0,631 | 0,331 | 0,295 |
| C · minería Chile | chileno | 0,418 | 0,113 | 0,279 |

La prueba formal de igualdad de coeficientes (panel combinado con interacción factor × mercado)
muestra que la sensibilidad al cobre es **significativamente mayor en el mercado internacional**
(diferencia = +0,254; p = 0,010), respaldando la hipótesis de transmisión diferenciada.

![Triangulación: sensibilidad al cobre y dominancia global por muestra (B, A, C).](outputs/figures/fig_triangulacion.png)

### 3.1.7 Diagnósticos y robustez

El test de Pesaran (CD = 24,50; p = 0,000) detecta dependencia de sección cruzada, lo que valida los
errores Driscoll-Kraay. La corrección de Benjamini-Hochberg mantiene la significancia del cobre, el
VIX y el tipo de cambio. El modelo GJR-GARCH detecta un efecto apalancamiento (γ = 0,22; p = 0,023).
La prueba de Pesaran-Yamagata rechaza la homogeneidad de pendientes, por lo que el coeficiente del
panel se interpreta como un efecto promedio. El efecto del cobre se mantiene robusto entre
subperíodos (0,56 en 2004-2019; 0,75 en 2020-2024). En términos estandarizados, el VIX (−0,31 σ) y
el cobre (+0,29 σ) encabezan la importancia económica.

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

Estos hallazgos son consistentes con la literatura previa —Zurita et al. (2005) para el efecto del
cobre en retornos chilenos, Pincheira y Hardy (2019) para el nexo cobre-peso, y Bekaert y Harvey
(1995) para la segmentación—, a la vez que la extienden al nivel de empresa y a la comparación entre
mercados, dimensiones no cubiertas previamente. Una salvedad pertinente es que la muestra chilena
corresponde al sector minero mixto, por lo que parte de la diferencia de sensibilidad puede reflejar
la composición por commodity además del efecto de mercado.

## 3.3 Aporte práctico

El estudio ofrece aportes concretos. Para los **inversionistas**, evidencia que la diversificación
frente al ciclo del cobre y al riesgo global es más determinante para el riesgo de una posición en el
sector que la exposición a las variables locales. Para la **gestión empresarial**, la exposición
cambiaria significativa y la persistencia asimétrica de la volatilidad justifican políticas de
cobertura que contemplen escenarios de tensión prolongada. Para el **mercado de capitales chileno**,
la evidencia de transmisión diferenciada plantea la cuestión de política de fortalecer la
representación del sector cuprífero en la bolsa nacional. Adicionalmente, el proyecto aporta una
**plataforma web interactiva** y un **conjunto de herramientas reproducibles** que permiten replicar
y extender el análisis.
