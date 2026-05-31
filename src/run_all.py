"""
run_all.py
=========
Orquestador de reproducibilidad: ejecuta TODO el pipeline de análisis en orden, con
manejo de errores por paso y un resumen final. Permite regenerar el proyecto completo
con un solo comando:

    python -m src.run_all              # usa datos en caché (data/interim)
    python -m src.run_all --descargar  # vuelve a descargar de FRED/Yahoo primero

Pasos:
  1. (opcional) Adquisición de datos (FRED + Yahoo).
  2. Construcción de los tres paneles (B, A, C) -> data/processed + JSON a la plataforma.
  3. Análisis avanzado, extensiones, robustez extra, predictor.
  4. Tests adicionales (Hausman, CIPS, comparación de mercados).
  5. Exportación de datos web, figuras y anexos.

No genera el .docx/.pdf (requiere Word); ese paso es `python build_thesis.py`.
"""
from __future__ import annotations
import sys
import time

from . import config as C


def _step(nombre, fn):
    t0 = time.time()
    try:
        fn()
        print(f"[OK]    {nombre}  ({time.time()-t0:.1f}s)")
        return True
    except Exception as e:
        print(f"[FALLA] {nombre}: {type(e).__name__}: {e}")
        return False


def main(descargar=False):
    from . import build_panel, advanced_results, extensions, robustness_extra
    from . import predictor, hausman_test, panel_unit_root, market_comparison
    from . import export_web, make_figures, full_tables

    print("=" * 64)
    print("PIPELINE COMPLETO — Tesis cobre")
    print("=" * 64)
    ok = []

    if descargar:
        from . import data_acquisition

        def _adq():
            da = data_acquisition
            g = da.descargar_fred(C.MACRO_GLOBAL); g.to_parquet(C.DATA_INTERIM / "raw_macro_global.parquet")
            lf = da.descargar_fred(C.MACRO_LOCAL_FRED); lf.to_parquet(C.DATA_INTERIM / "raw_macro_local_fred.parquet")
            todos = {**C.MUESTRA_A_LOCAL_COBRE, **C.MUESTRA_B_GLOBAL_COBRE, **C.MUESTRA_C_LOCAL_MINERIA}
            px = da.descargar_precios_yahoo(list(todos.keys())); px.to_parquet(C.DATA_INTERIM / "raw_precios.parquet")
        ok.append(_step("1. Adquisición de datos", _adq))

    def _paneles():
        for suf, uni in [("_B", C.UNIVERSO_PRINCIPAL), ("_A", C.UNIVERSO_LOCAL_COBRE),
                         ("_C", C.UNIVERSO_LOCAL_MINERIA)]:
            build_panel.construir(guardar=True, universo=uni, sufijo=suf)
    ok.append(_step("2. Construcción de paneles B/A/C", _paneles))

    ok.append(_step("3. Análisis avanzado (OE5, CD, ZA, IRF)", advanced_results.construir))
    ok.append(_step("4. Extensiones (GARCH, Gregory-Hansen)", extensions.construir))
    ok.append(_step("5. Robustez extra (FDR, betas, GJR, LP)", robustness_extra.construir))
    ok.append(_step("6. Predictor del cobre", predictor.evaluar))
    ok.append(_step("7. Test de Hausman (FE vs RE)", hausman_test.analizar))
    ok.append(_step("8. Raíz unitaria en panel (CIPS)", panel_unit_root.analizar))
    ok.append(_step("9. Comparación de mercados (H7)", market_comparison.analizar))
    from . import variance_ratio
    ok.append(_step("9b. Razón de varianzas (Lo-MacKinlay)", variance_ratio.analizar))
    ok.append(_step("10. Exportar datos web", export_web.construir_json))
    ok.append(_step("11. Figuras de publicación", make_figures.construir))
    ok.append(_step("12. Anexos con tablas reales", full_tables.construir))

    print("=" * 64)
    print(f"RESUMEN: {sum(ok)}/{len(ok)} pasos OK")
    print("Siguiente: `python build_thesis.py` para regenerar el documento (requiere Word).")
    return all(ok)


if __name__ == "__main__":
    sys.exit(0 if main(descargar="--descargar" in sys.argv) else 1)
