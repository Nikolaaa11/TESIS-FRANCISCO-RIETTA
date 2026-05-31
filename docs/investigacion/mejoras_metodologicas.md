# Mejoras metodológicas para tesis de nota máxima

**Tesis:** *Impacto de las variables macroeconómicas en los retornos accionarios de las empresas de cobre con exposición a Chile: una comparación entre el mercado bursátil internacional y el chileno, 2004–2024.*

Documento de asesoría metodológica. Sintetiza (1) qué caracteriza a una tesis de magíster de nota máxima en finanzas/econometría empírica según rúbricas universitarias reales, (2) mejoras concretas priorizadas que elevarían esta tesis, y (3) errores comunes que bajan la nota. Última actualización: 2026-05-31.

---

## 1. Qué caracteriza a una tesis de NOTA MÁXIMA (rúbricas reales)

Las rúbricas convergen en cinco ejes. Síntesis a partir de guías universitarias publicadas:

| Eje | Qué exige el nivel sobresaliente (A / >85%) |
|---|---|
| **Pregunta y aporte** | Pregunta clara que "busca ampliar el estado del conocimiento"; gap explícito; contribución delimitada y honesta (no sobre-vendida). |
| **Teoría y método** | Conocimiento de las teorías y métodos relevantes y **buen juicio en la elección**; diseño de investigación descrito de forma clara y objetiva; método aplicado de forma "apropiada y convincente". |
| **Análisis y resultados** | Ejecución técnicamente correcta; conclusiones apropiadas que identifican los hallazgos clave; **reflexión crítica sobre supuestos y limitaciones**. |
| **Rigor y reproducibilidad** | Diseño, ejecución, análisis e interpretación sin fallos fundamentales; transparencia que permita replicar (datos, código, semillas, versiones). |
| **Redacción e integridad** | Argumentación efectiva, texto legible, ética de investigación y citación correcta. |

Fuentes:
- NHH (Norwegian School of Economics), *Assessment criteria for the Master Thesis* — https://www.nhh.no/en/for-students/masters-thesis/assessment-criteria/
- University of the Free State, *Rubric Masters Dissertation* (criterios para puntajes >85%) — https://www.ufs.ac.za/docs/default-source/regulations-documents/rubric-masters-dissertation-1004-eng.pdf
- University of Twente (EST), *Master's Thesis Rubric and Grading Form* — https://www.utwente.nl/en/est/masterest/final-project-trajectory-started-in-2025-2026/assessment-form-and-rubric-final-project-est.pdf
- NIH rigor & reproducibility: Lithgow et al., *Rigor Me This* — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9283916/
- Reproducibilidad/robustez en economía empírica: Lusher et al. (Nature) — https://lrlusher.weebly.com/uploads/1/0/0/4/10048967/meta_paper_i__nature_v2___4_.pdf

**Lectura para esta tesis:** la suite econométrica ya es ambiciosa (cubre el eje "teoría y método" con holgura). Donde se gana o se pierde la nota máxima es en los ejes **rigor/identificación**, **reproducibilidad** y **reflexión crítica** — precisamente donde concentro las recomendaciones de la sección 2.

---

## 2. Mejoras priorizadas y accionables

Leyenda de estado: ✅ ya cubierto · 🟡 parcial / a reforzar · ❌ falta.

### Prioridad ALTA — alto impacto, implementable en Python (statsmodels/linearmodels/arch)

#### 2.1 ❌ Local Projections (Jordà 2005) como IRF alternativa al VAR/VECM
La comisión valora ver que las IRF no dependen de una sola tecnología. Las LP se estiman por OLS horizonte a horizonte, son **más robustas a mala especificación** (no propagan el error de lags al iterar hacia adelante) y permiten bandas analíticas simples. Úsalas como **chequeo de robustez de tus IRF del VAR**: si la forma y el signo coinciden, tu narrativa se blinda.
- Implementación: para cada horizonte `h`, regresión `ret_{t+h} = α + β_h · shock_t + controles_{t-1} + Σ lags + ε`, con HAC/Newey-West. `statsmodels.OLS` + `cov_type='HAC'`. Graficar `β_h` con IC 90/95%.
- LP no lineales por estado del ciclo (interacción con tu dummy expansión/contracción BBQ) refuerzan directamente OE5 — es el "state-dependent LP" que impresiona.
- Refs: Jordà (2005, AER) — https://www.aeaweb.org/articles?id=10.1257/0002828053828518 ; Montiel Olea et al., *Local Projections or VARs? A Primer* — https://arxiv.org/pdf/2503.17144 ; Plagborg-Møller & Wolf, *LP and VARs Estimate the Same IRF* — https://www.mikkelpm.com/files/lp_var.pdf

