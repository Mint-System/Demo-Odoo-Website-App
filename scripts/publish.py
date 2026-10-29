#!/usr/bin/env python3
"""Publish snippet.html into the Odoo website embed code block.

ir.ui.view.save expects the REPLACEMENT content for the given xpath,
not the full view arch.
"""

import json
import sys
import urllib.request

BASE_URL = "http://localhost:8069"
DB = "19.0"
LOGIN = "admin"
PASSWORD = "admin"
VIEW_ID = 1545
XPATH = "/t[1]/t[1]/div[1]"


def rpc(path, params, session_id=None):
    """Perform a JSON-RPC call."""
    body = json.dumps(
        {"jsonrpc": "2.0", "method": "call", "params": params, "id": 1}
    ).encode()
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    if session_id:
        req.add_header("Cookie", f"session_id={session_id}")

    with urllib.request.urlopen(req, timeout=30) as resp:
        new_sid = session_id
        if not session_id:
            for cookie in resp.info().get_all("Set-Cookie") or []:
                if "session_id=" in cookie:
                    new_sid = cookie.split("session_id=")[1].split(";")[0]
        result = json.loads(resp.read().decode())
        return result, new_sid


def wrap_snippet(snippet):
    """Build the replacement <div id="wrap"> content."""
    return (
        '<div id="wrap" class="oe_structure oe_empty"'
        ' data-oe-model="ir.ui.view"'
        f' data-oe-id="{VIEW_ID}"'
        ' data-oe-field="arch"'
        f' data-oe-xpath="{XPATH}"'
        ' data-editor-message-default="true"'
        ' data-editor-message="ZIEHEN SIE BAUSTEINE HIERHER">'
        '  <section class="s_embed_code pt16 pb16 o_colored_level text-center"'
        ' data-snippet="s_embed_code" data-name="Code einbetten">'
        '    <template class="s_embed_code_saved">\n'
        f"      {snippet}\n"
        '    </template>'
        '    <div class="s_embed_code_embedded container o_not_editable">\n'
        f"      {snippet}\n"
        '    </div>'
        '  </section>'
        '</div>'
    )


def main(snippet_path):
    # 1. Authenticate
    result, sid = rpc(
        "/web/session/authenticate",
        {"db": DB, "login": LOGIN, "password": PASSWORD},
    )
    if result.get("error"):
        print("Auth failed:", result["error"], file=sys.stderr)
        return 1

    uid = result["result"]["uid"]
    print(f"Authenticated as user {uid}")

    # 2. Read snippet
    with open(snippet_path, "r", encoding="utf-8") as fh:
        snippet = fh.read().strip()

    # 3. Build replacement content (ONLY the xpath node, not full arch)
    value = wrap_snippet(snippet)

    # 4. Save view
    result, sid = rpc(
        "/web/dataset/call_kw",
        {
            "model": "ir.ui.view",
            "method": "save",
            "args": [VIEW_ID, value, XPATH],
            "kwargs": {
                "context": {
                    "lang": "de_CH",
                    "tz": "Europe/Zurich",
                    "uid": uid,
                    "allowed_company_ids": [1],
                    "website_id": 1,
                    "delay_translations": True,
                }
            },
        },
        sid,
    )

    if result.get("error"):
        print("Save failed:", result["error"], file=sys.stderr)
        return 1

    print("Published successfully.")
    return 0


if __name__ == "__main__":
    snippet_file = sys.argv[1] if len(sys.argv) > 1 else "snippet.html"
    sys.exit(main(snippet_file))
