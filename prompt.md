---
title: "Pricelist Importer"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-11-09
harness: pi
provider: deepseek
model: deepseek-v4-1-flash-1017
input_tokens: 991991
output_tokens: 58698
---

# Pricelist Importer

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

Every month I receive a pricelist from a Vendor and would like to import it into Odoo.

Please create an Odoo Website App (HTML/CSS/JavaScript) that helps importing the pricelist into Odoo.

### Access 

My Odoo instance is running at:

Url: http://localhost:8069  
Database: 19.0  
Username: admin  
Password: admin  

I have installed the `website` module.

### Pricelist App

Create an HTML/CSS/JavaScript-App and create a script to embed it on the Odoo website.

The app allows me to upload a pricelist in the format of `input/vendor_pricelist.csv`. Here is an example:

```csv
sku,product,price,currency
P001,Table,100,CHF
P002,Chair,50,CHF
P003,Desk,75,CHF
```

Create an Odoo website page "Pricelist Importer" and embed the Code on this page.

After the import the app must show a summary.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

Implemented the Pricelist Importer website app.

**App** – `pricelist-importer.html`, a self-contained HTML/CSS/JS snippet with four steps:

1. **Upload** – click or drag & drop, 2 MB limit, configurable pricelist name and an "create missing products" toggle.
2. **Preview** – client-side CSV parsing with per-row validation (missing SKU/product, invalid price/currency). Supports `,`/`;`/tab delimiters, quoted values, BOM and both `1,234.50` and `1.234,50` price formats.
3. **Progress** – progress bar while rows are imported sequentially.
4. **Summary** – products created/updated, pricelist rules written, skipped rows with reasons, resolved currencies, total value per currency.

**Import logic** – via `/web/dataset/call_kw` on the same origin (session cookie): resolves and activates currencies, finds or creates the pricelist by name, matches products on `default_code` (SKU), creates missing products, then writes a fixed-price `product.pricelist.item` (`applied_on=1_product`, `compute_price=fixed`) per row.

**Publishing** – `scripts/publish_pricelist_importer.py` creates or updates the `website.page` `/pricelist-importer` (QWeb view `website.pricelist_importer`) with an `s_embed_code` snippet. Wired as `./task publish-pricelist-importer`. Re-running is idempotent. The script normalises void tags and boolean attributes for Odoo's XML arch validation.

**Verification**

- Page published and served with HTTP 200; rendered app script passes `node --check`.
- CSV parser unit-tested in Node against the sample file and edge cases.
- RPC flow replayed against Odoo: 3 products created, 3 pricelist rules written, summary correct.
- Full UI flow driven in headless Chromium via CDP: upload → preview → import → summary, for both the "products created" and "products already exist" paths, plus the reset action.
- Screenshots of each step (app card only) stored in `output/`.
- All test data (pricelists, products, rules, currency activation) cleaned up afterwards.

**Notes**

- Odoo validates view arch as XML: `<` inside `<script>` must be written as `&lt;` and `&&` as `&amp;&amp;`. Documented in `AGENTS.md`.
- The legacy `publish-app` task now points at the renamed `scripts/publish_pricelist.py`.

Verify at <http://localhost:8069/pricelist-importer>.
