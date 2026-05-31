# Diseño de triangulación por tres muestras (decidido mayo 2026)

La aclaración "impacto de variables macro en acciones de **extracción de cobre** en el
**mercado chileno**" reveló una tensión de factibilidad: en la Bolsa de Santiago casi no hay
productoras de cobre puro cotizadas (las grandes son estatales o subsidiarias extranjeras).
La solución adoptada **convierte esa limitación en una fortaleza**: triangular el fenómeno
desde tres muestras complementarias, lo que habilita una pregunta nueva y más rica.

## La idea central

Comparar **cómo el mercado global y el mercado chileno precian el impacto macroeconómico**
sobre las mismas materias primas. Esto eleva la hipótesis global-vs-local (H6) de
"¿qué factores importan más?" a "¿**dónde** —en qué mercado— se transmite mejor el shock?".

## Las tres muestras (cobertura 2004-2024 verificada en Yahoo)

| Muestra | Definición | Empresas | N | Método principal | Rol |
|---|---|---|---|---|---|
| **B** | Cobre puro, **mercado global**, con operación en Chile | ANTO.L, BHP, AAL.L, LUN.TO, TECK | 5 | Panel FE + Driscoll-Kraay | Referencia "cobre puro" |
| **A** | Cobre puro, **mercado chileno** (Bolsa de Santiago) | PUCOBRE.SN | 1 | Serie de tiempo (ARDL, VAR/IRF) | Caso local puro |
| **C** | **Sector minero** chileno (Bolsa de Santiago) | PUCOBRE, CAP, SQM-B, MOLYMET | 4 | Panel FE + Driscoll-Kraay | Mercado local con N para panel |

> Muestra C mezcla commodities (cobre, hierro, litio, molibdeno): incluir el **precio propio de
> cada commodity** como control, de modo que el coeficiente del cobre quede bien identificado y,
> además, se pueda testear si el cobre afecta al sector minero local más allá de su propio metal.

## Foco y rol de cada muestra (definido)

**El objeto de estudio es el cobre.** Dado que en la Bolsa de Santiago el cobre puro cotizado se
reduce esencialmente a Pucobre, la **muestra C (sector minero local) actúa como *vehículo* del
mercado chileno**, no como objeto de estudio en sí: permite estimar con tamaño de sección cruzada
cómo el mercado local incorpora los shocks macro, controlando por el precio propio de cada
commodity para aislar el efecto del cobre. Así, la tesis mantiene su foco en el cobre sin renombrarse
a "minería".

## Objetivo general (definido)

> *Cuantificar y comparar el impacto de las variables macroeconómicas globales y nacionales sobre
> los retornos accionarios de las empresas de cobre con exposición a Chile durante 2004–2024,
> contrastando su transmisión entre el mercado bursátil internacional y el chileno, mediante
> modelos econométricos de series de tiempo y datos de panel.*

### Título (definido)
> *"Impacto de las variables macroeconómicas en los retornos accionarios de las empresas de cobre
> con exposición a Chile: una comparación entre el mercado bursátil internacional y el chileno,
> 2004–2024."*

## Pregunta e hipótesis adicionales que habilita

- **PI6 (nueva):** ¿Difiere la sensibilidad de los retornos al precio del cobre y a las
  variables macro entre las empresas que cotizan en el mercado global (B) y las que cotizan en
  el mercado chileno (A/C)?
- **H7 (nueva):** El mercado global incorpora el shock del cobre de forma más rápida y completa
  que el mercado chileno (menor profundidad/liquidez local → transmisión más lenta o parcial).
  *Contrastable comparando coeficientes, IRF y FEVD entre muestras.*

## Cómo se ejecuta (sin reescribir código)

El pipeline ya es paramétrico. Para cada muestra:
```python
from src import build_panel as bp
from src import config as C
# Muestra B / A / C respectivamente:
bp.construir(guardar=True, universo=C.UNIVERSO_PRINCIPAL)      # -> panel.parquet
bp.construir(guardar=True, universo=C.UNIVERSO_LOCAL_COBRE)    # (renombrar salida: _A)
bp.construir(guardar=True, universo=C.UNIVERSO_LOCAL_MINERIA)  # (renombrar salida: _C)
```
Luego se corren los mismos notebooks 02–06 sobre cada panel y se **comparan** los resultados en
una tabla única (coeficiente del cobre, velocidad de ajuste, FEVD global) por muestra.

> Pendiente menor de implementación: parametrizar el sufijo de salida en `build_panel.construir()`
> (p. ej. `sufijo='_B'`) para guardar `panel_B/A/C.parquet` sin pisarse. Trivial; lo hago cuando
> arranques esta etapa.

## Qué documentos hay que ajustar a este diseño

- [ ] `matriz_consistencia.md` — agregar PI6/H7 y la dimensión "muestra".
- [ ] `metodologia_capitulo3.md` §3.1 — describir las tres muestras.
- [ ] `marco_teorico_capitulo2.md` — agregar sub-bloque sobre integración/segmentación de
      mercados y velocidad de incorporación de información (eficiencia informacional).
- [ ] `introduccion_capitulo1.md` — reflejar la comparación de mercados en problema y aportes.
- [ ] Título de la tesis.