#### 2.2 🟡 Inferencia robusta con pocos clusters / pocas series (wild cluster bootstrap)
Tus paneles tienen **N pequeño** (B=5, C=4 empresas). Driscoll-Kraay es correcto para dependencia cross-sectional, pero su validez descansa en **T grande y número de unidades razonable**; con N=4–5 el clustering asintótico es frágil. Reporta además **wild cluster bootstrap-t** (Cameron-Gelbach-Miller) como inferencia complementaria sobre los coeficientes macro clave. Si la significancia sobrevive, tienes un argumento muy fuerte; si no, lo reportas con honestidad (eso sube nota, no la baja).
- Implementación: bootstrap manual con remuestreo de signos de Rademacher por cluster (empresa), o vía `wildboottest` (paquete Python `wildboottest`). Complementa, no reemplaza, a Driscoll-Kraay.
- Refs: Hoechle (2007), *Robust SE for panel regressions with cross-sectional dependence* (xtscc) — https://journals.sagepub.com/doi/pdf/10.1177/1536867X0700700301 ; literatura wild bootstrap pocos clusters — https://arxiv.org/pdf/2301.04522

#### 2.3 ❌ Corrección por pruebas múltiples (FWER/FDR)
Estimas muchos coeficientes (varias macro × 3 muestras × subperíodos × fases del ciclo). Sin corregir, parte de los "***" pueden ser falsos positivos — un evaluador con ojo econométrico lo detecta. Aplica **Benjamini-Hochberg (FDR)** a la familia de p-valores de las hipótesis principales H1–H6, y reporta cuáles sobreviven. Es media página de código y demuestra madurez estadística.
- Implementación: `statsmodels.stats.multitest.multipletests(pvals, method='fdr_bh')`. Reportar p-valores crudos y ajustados lado a lado.
- Refs: NBER, *Hierarchical Multiple Testing in Empirical [Asset Pricing]* — https://www.nber.org/system/files/working_papers/w34050/w34050.pdf ; revisión FDR (Cai) — http://www-stat.wharton.upenn.edu/~tcai/paper/FDR-Review.pdf

#### 2.4 🟡 Fortalecer la identificación: de "impacto" a algo más causal
El diseño es explicativo (correcto para una tesis de medición), pero la comisión preguntará por endogeneidad/simultaneidad (¿el retorno del cobre causa el precio, o viceversa? ¿variables omitidas?). No necesitas un experimento, pero sí **blindar la interpretación**:
- **Sorpresas / componente no anticipado** en lugar de niveles: regresar retornos sobre la *innovación* macro (residuo de un AR o "surprise" = realizado − esperado) reduce el problema de simultaneidad y es el estándar en la literatura de news/announcement. La evidencia muestra respuestas de ~11–25 pb por 1 SD de sorpresa.
- **Predeterminación temporal:** usa controles rezagados (ya lo haces en VAR; hazlo explícito en panel).
- **Granger / exogeneidad por bloques** ya lo tienes (cobre→retorno F=9.1, p=0.003): preséntalo como evidencia de dirección, con la salvedad de que Granger ≠ causalidad estructural.
- Refs: respuesta de acciones a noticias macro — https://arxiv.org/pdf/2212.04525 ; anuncios macro y mercados — https://actacommercii.co.za/index.php/acta/article/view/1135/2106

#### 2.5 🟡 GARCH: ampliar a la familia asimétrica y vincularlo a la pregunta
Ya tienes GARCH(1,1). Para nota máxima, motiva el modelo con la pregunta (¿la transmisión del shock macro a la **volatilidad** difiere entre mercado global y chileno?) y compara contra **EGARCH / GJR-GARCH** para capturar apalancamiento (las malas noticias elevan más la volatilidad). Selección por AIC/BIC y test de signo de Engle-Ng. El paquete `arch` lo soporta nativamente.
- Implementación: `arch_model(y, vol='EGARCH'...)` y `o=1` para GJR; comparar log-lik/BIC y persistencia (α+β) entre muestras B vs A/C. Opcional: **GARCH-X** con la variable macro como regresor en la varianza, o **DCC** para correlación dinámica global↔local.

