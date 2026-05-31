# Guía de defensa de la tesis — preguntas difíciles y cómo responderlas

> Prepárate para que la comisión ataque tus **decisiones de diseño**, no tus cálculos. Abajo, las
> preguntas más probables con una respuesta sólida y honesta para cada una. Practícalas en voz alta.

## A. Sobre el diseño y el alcance

**P1. ¿Por qué solo el cobre y no toda la minería?**
> Porque el cobre es el commodity que define la economía chilena y concentra la exposición de
> ingresos del sector. La minería mixta (muestra C) la incluyo solo como *vehículo* del mercado
> local, controlando por el precio de cada commodity, justamente para aislar el efecto del cobre.

**P2. Con tan pocas empresas, ¿es válido un panel?**
> Por eso uso un **diseño de triangulación**: la muestra B (cinco empresas internacionales) da el
> panel principal; la muestra A (Pucobre) la trato como serie de tiempo; y reporto siempre la
> cartera del sector como baseline robusto. No descanso en un solo estimador. Además, el test
> **CD de Pesaran (24,5; p=0,000)** me obligó a usar errores Driscoll-Kraay, que corrigen la
> dependencia de sección cruzada propia de un N pequeño con shock común.

**P3. Antofagasta y BHP no cotizan en Chile. ¿No contradice el título?**
> No: el título dice "empresas de cobre **con exposición a Chile**", y la comparación entre el
> mercado internacional y el chileno es precisamente el aporte. La muestra A/C cubre el mercado
> chileno; la B, el internacional. La tensión está resuelta y declarada en la metodología.

**P4. ¿Por qué 2004–2024?**
> Para cubrir al menos un ciclo completo del cobre (súper-ciclo 2004–2011, corrección, COVID,
> alza de tasas 2022) y disponer de ~250 observaciones mensuales, suficientes para VAR/VECM/ARDL.

## B. Sobre la econometría

**P5. ¿Por qué retornos y no precios?**
> Los precios son I(1) (lo confirmo con ADF/PP/KPSS y Zivot-Andrews); modelarlos en nivel daría
> regresiones espurias. Uso retornos I(0) para el impacto de corto plazo y reservo los niveles
> I(1) para la cointegración. Es la doble vía estándar.

**P6. El tipo de cambio dio "I(2)?" en su tabla. ¿Eso no invalida el VECM?**
> Fue un falso positivo de las pruebas convencionales por los quiebres del período. **Zivot-Andrews,
> que admite quiebre, confirma que el tipo de cambio es I(1)** (nivel no estacionario, p=0,95;
> diferencia estacionaria). El orden de integración está resuelto.

**P7. ARDL y Johansen daban resultados distintos sobre cointegración. ¿En qué quedamos?**
> Esa discrepancia era la pista. La prueba de **Gregory-Hansen confirma cointegración con un
> quiebre en junio de 2008** (ADF\* = −6,68 < −4,92). La relación de largo plazo existe pero se
> reconfiguró con la crisis financiera; por eso las pruebas sin quiebre la veían débil. Es un
> hallazgo, no una inconsistencia.

**P8. ¿Cómo identifica los shocks en el VAR? El orden de Cholesky es arbitrario.**
> Lo ordeno por **exogeneidad económica**: el precio del cobre, fijado en el mercado global, va
> primero —es plausible que sea exógeno a una empresa chilena—; la acción, la más endógena, al
> final. Y reporto robustez con impulso-respuestas generalizadas (Pesaran-Shin), invariantes al
> orden. La conclusión sobre dominancia global no depende del ordenamiento.

**P9. ¿No hay endogeneidad entre tipo de cambio, tasas y retornos?**
> El cobre es plausiblemente exógeno a una empresa individual (buena identificación). Para TC y
> tasas locales reconozco posible simultaneidad; por eso el análisis dinámico va por VAR (todas
> endógenas) y no solo por regresión. Es una limitación declarada.

**P10. El signo del tipo de cambio (−1,57) es muy grande. ¿Lo cree?**
> Es economicamente coherente: para empresas que valoran en dólares, la depreciación del peso
> suele coincidir con aversión al riesgo y caída del cobre, así que el coeficiente capta el canal
> de riesgo además del de competitividad. La magnitud se afinará con el EMBI y los controles de
> empresa, que hoy faltan.

## C. Sobre los resultados y su estatus

**P11. Usted mismo dice que los resultados son "preliminares". ¿Entonces qué defiende?**
> Defiendo un **marco completo, reproducible y ya ejecutado** cuyo grueso es concluyente
> (estacionariedad, panel con diagnósticos, cointegración con quiebre, VAR/IRF/FEVD, GARCH,
> robustez). Lo "preliminar" se reduce a dos adiciones —EMBI y controles de empresa— que afinarán
> magnitudes, no a un vacío metodológico.

**P12. ¿Cuál es el hallazgo memorable, en una frase?**
> Que el **mismo cobre se precia de forma comparable en distintos mercados, pero el mercado
> internacional incorpora algo más completamente los shocks globales**, y que la relación de largo
> plazo del sector con el cobre **se quebró con la crisis de 2008**.

**P13. ¿Qué aporta que no estuviera ya en la literatura?**
> La literatura macro→retornos se concentra en mercados desarrollados e índices agregados, y la de
> commodity→equity en energía. Aquí está el **cobre**, a nivel de **empresas con exposición a
> Chile**, con una **comparación explícita de mercados** y análisis por **fase del ciclo** —una
> combinación no documentada para el caso chileno.

## D. Preguntas trampa frecuentes
- *"¿Por qué no usó machine learning?"* → Porque el objetivo es **explicar y medir impacto**, no
  predecir; la econometría ofrece inferencia y interpretabilidad que un modelo de caja negra no da.
- *"¿Su R² es bajo (0,24)."* → Es lo esperable en retornos mensuales; el interés está en el **signo,
  la significancia y la descomposición de varianza**, no en el ajuste predictivo.
- *"¿Sobreajustó con tantas variables?"* → No: prioricé un set parsimonioso, controlé
  multicolinealidad (VIF) y la robustez por subperíodos confirma estabilidad.

## E. Checklist el día de la defensa
- [ ] Una frase de apertura con el aporte (P12).
- [ ] Dominar la lógica I(0)/I(1) → qué modelo para qué pregunta.
- [ ] Tener a mano: CD-Pesaran, Gregory-Hansen (quiebre 2008), FEVD global vs local.
- [ ] Reconocer las limitaciones **antes** de que las pregunten (genera credibilidad).
- [ ] Practicar la diapositiva de la triangulación: es tu diferenciador.
