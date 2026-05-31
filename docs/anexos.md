# Anexos

> Tablas generadas automáticamente a partir de los datos reales del proyecto (`python -m src.full_tables`). Reproducibles desde el repositorio.

## Anexo A. Estadística descriptiva

| Serie | Media | Desv. | Asimetría | Curtosis | Mín | Máx | N |
|---|---|---|---|---|---|---|---|
| Cartera B | 0.0068 | 0.1072 | -0.3391 | 1.8418 | -0.4371 | 0.3894 | 251.0000 |
| Pucobre (A) | 0.0065 | 0.0807 | 0.3730 | 4.5009 | -0.3711 | 0.3300 | 251.0000 |
| Cartera C | 0.0084 | 0.0671 | -0.3588 | 0.9823 | -0.2302 | 0.2005 | 251.0000 |
| Δ Cobre | 0.0052 | 0.0652 | -0.7737 | 5.4469 | -0.3542 | 0.2298 | 251.0000 |
| Δ VIX | 0.0029 | 5.1869 | 0.4442 | 3.6313 | -19.3900 | 21.2700 | 251.0000 |
| Δ Fed Funds | 0.0139 | 0.1746 | -1.5083 | 11.1211 | -0.9600 | 0.7000 | 251.0000 |
| Δ Treasury 10Y | 0.0017 | 0.2521 | -0.1802 | 1.1698 | -1.0800 | 0.6800 | 251.0000 |
| Δ TC CLP | -0.0005 | 0.0106 | 0.6460 | 2.5948 | -0.0347 | 0.0415 | 251.0000 |
| Δ Tasa local | 0.0100 | 0.3887 | -1.3252 | 8.9593 | -2.3100 | 1.1824 | 225.0000 |
| Δ Actividad local | 0.0010 | 0.0207 | 0.1473 | 3.9632 | -0.0965 | 0.1045 | 242.0000 |

## Anexo B. Matriz de correlación de los factores

|  | Retorno cartera | Δ Cobre | Δ VIX | Δ Fed Funds | Δ Treasury 10Y | Δ TC CLP | Δ Tasa local | Δ Actividad local |
|---|---|---|---|---|---|---|---|---|
| Retorno cartera | 1.0000 | 0.3962 | -0.4199 | 0.0301 | 0.1167 | -0.2938 | -0.0938 | -0.0623 |
| Δ Cobre | 0.3962 | 1.0000 | -0.0451 | 0.0495 | 0.1716 | -0.2339 | -0.0971 | 0.0276 |
| Δ VIX | -0.4199 | -0.0451 | 1.0000 | -0.0009 | -0.0659 | 0.1781 | 0.0879 | -0.0537 |
| Δ Fed Funds | 0.0301 | 0.0495 | -0.0009 | 1.0000 | 0.1536 | 0.1096 | 0.1630 | 0.0412 |
| Δ Treasury 10Y | 0.1167 | 0.1716 | -0.0659 | 0.1536 | 1.0000 | 0.1634 | -0.0154 | -0.0395 |
| Δ TC CLP | -0.2938 | -0.2339 | 0.1781 | 0.1096 | 0.1634 | 1.0000 | 0.0010 | -0.0649 |
| Δ Tasa local | -0.0938 | -0.0971 | 0.0879 | 0.1630 | -0.0154 | 0.0010 | 1.0000 | 0.0547 |
| Δ Actividad local | -0.0623 | 0.0276 | -0.0537 | 0.0412 | -0.0395 | -0.0649 | 0.0547 | 1.0000 |

## Anexo C. Pruebas de raíz unitaria y orden de integración

| Variable | ADF (p) | PP (p) | KPSS (p) | Zivot-A. (p) | Orden |
|---|---|---|---|---|---|
| Cobre (log nivel) | 0.0135 | 0.0277 | 0.0120 | 0.1697 | I(1) |
| TC CLP (log nivel) | 0.1584 | 0.2622 | 0.0100 | 0.9504 | I(2)?/revisar |
| VIX (nivel) | 0.0000 | 0.0000 | 0.1000 | 0.0009 | I(0) |
| Valor ANTO.L (log) | 0.1851 | 0.3084 | 0.0100 | 0.4233 | I(1) |

*Nota:* la clasificación automática marca el tipo de cambio como dudoso por la pérdida de potencia de las pruebas ante quiebres; la prueba de Zivot-Andrews lo resuelve como **I(1)** (véase la sección de resultados). VIX resulta I(0).


## Anexo D. Resultados completos del modelo de panel

### D.1 Muestra B — cobre, mercado internacional

