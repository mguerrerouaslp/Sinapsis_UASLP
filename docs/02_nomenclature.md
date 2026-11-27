# OpenType Nomenclature & Font Metadata — Sinapsis

> [**← Return to README**](../README.md) · [**00 Context**](00_context.md) · [**01 Workflow**](01_workflow.md) · [**02 Nomenclature**](02_nomenclature.md) · [**03 Releases**](03_releases.md)

---

## 1. Scope & Single-Style Architecture

Sinapsis is designed and released strictly as a single-weight typeface: **Regular** (`Fh-Sinapsis Regular`). It intentionally omits synthetic or interpolated weights (Light, Bold, Black) and Italics in order to focus with absolute typographic integrity on the authentic handwriting and drafting pen ductus of architect Juan Fernando Cárdenas Guillén.

* **Family Name (ID 1):** `Fh-Sinapsis`
* **Subfamily Name (ID 2):** `Regular`
* **Unique Font Identifier (ID 3):** `1.002;BLTY;FhSinapsis-Regular`
* **Full Font Name (ID 4):** `Fh-Sinapsis Regular`
* **Version String (ID 5):** `Version 1.002`
* **PostScript Name (ID 6):** `FhSinapsis-Regular`
* **Typographic Family Name (ID 16):** `Fh-Sinapsis`
* **Typographic Subfamily Name (ID 17):** `Regular`

---

## 2. Weight Encoding & OS/2 Table Values

Weight and width classifications in the `OS/2` table conform to OpenType specifications for a standard Regular weight:

| Parameter | Setting | Description |
| :--- | :--- | :--- |
| `usWeightClass` | `400` | Normal / Regular |
| `usWidthClass` | `5` | Medium (100% normal width) |
| `sFamilyClass` | `0` | No classification |
| `panose` | `(0, 0, 4, 0, 0, 0, 0, 0, 0, 0)` | Normal weight, proportioned ductus |
| `fsSelection` | Bit 6 (`REGULAR`), Bit 7 (`USE_TYPO_METRICS`) | Standard regular selection with typo metrics enabled |

---

## 3. Style Linking Specification

Because Sinapsis is a standalone single-style typeface:
* It does not link to separate Bold or Italic font files.
* Standard office applications (Microsoft 365, Google Docs) will identify the font as a self-contained Regular style.

---

## 4. PostScript Name Conventions (ID 6) & Binary Filenames

PostScript names do not exceed 29 characters, contain no spaces or special characters, and strictly match the compiled binary filenames:

| Format | Target Directory | Filename | PostScript Name (ID 6) |
| :--- | :--- | :--- | :--- |
| **Desktop OpenType-CFF** | `builds/otf/proof/` | `FhSinapsis-Regular.otf` | `FhSinapsis-Regular` |
| **Desktop TrueType** | `builds/ttf/` | `FhSinapsis-Regular.ttf` | `FhSinapsis-Regular` |
| **Webfont WOFF** | `builds/woff/proof/` | `FhSinapsis-Regular.woff` | `FhSinapsis-Regular` |
| **Webfont WOFF2** | `builds/woff2/` | `FhSinapsis-Regular.woff2` | `FhSinapsis-Regular` |
| **Release Archive** | `builds/release/` | `Sinapsis_v1.0.2.zip` | — |
