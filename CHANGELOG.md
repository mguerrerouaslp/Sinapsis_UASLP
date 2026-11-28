# Changelog — Sinapsis

All notable technical changes and releases for the Sinapsis typeface project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.3] - 2026-11-28
### Added
- **Editorial Typographic Specimen (`specimen/Sinapsis_specimen.pdf`):**
  - Full multi-page PDF specimen showcasing `Fh-Sinapsis Regular` alongside architectural ink illustrations of the Sagrada Familia, character sets (basic, extended Latin, small caps, ligatures, contextual alternates, stylistic sets, fractions, math/currency, localized forms), and Spanish/Catalan texts.
- **Archival Manuscript Scans (`assets/scans/`):**
  - Published 23 digitized archival manuscript pages documenting the original architectural handwriting source material.
- **Public Showcase & Download Page (`index.html`):**
  - Added static web specimen with live type tester, automatic latest-release download link, and full 126-language support list.
- **Repository Hygiene (`.gitignore`):**
  - Added `.gitignore` excluding OS metadata, unpacked release staging folders, and private Glyphs master files (`sources/`, `*.glyphs`, `*.glyphspackage/`).

### Changed
- **Naming & Documentation Adjustments:**
  - Standardized repository and distribution naming (`Sinapsis_UASLP`, `Sinapsis_v1.0.3.zip`) and aligned `README.md` and `docs/` with the public distribution structure.
  - Added the complete list of **126 supported Latin-based languages** to `README.md` and `index.html`.
  - Updated specimen image links to relative paths across `README.md` and `docs/`.
- **Release Packaging (`builds/package_release.sh`):**
  - Kept the release archive lightweight by excluding archival `assets/scans/` and `specimen/` (retained in the repository).
  - Removed duplicate unpacked release directory from Git history.

---

## [1.0.2] - 2026-11-21
### Added
- **Contextual Alternates Engine (`calt`):**
  - Advanced OpenType scripting for dynamic letterform alternation across running text (`a`, `n`, `o`, `s`, `y`, `&`), mimicking authentic handwriting variability and eliminating repetitive patterns.
  - Contextual end-of-word substitutions and letter-pair flow handling.
- **Stylistic Sets (`ss01`, `ss02`):**
  - `ss01`: Alternate single-story forms and idiosyncratic cursive variants (`a.ss01`, `n.ss01`, `o.ss01`, `s.ss01`, `y.ss01`, `ampersand.ss01`, `e_s.ss01`).
  - `ss02`: Terminal flourishing variants for capitals and lowercase endings (`E.ss02`, `K.ss02`, `T.ss02`, `a.ss02`, `s.ss02`, `e_s.ss02`).
- **Standard & Discretionary Ligatures (`liga`, `dlig`):**
  - Standard f-ligatures (`fi`, `fl`).
  - Script-like discretionary ligatures (`e_n`, `e_s`, `s_t`, `t_i`, `z_a`, `C_O`, `S_P`).
- **Small Capitals & Full Small Cap Suite (`smcp`, `c2sc`):**
  - Dedicated small capital glyphs (`.sc`) for the complete basic and extended Latin character set, including accented small caps and case-sensitive diacritics.
- **Diacritics & Extended Language Support:**
  - Full Pan-European Latin language coverage (Western, Central, Eastern European, Baltic, and Vietnamese accents): grave, acute, circumflex, tilde, dieresis, ring, caron, macron, breve, dotaccent, cedilla, ogonek, hungarumlaut, and composite forms via `ccmp`.
  - Localized forms (`locl`) for Catalan punt volat (`periodcentered.loclCAT`, `periodcentered.loclCAT.case`) and Turkish dotless/dotted i (`i.loclTRK`).
- **Numerals, Fractions & Mathematical Signs:**
  - Arbitrary fraction feature (`frac`) with dedicated numerators (`numr`), denominators (`dnom`), superscripts (`sups`), subscripts/inferiors (`subs`, `sinf`), and ordinals (`ordn`).
  - Comprehensive mathematical operators and symbols ($\neq$, $\ge$, $\le$, $\approx$, $\infty$, $\int$, $\prod$, $\sum$, $\sqrt{}$, $\partial$, $\lozenge$, $\Delta$, $\mu$, etc.).
  - International currency signs (Euro, Yen, Sterling, Dollar, etc.).
- **Punctuation & Case-Sensitive Forms (`case`):**
  - Vertically shifted punctuation and brackets optimized for all-caps and small-caps settings.
- **Production Automation Scripts:**
  - `scripts/AjustarMetricasVerticales.py`: Glyphs Python script that measures reference glyphs, aligns master metrics, and enforces Google Fonts / Type Network vertical metric specifications.
  - `scripts/Smooth2Sharp.py`: Bézier contour simplification and node handle alignment utility.
- **Multi-Format Binary Builds:**
  - Production builds generated in `builds/`: Desktop (`OTF`, `TTF`) and Web (`WOFF`, `WOFF2`).
- **QA Reports & Typographic Testing Suite:**
  - Fontbakery Type Network QA compliance report (`tests/FhSinapsis-Regular-fontbakery-typenetwork.html`).
  - Vertical metrics validation report (`tests/Sinapsis-reporte-metricas-verticales.pdf`).
  - InDesign proofing test specimen suite (`tests/InD/FhSinapsis_Regular_Font_Testing_corregido_v2.indd`, `.idml`, `.pdf`).

### Changed
- **Vertical Metrics Normalization:**
  - Harmonized `typoAscender` (935), `typoDescender` (-355), `winAscent` (1060), `winDescent` (355), and `hhea` metrics with zero line gaps, enabling `Use Typo Metrics` for cross-platform alignment stability.
- **Kerning & Spacing:**
  - Extensive audit and refinement of group kerning and sidebearing spacing across Latin lowercase, uppercase, small caps, numerals, and punctuation pairs.
- **Digitization Methodology:**
  - Updated scanning and vectorization standard to 600 DPI archival scans, AI-assisted detail reconstruction, and normalized 1000 UPM Em-square scaling.

---

## [0.1.0] - 2026-11-04
### Added
- **Repository Initialization:** Established modular repository structure engineered to professional font development standards.
- **Directory Hierarchy:**
  - `sources/` for master design sources (`Sinapsis.glyphs`).
  - `builds/` for multi-format proofing and production binaries (`otf/proof`, `ttf`, `woff/proof`, `woff2`, `release`).
  - `docs/` for comprehensive technical documentation (`00_context.md`, `01_workflow.md`, `02_nomenclature.md`, `03_releases.md`).
  - `tests/` for automated linters, rendering tests, and Fontbakery reporting.
  - `assets/` for high-resolution notebook scans, sketches, and typographic specimens.
- **Comprehensive Digitization & Vectorization Workflow:**
  - Documented 9-step pipeline spanning archival scanning, perspective correction, case segregation, ligature and contextual alternate identification, path optimization, Glyphs 3 ingestion, and OpenType scripting.
- **Open Access Legal Framework:**
  - Standard SIL Open Font License 1.1 (`LICENSE.txt`).
  - Plaintext and Markdown End User License Agreements (`EULA.md`, `EULA.txt`) confirming royalty-free Open Access terms.
  - Author and institution attribution (`CONTRIBUTORS.md`).
- **Build & Packaging Utilities:**
  - Shell packaging utility (`builds/package_release.sh`) designed to produce sanitized distribution zip archives.
