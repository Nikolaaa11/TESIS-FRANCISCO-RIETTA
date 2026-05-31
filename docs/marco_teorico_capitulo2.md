# Capítulo 2 — Marco teórico y revisión de literatura (borrador redactable)

> **Cómo usar este borrador.** Es prosa académica estructurada y lista para editar, construida
> sobre obras seminales reales. Reglas de integridad antes de entregarlo:
> 1. **Verifica cada cita** (autor, año, revista, páginas) en la fuente original.
> 2. Sustituye cada marca **`[COMPLETAR: …]`** por evidencia de TU búsqueda (sobre todo la
>    chilena), con sus citas verificadas. No hay hallazgos empíricos inventados en este texto.
> 3. Adapta tiempos verbales y conectores al estilo de tu programa.

---

## 2.1 Determinantes macroeconómicos de los retornos accionarios

La relación entre las condiciones macroeconómicas y la valoración de los activos financieros
constituye un eje central de la economía financiera. El marco de referencia es la **Teoría de
Valoración por Arbitraje** (Arbitrage Pricing Theory, APT) de Ross (1976), que postula que el
retorno esperado de un activo se explica por su exposición a un conjunto de factores de riesgo
sistemáticos, sin restringirse a un único factor de mercado como en el CAPM. Bajo este marco,
las variables macroeconómicas son candidatas naturales a factores de riesgo, en la medida en
que afectan de manera no diversificable los flujos de caja futuros de las empresas y la tasa a
la que estos se descuentan.

La operacionalización empírica más influyente de esta idea es la de Chen, Roll y Ross (1986),
quienes muestran que un conjunto de fuerzas económicas —la producción industrial, los cambios
en la prima de riesgo, la estructura temporal de tasas y la inflación no anticipada— se
encuentran sistemáticamente asociadas a los retornos accionarios. En la misma línea, Fama
(1981) documenta el vínculo entre la actividad real y los retornos, y Fama y French (1989)
identifican variables de estado macro-financieras con capacidad de explicar la variación de
los retornos a lo largo del ciclo económico. Esta literatura fundamenta el enfoque
multifactorial que adopta la presente investigación: modelar el retorno del sector como
función de un vector de factores macroeconómicos y financieros [ver Capítulo 3].

Formalmente, bajo la APT el retorno del activo *i* se expresa como una combinación lineal de su
exposición a *k* factores comunes:

> r_i = E(r_i) + β_{i,1} f_1 + β_{i,2} f_2 + … + β_{i,k} f_k + ε_i,

donde f_j son los factores sistemáticos (no anticipados), β_{i,j} las sensibilidades (cargas
factoriales) del activo a cada factor, y ε_i un componente idiosincrático diversificable con
E(ε_i)=0. Ausente el arbitraje, el retorno esperado satisface E(r_i) = r_f + Σ_j β_{i,j} λ_j,
donde λ_j es el precio de mercado del riesgo asociado al factor j. La contribución empírica de
esta tesis consiste, precisamente, en estimar las cargas β del sector cobre respecto de un
conjunto explícito de factores macroeconómicos y financieros, y en contrastar su signo, magnitud
y significancia.

**Canales de transmisión.** La teoría identifica dos vías por las cuales un factor macroeconómico
afecta la valoración de una empresa, ambas derivables del modelo de descuento de dividendos
P_t = Σ_s E_t(D_{t+s}) / (1+k)^s: (i) el **canal de flujos de caja**, por el cual el factor altera
los dividendos o utilidades esperadas E_t(D_{t+s}) —dominante para el precio del cobre, que
determina los ingresos de una minera—; y (ii) el **canal de la tasa de descuento**, por el cual el
factor modifica la tasa k a la que se descuentan dichos flujos —relevante para las tasas de interés
y la prima de riesgo—. En una empresa con elevado **apalancamiento operativo**, como es típico en
la minería, las variaciones del precio del commodity se amplifican sobre el margen y, por tanto,
sobre el valor, lo que anticipa una sensibilidad β al cobre elevada.

