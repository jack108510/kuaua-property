"""Give Maui its own password-only admin session; keep public booking behavior."""
from pathlib import Path
root=Path(__file__).parent
s=(root/'assets/index-admin-feedback-20261122.js').read_text()
def once(old,new):
 global s
 assert s.count(old)==1,old[:90]
 s=s.replace(old,new,1)
once('auth:{persistSession:!0,autoRefreshToken:!0,detectSessionInUrl:!1}', 'auth:{persistSession:!1,autoRefreshToken:!1,detectSessionInUrl:!1}')
once('E.useEffect(()=>{ft&&ft.auth.getUser().then(({data:re})=>{re.user?.id===WildeMauiAdminUid&&e(!0)}).catch(()=>{})},[]);', 'E.useEffect(()=>{const expired=()=>e(!1);window.addEventListener("maui-admin-expired",expired);window.MauiAdminBridge.restore().then(ok=>{if(ok)e(!0)}).catch(()=>{});return()=>window.removeEventListener("maui-admin-expired",expired)},[]);')
start=s.index('async function ne(re){');end=s.index('async function me(){',start)
s=s[:start]+'''async function ne(re){
re.preventDefault();l("");const button=re.currentTarget?.querySelector('button[type="submit"]');
if(button?.disabled)return;if(button)button.disabled=true;
try{await window.MauiAdminBridge.login(s);a("");e(!0);}catch(error){l(error.message||"Password not recognized.");}finally{if(button)button.disabled=false;}
}'''+s[end:]
once('async function me(){await ft?.auth.signOut();e(!1);a("")}', 'async function me(){window.MauiAdminBridge.logout();e(!1);a("")}')
once('children:"Sign in as "+ZH+". Uses your shared Reachr account password."', 'children:"Enter the shared Maui admin password"')
once('children:typeof r==="string"?r:"Admin sign-in failed. Use the password for "+ZH+" or reset it."','children:typeof r==="string"?r:"Password not recognized."')
once('children:"Forgot admin password?"','children:"Ask the owner for the admin password"')
s=s.replace('label:"Password",icon:eN','label:"Visitor Code",icon:eN').replace('children:"Site Password"','children:"Visitor Access Code"')
s=s.replace('ft.from(', 'MauiData(')
s='function MauiData(table){return window.MauiAdminBridge.active()?window.MauiAdminBridge.from(table):ft.from(table)}\n'+s
(root/'assets/index-shared-admin-20261122.js').write_text(s)
for name in ['index.html','admin/index.html','404.html']:
 p=root/name;html=p.read_text();assert html.count('/assets/index-admin-feedback-20261122.js')==1
 html=html.replace('    <script type="module" crossorigin src="/assets/index-admin-feedback-20261122.js"></script>','    <script src="/assets/maui-admin-client-20261122.js"></script>\n    <script type="module" crossorigin src="/assets/index-shared-admin-20261122.js"></script>',1)
 assert '/assets/maui-admin-client-20261122.js' in html
 p.write_text(html)
