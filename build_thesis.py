"""
build_thesis.py
==============
Ensambla la tesis completa en un .docx con estructura formal de magíster:
portada · página de aprobación · declaración de originalidad · dedicatoria ·
agradecimientos · resumen · abstract (inglés) · índice general · índice de tablas ·
índice de figuras · lista de abreviaturas · capítulos 1-5 · referencias.

Numeración romana en preliminares y arábiga en el cuerpo. Figuras y tablas con
rótulos de Word (campos SEQ) para que los índices se autogeneren.
Salida: outputs/Tesis_Francisco_Rietta.docx
"""
from pathlib import Path
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
OUT = ROOT / "outputs" / "Tesis_Francisco_Rietta.docx"

TITULO = ("Impacto de las variables macroeconómicas en los retornos accionarios de las "
          "empresas de cobre con exposición a Chile: una comparación entre el mercado "
          "bursátil internacional y el chileno, 2004–2024")

CAPS = ["introduccion_capitulo1.md", "marco_teorico_capitulo2.md",
        "metodologia_capitulo3.md", "resultados_capitulo4.md",
        "conclusiones_capitulo5.md", "referencias.md"]

ABREV = [
    ("APT", "Arbitrage Pricing Theory (teoría de valoración por arbitraje)"),
    ("ADF", "Augmented Dickey-Fuller (prueba de raíz unitaria)"),
    ("ARDL", "Autoregressive Distributed Lag (modelo de rezagos distribuidos)"),
    ("BCCh", "Banco Central de Chile"),
    ("CD", "Cross-section Dependence (prueba de Pesaran)"),
    ("CMF", "Comisión para el Mercado Financiero"),
    ("EMBI", "Emerging Markets Bond Index (índice de riesgo soberano)"),
    ("FEVD", "Forecast Error Variance Decomposition"),
    ("FE", "Fixed Effects (efectos fijos)"),
    ("FRED", "Federal Reserve Economic Data"),
    ("IMACEC", "Índice Mensual de Actividad Económica"),
    ("IPSA", "Índice de Precios Selectivo de Acciones"),
    ("KPSS", "Kwiatkowski-Phillips-Schmidt-Shin (prueba de estacionariedad)"),
    ("TPM", "Tasa de Política Monetaria"),
    ("VAR", "Vector Autoregression (vector autorregresivo)"),
    ("VECM", "Vector Error Correction Model"),
    ("VIX", "CBOE Volatility Index"),
]


# ---------- estilos ----------
def set_base_styles(doc):
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"; st.font.size = Pt(12)
    pf = st.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_after = Pt(6); pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for h, sz in [("Heading 1", 16), ("Heading 2", 14), ("Heading 3", 12.5)]:
        s = doc.styles[h]
        s.font.name = "Times New Roman"; s.font.size = Pt(sz)
        s.font.color.rgb = RGBColor(0x1a, 0x1a, 0x2e)


def _fld(run, instr, default="1"):
    fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr
    fc2 = OxmlElement("w:fldChar"); fc2.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = default
    fc3 = OxmlElement("w:fldChar"); fc3.set(qn("w:fldCharType"), "end")
    for el in (fc, it, fc2, t, fc3):
        run._r.append(el)


def set_pgnum_format(section, fmt, start=None):
    sectPr = section._sectPr
    pg = sectPr.find(qn("w:pgNumType"))
    if pg is None:
        pg = OxmlElement("w:pgNumType"); sectPr.append(pg)
    pg.set(qn("w:fmt"), fmt)
    if start is not None:
        pg.set(qn("w:start"), str(start))


def footer_pagenum(section):
    section.footer.is_linked_to_previous = False
    p = section.footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.text = ""
    run = p.add_run(); _fld(run, "PAGE"); run.font.size = Pt(10)


def field_block(doc, instr, placeholder):
    p = doc.add_paragraph(); run = p.add_run(); _fld(run, instr, placeholder)


