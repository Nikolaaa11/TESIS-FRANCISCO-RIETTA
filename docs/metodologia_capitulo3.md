# Capítulo 3 — Datos y metodología (borrador redactable)

> Borrador de prosa académica alineado 1:1 con lo implementado en `src/`. Ajusta tiempos
> verbales y cifras finales tras correr el dataset completo. No incluye resultados (van en Cap. 4).

---

## 3.1 Definición del universo de empresas y período

El estudio abarca el período **2004–2024** con frecuencia **mensual**. Dado que las grandes
productoras de cobre con operación en Chile no cotizan en el mercado bursátil local —por ser
estatales (Codelco) o subsidiarias de empresas extranjeras (Escondida, Los Bronces)—, el diseño
adopta una **estrategia de triangulación por tres muestras complementarias**, que permite
comparar la transmisión del impacto macroeconómico entre el mercado bursátil global y el chileno:

- **Muestra B (cobre, mercado global):** empresas de cobre con operación en Chile que cotizan en
  mercados internacionales (Antofagasta plc, BHP, Anglo American, Lundin Mining, Teck). Constituye
  la referencia de "cobre puro" y, por su tamaño de sección cruzada, el panel principal.
- **Muestra A (cobre, mercado chileno):** empresas de extracción de cobre que cotizan en la Bolsa
  de Santiago (Sociedad Punta del Cobre). De cardinalidad reducida, se analiza mediante técnicas
  de serie de tiempo.
- **Muestra C (sector minero, mercado chileno):** empresas mineras cotizadas en la Bolsa de
  Santiago (Punta del Cobre, CAP, SQM-B, Molibdenos y Metales). Esta muestra **no es objeto de
  estudio en sí**, sino el *vehículo* que permite estimar con tamaño de sección cruzada cómo el
  mercado bursátil chileno incorpora los shocks macroeconómicos; al combinar distintos commodities,
  se **controla por el precio propio de cada uno** para aislar el efecto del cobre. El objeto de
  estudio sigue siendo el cobre.

La comparación de los resultados entre las tres muestras permite evaluar si el mercado global y
el mercado chileno incorporan los shocks macroeconómicos de manera diferenciada.

La elección de la frecuencia mensual responde a tres consideraciones: (i) el período provee
del orden de 250 observaciones temporales, suficientes para la estimación de modelos VAR/VECM
y ARDL; (ii) el principal indicador de actividad doméstica (IMACEC) es de periodicidad
mensual; y (iii) se atenúa el ruido de microestructura propio de los datos diarios.

## 3.2 Variable dependiente

La variable dependiente es el **retorno logarítmico mensual** de cada empresa,
$rᵢₜ = ln(Pᵢₜ) − ln(Pᵢ,ₜ₋₁)$, calculado sobre precios de cierre **ajustados** por
dividendos y splits. Para el análisis agregado de series de tiempo se construye además una
**cartera del sector**, en sus versiones equiponderada y ponderada por capitalización
bursátil (con pesos rezagados un período para evitar sesgo de anticipación).

## 3.3 Variables explicativas

Las variables explicativas se agrupan en tres bloques: (a) **macroeconómicas globales**
—precio del cobre, índice de volatilidad VIX, tasa de fondos federales, rendimiento del bono
del Tesoro a 10 años y precio del petróleo WTI como control—; (b) **macroeconómicas locales**
—tipo de cambio USD/CLP, Tasa de Política Monetaria, IMACEC, EMBI Chile e IPC—; y
(c) **financieras de empresa** —tamaño, volatilidad y apalancamiento como controles
prioritarios—. La definición operativa, fuente y frecuencia de cada serie se detallan en la
Tabla 3.1 (ver `src/config.py`).

## 3.4 Tratamiento de datos y frecuencias mixtas

Todas las series se llevan a frecuencia mensual (último dato del mes para precios, índices y
tasas de nivel). Las variables contables, de periodicidad trimestral, se incorporan mediante
arrastre del último valor conocido (*forward fill*) con un rezago de publicación que evita el
sesgo de anticipación. Las variables identificadas como integradas de orden uno se incorporan
en **primera diferencia** (logarítmica para precios y tipo de cambio), mientras que las
estacionarias entran en nivel. Los retornos se winsorizan opcionalmente al 1% para acotar el
efecto de colas pesadas, reportándose la sensibilidad de los resultados a este tratamiento.

## 3.5 Datación de las fases del ciclo del cobre

