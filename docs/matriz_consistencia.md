# Matriz de consistencia

**Tesis:** Impacto de las variables macroeconómicas globales y financieras en la valoración bursátil del sector de minería de cobre en Chile.

**Objetivo general:** Cuantificar el impacto de las variables macroeconómicas globales y nacionales, y de los indicadores financieros de mercado y de empresa, sobre los retornos accionarios de las empresas de minería de cobre con exposición a Chile durante el período 2004–2024, evaluando la estabilidad de dichas relaciones a lo largo de las distintas fases del ciclo del precio del cobre, mediante modelos econométricos de series de tiempo y datos de panel.

---

## 1. Matriz principal (Objetivo específico → Pregunta → Hipótesis → Método → Prueba)

| OE | Objetivo específico | Pregunta (PI) | Hipótesis | Variables principales | Método / Modelo | Prueba estadística clave | Resultado esperado (contraste) |
|----|--------------------|----------------|-----------|----------------------|-----------------|--------------------------|-------------------------------|
| **OE1** | Caracterizar las propiedades estadísticas de las series (estacionariedad, volatilidad, quiebres). | — (transversal) | — | Retornos; niveles de cobre, TC, tasas, VIX, IMACEC. | EDA + raíz unitaria. | ADF, Phillips-Perron, KPSS, Zivot-Andrews, IPS/CIPS (panel). | Retornos I(0); precios/TC I(1). Define la estrategia OE2–OE4. |
| **OE2** | Estimar la sensibilidad de los retornos a las variables macro-financieras, distinguiendo factores globales vs locales. | PI1, PI2 | H1, H2, H3, H4, H6 | **Dep:** retorno log. **Indep:** Δcobre, ΔTC, Δtasa, ΔVIX, controles de empresa. | Serie de tiempo (cartera) como baseline + **Panel FE con Driscoll-Kraay**. | t/F sobre coeficientes; Wald conjunto por bloque (global vs local); Hausman; CD-Pesaran. | Signos H1(+), H2(±), H3(−), H4(−) significativos; bloque global ≳ local. |
| **OE3** | Determinar relaciones de equilibrio de largo plazo y dinámicas de corto plazo. | PI3 | H5 | Niveles I(1): valor cartera, cobre, TC, tasa. | **ARDL bounds** (principal) + **Johansen** (robustez) + **Westerlund** (panel) → **VECM**. | Test de bordes (F-bounds); traza/máx. autovalor; α (velocidad de ajuste). | ≥1 vector de cointegración; ECM con α<0 significativo. |
| **OE4** | Cuantificar la respuesta dinámica de los retornos ante shocks macro. | PI4 | H1, H6 | Sistema {cobre, VIX/Fed, TC, tasa, retorno}. | **VAR** (o **VECM** si cointegran) sobre la cartera. | Funciones impulso-respuesta (IRF); descomposición de varianza (FEVD); causalidad de Granger. | Respuesta positiva y persistente al shock de cobre; FEVD: cobre/global dominan. |
| **OE5** | Evaluar la estabilidad de las relaciones a lo largo de las fases del ciclo del cobre. | PI5 | H1–H4 condicionadas al régimen | + dummy/interacción de fase del ciclo. | **Fechado BBQ** del cobre + interacciones; re-estimación por subperíodo; (robustez: Markov-switching). | Significancia de términos de interacción; comparación de IRF entre fases; tests de quiebre (Bai-Perron, Chow). | Sensibilidad al cobre mayor en expansión vs contracción (asimetría de régimen). |

---

## 2. Preguntas de investigación (texto completo)

- **PI1 (→OE2):** ¿Qué variables macroeconómicas globales y nacionales explican significativamente los retornos del sector cobre en Chile, y cuál es su magnitud y signo?
- **PI2 (→OE2):** ¿Predominan los factores globales (cobre, riesgo internacional, tasas externas) o los locales (TC, actividad e interés domésticos)?
- **PI3 (→OE3):** ¿Existe relación de largo plazo (cointegración) entre la valoración del sector y sus determinantes macro? ¿A qué velocidad se corrige una desviación?
- **PI4 (→OE4):** Ante un shock en el precio del cobre o el tipo de cambio, ¿cómo y por cuánto tiempo responden los retornos?
- **PI5 (→OE5):** ¿Son estables estas relaciones o cambian según la fase del ciclo del cobre?
- **PI6 (→OE6, triangulación):** ¿Difiere la sensibilidad de los retornos al precio del cobre y a las variables macro entre las empresas que cotizan en el **mercado global** (muestra B) y las que cotizan en el **mercado chileno** (muestras A y C)?

## 3. Hipótesis (texto completo y sustento)

