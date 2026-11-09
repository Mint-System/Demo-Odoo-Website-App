#!/usr/bin/env python3
"""Create or update the "Pricelist Importer" page on the Odoo website.

The page embeds the contents of pricelist-importer.html inside a standard
`s_embed_code` snippet. Running the script twice updates the same page.
"""

import json
import os
import re
import sys
import urllib.request

BASE_URL = os.environ.get("ODOO_URL", "http://localhost:8069")
DB = os.environ.get("ODOO_DB", "19.0")
LOGIN = os.environ.get("ODOO_LOGIN", "admin")
PASSWORD = os.environ.get("ODOO_PASSWORD", "admin")

PAGE_NAME = "Pricelist Importer"
PAGE_URL = "/pricelist-importer"
PAGE_KEY = "website.pricelist_importer"
VIEW_KEY = "website.pricelist_importer"

ARCH_TEMPLATE = """<t name="{name}" t-name="{key}">
    <t t-call="website.layout">
        <div id="wrap" class="oe_structure oe_empty">
            <section class="s_embed_code pt32 pb32 o_colored_level" data-snippet="s_embed_code" data-name="Embed Code">
                <template class="s_embed_code_saved">
{snippet}
                </template>
                <div class="s_embed_code_embedded container o_not_editable">
{snippet}
                </div>
            </section>
        </div>
    </t>
</t>
"""


def rpc(path, params, session_id=None):
    """Perform a JSON-RPC call and return (result, session_id)."""
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(
            {"jsonrpc": "2.0", "method": "call", "params": params, "id": 1}
        ).encode(),
        headers={"Content-Type": "application/json"},
    )
    if session_id:
        req.add_header("Cookie", f"session_id={session_id}")

    with urllib.request.urlopen(req, timeout=60) as resp:
        sid = session_id
        for cookie in resp.info().get_all("Set-Cookie") or []:
            if "session_id=" in cookie:
                sid = cookie.split("session_id=")[1].split(";")[0]
        payload = json.loads(resp.read().decode())

    if payload.get("error"):
        message = payload["error"].get("data", {}).get("message") or payload["error"]["message"]
        raise RuntimeError(message)
    return payload["result"], sid


def login():
    """Authenticate and return the session id."""
    result, sid = rpc(
        "/web/session/authenticate",
        {"db": DB, "login": LOGIN, "password": PASSWORD},
    )
    return result["uid"], sid


def call_kw(sid, model, method, args, kwargs=None):
    """Shortcut for /web/dataset/call_kw."""
    result, sid = rpc(
        "/web/dataset/call_kw",
        {"model": model, "method": method, "args": args, "kwargs": kwargs or {}},
        sid,
    )
    return result, sid


def to_xml(content):
    """Make the HTML snippet parseable as XML (Odoo view arch is XML)."""
    content = re.sub(r"<(input|br|img|hr|meta|link)\b([^>]*?)/?>", r"<\1\2/>", content)
    return re.sub(
        r"\s(checked|disabled|selected|readonly)(?=[\s/>])", r' \1="1"', content
    )


def read_snippet(path):
    """Return the snippet indented for the view arch."""
    with open(path, "r", encoding="utf-8") as fh:
        content = to_xml(fh.read().strip())
    return "\n".join(f"                    {line}" for line in content.splitlines())


def find_page(sid):
    """Return the existing website page record for PAGE_URL, if any."""
    pages, sid = call_kw(
        sid,
        "website.page",
        "search_read",
        [[("url", "=", PAGE_URL)], ["id", "name", "view_id", "website_id"]],
        {"limit": 1, "context": {"active_test": False}},
    )
    return (pages[0] if pages else None), sid


def update_page(sid, page, arch):
    """Write the arch to the page view and refresh its metadata."""
    view_id = page["view_id"][0]
    _, sid = call_kw(sid, "ir.ui.view", "write", [[view_id], {"arch": arch}])
    _, sid = call_kw(
        sid,
        "website.page",
        "write",
        [[page["id"]], {"name": PAGE_NAME, "website_published": True}],
    )
    return view_id, sid


def create_page(sid, arch):
    """Create the page view and its website.page record."""
    website_id = 1
    view_id, sid = call_kw(
        sid,
        "ir.ui.view",
        "create",
        [
            {
                "name": PAGE_NAME,
                "key": VIEW_KEY,
                "type": "qweb",
                "mode": "primary",
                "arch": arch,
                "website_id": website_id,
            }
        ],
    )
    page_id, sid = call_kw(
        sid,
        "website.page",
        "create",
        [
            {
                "name": PAGE_NAME,
                "url": PAGE_URL,
                "view_id": view_id,
                "website_id": website_id,
                "is_published": True,
                "website_indexed": True,
            }
        ],
    )
    return view_id, page_id, sid


def main(snippet_path):
    """Publish the snippet and return an exit code."""
    uid, sid = login()
    print(f"Authenticated as user {uid} on {BASE_URL} (db {DB})")

    arch = ARCH_TEMPLATE.format(
        name=PAGE_NAME, key=PAGE_KEY, snippet=read_snippet(snippet_path)
    )

    page, sid = find_page(sid)
    if page:
        view_id, sid = update_page(sid, page, arch)
        print(f"Updated page {PAGE_URL} (page #{page['id']}, view #{view_id}).")
    else:
        view_id, page_id, sid = create_page(sid, arch)
        print(f"Created page {PAGE_URL} (page #{page_id}, view #{view_id}).")

    print(f"Open {BASE_URL}{PAGE_URL}")
    return 0


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    snippet_file = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.join(project_root, "pricelist-importer.html")
    )
    sys.exit(main(snippet_file))
