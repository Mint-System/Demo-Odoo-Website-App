---
title: "Init Odoo Website App"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: review
date_completed: 2026-10-29
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens: 43000
output_tokens: 18000
---

# Init Odoo Website App

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

This is a test.

I have an Odoo instance running:

Url: http://localhost:8069
Database: 19.0
Username: admin
Password: admin

I have prepared an Odoo website site: http://localhost:8069/

On the website I have added a code block to embed html. I click on "Edit" on the code block I see:

```html
<div class="alert alert-info mb-0">
    In der rechten Leiste auf <b>„Bearbeiten“</b> klicken, um diesen mit Ihrem eigenen HTML-Code zu ersetzen.
</div>
```

As I understand I can create a JavaScript-App and embed it here.

Please create a simple app that shows the "product.pricelist" records. Moreover the app should make it possible to edit the pricelist name.

Document the steps you took to create this app and how you published the app to the website.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

- Created a standalone HTML+JS snippet (`snippet.html`) that uses vanilla JavaScript and `fetch` to call Odoo's standard `/web/dataset/call_kw` JSON-RPC endpoint.
- The snippet displays `product.pricelist` records in a Bootstrap-styled table and supports inline name editing via `product.pricelist.write`.
- Authentication is handled automatically by the browser's session cookie (same-origin policy).
- Tested the JSON-RPC endpoints with curl to verify search and write operations work.
- Documented the exact steps to embed the snippet into an Odoo Website **Embed Code** block in `README.md`.
- Initially created an Odoo module as an alternative approach, then removed it after clarifying the requirement for a pure JS snippet.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness and model. If you have access to session info also add token count.