def add_runs_with_bold(paragraph, text):
    for part in re.split(r"(\*\*.+?\*\*|\[COMPLETAR[^\]]*\])", text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            paragraph.add_run(part[2:-2]).bold = True
        elif part.startswith("[COMPLETAR"):
            r = paragraph.add_run(part); r.font.highlight_color = 7
            r.font.color.rgb = RGBColor(0x8a, 0x5a, 0x18)
        else:
            paragraph.add_run(part)


def clean_heading(text):
    return re.sub(r"\s*\((borrador|texto)[^)]*\)", "", text).strip()


def caption(doc, label, text):
    """Rótulo con campo SEQ (Figura/Tabla N. texto) en estilo Caption."""
    try:
        p = doc.add_paragraph(style="Caption")
    except KeyError:
        p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"{label} "); r.bold = True; r.font.size = Pt(10)
    fs = OxmlElement("w:fldSimple"); fs.set(qn("w:instr"), f" SEQ {label} \\* ARABIC ")
    rr = OxmlElement("w:r"); tt = OxmlElement("w:t"); tt.text = "1"; rr.append(tt); fs.append(rr)
    p._p.append(fs)
    r2 = p.add_run(f". {text}"); r2.font.size = Pt(10)


# ---------- parser markdown ----------
def add_table(doc, rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(set(c) <= set("-: ") for c in r)]
    if not cells:
        return
    caption(doc, "Tabla", "")
    tbl = doc.add_table(rows=len(cells), cols=len(cells[0])); tbl.style = "Light Grid Accent 1"
    for i, row in enumerate(cells):
        for j, val in enumerate(row):
            if j >= len(tbl.rows[i].cells):
                continue
            cp = tbl.rows[i].cells[j].paragraphs[0]; cp.text = ""
            add_runs_with_bold(cp, val.replace("**", "") if i == 0 else val)
            for run in cp.runs:
                run.font.size = Pt(10)
                if i == 0:
                    run.bold = True
    doc.add_paragraph()


def add_figure(doc, cap, path):
    img = ROOT / path
    if not img.exists():
        return
    doc.add_picture(str(img), width=Inches(5.9))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption(doc, "Figura", cap)


def render_markdown(doc, md_text):
    lines = md_text.split("\n"); i = 0; tablebuf = []
    def flush():
        nonlocal tablebuf
        if tablebuf:
            add_table(doc, tablebuf); tablebuf = []
    while i < len(lines):
        line = lines[i].rstrip()
        if line.startswith("|") and "|" in line[1:]:
            tablebuf.append(line); i += 1; continue
        flush()
        if not line.strip() or line.startswith(">") or line.startswith("---"):
            i += 1; continue
        m = re.match(r"!\[(.*?)\]\((.*?)\)", line)
        if m:
            add_figure(doc, m.group(1), m.group(2)); i += 1; continue
        if line.startswith("# "):
            doc.add_heading(clean_heading(line[2:]), 1); i += 1; continue
        if line.startswith("## "):
            doc.add_heading(clean_heading(line[3:]), 2); i += 1; continue
        if line.startswith("### "):
            doc.add_heading(clean_heading(line[4:]), 3); i += 1; continue
        if line.startswith("#### "):
            doc.add_heading(clean_heading(line[5:]), 3); i += 1; continue
        if re.match(r"^\s*[-*] ", line):
            add_runs_with_bold(doc.add_paragraph(style="List Bullet"),
                               re.sub(r"^\s*[-*] ", "", line)); i += 1; continue
        if re.match(r"^\s*\d+\. ", line):
            add_runs_with_bold(doc.add_paragraph(style="List Number"),
                               re.sub(r"^\s*\d+\. ", "", line)); i += 1; continue
        add_runs_with_bold(doc.add_paragraph(), line); i += 1
    flush()


# ---------- preliminares ----------
def centered(doc, text, size, bold=False, italic=False, space=6):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space)
    r = p.add_run(text); r.font.size = Pt(size); r.bold = bold; r.italic = italic
    r.font.name = "Times New Roman"
    return p


