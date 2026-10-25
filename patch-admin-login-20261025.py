"""Make /admin use only its Supabase login and expose account recovery.

The React source is not retained in this Pages repository. Keep all replacements
exact so a future bundle change fails instead of silently changing the wrong UI.
"""
from pathlib import Path

root = Path(__file__).parent
source = root / "assets/index-availability-ipad-20261011.js"
target = root / "assets/index-admin-login-20261025.js"
bundle = source.read_text()


def replace_once(old: str, new: str) -> None:
    global bundle
    count = bundle.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match, found {count}: {old[:90]}")
    bundle = bundle.replace(old, new, 1)


# The rental site password is a separate visitor gate. An administrator should
# reach the Supabase sign-in without entering that site's access code first.
replace_once(
    'E.useState(()=>sessionStorage.getItem(n1)==="1")',
    'E.useState(()=>sessionStorage.getItem(n1)==="1"||location.pathname==="/admin"||location.pathname==="/admin/")',
)

# Keep failed sign-in feedback visible and clear it when the user retries.
replace_once(
    'else{Oe.user&&await ft.auth.signOut();l(!0);setTimeout(()=>{l(!1),a("")},600)}',
    'else{Oe.user&&await ft.auth.signOut();l(!0)}',
)
replace_once(
    'value:s,onChange:re=>a(re.target.value),autoFocus:!0,placeholder:"Password"',
    'value:s,onChange:re=>{a(re.target.value);l(!1)},autoFocus:!0,placeholder:"Password"',
)
replace_once(
    'children:"Enter password"}),y.jsxs("form",{"data-loc":"client/src/pages/Admin.tsx:364"',
    'children:"Use your admin account password"}),y.jsxs("form",{"data-loc":"client/src/pages/Admin.tsx:364"',
)
replace_once(
    'children:"Sign in"})]}),y.jsx("div",{"data-loc":"client/src/pages/Admin.tsx:394"',
    'children:"Sign in"}),r&&y.jsx("p",{role:"alert",className:"font-[\'Lato\'] text-xs text-red-300 text-center",children:"Admin sign-in failed. Check your password or reset it."}),y.jsx("a",{href:"/reset-password/",className:"font-[\'Lato\'] text-xs text-white/60 hover:text-white text-center underline",children:"Forgot admin password?"})]}),y.jsx("div",{"data-loc":"client/src/pages/Admin.tsx:394"',
)

target.write_text(bundle)
old_src = "/assets/index-availability-ipad-20261011.js"
new_src = "/assets/index-admin-login-20261025.js"
for page_path in (root / "index.html", root / "404.html"):
    page = page_path.read_text()
    if page.count(old_src) != 1:
        raise RuntimeError(f"Expected one active bundle reference in {page_path.name}")
    page_path.write_text(page.replace(old_src, new_src, 1))
