# Capítulo 1 — Introducción (borrador redactable)

> **Título (definido):** *"Impacto de las variables macroeconómicas en los retornos accionarios
> de las empresas de cobre con exposición a Chile: una comparación entre el mercado bursátil
> internacional y el chileno, 2004–2024."*
>
> Prosa lista para editar. **Regla de integridad:** cada marca `[COMPLETAR: cifra + fuente]`
> debe reemplazarse por un dato verificado de fuente oficial (Cochilco, Banco Central de Chile,
> INE, Bolsa de Santiago). No hay cifras inventadas en este borrador.

---

## 1.1 Contextualización

El cobre ocupa un lugar estructural en la economía chilena. Chile es el principal productor
mundial de cobre, y este metal representa una fracción central de sus exportaciones y un aporte
significativo a los ingresos fiscales y al producto. [COMPLETAR: participación del cobre en las
exportaciones totales y en el PIB, con cifra y año, fuente Cochilco / Banco Central de Chile.]
Esta dependencia convierte al precio del cobre en una variable macroeconómica de primer orden
para el país, con efectos documentados sobre el tipo de cambio, las cuentas externas y el ciclo
económico nacional.

En el plano financiero, las empresas dedicadas a la extracción y procesamiento de cobre
constituyen un sector cuya valoración bursátil está, en principio, estrechamente ligada a la
evolución del precio del metal y a las condiciones macroeconómicas globales y locales. Sin
embargo, la magnitud, el signo y la estabilidad de esa relación no son evidentes a priori:
dependen de la estructura de ingresos y costos de las empresas, de su exposición cambiaria, del
entorno de tasas de interés y del apetito por riesgo de los mercados internacionales. Cuantificar
empíricamente esta relación, para el caso específico de las empresas de minería de cobre con
exposición a Chile, es el propósito de esta investigación.

## 1.2 Problema de investigación y justificación

La literatura financiera ha establecido que las variables macroeconómicas constituyen factores
de riesgo sistemático que afectan los retornos accionarios. No obstante, la mayor parte de la
evidencia se concentra en mercados desarrollados, en índices agregados y, en el ámbito de los
commodities, en el sector energético. Para el caso chileno, si bien existe evidencia que vincula
el precio del cobre con variables macroeconómicas agregadas como el tipo de cambio y el
crecimiento, son escasos los estudios que analizan su impacto sobre la **valoración bursátil de
las propias empresas mineras**, y prácticamente inexistentes los que evalúan si dicho impacto es
**estable a lo largo de las distintas fases del ciclo del precio del cobre**.

Este vacío es relevante por tres razones. Primero, desde la perspectiva de los **inversionistas**,
comprender qué factores mueven los retornos del sector y con qué intensidad es esencial para la
valoración y la gestión de riesgos. Segundo, desde la perspectiva de la **política y la gestión
empresarial**, identificar la sensibilidad del valor de las empresas a shocks macroeconómicos
informa decisiones de cobertura y planificación. Tercero, desde la perspectiva **académica**, el
caso chileno ofrece un laboratorio natural para estudiar la transmisión de un precio de commodity
a la valoración de empresas en una economía pequeña, abierta y exportadora.

## 1.3 Pregunta y objetivos de investigación

**Pregunta general.** ¿Cuál es el impacto de las variables macroeconómicas globales y nacionales
sobre los retornos accionarios de las empresas de cobre con exposición a Chile; es dicho impacto
estable a lo largo de las fases del ciclo del precio del cobre; y se transmite de manera
diferenciada en el **mercado bursátil internacional** frente al **chileno**?

**Objetivo general.** Cuantificar y comparar el impacto de las variables macroeconómicas globales
y nacionales sobre los retornos accionarios de las empresas de cobre con exposición a Chile
durante el período 2004–2024, contrastando su transmisión entre el mercado bursátil internacional
y el chileno, mediante modelos econométricos de series de tiempo y datos de panel.