La evidencia reciente confirma la vigencia de este enfoque en **mercados emergentes**, contexto
más cercano al caso chileno. Diversos estudios que contrastan el APT frente al CAPM en bolsas
emergentes hallan que el primero se sostiene mejor y que el **tipo de cambio** explica de manera
consistente los retornos. Específicamente para Chile, Pedersen (2015), en un documento de trabajo
del Banco Central de Chile, muestra que el efecto del precio del cobre sobre la economía depende
del **tipo de shock** —las alzas por demanda elevan el crecimiento, mientras que los shocks de
oferta o de demanda específica del cobre tienen efectos negativos de corto plazo—, lo que motiva
distinguir la naturaleza de las perturbaciones. Este hallazgo es directamente relevante para la
identificación de shocks de la presente tesis.

## 2.2 Precios de commodities y valoración de empresas mineras

Para una empresa cuyo ingreso depende crucialmente del precio de un commodity, dicho precio
opera como un factor de riesgo de primer orden. La transmisión ocurre por el **canal de los
flujos de caja**: variaciones en el precio del metal alteran directamente los ingresos y, dado
un apalancamiento operativo típicamente elevado en la minería, amplifican el efecto sobre los
márgenes y el valor de la firma. La literatura sobre empresas de recursos naturales ha
formalizado esta relación principalmente en el sector energético: Sadorsky (2001) analiza la
sensibilidad de los retornos de empresas de energía al precio del petróleo, y Boyer y Filion
(2007) examinan los determinantes de los retornos de productoras canadienses de petróleo y gas,
incorporando conjuntamente el precio del commodity, el tipo de cambio y las tasas de interés.
La estructura metodológica de estos trabajos es directamente trasladable al caso del cobre.

La evidencia específica sobre **acciones mineras y precios de metales** es más reciente y
predominantemente internacional. Zhu, Chen y Chen (2021), en *Resources Policy*, documentan que los
precios de los metales no ferrosos tienen un impacto positivo sobre la valoración bursátil del
sector, con efectos que se intensifican tras la crisis financiera de 2008 (financiarización y
co-movimiento de los mercados de commodities). Wallenstein, Mendiola y Chávez-Bedoya, en el marco
de la CLADEA, encuentran una relación positiva pero **inelástica** entre los retornos de acciones
cupríferas y el precio del cobre, más fuerte en empresas de gran capitalización. La literatura
reciente en *Mineral Economics* (2025) modela, mediante ecuaciones estructurales, el vínculo entre
los precios del cobre y del oro y las cotizaciones mineras en las bolsas de Nueva York, Toronto y
Australia. Es notable que esta literatura, pese a su relevancia, **excluye sistemáticamente a
Chile** —primer productor mundial de cobre—, omisión que la presente investigación subsana.

## 2.3 Tipo de cambio y exposición de empresas exportadoras

La exposición cambiaria —definida por Adler y Dumas (1984) como la elasticidad del valor de la
firma frente a variaciones del tipo de cambio— es especialmente relevante para una productora
de cobre con exposición a Chile, cuyos ingresos se denominan mayoritariamente en dólares y cuya
estructura de costos es parcialmente en moneda local. Jorion (1990) propone la metodología
estándar para medir esta exposición, regresando los retornos accionarios sobre la variación del
tipo de cambio; esta especificación es la que adopta la presente investigación para contrastar
su hipótesis sobre el efecto cambiario.

El signo del efecto no es teóricamente unívoco: una depreciación de la moneda local puede
beneficiar los márgenes de una exportadora con costos en moneda local, pero el resultado neto
depende de la estructura de costos, del grado de cobertura y de la moneda en que cotiza la
acción. Esta ambigüedad, lejos de ser una debilidad, constituye una pregunta empírica de
interés. En el caso de las economías exportadoras de commodities, la literatura de *commodity
currencies* (Chen y Rogoff, 2003; Cashin, Céspedes y Sahay, 2004) muestra que el tipo de cambio y
el precio del commodity comparten una relación de largo plazo, de modo que el efecto cambiario sobre
una minera exportadora no puede interpretarse de forma aislada del propio ciclo del metal —un
matiz que la presente investigación incorpora al modelar conjuntamente ambos factores.

## 2.4 Cobre, tipo de cambio y la economía chilena

