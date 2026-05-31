"""
build_thesis.py
==============
Ensambla la tesis completa en un .docx con formato académico de magíster:
portada (con logo si existe), resumen/abstract, índice automático (campo TOC),
capítulos 1-5, figuras, tablas, referencias y numeración de páginas.

Convierte los borradores markdown de docs/ a Word con un parser ligero.
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
FIG = ROOT / "outputs" / "figures"
OUT = ROOT / "outputs" / "Tesis_Francisco_Rietta.docx"

TITULO = ("Impacto de las variables macroeconómicas en los retornos accionarios de las "
          "empresas de cobre con exposición a Chile: una comparación entre el mercado "
          "bursátil internacional y el chileno, 2004–2024")

# Capítulos a ensamblar, en orden
CAPS = [
    "introduccion_capitulo1.md",
    "marco_teorico_capitulo2.md",
    "metodologia_capitulo3.md",
    "resultados_capitulo4.md",
    "conclusiones_capitulo5.md",
    "referencias.md",
]


# ---------- helpers de formato ----------
def set_base_styles(doc):
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    pf = st.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_after = Pt(6)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for h, sz in [("Heading 1", 16), ("Heading 2", 14), ("Heading 3", 12.5)]:
        s = doc.styles[h]
        s.font.name = "Times New Roman"; s.font.size = Pt(sz)
        s.font.color.rgb = RGBColor(0x1a, 0x1a, 0x2e)


def add_page_number(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    for t, attr in [("begin", None), (None, "PAGE"), ("end", None)]:
        if attr:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
            it.text = attr; run._r.append(it)
        else:
            fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), t); run._r.append(fc)
    run.font.size = Pt(10)


def add_toc(doc):
    p = doc.add_paragraph(); run = p.add_run()
    fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
    it.text = 'TOC \\o "1-3" \\h \\z \\u'
    fc2 = OxmlElement("w:fldChar"); fc2.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = "Clic derecho → Actualizar campo para generar el índice."
    fc3 = OxmlElement("w:fldChar"); fc3.set(qn("w:fldCharType"), "end")
    for el in (fc, it, fc2, t, fc3):
        run._r.append(el)


def add_runs_with_bold(paragraph, text):
    """Inserta texto resolviendo **negrita** y [COMPLETAR: ...] resaltado."""
    parts = re.split(r"(\*\*.+?\*\*|\[COMPLETAR[^\]]*\])", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            r = paragraph.add_run(part[2:-2]); r.bold = True
        elif part.startswith("[COMPLETAR"):
            r = paragraph.add_run(part)
            r.font.highlight_color = 7  # amarillo
            r.font.color.rgb = RGBColor(0x8a, 0x5a, 0x18)
        else:
            paragraph.add_run(part)


def clean_heading(text):
    return re.sub(r"\s*\((borrador|texto)[^)]*\)", "", text).strip()


# ---------- parser markdown ligero ----------
def add_table(doc, rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(set(c) <= set("-: ") for c in r)]  # quita separador
    if not cells:
        return
    tbl = doc.add_table(rows=len(cells), cols=len(cells[0]))
    tbl.style = "Light Grid Accent 1"
    for i, row in enumerate(cells):
        for j, val in enumerate(row):
            if j >= len(tbl.rows[i].cells):
                continue
            cell = tbl.rows[i].cells[j]
            cell.paragraphs[0].text = ""
            add_runs_with_bold(cell.paragraphs[0], val.replace("**", "") if i == 0 else val)
            for run in cell.paragraphs[0].runs:
                run.font.size = Pt(10)
                if i == 0:
                    run.bold = True
    doc.add_paragraph()


def add_figure(doc, caption, path):
    img = ROOT / path
    if not img.exists():
        return
    doc.add_picture(str(img), width=Inches(5.9))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(caption); r.italic = True; r.font.size = Pt(10)


def render_markdown(doc, md_text, first_chapter=False):
    lines = md_text.split("\n")
    i, tablebuf, listbuf = 0, [], None
    def flush_table():
        nonlocal tablebuf
        if tablebuf:
            add_table(doc, tablebuf); tablebuf = []
    while i < len(lines):
        line = lines[i].rstrip()
        if line.startswith("|") and "|" in line[1:]:
            tablebuf.append(line); i += 1; continue
        flush_table()
        if not line.strip():
            i += 1; continue
        if line.startswith(">"):            # admoniciones editoriales → omitir
            i += 1; continue
        if line.startswith("---"):
            i += 1; continue
        m = re.match(r"!\[(.*?)\]\((.*?)\)", line)
        if m:
            add_figure(doc, m.group(1), m.group(2)); i += 1; continue
        if line.startswith("# "):
            doc.add_heading(clean_heading(line[2:]), level=1); i += 1; continue
        if line.startswith("## "):
            doc.add_heading(clean_heading(line[3:]), level=2); i += 1; continue
        if line.startswith("### "):
            doc.add_heading(clean_heading(line[4:]), level=3); i += 1; continue
        if line.startswith("#### "):
            doc.add_heading(clean_heading(line[5:]), level=3); i += 1; continue
        if re.match(r"^\s*[-*] ", line):
            p = doc.add_paragraph(style="List Bullet")
            add_runs_with_bold(p, re.sub(r"^\s*[-*] ", "", line)); i += 1; continue
        if re.match(r"^\s*\d+\. ", line):
            p = doc.add_paragraph(style="List Number")
            add_runs_with_bold(p, re.sub(r"^\s*\d+\. ", "", line)); i += 1; continue
        p = doc.add_paragraph()
        add_runs_with_bold(p, line)
        i += 1
    flush_table()


# ---------- portada ----------
def add_cover(doc):
    logo = None
    for cand in (ROOT / "assets" / "logo_uss.png", ROOT / "web" / "logo_uss.png"):
        if cand.exists():
            logo = cand; break
    if logo:
        doc.add_picture(str(logo), width=Inches(1.8))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    def center(text, size, bold=False, italic=False, space=6):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(space)
        r = p.add_run(text); r.font.size = Pt(size); r.bold = bold; r.italic = italic
        r.font.name = "Times New Roman"
        return p

    center("UNIVERSIDAD SAN SEBASTIÁN", 14, bold=True, space=2)
    center("Magíster en Data Science", 12, space=40)
    center(TITULO, 17, bold=True, space=36)
    center("Tesis para optar al grado de Magíster en Data Science", 12, italic=True, space=40)
    center("Autor: Francisco Rietta", 12, space=2)
    center("Profesor guía: [Nombre del profesor]", 12, space=40)
    center("Santiago, Chile — 2026", 12)
    doc.add_page_break()


def add_resumen(doc):
    doc.add_heading("Resumen", level=1)
    doc.add_paragraph(
        "Esta investigación cuantifica y compara el impacto de las variables macroeconómicas "
        "globales y nacionales sobre los retornos accionarios de las empresas de cobre con "
        "exposición a Chile durante el período 2004–2024, contrastando su transmisión entre el "
        "mercado bursátil internacional y el chileno. Mediante un diseño de triangulación por tres "
        "muestras y un conjunto de modelos econométricos de series de tiempo y datos de panel "
        "—pruebas de raíz unitaria, panel de efectos fijos con errores Driscoll-Kraay, "
        "cointegración (ARDL/Johansen) y vectores autorregresivos con descomposición de varianza—, "
        "se evalúa la sensibilidad de los retornos a los factores macro-financieros, su estabilidad "
        "a lo largo de las fases del ciclo del cobre y la transmisión diferenciada entre mercados. "
        "La evidencia preliminar respalda al precio del cobre como principal determinante de los "
        "retornos y la dominancia de los factores globales sobre los locales.")
    p = doc.add_paragraph()
    add_runs_with_bold(p, "**Palabras clave:** cobre, retornos accionarios, variables "
                          "macroeconómicas, Chile, datos de panel, cointegración, segmentación de "
                          "mercados.")
    doc.add_page_break()


# ---------- main ----------
def build():
    doc = Document()
    set_base_styles(doc)
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Inches(1.18)
    sec.top_margin = sec.bottom_margin = Inches(1.0)

    add_cover(doc)
    add_resumen(doc)
    doc.add_heading("Índice", level=1)
    add_toc(doc)
    doc.add_page_break()
    add_page_number(sec)

    for k, fname in enumerate(CAPS):
        md = (DOCS / fname).read_text(encoding="utf-8")
        render_markdown(doc, md, first_chapter=(k == 0))
        if k < len(CAPS) - 1:
            doc.add_page_break()

    OUT.parent.mkdir(exist_ok=True)
    doc.save(OUT)
    print(f"[ok] {OUT}  ({OUT.stat().st_size//1024} KB)")
    return OUT


if __name__ == "__main__":
    build()
