# II. MATERIAL Y MÉTODO

## 2.1 Tipo y Diseño de Investigación

La investigación se inscribe en el **paradigma positivista** y adopta un **enfoque cuantitativo**,
en tanto cuantifica relaciones entre variables medibles a partir de datos secundarios objetivos y
contrasta hipótesis mediante técnicas estadísticas. El **tipo** de investigación es **explicativo o
de medición de impacto** —no predictivo—, pues su propósito es determinar la magnitud, el signo y la
significancia del efecto de las variables macroeconómicas sobre los retornos accionarios, así como
las relaciones de causalidad y de equilibrio entre ellas.

El **diseño** es **no experimental**, dado que las variables no se manipulan sino que se observan en
su contexto natural, y **longitudinal de tendencia**, pues abarca el período 2004-2024 con frecuencia
mensual. Metodológicamente combina dos aproximaciones complementarias: el análisis de **series de
tiempo** sobre la cartera del sector y el análisis de **datos de panel** sobre el conjunto de
empresas. El **alcance** es correlacional-explicativo y, de manera distintiva, **comparativo**, ya
que contrasta la transmisión del impacto macroeconómico entre dos mercados bursátiles de distinta
profundidad. Esta combinación de técnicas, articulada bajo un diseño de triangulación por muestras,
busca robustecer la validez de las conclusiones mediante la convergencia de evidencia proveniente de
distintos estimadores y fuentes.

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

El período de estudio comprende desde enero de 2004 hasta diciembre de 2024, con frecuencia mensual,
ventana que cubre al menos un ciclo completo del precio del cobre —el súper-ciclo con auge hasta 2011,
la corrección posterior, el shock de 2020 y la recuperación reciente— y que provee del orden de 250
observaciones temporales por empresa. El criterio de inclusión es explícito y replicable: empresas
cuya acción transa en un mercado regulado, cuyos ingresos provienen mayoritariamente de la producción
de cobre y con operaciones relevantes en Chile. La cobertura temporal de cada serie se verificó al
construir la base de datos.

La comparación de los resultados entre las tres muestras permite evaluar si el mercado internacional
y el chileno incorporan los shocks macroeconómicos de manera diferenciada, convirtiendo la limitación
estructural —la escasa presencia del cobre puro en la bolsa local— en una oportunidad de diseño que
contrasta la formación de precios en mercados de distinta profundidad.

## 2.3 Variables y Operacionalización

La **variable dependiente** es el retorno logarítmico mensual de cada empresa,
$rᵢₜ = ln(Pᵢₜ) − ln(Pᵢ,ₜ₋₁)$, calculado sobre precios de cierre ajustados por dividendos y splits. La
elección del retorno logarítmico, en lugar del precio en nivel, responde a su mejor comportamiento
estadístico —estacionariedad y propiedades de aditividad temporal— y es estándar en la literatura
financiera. Para el análisis agregado de series de tiempo se construye, adicionalmente, una cartera
del sector en sus versiones equiponderada y ponderada por capitalización bursátil, esta última con
pesos rezagados un período para evitar el sesgo de anticipación.

Las **variables independientes** se agrupan en factores macroeconómicos globales (precio del cobre,
VIX, tasa de fondos federales, rendimiento del bono del Tesoro a 10 años, petróleo WTI como control)
y locales (tipo de cambio USD/CLP, tasa de interés local, actividad económica e IPC), a los que se
suman controles a nivel de empresa (tamaño, volatilidad y apalancamiento). Cada variable se
operacionaliza mediante un indicador observable de fuente oficial y se somete a la transformación
correspondiente a su orden de integración. La siguiente tabla resume la operacionalización.

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

Las fuentes se seleccionaron por su carácter oficial, su continuidad y su uso extendido en la
literatura financiera. Para las variables macroeconómicas globales se recurre a la base de datos
Federal Reserve Economic Data (FRED), que centraliza series de organismos como la Reserva Federal y
la OCDE; para los precios accionarios, a Yahoo Finance, que provee series ajustadas por dividendos y
splits; y como referencias institucionales del cobre y de la economía chilena, a la Comisión Chilena
del Cobre (Cochilco) y al Banco Central de Chile. Los proxies de las variables locales (tasa de
interés, actividad económica e inflación) se obtienen de las series de la OCDE disponibles en FRED,
lo que asegura su comparabilidad internacional.

