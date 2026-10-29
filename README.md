# Demo Odoo Website Apps

A collection of standalone JavaScript apps that run inside Odoo Website code blocks.

## Apps

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
├── README.md        # This file
├── snippet.html     # Standalone pricelist app snippet
├── scripts/
│   └── publish.py   # Publish snippet to Odoo via JSON-RPC
└── task             # Task runner with `publish-app` command
```