*(La estabilidad de las relaciones a lo largo de las fases del ciclo del cobre y la comparación
entre mercados se desarrollan como objetivos específicos OE5 y OE6.)*

**Objetivos específicos.**
1. Caracterizar las propiedades estadísticas de las series de retornos y de las variables
   explicativas (estacionariedad, volatilidad y quiebres estructurales).
2. Estimar la sensibilidad de los retornos a las variables macro-financieras, distinguiendo
   factores globales de locales.
3. Determinar la existencia de relaciones de equilibrio de largo plazo y dinámicas de corto plazo
   entre el valor bursátil del sector y sus determinantes macroeconómicos.
4. Cuantificar la respuesta dinámica de los retornos ante shocks en las variables macro clave.
5. Evaluar la estabilidad de estas relaciones a lo largo de las fases del ciclo del precio del
   cobre.
6. Comparar la transmisión del impacto macroeconómico entre el mercado bursátil global y el
   mercado bursátil chileno.

*(Las preguntas específicas PI1–PI6 y las hipótesis H1–H7 se presentan en el Capítulo 2 y se
sintetizan en la matriz de consistencia.)*

## 1.4 Hipótesis general

Se postula que el precio del cobre constituye el principal determinante de los retornos del
sector, con un efecto positivo y significativo; que los factores globales predominan sobre los
locales en la explicación de la varianza de los retornos; que la sensibilidad de los retornos a
los factores macroeconómicos varía según la fase del ciclo del cobre; y que el mercado bursátil
global incorpora los shocks del cobre de forma más rápida y completa que el mercado chileno. El
detalle y el sustento teórico de cada hipótesis se desarrollan en el Capítulo 2.

## 1.5 Aspectos metodológicos y alcance

La investigación adopta un enfoque **explicativo y de medición de impacto**, no predictivo,
empleando herramientas de econometría de series de tiempo y datos de panel. El universo de
estudio se organiza bajo un **diseño de triangulación por tres muestras**: empresas de cobre que
cotizan en el mercado global con operación en Chile (muestra B), empresas de extracción de cobre
que cotizan en el mercado chileno (muestra A) y el sector minero cotizado en el mercado chileno
(muestra C). La comparación de los resultados entre las tres muestras permite contrastar si el
mercado global y el chileno precian de manera diferenciada los shocks macroeconómicos. El período
de estudio abarca 2004–2024 con frecuencia mensual, cubriendo al menos un ciclo completo del
precio del cobre. El análisis se implementa en Python.

Entre las **limitaciones** del estudio cabe anticipar el reducido número de empresas de cobre
puro cotizadas con exposición a Chile, la heterogeneidad de los mercados en que transan y la
disponibilidad de algunas series macroeconómicas locales, aspectos que se abordan explícitamente
en el diseño metodológico (Capítulo 3).

## 1.6 Aportes esperados

El principal aporte de esta tesis es proporcionar evidencia empírica cuantitativa sobre los
determinantes macroeconómicos de la valoración bursátil del sector de minería de cobre en Chile,
integrando en un mismo marco la medición de sensibilidad, el análisis de largo plazo, la dinámica
de shocks y la evaluación de la estabilidad de estas relaciones según la fase del ciclo del cobre.
De manera distintiva, el diseño de triangulación por tres muestras permite **comparar cómo el
mercado bursátil global y el mercado bursátil chileno incorporan los shocks macroeconómicos**
sobre las mismas materias primas, conectando la evidencia con la literatura sobre eficiencia
informacional y segmentación de mercados —un ángulo escasamente explorado para el caso chileno.

## 1.7 Estructura de la tesis

El resto del documento se organiza como sigue. El Capítulo 2 presenta el marco teórico y la
revisión de literatura, junto con las hipótesis. El Capítulo 3 describe los datos, su tratamiento
y la estrategia econométrica. El Capítulo 4 expone y discute los resultados, organizados por
objetivo específico. El Capítulo 5 concluye, sintetizando los hallazgos, sus implicancias, las
limitaciones del estudio y las líneas futuras de investigación.
