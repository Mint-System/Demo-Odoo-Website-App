# Demo Odoo Website Apps

A collection of standalone JavaScript apps that run inside Odoo Website code blocks.

## Apps

### Pricelist Importer

A self-contained HTML+JS app that imports a vendor pricelist CSV into Odoo products and pricelist rules.

**File:** [`pricelist-importer.html`](pricelist-importer.html)

#### How it works

1. Upload a CSV (`sku, product, price, currency`), or drag & drop it. Comma, semicolon and tab delimiters, quoted values and both `1,234.50` / `1.234,50` price formats are supported.
2. The file is parsed in the browser and previewed with per-row validation.
3. On import the app calls `/web/dataset/call_kw` to:
   - resolve (and activate) the currencies,
   - find or create the pricelist by name,
   - match products by `default_code` (SKU) and create missing ones (optional),
   - create a fixed-price `product.pricelist.item` per row.
4. A summary shows products created/updated, rules written, skipped rows and the total value.

#### Publish

```bash
./task publish-pricelist-importer
```

This creates the page `/pricelist-importer` (or updates it on re-run) and prints the URL.

#### Screenshots

| Step | Image |
| --- | --- |
| Upload | [`output/01-upload.png`](output/01-upload.png) |
| Preview | [`output/02-preview.png`](output/02-preview.png) |
| Progress | [`output/03-progress.png`](output/03-progress.png) |
| Summary | [`output/04-summary.png`](output/04-summary.png) |

### Product Pricelist Editor

A self-contained HTML+JS snippet that displays `product.pricelist` records on the Odoo website and allows inline editing of the pricelist name.

**File:** [`snippet.html`](snippet.html)

#### How it works

- The snippet is pasted into an Odoo Website **Embed Code** block.
- On page load it calls the standard Odoo JSON-RPC endpoint `/web/dataset/call_kw` to fetch pricelists.
- Because the script runs on the same origin as Odoo, the browser automatically sends the active session cookie, so the user is authenticated without extra login.
- Inline editing triggers another `call_kw` to `product.pricelist.write` to persist changes.

#### Prerequisites

- Odoo 19.0 (or compatible) with the Website and Product apps installed.
- The user must be logged into Odoo (e.g., as admin) so the session cookie is present.

#### Steps to publish

1. Open your Odoo website homepage: `http://localhost:8069/`
2. Click the **Edit** button in the top-right to enter the Website Builder.
3. Drag the **Embed Code** block from the editing panel onto the page.
4. Click the **Edit** button on the code block.
5. Replace the default HTML with the contents of [`snippet.html`](snippet.html).
6. Save the page.

Alternatively, run `./task publish-app` from the project root (requires Python 3).

The app automatically loads the pricelist data and renders an editable table.

## Structure

```text
demo-odoo-website-apps/
├── README.md                     # This file
├── pricelist-importer.html       # CSV pricelist importer app
├── snippet.html                  # Standalone pricelist editor snippet
├── input/                        # Sample vendor pricelists
├── output/                       # Screenshots of the importer steps
├── scripts/
│   ├── publish_pricelist_importer.py  # Publish the importer page
│   └── publish.py                     # Publish snippet.html (legacy)
└── task                          # Task runner
```
