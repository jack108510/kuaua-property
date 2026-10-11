"""Patch the retained Manus build to use Supabase Auth for /admin.

The source project is not in this Pages repository; keep replacements exact so
a changed upstream build fails loudly instead of silently restoring the old gate.
"""
from pathlib import Path

root = Path(__file__).parent
source = root / "assets/index-0548bf05cc.js"
target = root / "assets/index-admin-auth-20261011.js"
pages = [root / "index.html", root / "404.html"]
bundle = source.read_text()


def replace_once(old: str, new: str) -> None:
    global bundle
    count = bundle.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match, found {count}: {old[:80]}")
    bundle = bundle.replace(old, new, 1)


replace_once(
    "auth:{persistSession:!1,autoRefreshToken:!1,detectSessionInUrl:!1}",
    "auth:{persistSession:!0,autoRefreshToken:!0,detectSessionInUrl:!1}",
)
replace_once(
    "const ZH=xs;",
    'const ZH="wildejack1010@gmail.com",WildeMauiAdminUid="45717c8c-08f9-469f-bf7d-2fa2ef5ad441";',
)
replace_once(
    ";function W(re,Oe){M({type:re,msg:Oe})",
    ";E.useEffect(()=>{ft&&ft.auth.getUser().then(({data:re})=>{re.user?.id===WildeMauiAdminUid&&e(!0)}).catch(()=>{})},[]);function W(re,Oe){M({type:re,msg:Oe})",
)
replace_once(
    'function ne(re){re.preventDefault(),s===ZH?e(!0):(l(!0),setTimeout(()=>{l(!1),a("")},600))}',
    'async function ne(re){re.preventDefault();if(!ft){l(!0);return}const{data:Oe,error:mt}=await ft.auth.signInWithPassword({email:ZH,password:s});if(!mt&&Oe.user?.id===WildeMauiAdminUid){a("");e(!0)}else{Oe.user&&await ft.auth.signOut();l(!0);setTimeout(()=>{l(!1),a("")},600)}}',
)
replace_once(
    'function me(){e(!1),a("")}',
    'async function me(){await ft?.auth.signOut();e(!1);a("")}',
)

target.write_text(bundle)
old_src = "/assets/index-0548bf05cc.js"
for html in pages:
    page = html.read_text()
    if page.count(old_src) != 1:
        raise RuntimeError(f"Expected one active bundle reference in {html.name}")
    html.write_text(page.replace(old_src, "/assets/index-admin-auth-20261011.js", 1))