Las fases del ciclo se determinan aplicando un algoritmo de puntos de giro tipo
**Bry-Boschan / Harding-Pagan** sobre el logaritmo del precio del cobre, que identifica
máximos y mínimos locales en una ventana simétrica, impone alternancia pico-valle y censura
fases y ciclos de duración inferior a los umbrales mínimos. El procedimiento entrega una
clasificación objetiva y replicable en fases de **expansión** (valle→pico) y **contracción**
(pico→valle). La datación se realiza sobre el precio del cobre —no sobre las acciones— para
evitar circularidad (implementación en `src/cycle_dating.py`).

## 3.6 Estrategia econométrica

### 3.6.1 Estacionariedad y orden de integración (OE1)
Se aplica una batería de pruebas de raíz unitaria —Dickey-Fuller aumentada (ADF),
Phillips-Perron y KPSS— complementadas con el test de Zivot-Andrews para quiebres
estructurales endógenos, y sus análogos de panel (Im-Pesaran-Shin, CIPS de Pesaran). La
conclusión sobre el orden de integración de cada serie determina la especificación posterior:
las variables I(0) ingresan en nivel a los modelos de impacto; las I(1) se diferencian para
dichos modelos y se conservan en nivel para el análisis de cointegración.

### 3.6.2 Modelo de impacto: panel de efectos fijos (OE2)
La sensibilidad de los retornos a los factores macro-financieros se estima mediante un
modelo de **datos de panel con efectos fijos por empresa**:
$$rᵢₜ = αᵢ + β₁ Δcobreₜ + β₂ ΔTCₜ + β₃ Δtasaₜ + β₄ ΔVIXₜ + γ′ Xᵢₜ + εᵢₜ$$
La inferencia emplea errores estándar de **Driscoll-Kraay**, robustos a heterocedasticidad,
autocorrelación y **dependencia de sección cruzada** —esta última esperable dado el factor
común que representa el precio del cobre—. Como especificación de referencia se estima en
paralelo un modelo de serie de tiempo sobre la cartera del sector con errores HAC
(Newey-West). El contraste de dominancia **global versus local** (H6) se realiza mediante
tests de Wald de significancia conjunta por bloque de regresores.

### 3.6.3 Relaciones de largo plazo: cointegración (OE3)
Sobre las variables en nivel I(1) se evalúa la existencia de relaciones de equilibrio de
largo plazo. El procedimiento principal es el **test de bordes ARDL** (Pesaran, Shin y Smith,
2001), por su flexibilidad ante regresores de distinto orden de integración, contrastado con
el test de **Johansen** sobre el subconjunto claramente I(1) y, a nivel de panel, con el test
de **Westerlund**. De verificarse cointegración, se estima un **modelo vectorial de corrección
de error (VECM)** de la forma

$$Δyₜ = α (β′ yₜ₋₁) + Σ Γᵢ Δyₜ₋ᵢ + μ + εₜ$$

donde yₜ agrupa las variables en nivel I(1), β′yₜ₋₁ es el término de corrección de error que
recoge la desviación respecto del equilibrio de largo plazo, α mide la velocidad con que cada
variable corrige dicha desviación, y Γᵢ captura la dinámica de corto plazo. Adicionalmente, dado
que las pruebas anteriores suponen una relación estable, se aplica el test de **Gregory-Hansen
(1996)**, que admite un quiebre estructural endógeno en la relación de cointegración, apropiado
para un sector sujeto a ciclos pronunciados del commodity.

### 3.6.4 Dinámica de shocks: VAR, impulso-respuesta y descomposición de varianza (OE4)
La respuesta dinámica de los retornos a perturbaciones macroeconómicas se analiza mediante un
modelo **VAR** de orden *p*, yₜ = c + Σᵢ Aᵢ yₜ₋ᵢ + uₜ, cuya representación de medias
móviles yₜ = μ + Σⱼ Φⱼ uₜ₋ⱼ permite computar las funciones impulso-respuesta. La
**descomposición de la varianza del error de pronóstico (FEVD)** a horizonte *h* mide la fracción
de la varianza del error de predicción de cada variable atribuible a cada shock estructural,
ωᵢ←ⱼ(h) = [Σₛ (eᵢ′ Θₛ eⱼ)²] / [Σₛ (eᵢ′ Θₛ Θₛ′ eᵢ)], donde Θ_s son
los coeficientes de impulso-respuesta ortogonalizados. La identificación de los shocks
estructurales se realiza por **descomposición de Cholesky**, con un ordenamiento de las
variables según su grado de exogeneidad —el precio del cobre, determinado en el mercado
global, se ordena primero, y la acción, como variable más endógena, al final—. Se reportan las
**funciones impulso-respuesta** y la **descomposición de la varianza del error de pronóstico**,
esta última como evidencia directa para la hipótesis de dominancia global (H6). La robustez de
las conclusiones a la identificación se verifica mediante reordenamientos e impulso-respuestas
generalizadas (Pesaran y Shin, 1998), así como con tests de causalidad de Granger.

