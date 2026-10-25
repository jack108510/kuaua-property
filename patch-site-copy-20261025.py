"""Remove the visitor-facing 'rental' label from the active Pages bundle.

The React source is not retained in this repository, so use exact replacements.
"""
from pathlib import Path

root = Path(__file__).parent
old_name = "index-admin-login-20261025.js"
new_name = "index-private-retreat-20261025.js"
source = root / "assets" / old_name
target = root / "assets" / new_name

bundle = source.read_text()
old_copy = 'children:"Private Rental"'
new_copy = 'children:"Private Retreat"'
if bundle.count(old_copy) != 1:
    raise RuntimeError("Expected exactly one visitor label in the active bundle")
target.write_text(bundle.replace(old_copy, new_copy, 1))

for page in (root / "index.html", root / "404.html", root / "admin/index.html"):
    html = page.read_text()
    old_src = f"/assets/{old_name}"
    if html.count(old_src) != 1:
        raise RuntimeError(f"Expected exactly one active bundle reference in {page}")
    page.write_text(html.replace(old_src, f"/assets/{new_name}", 1))