| H | Enunciado | Signo esperado | Sustento teórico |
|---|-----------|----------------|------------------|
| **H1** | El precio del cobre afecta positivamente los retornos del sector. | + | Canal de ingresos; el cobre es el principal *driver* de flujos. |
| **H2** | La depreciación del peso (↑USD/CLP) afecta los retornos de productoras con ingresos en USD. | ± (a determinar) | Canal de competitividad/márgenes; signo depende de bolsa y estructura de costos. |
| **H3** | Un alza de tasas (local y/o externa) afecta negativamente los retornos. | − | Canal de descuento y apetito por riesgo. |
| **H4** | Un aumento del riesgo/aversión global (VIX, EMBI) afecta negativamente los retornos. | − | *Flight to quality*; activos cíclicos y emergentes. |
| **H5** | Existe cointegración entre el valor del sector y {cobre, TC, tasa}, con ECM significativo. | — | Relación de equilibrio de largo plazo. |
| **H6** | Los factores globales explican mayor fracción de la varianza de los retornos que los locales. | global > local | Economía pequeña, abierta y exportadora de commodity. |
| **H7** | El **mercado global** (muestra B) incorpora el shock del cobre de forma más rápida y completa que el **mercado chileno** (muestras A/C). | global > local en velocidad/magnitud | Menor profundidad y liquidez del mercado local → transmisión más lenta/parcial (eficiencia informacional, segmentación de mercados). |

## 3bis. Dimensión transversal: triangulación por muestras

Todo el análisis (OE2–OE5) se ejecuta en paralelo sobre **tres muestras** y se compara:

| Muestra | Definición | Empresas | Método principal |
|---|---|---|---|
| **B** | Cobre puro, mercado global, operación en Chile | ANTO.L, BHP, AAL.L, LUN.TO, TECK | Panel FE + Driscoll-Kraay |
| **A** | Cobre puro, mercado chileno | PUCOBRE.SN | Serie de tiempo (ARDL, VAR/IRF) |
| **C** | Sector minero chileno | PUCOBRE, CAP, SQM-B, MOLYMET | Panel FE + Driscoll-Kraay |

**OE6 (nuevo):** Comparar la transmisión del impacto macro entre el mercado global y el chileno
(contrasta PI6/H7). En la muestra C se controla por el precio propio de cada commodity.

## 4. Trazabilidad capítulo ↔ objetivo

| Sección de resultados (Cap. 4) | Objetivo | Hipótesis contrastadas |
|---|---|---|
| 4.1 Descriptivo y propiedades de series | OE1 | — |
| 4.2 Determinantes: global vs local | OE2 | H1, H2, H3, H4, H6 |
| 4.3 Largo plazo y corrección de error | OE3 | H5 |
| 4.4 Respuesta dinámica a shocks | OE4 | H1, H6 |
| 4.5 Estabilidad por fases del ciclo | OE5 | H1–H4 (condicionadas) |
| 4.6 Comparación entre mercados (global vs chileno) | OE6 | PI6, H7 |

> **Regla de oro de coherencia:** ningún objetivo sin su sección de resultados; ninguna hipótesis sin su prueba; ninguna variable sin su fuente (ver `src/config.py`).

## 5. Veredicto empírico (síntesis)

Resultado del contraste de cada hipótesis sobre los datos (preliminar en cuanto a magnitudes; ver Cap. 4).

| H | Veredicto | Evidencia / prueba |
|---|-----------|--------------------|
| **H1** | Respaldada | β cobre +0,57\*\*\*; robusta a corrección FDR y a subperíodos (0,56→0,75). |
| **H2** | Respaldada (signo −) | ΔTC −1,57\*\*\*; capta competitividad y riesgo. |
| **H3** | No respaldada | Tasa local y externa no significativas en la especificación base. |
| **H4** | Respaldada | VIX negativo y significativo; mayor efecto estandarizado (−0,31 σ). |
| **H5** | Respaldada con quiebre | Gregory-Hansen: cointegración con quiebre en 2008 (ADF\* = −6,68). |
| **H6** | Respaldada | FEVD: global ≈ 32% vs local ≈ 5%; jerarquía de betas estandarizados. |
| **H7** | Respaldada | Interacción d_cobre × global = +0,25 (p = 0,01); mayor sensibilidad internacional. |

**Diagnósticos de soporte:** CD-Pesaran (dependencia cruzada → Driscoll-Kraay); CIPS (precios I(1),
retornos I(0)); estabilidad del VAR y Granger; GJR-GARCH (apalancamiento); Local Projections
(cross-validación de la IRF); razón de varianzas de Lo-MacKinlay (eficiencia débil accionaria). La
síntesis completa figura en el Anexo J.