El caso chileno se inserta en la literatura sobre **monedas-commodity**, que documenta la
estrecha relación entre los términos de intercambio de los países exportadores de materias
primas y sus tipos de cambio. Chen, Rogoff y Rossi (2010) examinan la relación entre los tipos
de cambio de exportadores de commodities y los precios de estos, y Cashin, Céspedes y Sahay
(2004) caracterizan un conjunto de monedas —entre ellas el peso chileno— cuya dinámica está
ligada a los precios de las materias primas que exportan. Esta literatura sustenta la inclusión
conjunta del precio del cobre y del tipo de cambio entre los determinantes del valor del sector,
y motiva la pregunta sobre la **dominancia relativa de los factores globales frente a los
locales**.

La evidencia empírica chilena puede ordenarse en tres eslabones. El primero, **cobre ↔ tipo de
cambio**, es el más sólido: Chen y Rogoff (2003) y Chen, Rogoff y Rossi (2010) sitúan al peso
chileno entre las *commodity currencies* canónicas, y Pincheira y Hardy (2019), en *Resources
Policy*, muestran que el tipo de cambio chileno tiene poder predictivo sobre los retornos del
índice de metales base —incluido el cobre—, dado que este representa cerca de la mitad de las
exportaciones del país. Labbé y De Gregorio (2011), en un documento de trabajo del Banco Central
de Chile, documentan cómo el tipo de cambio real opera como *amortiguador* de los shocks del precio
del cobre. El segundo eslabón, **cobre ↔ mercado accionario chileno agregado**, está representado
de forma directa por Zurita, Fuentes y Gregoire (2005), quienes, mediante un modelo APT sobre
retornos accionarios chilenos (1990–2003), encuentran que las **sorpresas en el precio del cobre**
están preciadas con una prima por riesgo estadísticamente significativa, rechazando el CAPM en
favor del APT. El tercer eslabón, **cobre ↔ acciones mineras**, solo está documentado a nivel
internacional: Wallenstein, Mendiola y Chávez-Bedoya (CLADEA) hallan una relación positiva pero
inelástica entre los retornos de acciones cupríferas y el precio del cobre, y la literatura
reciente en *Mineral Economics* (2025) modela ese vínculo para las bolsas de Nueva York, Toronto y
Australia —excluyendo explícitamente a Chile y la Bolsa de Santiago—.

**El vacío que esta tesis llena** emerge con nitidez de esa revisión: no se identificó ningún
estudio académico que estime econométricamente el efecto del precio del cobre y las variables
macroeconómicas sobre los retornos de las **acciones cupríferas con exposición a Chile a nivel de
empresa**, ni que compare formalmente el mercado bursátil internacional con el chileno para el
período 2004–2024. El antecedente chileno más próximo (Zurita et al., 2005) trabaja con el índice
agregado y termina en 2003; los estudios que sí desagregan a nivel de acción minera excluyen a
Chile. La presente investigación se ubica, por tanto, en la intersección no cubierta de tres
literaturas bien establecidas por separado.

## 2.5 Eficiencia informacional y segmentación de mercados

Un mismo activo subyacente —en este caso, la exposición al precio del cobre— puede ser valorado
de manera distinta según el mercado bursátil en que se transe. La **hipótesis de eficiencia de
mercado** (Fama, 1970) sostiene que los precios incorporan la información disponible; sin embargo,
el grado y la velocidad con que un mercado refleja un shock dependen de su **profundidad,
liquidez y grado de integración** con los mercados internacionales. La literatura sobre
**segmentación de mercados** (Errunza y Losq, 1985; Bekaert y Harvey, 1995) muestra que los
mercados emergentes, parcialmente segmentados, pueden incorporar la información global de forma
más lenta o incompleta que los mercados desarrollados.

Este marco fundamenta la dimensión comparativa de la presente investigación: dado que las mismas
materias primas se transan a través de empresas que cotizan en mercados de distinta profundidad
—el mercado bursátil global frente al chileno—, es teóricamente plausible que la transmisión del
shock del cobre difiera entre ellos. Contrastar esta diferencia constituye el aporte distintivo
del diseño de triangulación por muestras. La literatura sobre la integración del mercado bursátil
chileno —en particular los estudios del Mercado Integrado Latinoamericano (MILA), que reúne a
Chile, Colombia y Perú— documenta una integración **parcial y dependiente del régimen**, con
correlaciones dinámicas que varían entre episodios de calma y de crisis (por ejemplo, en la
comparación entre el período previo a la crisis financiera global y la pandemia de COVID-19).
Asimismo, se ha mostrado que una mayor integración bursátil **reduce la asimetría de información**
y mejora la eficiencia de la inversión en América Latina. Esta evidencia respalda la hipótesis de
que el mercado chileno, comparativamente menos profundo, podría incorporar los shocks globales de
forma más lenta o incompleta que los mercados internacionales.