def add_cover(doc):
    logo = next((c for c in (ROOT/"assets"/"logo_uss.png", ROOT/"web"/"logo_uss.png")
                 if c.exists()), None)
    if logo:
        doc.add_picture(str(logo), width=Inches(1.8))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    centered(doc, "UNIVERSIDAD SAN SEBASTIÁN", 14, bold=True, space=2)
    centered(doc, "Facultad de Ingeniería · Magíster en Data Science", 12, space=44)
    centered(doc, TITULO, 17, bold=True, space=40)
    centered(doc, "Tesis para optar al grado de Magíster en Data Science", 12, italic=True, space=44)
    centered(doc, "Autor: Francisco Rietta", 12, space=2)
    centered(doc, "Profesor guía: [Nombre del profesor]", 12, space=44)
    centered(doc, "Santiago, Chile — 2026", 12)


def page(doc): doc.add_page_break()


def add_approval(doc):
    doc.add_heading("Página de aprobación", 1)
    doc.add_paragraph("La presente tesis, titulada «" + TITULO + "», ha sido revisada y aprobada "
                      "por la comisión examinadora abajo firmante, como requisito para optar al "
                      "grado de Magíster en Data Science de la Universidad San Sebastián.")
    for rol in ["Profesor guía", "Profesor informante", "Director(a) de programa"]:
        doc.add_paragraph()
        l = doc.add_paragraph("_______________________________"); l.alignment = WD_ALIGN_PARAGRAPH.CENTER
        n = doc.add_paragraph(rol); n.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(); cal = doc.add_paragraph("Calificación: __________     Fecha: ____ / ____ / ______")
    cal.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_originality(doc):
    doc.add_heading("Declaración de originalidad", 1)
    doc.add_paragraph("Declaro que esta tesis es de mi autoría y que constituye un trabajo original. "
                      "Toda fuente, idea o resultado de terceros utilizado en su elaboración ha sido "
                      "debidamente citado y referenciado conforme a las normas académicas vigentes. "
                      "Declaro asimismo que este documento no ha sido presentado previamente para la "
                      "obtención de otro grado o título.")
    doc.add_paragraph(); doc.add_paragraph();
    f = doc.add_paragraph("_______________________________"); f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    a = doc.add_paragraph("Francisco Rietta"); a.alignment = WD_ALIGN_PARAGRAPH.RIGHT


def add_simple_page(doc, titulo, cuerpo, italic=False, align=WD_ALIGN_PARAGRAPH.RIGHT):
    doc.add_heading(titulo, 1)
    for _ in range(3):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = align
    r = p.add_run(cuerpo); r.italic = italic


def add_abstract_en(doc):
    doc.add_heading("Abstract", 1)
    doc.add_paragraph(
        "This thesis quantifies and compares the impact of global and national macroeconomic "
        "variables on the stock returns of copper firms with exposure to Chile over 2004–2024, "
        "contrasting how the shock is transmitted across the international and the Chilean equity "
        "markets. Using a triangulation design across three samples and a battery of time-series "
        "and panel-data models —unit-root tests, fixed-effects panels with Driscoll-Kraay standard "
        "errors, cointegration (ARDL/Johansen) and vector autoregressions with variance "
        "decomposition—, the study assesses the sensitivity of returns to macro-financial factors, "
        "its stability across copper-cycle phases, and its differential transmission across markets. "
        "Preliminary evidence supports the copper price as the main driver of returns and the "
        "dominance of global over local factors.")
    p = doc.add_paragraph();
    p.add_run("Keywords: ").bold = True
    p.add_run("copper, stock returns, macroeconomic variables, Chile, panel data, cointegration, "
              "market segmentation.")