La **validez** se sustenta en el uso de estas series oficiales y en la verificación sistemática de su
cobertura temporal y de su correcta alineación. La **confiabilidad** se garantiza mediante la
**reproducibilidad** del proceso: el pipeline completo de análisis se regenera con un solo comando y
produce resultados idénticos en cada ejecución —se verificó la ausencia de divergencias entre
corridas sucesivas—, y se acompaña de una suite de pruebas unitarias que valida las funciones
econométricas clave sobre casos de referencia conocidos, tales como la correcta clasificación del
orden de integración de series simuladas.

## 2.5 Procedimiento de análisis de datos

El análisis se realiza con el lenguaje Python y sus librerías especializadas (pandas, numpy,
statsmodels, linearmodels y arch). Las series de distinta periodicidad —diaria, mensual y
trimestral— se armonizan a frecuencia **mensual** (último dato del mes para precios e índices),
criterio que ofrece del orden de 250 observaciones temporales, suficientes para los modelos
empleados, y que coincide con la periodicidad del principal indicador de actividad doméstica. Las
variables contables, de periodicidad trimestral, se incorporan mediante arrastre del último valor
conocido con un rezago de publicación que evita el sesgo de anticipación. Las series identificadas
como integradas de orden uno ingresan en primera diferencia a los modelos de impacto y se conservan
en nivel para el análisis de cointegración.

La secuencia analítica está organizada de modo que el orden de integración de las series bifurca la
estrategia: las variables estacionarias alimentan los modelos de impacto de corto plazo, mientras que
las no estacionarias se reservan para el análisis de equilibrio de largo plazo. A continuación se
detalla el procedimiento por objetivo específico.

**Estacionariedad (OE1).** Se aplican pruebas de raíz unitaria de Dickey-Fuller aumentada (ADF),
Phillips-Perron y KPSS. Las dos primeras contrastan la hipótesis nula de raíz unitaria, mientras que
la prueba KPSS invierte la nula —estacionariedad—, de modo que su uso conjunto permite una conclusión
robusta cuando ambos enfoques coinciden. Se complementan con la prueba de Zivot-Andrews, que admite
un quiebre estructural endógeno y resulta apropiada para un período marcado por el súper-ciclo, la
crisis de 2008 y la pandemia de 2020. Dado que el análisis de panel involucra series correlacionadas
entre empresas, se aplica además la prueba de raíz unitaria de panel de segunda generación CIPS
(Pesaran, 2007), robusta a la dependencia de sección cruzada. El resultado de esta etapa determina la
especificación posterior: las variables I(0) ingresan en nivel a los modelos de impacto y las I(1) se
diferencian.

**Sensibilidad (OE2).** Se estima un modelo de datos de panel con efectos fijos por empresa:

$$rᵢₜ = αᵢ + β₁ Δcobreₜ + β₂ ΔTCₜ + β₃ Δtasaₜ + β₄ ΔVIXₜ + γ′ Xᵢₜ + εᵢₜ$$

con errores estándar de Driscoll-Kraay, robustos a heterocedasticidad, autocorrelación y dependencia
de sección cruzada —esta última esperable dado que el precio del cobre actúa como factor común a
todas las empresas—. La elección de los efectos fijos se justifica porque absorben la heterogeneidad
no observada y constante de cada firma; como especificación de referencia se estima en paralelo un
modelo de serie de tiempo sobre la cartera del sector con errores HAC de Newey-West. El contraste de
dominancia global versus local (H6) se realiza mediante tests de Wald de significancia conjunta por
bloque de regresores, complementado con el cálculo de coeficientes estandarizados que permiten
comparar la importancia económica de cada factor. Para controlar el riesgo de falsos positivos
derivado de la estimación simultánea de numerosos coeficientes, se aplica la corrección de
Benjamini-Hochberg sobre los p-valores.