## 2.6 Enfoques econométricos para la medición de impacto

La estrategia empírica de esta investigación se apoya en un conjunto de técnicas econométricas
consolidadas, cuyo fundamento metodológico se reseña a continuación. El análisis del orden de
integración de las series recurre a las pruebas de raíz unitaria de Dickey y Fuller (1979),
Phillips y Perron (1988) y Kwiatkowski et al. (1992, KPSS), complementadas con el test de
Zivot y Andrews (1992) para quiebres estructurales. El análisis de relaciones de largo plazo se
funda en la teoría de la cointegración de Engle y Granger (1987) y Johansen (1988), y en el
enfoque de **bordes ARDL** de Pesaran, Shin y Smith (2001), particularmente apropiado cuando
las variables presentan órdenes de integración mixtos. La dinámica de los shocks se modela
mediante vectores autorregresivos siguiendo a Sims (1980), con funciones impulso-respuesta
—incluyendo la variante generalizada de Pesaran y Shin (1998)— y descomposición de varianza.

Para el tratamiento de la dimensión de panel se emplean las pruebas de raíz unitaria de Im,
Pesaran y Shin (2003) y Pesaran (2007), la cointegración en panel de Westerlund (2007) y los
errores estándar de Driscoll y Kraay (1998), robustos a la dependencia de sección cruzada. La
datación de las fases del ciclo se basa en el algoritmo de Bry y Boschan (1971), formalizado
para datos de frecuencia trimestral y mensual por Harding y Pagan (2002), y se contempla como
robustez el modelo de cambio de régimen de Hamilton (1989). La modelación de la volatilidad,
cuando resulta pertinente, se apoya en los modelos ARCH/GARCH de Engle (1982) y Bollerslev
(1986).

La pertinencia de un análisis condicionado al régimen encuentra respaldo en la literatura reciente
de mercados de metales: Zhu, Chen y Chen (2021) documentan que el efecto de los precios de los
metales y de la incertidumbre sobre la valoración bursátil del sector **difiere según el estado del
mercado** (alcista o bajista), y Pedersen (2015) muestra que la respuesta de la economía chilena al
cobre depende de la **naturaleza del shock**. Ambos resultados motivan el análisis por fases del
ciclo y la identificación de shocks que adopta esta investigación.

## 2.7 Síntesis e identificación del vacío de investigación

La revisión precedente permite delimitar el aporte de esta investigación a partir de tres
constataciones. Primero, la literatura sobre la relación entre variables macroeconómicas y
retornos accionarios es abundante, pero se concentra en mercados desarrollados y, con
frecuencia, en índices agregados antes que en sectores específicos. Segundo, la evidencia sobre
la transmisión del precio de los commodities a la valoración de empresas se ha desarrollado
predominantemente para el **sector energético**, quedando el cobre y la minería metálica
comparativamente menos estudiados a nivel de acciones. Tercero, la evidencia chilena vincula el
cobre con variables macroeconómicas agregadas —tipo de cambio, crecimiento—, pero rara vez con
la **valoración bursátil de las propias empresas mineras**, y prácticamente no aborda la
**estabilidad de estas relaciones a lo largo de las fases del ciclo del cobre**. Cuarto, no se ha
explorado de manera sistemática si la transmisión del shock macroeconómico **difiere entre el
mercado bursátil global y el chileno** para empresas expuestas a las mismas materias primas.

En consecuencia, esta tesis contribuye a la literatura al cuantificar el impacto de los factores
macroeconómicos globales y locales sobre los retornos del sector de minería de cobre con
exposición a Chile, integrando la medición de sensibilidad (panel), el análisis de equilibrio de
largo plazo (cointegración), la dinámica de shocks (impulso-respuesta y descomposición de
varianza) y, de manera distintiva, la evaluación de la estabilidad de dichas relaciones según la
fase del ciclo del precio del cobre, así como la comparación de su transmisión entre el mercado
bursátil internacional y el chileno.
