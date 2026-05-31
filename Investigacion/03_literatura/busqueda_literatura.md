# Guía de búsqueda estructurada de literatura (bloque 2.4 — el aporte)

> Objetivo: cerrar la evidencia empírica **chilena** sobre cobre ↔ tipo de cambio ↔ mercado
> accionario, que es el núcleo del vacío que llena tu tesis. Sigue este protocolo y registra todo
> en la matriz de fichaje del final.

## 1. Bases de datos (en orden de prioridad)

| Base | URL | Para qué |
|---|---|---|
| **Google Scholar** | scholar.google.com | Barrido amplio inicial; "citado por" para rastrear |
| **SciELO Chile** | scielo.cl | Revistas chilenas (clave para el aporte local) |
| **Web of Science / Scopus** | (vía biblioteca USS) | Indexadas de alto impacto; filtros por país |
| **Repositorio BCCh** | bcentral.cl → Documentos de Trabajo | Working papers sobre cobre y macro chilena |
| **Cochilco** | cochilco.cl → Estudios | Informes sectoriales del cobre |
| **SSRN / RePEc** | ssrn.com / ideas.repec.org | Preprints de economía financiera |
| **Repositorios USS / tesis CL** | (bibliotecas universitarias) | Tesis previas comparables |

## 2. Cadenas de búsqueda (copiar y pegar)

**En español (SciELO, Scholar, repositorios):**
```
("precio del cobre" OR "cobre") AND ("retornos accionarios" OR "mercado bursátil" OR "acciones") AND Chile
("tipo de cambio" OR "peso chileno") AND ("precio del cobre" OR commodity) AND Chile
("IPSA" OR "Bolsa de Santiago") AND (cobre OR commodity OR macroeconómic*)
("variables macroeconómicas") AND ("retornos" OR "valoración bursátil") AND Chile
```

**En inglés (Scopus, WoS, Scholar):**
```
("copper price" OR copper) AND ("stock returns" OR "equity returns") AND Chile
("commodity currency" OR "commodity prices") AND ("exchange rate") AND Chile
("mining stocks" OR "mining equities") AND ("macroeconomic factors" OR "copper price")
("market segmentation" OR "informational efficiency") AND ("emerging market" OR Chile) AND equity
("arbitrage pricing theory" OR APT) AND ("macroeconomic") AND ("emerging market" OR "Latin America")
```

**Operadores útiles:** comillas para frase exacta; `AND/OR` en mayúsculas; en Scholar usa
`source:` para revista y el rango de años (2005–2025). En WoS/Scopus filtra por *Country = Chile*
y *Subject = Economics/Finance/Business*.

## 3. Criterios de inclusión / exclusión

**Incluir si:** (a) es seminal metodológico (cointegración, panel, APT, exposición cambiaria);
(b) es empírico commodity→equity (cualquier país, como plantilla); (c) **es chileno** sobre
cobre-macro-mercado (prioridad máxima, aunque sea working paper).
**Excluir si:** es puramente geológico/operacional del cobre, o macro chilena sin vínculo a
mercados financieros, o predicción pura sin inferencia.

## 4. Objetivos concretos a encontrar (mínimos para defender el vacío)

- [ ] ≥3 estudios chilenos que vinculen **cobre y tipo de cambio / peso** (probable: Documentos de
      Trabajo del BCCh; Cashin-Céspedes-Sahay ya lo tienes como internacional).
- [ ] ≥2 estudios sobre **determinantes macro del IPSA o de acciones chilenas**.
- [ ] ≥1 estudio sobre **exposición cambiaria de empresas chilenas**.
- [ ] ≥1 referencia de **segmentación/eficiencia del mercado bursátil chileno** (para el bloque 2.5).
- [ ] Confirmar la **ausencia** de estudios que hagan exactamente lo tuyo (cobre + empresas +
      comparación de mercados) → ESE es tu vacío. Documenta qué buscaste y no encontraste.

## 5. Matriz de fichaje (rellena una fila por paper)

| Autor (año) | País / datos | Período | Variables | Método | Hallazgo principal | Relación con mi tesis | Cita verificada ✔ |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | | | | | |

> Mantén esta tabla en una hoja de cálculo (xlsx). Te servirá para escribir en prosa las secciones
> 2.2–2.4 y, sobre todo, para **argumentar el vacío en 2.7**: "se encontró X, pero nadie ha
> abordado Y".

## 6. Gestión bibliográfica

- Usa **Zotero** (gratis): instala el conector del navegador, guarda cada referencia con un clic,
  y exporta a BibTeX (LaTeX) o a Word (cita y bibliografía automáticas).
- Crea una colección "Tesis Cobre" con subcarpetas: *Metodología*, *Commodity-Equity*,
  *Chile-Cobre*, *Segmentación*.
- Al cerrar, exporta la bibliografía en **formato APA 7** y reemplaza el archivo
  `docs/referencias.md` (las 32 referencias actuales ya están en APA como base verificable).

## 7. Errores a evitar
- No cites lo que no leíste (al menos el abstract y las conclusiones).
- No mezcles "no encontré evidencia" con "no existe evidencia": documenta tu estrategia de búsqueda.
- Verifica **cada** cita en la fuente original antes de la entrega (año, revista, páginas).