**Largo plazo (OE3).** Se evalúa la cointegración mediante el test de bordes ARDL (Pesaran, Shin y
Smith, 2001), el test de Johansen y, ante la posibilidad de quiebres, el test de Gregory-Hansen
(1996), del que se obtiene el modelo de corrección de error.

**Dinámica de shocks (OE4).** Se estima un VAR (o un VECM, si las series cointegran) cuya
identificación de los shocks estructurales se realiza por descomposición de Cholesky, con un
ordenamiento de las variables según su grado de exogeneidad: el precio del cobre, determinado en el
mercado global, se ordena primero, y la acción, como variable más endógena, al final. De este sistema
se obtienen las **funciones impulso-respuesta**, que trazan la reacción del retorno ante un shock del
cobre a lo largo del horizonte, y la **descomposición de la varianza del error de pronóstico**
(FEVD), que cuantifica la fracción de la varianza del retorno atribuible a cada shock y constituye la
evidencia central para la hipótesis de dominancia global. La robustez de estas conclusiones a la
identificación se verifica mediante reordenamientos y mediante las **proyecciones locales** de Jordà
(2005), una alternativa más robusta a la mala especificación, así como con pruebas de causalidad de
Granger.

**Estabilidad por fases del ciclo (OE5).** Las fases del ciclo del precio del cobre se fechan de
manera objetiva con el algoritmo de puntos de giro de Bry-Boschan, que identifica máximos y mínimos
locales, impone alternancia pico-valle y censura las fases demasiado breves, clasificando el período
en expansiones y contracciones. La estabilidad de la relación se evalúa incorporando una variable
indicadora de fase y sus interacciones con los factores, lo que permite contrastar si la sensibilidad
de los retornos —en particular al cobre— difiere entre regímenes. Como robustez de la dinámica de la
volatilidad se estiman modelos GARCH y GJR-GARCH, que capturan, respectivamente, el agrupamiento y la
asimetría de la volatilidad condicional.

**Comparación entre mercados (OE6).** El conjunto del análisis se ejecuta en paralelo sobre las tres
muestras y se consolida en una comparación sistemática. La hipótesis de transmisión diferenciada se
contrasta de manera formal mediante un panel combinado de las muestras del mercado internacional y del
chileno, con términos de interacción factor × mercado: la significancia de la interacción con el
precio del cobre constituye la prueba directa de si la sensibilidad difiere entre mercados.
Adicionalmente, como contraste de la hipótesis de eficiencia, se aplica el test de razón de varianzas
de Lo y MacKinlay (1988) a los retornos. La homogeneidad de las pendientes entre empresas se examina
con la prueba de Pesaran-Yamagata, y la robustez general se valida con submuestras y definiciones
alternativas de las variables.

## 2.6 Criterios éticos

La investigación se sustenta en **datos públicos y de libre acceso**, de carácter agregado y de
mercado, sin información personal ni confidencial de individuos, por lo que no requiere consentimiento
informado ni la aprobación de un comité de ética en seres humanos. Se respeta la **propiedad
intelectual** mediante la citación rigurosa de toda fuente conforme a las normas APA, evitando el
plagio en cualquiera de sus formas. Se observa el principio de **integridad científica**: no se
inventan ni se manipulan datos o resultados, las cifras provienen de fuentes verificables y
documentadas, y los hallazgos se reportan tal como resultan, incluyendo de manera explícita los
coeficientes no significativos y las limitaciones del estudio. Asimismo, se adhiere al principio de
**transparencia y ciencia abierta**, poniendo a disposición el código y el procedimiento que permiten
auditar y replicar cada resultado.

## 2.7 Criterios de Rigor Científico

El rigor se asegura mediante: (i) la **validez interna**, con una batería completa de diagnósticos
(dependencia de sección cruzada, estabilidad del sistema dinámico, homogeneidad de pendientes); (ii)
la **robustez**, contrastando los resultados en submuestras, con definiciones alternativas de las
variables y con métodos complementarios (proyecciones locales frente a VAR, corrección por pruebas
múltiples); (iii) la **reproducibilidad**, dado que todo resultado puede regenerarse desde el
repositorio del proyecto; y (iv) la **transparencia**, declarando explícitamente las limitaciones y
el carácter de los resultados.