| Regresor | Coef. | Error est. | t | p-valor |
|---|---|---|---|---|
| Constante | 0.0063 | 0.0053 | 1.1929 | 0.2332 |
| Δ Cobre | 0.5712 | 0.1082 | 5.2802 | 0.0000 |
| Δ VIX | -0.0077 | 0.0014 | -5.4813 | 0.0000 |
| Δ Fed Funds | 0.0196 | 0.0208 | 0.9447 | 0.3450 |
| Δ Treasury 10Y | 0.0226 | 0.0256 | 0.8851 | 0.3763 |
| Δ TC CLP | -1.5735 | 0.4011 | -3.9228 | 0.0001 |
| Δ Tasa local | -0.0073 | 0.0167 | -0.4371 | 0.6621 |
| Δ Actividad local | -0.5231 | 0.2946 | -1.7754 | 0.0761 |

N = 1080; R² = 0.2446; empresas = 5.

### D.2 Muestra A — cobre, mercado chileno (Pucobre)

| Regresor | Coef. | Error est. | t | p-valor |
|---|---|---|---|---|
| Constante | 0.0024 | 0.0038 | 0.6179 | 0.5367 |
| Δ Cobre | 0.6308 | 0.0851 | 7.4143 | 0.0000 |
| Δ VIX | -0.0034 | 0.0009 | -3.7113 | 0.0002 |
| Δ Fed Funds | -0.0025 | 0.0232 | -0.1100 | 0.9124 |
| Δ Treasury 10Y | 0.0467 | 0.0159 | 2.9308 | 0.0034 |
| Δ TC CLP | 0.1041 | 0.3186 | 0.3267 | 0.7439 |
| Δ Tasa local | -0.0034 | 0.0153 | -0.2254 | 0.8217 |
| Δ Actividad local | 0.2122 | 0.2660 | 0.7976 | 0.4251 |

N = 216; R² = 0.3305; empresas = 1.

### D.3 Muestra C — sector minero, mercado chileno

| Regresor | Coef. | Error est. | t | p-valor |
|---|---|---|---|---|
| Constante | 0.0071 | 0.0044 | 1.6123 | 0.1073 |
| Δ Cobre | 0.4185 | 0.0669 | 6.2597 | 0.0000 |
| Δ VIX | -0.0034 | 0.0008 | -3.9640 | 0.0001 |
| Δ Fed Funds | 0.0153 | 0.0269 | 0.5680 | 0.5702 |
| Δ Treasury 10Y | 0.0346 | 0.0180 | 1.9229 | 0.0548 |
| Δ TC CLP | -0.6474 | 0.3140 | -2.0620 | 0.0395 |
| Δ Tasa local | 0.0096 | 0.0106 | 0.9062 | 0.3651 |
| Δ Actividad local | -0.0784 | 0.1577 | -0.4970 | 0.6193 |

N = 864; R² = 0.1132; empresas = 4.

## Anexo E. Cointegración (test de Johansen)

| Rango | Traza | VC 95% | Máx-Eig | VC 95% (ME) | Cointegra |
|---|---|---|---|---|---|
| r<=0 | 32.1032 | 29.7961 | 23.0885 | 21.1314 | 1.0000 |
| r<=1 | 9.0147 | 15.4943 | 7.0567 | 14.2639 | 0.0000 |
| r<=2 | 1.9580 | 3.8415 | 1.9580 | 3.8415 | 0.0000 |

## Anexo F. Descomposición de varianza (FEVD) por horizonte — muestra B

| Horizonte | Δ Cobre | Δ VIX | Δ TC CLP | Δ Tasa local | Retorno cartera |
|---|---|---|---|---|---|
| h = 1 | 0.1821 | 0.1493 | 0.0229 | 0.0008 | 0.6449 |
| h = 6 | 0.1802 | 0.1405 | 0.0222 | 0.0284 | 0.6287 |
| h = 12 | 0.1798 | 0.1401 | 0.0222 | 0.0308 | 0.6271 |
| h = 24 | 0.1798 | 0.1401 | 0.0222 | 0.0308 | 0.6271 |

## Anexo G. Fuentes de datos

| Variable | Fuente | Código/Ticker | Frecuencia |
|---|---|---|---|
| Precio del cobre | FRED (OCDE) | PCOPPUSDM | Mensual |
| VIX | FRED / CBOE | VIXCLS | Diaria |
| Fed Funds | FRED | FEDFUNDS | Mensual |
| Treasury 10Y | FRED | DGS10 | Diaria |
| Tipo de cambio CLP | FRED | DEXCHUS | Diaria |
| Tasa local (proxy TPM) | FRED (OCDE) | IR3TIB01CLM156N | Mensual |
| Actividad local (proxy IMACEC) | FRED (OCDE) | CHLPROINDMISMEI | Mensual |
| Acciones (B) | Yahoo Finance | ANTO.L, BHP, AAL.L, LUN.TO, TECK | Diaria |
| Acciones (A, C) | Yahoo Finance | PUCOBRE.SN, CAP.SN, SQM-B.SN, MOLYMET.SN | Diaria |
| EMBI Chile (pendiente) | Banco Central de Chile | — | Diaria |