### Prioridad MEDIA — robustez y presentación que distinguen

#### 2.6 🟡 Batería de robustez sistemática (placebo, submuestras, especificaciones alternativas)
Una tabla de robustez bien armada es de lo que más mueve la nota. Faltan o conviene formalizar:
- **Submuestras / estabilidad temporal:** ya reportas 2004-19 vs 2020-24 (β cobre 0.56→0.75) y el quiebre 2008 (Gregory-Hansen). Conviértelo en una **tabla de robustez** explícita, no en texto suelto.
- **Placebo temporal:** reasignar el evento/quiebre a fechas falsas y verificar que el efecto desaparece.
- **Sensibilidad a la transformación:** retornos log vs simples; winsorización al 1% de outliers; con/sin COVID.
- **Especificaciones alternativas de SE:** OLS-robust vs cluster por empresa vs Driscoll-Kraay vs wild bootstrap, todas en una fila comparativa.
- **Sensibilidad a controles:** mostrar coeficiente clave con y sin precio de cada commodity (el control que ancla tu diseño de triangulación).
- Refs (robustez/reproducibilidad en econ empírica): https://lrlusher.weebly.com/uploads/1/0/0/4/10048967/meta_paper_i__nature_v2___4_.pdf

#### 2.7 ✅→🟡 Cointegración: cerrar el resultado "inconcluso" de H5
Tienes ARDL, Johansen y Gregory-Hansen (quiebre 2008) — cobertura excelente. El problema es que H5 quedó "inconcluso". Para nota máxima:
- Reporta los **bounds test** del ARDL (F y t) con sus valores críticos I(0)/I(1) y la conclusión explícita (cointegra / no / zona inconclusa).
- Si Pesaran indica cointegración, presenta el **ECM con velocidad de ajuste** (coef. del término de corrección de error, signo negativo y significativo = evidencia fuerte) e interprétalo económicamente.
- Triangula: si ARDL-bounds, Johansen-traza y Gregory-Hansen apuntan distinto, explica *por qué* (quiebre estructural, potencia de cada test). Convertir un "inconcluso" en una discusión razonada **sube la nota**.

#### 2.8 ❌ Diagnóstico de dependencia transversal y heterogeneidad de pendientes
Ya validaste dependencia cross-sectional con Pesaran CD (24.5, p≈0) — perfecto, justifica Driscoll-Kraay. Complementa con:
- **CIPS (Pesaran)**: raíz unitaria de segunda generación que es *robusta a dependencia transversal* (tus ADF/PP/KPSS son de primera generación y pueden fallar bajo CD). Refuerza tu sección de raíz unitaria.
- **Test de homogeneidad de pendientes (Pesaran-Yamagata)**: si las pendientes difieren entre empresas, el FE pooled puede sesgar; podrías necesitar **Mean Group / Pooled Mean Group (PMG)**, que además da la relación de largo plazo común — encaja perfecto con tu pregunta global vs local.

#### 2.9 🟡 Tamaños de efecto e interpretación económica, no solo estadística
La rúbrica premia "identificar los hallazgos clave". Para cada coeficiente importante reporta la **magnitud económica** (p. ej. "1 SD de sorpresa en TC ⇒ X pb de retorno mensual; equivale a Y% de la volatilidad mensual típica"), no solo el signo y los asteriscos. Estandariza variables (beta estandarizado) para comparar la *importancia relativa* de cada macro entre mercados — esto materializa tu H6/H7 (quién transmite más).

### Prioridad TRANSVERSAL — reproducibilidad (eje de rúbrica que muchos descuidan)

#### 2.10 🟡 Paquete de reproducibilidad
Es un criterio explícito de rigor y suele ser un diferenciador fácil:
- `requirements.txt` con **versiones fijadas** (ya consta el gotcha pandas 3.0 / pandas-datareader: documéntalo en el repo).
- **Semilla fija** en bootstraps/GARCH y registro de versiones de librerías.
- **Script maestro** que reproduce todas las tablas/figuras de punta a punta (ya tienes `build_thesis.py`, `full_tables.py`, `make_figures.py` — documenta el orden en un README).
- Anexo con **diccionario de variables y fuentes** (FRED IDs ya los tienes en memoria; EMBI del BCCh pendiente). Mapear cada serie a su fuente y transformación.
- Refs: criterios de transparencia/reproducibilidad — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9283916/

---

## 3. Errores comunes que BAJAN la nota (y cómo evitarlos aquí)

