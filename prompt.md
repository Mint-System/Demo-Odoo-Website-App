---
title: "Pricelist Importer"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: draft
date_completed: YYYY-MM-DD
harness:
provider:
model:
input_tokens:
output_tokens:
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

The app allows me to upload a pricelsit in the format of `input/vendor_pricelist.csv`.

Create an Odoo website page "Pricelist Importer" and embed the Code on this page.

After the import the app gives a summary.
@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness, provider and model. If you have access to session info also add token count.