## Anexo H. Disponibilidad del código

Todo el código de adquisición, transformación, estimación y generación de figuras y tablas está disponible en el repositorio público del proyecto, organizado en módulos reproducibles (`src/`) y cuadernos Jupyter (`notebooks/`). Cada resultado de esta tesis puede regenerarse ejecutando los scripts correspondientes.


## Anexo J. Síntesis de pruebas de diagnóstico y robustez

La siguiente tabla consolida el conjunto de pruebas de diagnóstico y robustez ejecutadas, todas sobre datos reales y reproducibles desde el repositorio.

| Prueba | Resultado | Conclusión |
|---|---|---|
| Dependencia de sección cruzada (CD de Pesaran) | CD = 24.5049, p = 0.0 | Dependencia significativa → errores Driscoll-Kraay |
| Raíz unitaria en panel (CIPS, Pesaran 2007) | log-precios I(1); retornos I(0) | Confirma la doble vía, robusto a dependencia cruzada |
| Raíz unitaria con quiebre (Zivot-Andrews) | TC nivel p = 0.9504 | Tipo de cambio confirmado I(1) |
| Cointegración con quiebre (Gregory-Hansen) | ADF* = -6.6825 < -4.92; quiebre 2008-06 | Relación de largo plazo confirmada (reconfigurada en 2008) |
| Estabilidad del VAR y causalidad de Granger | estable = True; Granger cobre→retorno p = 0.0026 | Sistema válido; el cobre antecede al retorno |
| Corrección por pruebas múltiples (FDR) | sig.: Cobre, VIX, TC CLP | Los hallazgos centrales no son falsos positivos |
| Volatilidad asimétrica (GJR-GARCH) | γ = 0.2208, p = 0.0233 | Efecto apalancamiento significativo |
| Estabilidad por fase del ciclo (interacción) | cobre×exp p = 0.6267 | Sensibilidad estable entre regímenes |
| Robustez por subperíodos | β cobre 0.5594 → 0.7509 | Efecto estable, se intensifica tras 2020 |
| Igualdad de coeficientes entre mercados (H7) | d_cobre×global = +0,25 (p = 0,01) | Mayor sensibilidad en el mercado internacional |
| Razón de varianzas (Lo-MacKinlay) | cartera: no rechaza paseo aleatorio | Eficiencia débil del lado accionario |
| Local Projections (Jordà) | respuesta positiva al impacto | Cross-valida la IRF del VAR |


## Anexo I. Extensión predictiva: ¿explican o anticipan?

Como complemento a la naturaleza explicativa de la tesis, se evaluó la capacidad **predictiva** fuera de muestra de los factores macroeconómicos sobre el retorno mensual del cobre (a un mes), comparando un baseline ingenuo, un AR(1), un modelo lineal regularizado (Ridge) y dos modelos no lineales (Random Forest, Gradient Boosting), con división temporal 180/61 (entrenamiento/prueba).

| Modelo | R² fuera de muestra | Acierto direccional | RMSE | MAE |
|---|---|---|---|---|
| Random walk (0) | -0.016 | 0% | 0.0500 | 0.0372 |
| AR(1) | +0.056 | 64% | 0.0482 | 0.0357 |
| Ridge (lineal) | -0.117 | 54% | 0.0525 | 0.0388 |
| Random Forest | +0.033 | 56% | 0.0488 | 0.0361 |
| Gradient Boosting | -0.167 | 54% | 0.0536 | 0.0399 |

El **R² fuera de muestra es cercano a cero o negativo** en todos los modelos: los factores macroeconómicos **explican** el retorno contemporáneo del cobre (Capítulo 4) pero apenas lo **anticipan** a un mes. Este resultado, lejos de ser una debilidad, **refuerza la hipótesis de eficiencia de mercado en su forma débil** y justifica el enfoque explicativo —y no predictivo— adoptado. El mejor desempeño direccional corresponde al término de momentum (AR(1)). Una versión interactiva de este modelo se encuentra en la plataforma web del proyecto.

Como contraste complementario de la hipótesis de paseo aleatorio se aplica el test de razón de varianzas de Lo y MacKinlay (1988), con estadístico robusto a heterocedasticidad. Para el **precio del cobre** se rechaza el paseo aleatorio (VR(2) = 1.39; z = 2.99), evidencia de **momentum** propia de los mercados de commodities. En cambio, para los **retornos del sector** el paseo aleatorio **no se rechaza** (VR(2) = 1.10; z = 1.06), lo que es consistente con la eficiencia de mercado en forma débil del lado accionario y con la escasa predecibilidad documentada arriba.