def add_abbrev(doc):
    doc.add_heading("Lista de abreviaturas y siglas", 1)
    tbl = doc.add_table(rows=len(ABREV), cols=2); tbl.style = "Light List Accent 1"
    for i, (sig, desc) in enumerate(ABREV):
        c0, c1 = tbl.rows[i].cells
        c0.paragraphs[0].add_run(sig).bold = True
        c1.paragraphs[0].add_run(desc)
        for c in (c0, c1):
            for r in c.paragraphs[0].runs:
                r.font.size = Pt(11)


# ---------- main ----------
def build():
    doc = Document()
    set_base_styles(doc)
    sec0 = doc.sections[0]
    sec0.left_margin = sec0.right_margin = Inches(1.18)
    sec0.top_margin = sec0.bottom_margin = Inches(1.0)
    sec0.different_first_page_header_footer = True  # portada sin número

    # --- Preliminares (numeración romana) ---
    add_cover(doc); page(doc)
    add_approval(doc); page(doc)
    add_originality(doc); page(doc)
    add_simple_page(doc, "Dedicatoria", "[Espacio para la dedicatoria.]", italic=True); page(doc)
    add_simple_page(doc, "Agradecimientos",
                    "[Espacio para los agradecimientos.]", align=WD_ALIGN_PARAGRAPH.JUSTIFY); page(doc)
    doc.add_heading("Resumen", 1)
    for blk in _resumen_text().split("\n\n"):
        add_runs_with_bold(doc.add_paragraph(), blk)
    page(doc)
    add_abstract_en(doc); page(doc)
    doc.add_heading("Índice general", 1); field_block(doc, 'TOC \\o "1-3" \\h \\z \\u',
                    "Actualizar campo para generar el índice."); page(doc)
    doc.add_heading("Índice de tablas", 1); field_block(doc, 'TOC \\h \\z \\c "Tabla"',
                    "Actualizar campo."); page(doc)
    doc.add_heading("Índice de figuras", 1); field_block(doc, 'TOC \\h \\z \\c "Figura"',
                    "Actualizar campo."); page(doc)
    add_abbrev(doc)
    set_pgnum_format(sec0, "lowerRoman", start=1)
    footer_pagenum(sec0)

    # --- Cuerpo (numeración arábiga, reinicia en 1) ---
    body = doc.add_section(WD_SECTION.NEW_PAGE)
    body.left_margin = body.right_margin = Inches(1.18)
    body.top_margin = body.bottom_margin = Inches(1.0)
    set_pgnum_format(body, "decimal", start=1)
    footer_pagenum(body)
    for k, fname in enumerate(CAPS):
        render_markdown(doc, (DOCS / fname).read_text(encoding="utf-8"))
        if k < len(CAPS) - 1:
            page(doc)

    OUT.parent.mkdir(exist_ok=True)
    doc.save(OUT)
    print(f"[ok] {OUT}  ({OUT.stat().st_size//1024} KB)")
    return OUT


def _resumen_text():
    return (
        "Esta investigación cuantifica y compara el impacto de las variables macroeconómicas "
        "globales y nacionales sobre los retornos accionarios de las empresas de cobre con "
        "exposición a Chile durante 2004–2024, contrastando su transmisión entre el mercado "
        "bursátil internacional y el chileno. Mediante un diseño de triangulación por tres muestras "
        "y un conjunto de modelos econométricos de series de tiempo y datos de panel —pruebas de "
        "raíz unitaria, panel de efectos fijos con errores Driscoll-Kraay, cointegración "
        "(ARDL/Johansen) y vectores autorregresivos con descomposición de varianza—, se evalúa la "
        "sensibilidad de los retornos a los factores macro-financieros, su estabilidad a lo largo "
        "de las fases del ciclo del cobre y la transmisión diferenciada entre mercados. La evidencia "
        "preliminar respalda al precio del cobre como principal determinante de los retornos y la "
        "dominancia de los factores globales sobre los locales.\n\n"
        "**Palabras clave:** cobre, retornos accionarios, variables macroeconómicas, Chile, datos "
        "de panel, cointegración, segmentación de mercados.")


if __name__ == "__main__":
    build()
