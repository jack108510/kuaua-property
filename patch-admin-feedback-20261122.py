"""Keep admin account identity visible and show bounded, actionable auth errors.

Does not change passwords, account IDs, visitor gates, or authorization rules.
"""
from pathlib import Path
root = Path(__file__).parent
source = root / 'assets/index-grant-20261122.js'
target = root / 'assets/index-admin-feedback-20261122.js'
s = source.read_text()
def once(old, new):
 global s
 assert s.count(old) == 1, f'Unexpected match count for {old[:60]}'
 s = s.replace(old, new, 1)
once('async function ne(re){re.preventDefault();if(!ft){l(!0);return}const{data:Oe,error:mt}=await ft.auth.signInWithPassword({email:ZH,password:s});if(!mt&&Oe.user?.id===WildeMauiAdminUid){a("");e(!0)}else{Oe.user&&await ft.auth.signOut();l(!0)}}', '''async function ne(re){
re.preventDefault();l("");
const button=re.currentTarget?.querySelector('button[type="submit"]');
if(button?.disabled)return;
if(button)button.disabled=true;
function failure(error){
 const code=String(error?.code||"");
 if(error?.status===429||/rate_limit|too_many/.test(code))return "Too many sign-in attempts. Wait a few minutes, then try again.";
 if(code==="invalid_credentials"||(error?.status===400&&/^Invalid login credentials$/i.test(String(error?.message||""))))return "The password for "+ZH+" was not accepted. This is your shared Reachr account password, not the visitor access code. Use Forgot admin password if needed.";
 if(code==="email_not_confirmed")return "Your account email must be confirmed before admin sign-in.";
 if(error?.status===401||code==="invalid_api_key")return "The authentication service rejected this site's configuration. Contact the site administrator.";
 if(!error?.status||/fetch|network|retryable/i.test(String(error?.name||"")))return "Could not reach the sign-in service. Check your connection and try again.";
 return "Admin sign-in could not be completed. Try again or use Forgot admin password.";
}
try{
 if(!ft){l("The sign-in service is unavailable. Refresh the page and try again.");return;}
 const {data:result,error}=await ft.auth.signInWithPassword({email:ZH,password:s});
 if(error){l(failure(error));return;}
 if(result?.user?.id!==WildeMauiAdminUid){
  if(result?.user)await ft.auth.signOut();
  l("This account does not have Maui administrator access.");return;
 }
 a("");e(!0);
}catch(error){l(failure(error));}
finally{if(button)button.disabled=false;}
}''')
once('children:"Use your admin account password"','children:"Sign in as "+ZH+". Uses your shared Reachr account password."')
once('children:"Admin sign-in failed. Check your password or reset it."','children:typeof r==="string"?r:"Admin sign-in failed. Use the password for "+ZH+" or reset it."')
target.write_text(s)
for page in ['index.html','admin/index.html','404.html']:
 p=root/page;html=p.read_text();assert html.count('/assets/index-grant-20261122.js')==1
 p.write_text(html.replace('/assets/index-grant-20261122.js','/assets/index-admin-feedback-20261122.js',1))
p=root/'reset-password/index.html';html=p.read_text();needle='<p id="message">Checking your recovery link…</p>';assert html.count(needle)==1
p.write_text(html.replace(needle,needle+'\n    <p>This resets the password for <strong>wildejack1010@gmail.com</strong>, the account shared by Maui admin and Reachr. It does not change the visitor access code.',1).replace('It does not change the visitor access code.\n','It does not change the visitor access code.</p>\n'))
