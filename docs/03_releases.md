# Release History & Development Milestones — Sinapsis

> [**← Return to README**](../README.md) · [**00 Context**](00_context.md) · [**01 Workflow**](01_workflow.md) · [**02 Nomenclature**](02_nomenclature.md) · [**03 Releases**](03_releases.md)

---

## Architectural Scope: Single Regular Style

Sinapsis is conceived and finalized exclusively as a **single-style typeface: Regular**. The project prioritizes fidelity to the original notebook manuscripts of Arq. Juan Fernando Cárdenas Guillén, capturing the authentic stroke pressure, ductus, and rhythm of his architectural handwriting without synthetic or extraneous weight variations.

---

## Release History

### [v1.0.2] - 2026-11-21 (Production Release)
**Status:** Completed Production Release  
**Focus:** OpenType Contextual Alternates (`calt`), Small Caps suite, Kerning refinement, and Production Builds.

#### Key Engineering Deliverables:
- **Contextual Alternates Engine (`calt`):** Scripted lookup tables to dynamically alternate letters (`a`, `n`, `o`, `s`, `y`, `&`), preventing consecutive identical glyphs and emulating genuine handwritten cadence.
- **Stylistic Sets (`ss01`, `ss02`):** Implemented single-story forms (`ss01`) and contextual terminal flourishes for uppercase and lowercase letterforms (`ss02`).
- **Complete Small Capitals Suite (`smcp`, `c2sc`):** Comprehensive `.sc` glyph set covering basic and accented Latin.
- **Extended Language & Diacritics Support:** Full coverage for over 100 Latin-based languages, including Catalan localized punt volat (`periodcentered.loclCAT`) and Turkish dotless/dotted i (`i.loclTRK`).
- **Typographic Numerals & Math:** Fractions (`frac`), numerators (`numr`), denominators (`dnom`), superscripts (`sups`), subscripts/inferiors (`subs`, `sinf`), ordinals (`ordn`), and extended mathematical signs.
- **Comprehensive Kerning:** Optical spacing and group kerning audit across lowercase, uppercase, small caps, numerals, and punctuation.
- **Multi-Format Distribution Binaries:** Compiled Desktop (`OTF`, `TTF`) and Web (`WOFF`, `WOFF2`) binaries in `builds/`.
- **Packaging Automation:** Sanitized `.zip` distribution archive generation via `builds/package_release.sh`.

---

### [v1.0.0] - 2026-11-21 (Production Compilation & Normalization Milestone)
**Status:** Production Milestone  
**Focus:** Vertical metrics standardization, node contour optimization, and QA testing.

#### Key Engineering Deliverables:
- **Vertical Metrics Normalization:** Executed `scripts/AjustarMetricasVerticales.py` aligning typo, hhea, and win metrics to Google Fonts / Type Network standards (`typoAscender` = 935, `typoDescender` = -355, `winAscent` = 1060, `winDescent` = 355).
- **Node Contour Smoothing:** Applied `scripts/Smooth2Sharp.py` for Bézier handle alignment and redundant curve point elimination.
- **Fontbakery QA Audit:** Generated comprehensive compliance report (`tests/FhSinapsis-Regular-fontbakery-typenetwork.html`) and vertical metrics report (`tests/Sinapsis-reporte-metricas-verticales.pdf`).

---

### [v0.1.0] - 2026-11-04 (Initial Architecture)
**Status:** Repository Initialization & Architectural Setup  
**Focus:** Establishing technical repository scaffolding, documentation, licensing, and workflow standards.

#### Key Engineering Deliverables:
- Initialized modular Git repository adhering to font engineering industry standards.
- Prepared initial Glyphs master (`Sinapsis.glyphs`) and visual typographic specimens (`assets/`).
- Authored technical documentation (`docs/00_context.md`, `docs/01_workflow.md`, `docs/02_nomenclature.md`, `docs/03_releases.md`).
- Established legal framework: SIL Open Font License 1.1 (`LICENSE.txt`), EULA (`EULA.md`, `EULA.txt`), and attribution (`CONTRIBUTORS.md`).
- Implemented build tooling: sanitized release packaging automation script (`builds/package_release.sh`).
