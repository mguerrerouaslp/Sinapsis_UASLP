# Project Context — Sinapsis

![Sinapsis Specimen](https://raw.githubusercontent.com/bluetypo/Sinapsis/main/assets/Sinapsis_specimen.png)

> [**← Return to README**](../README.md) · [**00 Context**](00_context.md) · [**01 Workflow**](01_workflow.md) · [**02 Nomenclature**](02_nomenclature.md) · [**03 Releases**](03_releases.md)

---
**Sinapsis** is an Open Access typeface created for the **Sinapsis Architecture Workshop** at the Facultad del Hábitat, Universidad Autónoma de San Luis Potosí (UASLP). The typeface is rooted in the personal architectural handwriting of architect **Juan Fernando Cárdenas Guillén**, who founded the workshop in 2011.

The project captures, formalizes, and translates the architectural ductus, rhythm, and structural strokes of the architect's sketchbook lettering into a precision digital typographic system built to professional engineering standards. Sinapsis is developed strictly as a single-style typeface: **Regular** (`Fh-Sinapsis Regular`), ensuring complete fidelity to the original ink gestures and pen dynamics without synthetic weight variations.

---

## 2. Open Access Commitment & Academic Mission
Sinapsis is conceived from its inception as an **Open Access Resource** dedicated to higher public education, architectural research, and the international creative community:

* **Academic Public Good:** Providing students, educators, and researchers at the Facultad del Hábitat (and academic institutions worldwide) with a professional-grade type system without economic barriers or commercial licensing restrictions.
* **Open Source Transparency:** Beyond distributing compiled binaries (Desktop OTF/TTF and Web WOFF/WOFF2), the project maintains full transparency by publishing its complete design sources (`sources/Sinapsis.glyphs`), technical documentation, and build pipeline.
* **Culture of Libre Typography:** Distributed under the **SIL Open Font License (OFL 1.1)**, ensuring that academic adaptations, research uses, and derivative works remain free, open, and permanently accessible.

---

## 3. Design Space & Morphological Characteristics
The typeface bridges structural architectural intent and functional typographic performance:

* **Single-Style Architectural Fidelity:** Dedicated exclusively to the single **Regular** master, capturing the direct stroke weight, ductus, and cadence of the original drafting pen notes.
* **Dynamic Architectural Ductus:** Distinctive corner junctions and terminal angles that evoke technical drawing pens, drafting markers, and freehand construction notes.
* **Contextual Handwriting Engine (`calt`):** A sophisticated OpenType alternation routine that dynamically rotates letter variations (`a`, `n`, `o`, `s`, `y`, `&`), preserving the natural, non-mechanical rhythm of human handwriting.
* **Stylistic Sets (`ss01`, `ss02`):** Stylistic alternatives providing single-story and terminal flourishing glyph variants.
* **Metric Discipline:** Systematic optical adjustments across the x-height, ascenders, descenders, and cap height to guarantee legibility across technical drawings, body copy, and environmental signage.
* **Standardized Vertical Metrics:** Normalized to Google Fonts and Type Network technical specifications (`typoAscender` = 935, `typoDescender` = -355, `winAscent` = 1060, `winDescent` = 355) with `Use Typo Metrics` enabled for cross-platform alignment parity.

---

## 4. Credits & Development
* **Juan Fernando Cárdenas Guillén** — Original handwriting and conceptual inspiration.
* **Manuel Guerrero Salinas (Bluetypo)** — Digital type design, digitization, vectorization, and font engineering production.
* **Taller de Arquitectura Sinapsis** — Facultad del Hábitat, Universidad Autónoma de San Luis Potosí (UASLP).
* **Bluetypo** ([bluetypo.com](https://bluetypo.com)) — Technical direction, OpenType feature programming, and quality assurance.

---

## 5. Implemented Character Set (Charset)
Comprehensive **Latin Pro** coverage:
* Full support for over 100 Latin-based languages (Western, Central, Eastern European, Baltic, and Vietnamese).
* Full suite of Small Capitals (`smcp`, `c2sc`) for basic and accented Latin glyphs.
* Combining and precomposed diacritics via dynamic mark positioning (`ccmp`).
* Complete numeral and mathematical suites: arbitrary diagonal fractions (`frac`), numerators (`numr`), denominators (`dnom`), superscripts (`sups`), subscripts (`subs`, `sinf`), ordinals (`ordn`), and standard mathematical operators ($\neq$, $\ge$, $\le$, $\approx$, $\infty$, $\int$, $\prod$, $\sum$, $\sqrt{}$, etc.).
* Contextual alternates, architectural ligatures (`liga`, `dlig`), and case-sensitive punctuation forms (`case`).
* Localized forms (`locl`) for Catalan punt volat and Turkish dotless/dotted i.

---

## 6. Repository Architecture & Quality Standards
This repository serves as the development hub for:
1. **Master Source Control:** Tracking design iterations in `sources/Sinapsis.glyphs`.
2. **Automated Font Compilation:** Generating clean OTF, TTF, WOFF, and WOFF2 builds in `builds/`.
3. **Rigorous Quality Assurance:** Validation against automated linters (*Fontbakery*), vertical metric reports, and InDesign specimen suites.
4. **Clean Release Distribution:** Producing sanitized, metadata-free release archives in `builds/release/`.