### 3.6.5 Estabilidad por fases del ciclo (OE5)
La estabilidad de las relaciones se evalúa incorporando la fase del ciclo del cobre mediante
**términos de interacción** entre los factores y una variable indicadora de régimen, y
re-estimando los modelos por subperíodo. El término de interacción mide si la sensibilidad de
los retornos a cada factor —en particular al precio del cobre— difiere entre expansión y
contracción. Como análisis de robustez se considera un modelo de **cambio de régimen de
Markov** que detecta los estados de forma endógena.

### 3.6.6 Comparación entre mercados: triangulación (OE6)
La totalidad del análisis precedente (3.6.1 a 3.6.5) se ejecuta de forma paralela sobre las tres
muestras —cobre en el mercado global (B), cobre en el mercado chileno (A) y sector minero chileno
(C)—. La comparación sistemática de los coeficientes de sensibilidad, de la velocidad de ajuste
del mecanismo de corrección de error y de la descomposición de varianza entre muestras permite
contrastar si el mercado bursátil global incorpora los shocks macroeconómicos de manera más
rápida y completa que el mercado chileno (hipótesis H7). Esta comparación se sustenta en la
literatura sobre eficiencia informacional y segmentación de mercados, y constituye un aporte
distintivo del estudio. Los resultados se consolidan en una tabla comparativa única por muestra.

## 3.7 Validación de supuestos y robustez

Para cada familia de modelos se verifican los supuestos pertinentes: ausencia de
autocorrelación (Breusch-Godfrey, Ljung-Box) y de heterocedasticidad (con atención a efectos
ARCH, dada la naturaleza financiera de los retornos), dependencia de sección cruzada en el
panel (test CD de Pesaran), estabilidad del VAR (raíces dentro del círculo unitario) y
selección de rezagos por criterios de información.

El diseño contempla, además, una **batería ampliada de diagnósticos y de robustez de segunda
generación** que se reporta en el Capítulo 4: (i) pruebas de raíz unitaria en panel **CIPS**
(Pesaran, 2007), robustas a la dependencia de sección cruzada; (ii) cointegración con quiebre
estructural endógeno de **Gregory-Hansen (1996)**; (iii) modelación de la volatilidad asimétrica
mediante **GJR-GARCH** (efecto apalancamiento); (iv) funciones impulso-respuesta por **proyecciones
locales** (Jordà, 2005) como alternativa al VAR; (v) corrección por **pruebas múltiples**
(Benjamini-Hochberg) sobre los p-valores del panel; (vi) reporte de **magnitudes económicas**
mediante coeficientes estandarizados; (vii) una **prueba formal de igualdad de coeficientes entre
mercados** (interacciones factor × mercado) para contrastar la transmisión diferenciada; y (viii)
el **test de razón de varianzas** de Lo y MacKinlay (1988) para la hipótesis de paseo aleatorio. La
robustez se examina también mediante submuestras (pre/post 2008 y 2020), definiciones alternativas
de las variables y carteras equiponderada frente a ponderada por capitalización. El justificante de
la especificación de panel (efectos fijos frente a aleatorios) se discute en §4.2.

---

### Tabla 3.1 — Definición operativa de variables (resumen)

| Bloque | Variable | Proxy | Fuente | Frecuencia | Transformación |
|---|---|---|---|---|---|
| Dependiente | Retorno | Δlog precio ajustado | Yahoo Finance | Mensual | — |
| Global | Cobre | Precio LME/global | Cochilco / FRED | Mensual | Δlog |
| Global | Riesgo | VIX | FRED | Diaria→mensual | Δ |
| Global | Tasa externa | Fed Funds / 10Y | FRED | Mensual | Δ |
| Global | Control | WTI | FRED | Diaria→mensual | Δlog |
| Local | Tipo de cambio | USD/CLP | BCCh / FRED | Diaria→mensual | Δlog |
| Local | Tasa local | TPM | BCCh | Mensual | Δ |
| Local | Actividad | IMACEC | BCCh | Mensual | nivel/Δ |
| Local | Riesgo país | EMBI Chile | BCCh | Mensual | Δ |
| Empresa | Tamaño | log(cap. bursátil) | Mercado | Mensual | nivel |
| Empresa | Volatilidad | desv. móvil retornos | Calculada | Mensual | nivel |
| Empresa | Apalancamiento | Deuda/Patrimonio | CMF | Trimestral→mensual | ffill+rezago |