1. **Regresión espuria por no estacionariedad.** El error clásico: regresar series I(1) en niveles y celebrar R² altos y t grandes que son artefactos de tendencias comunes. *Mitigación en tu caso:* ya trabajas con retornos (estacionarios) y tienes batería ADF/PP/KPSS/Zivot-Andrews + cointegración para los niveles. Mantén la **regla**: niveles solo dentro de un marco de cointegración (VECM/ARDL); todo lo demás, en diferencias/retornos. Refs: Ventosa-Santaulària (2009) — https://www.hindawi.com/journals/jps/2009/802975/ ; Whelan, *Spurious Regressions and Cointegration* — https://www.karlwhelan.com/Teaching/MA%20Econometrics/part4.pdf

2. **Confundir cointegración con espuria.** Usar valores críticos DF normales para testear cointegración (los residuos parecen estacionarios aun cuando no lo son). *Mitigación:* usa los valores críticos correctos de Engle-Granger/Johansen/bounds — verifica que tu implementación los aplique. Ref Stata blog — https://blog.stata.com/2016/09/06/cointegration-or-spurious-regression/

3. **Ignorar el quiebre estructural en los tests de raíz unitaria.** Un ADF sin quiebre puede declarar I(1) algo que es estacionario alrededor de un quiebre (y viceversa). *Mitigación:* ya lo cubres con Zivot-Andrews (resolvió el falso "I(2)?" del TC) y Gregory-Hansen. Bien.

4. **Inferencia inválida por dependencia transversal / pocos clusters.** SE estándar subestimados ⇒ falsa significancia. *Mitigación:* Driscoll-Kraay (hecho) + wild bootstrap por el N pequeño (sección 2.2).

5. **p-hacking de facto por múltiples especificaciones sin corrección.** Reportar solo lo significativo entre decenas de pruebas. *Mitigación:* FDR (sección 2.3) y mostrar la **tabla completa** de especificaciones, no un cherry-pick.

6. **Sobre-interpretación causal.** Afirmar "X causa Y" desde Granger u OLS. *Mitigación:* lenguaje calibrado ("asociación", "transmisión", "respuesta condicional"), Granger presentado como precedencia temporal, y sorpresas para reducir simultaneidad (2.4).

7. **No reportar diagnósticos del modelo.** VAR sin test de estabilidad/autocorrelación de residuos; GARCH sin test de efectos ARCH remanentes; panel sin Hausman (FE vs RE) ni test de dependencia. *Mitigación:* tienes VAR estable y CD-Pesaran; añade Hausman explícito y Ljung-Box/ARCH-LM sobre residuos estandarizados del GARCH.

8. **Resultados sin magnitud económica ni límites.** Solo asteriscos, sin "cuánto" ni sección honesta de limitaciones. *Mitigación:* secciones 2.9 y la "reflexión crítica" que la rúbrica exige explícitamente.

---

## 4. Hoja de ruta sugerida (esfuerzo vs impacto)

| # | Mejora | Estado | Impacto | Esfuerzo | Herramienta |
|---|---|---|---|---|---|
| 2.3 | FDR (Benjamini-Hochberg) en H1–H6 | ❌ | Alto | Bajo | `statsmodels.stats.multitest` |
| 2.9 | Magnitudes económicas + betas estandarizados | 🟡 | Alto | Bajo | pandas |
| 2.6 | Tabla de robustez sistemática (submuestras/placebo/SE) | 🟡 | Alto | Medio | linearmodels/statsmodels |
| 2.2 | Wild cluster bootstrap (N pequeño) | 🟡 | Alto | Medio | `wildboottest` |
| 2.1 | Local Projections (IRF alternativa, + state-dependent) | ❌ | Alto | Medio | `statsmodels.OLS` HAC |
| 2.7 | Cerrar H5: bounds test + ECM interpretado | 🟡 | Alto | Bajo | statsmodels ARDL |
| 2.5 | EGARCH/GJR vs GARCH(1,1) + Engle-Ng | 🟡 | Medio | Bajo | `arch` |
| 2.8 | CIPS + Pesaran-Yamagata + (PMG) | ❌ | Medio | Medio | manual/`pmdarima`/custom |
| 2.10 | Paquete de reproducibilidad (semillas, versiones, README) | 🟡 | Medio | Bajo | repo |
| 2.4 | Sorpresas macro (componente no anticipado) | 🟡 | Alto | Medio | statsmodels AR |
