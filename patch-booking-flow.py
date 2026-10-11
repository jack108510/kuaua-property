"""Patch the retained Wilde Maui build to distinguish bookings from holds.

The original React source is unavailable in the GitHub Pages repository. Exact
replacements prevent a future bundle from silently missing this fix.
"""
from pathlib import Path

root = Path(__file__).parent
source = root / "assets/index-admin-auth-20261011.js"
target = root / "assets/index-booking-sync-20261011.js"
bundle = source.read_text()


def replace_once(old: str, new: str) -> None:
    global bundle
    count = bundle.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match, found {count}: {old[:100]}")
    bundle = bundle.replace(old, new, 1)


replace_once(
    '[ae,O]=E.useState(!1);E.useEffect(()=>{ft&&ft.auth.getUser()',
    '[ae,O]=E.useState(!1),[WildeBookingEmail,WildeSetBookingEmail]=E.useState(""),[WildeBookingGuests,WildeSetBookingGuests]=E.useState(2),[WildeConvertBlockId,WildeSetConvertBlockId]=E.useState("");E.useEffect(()=>{ft&&ft.auth.getUser()',
)

replace_once(
    'async function ie(re){if(re.preventDefault(),!(!T?.from||!T?.to)){H(!0);try{const Oe=await rL(Ut(T.from,"yyyy-MM-dd"),Ut(T.to,"yyyy-MM-dd"),N||void 0);g(mt=>[...mt,Oe].sort((Mt,Fn)=>Mt.from_date.localeCompare(Fn.from_date))),A(void 0),C(""),W("success","Dates blocked.")}catch{W("error","Failed to add. Try again.")}finally{H(!1)}}}',
    'async function ie(re){re.preventDefault();if(!T?.from||!T?.to)return;H(!0);try{if(WildeConvertBlockId&&!WildeBookingEmail.trim())throw Error("Add guest email to convert this hold.");if(WildeBookingEmail.trim()){if(!N.trim())throw Error("Enter the guest name.");const mt=v.find(Fn=>Fn.id===WildeConvertBlockId);if(WildeConvertBlockId&&(!mt||mt.from_date!==Ut(T.from,"yyyy-MM-dd")||mt.to_date!==Ut(T.to,"yyyy-MM-dd")))throw Error("Keep the original dates when converting a hold.");const Oe={id:crypto.randomUUID(),name:N.trim(),email:WildeBookingEmail.trim(),dates:`${Ut(T.from,"MMM d")} – ${Ut(T.to,"MMM d, yyyy")}`,guests:Number(WildeBookingGuests)||2,status:"confirmed",created_at:new Date().toISOString()};const{error:Fn}=await ft.from("stay_requests").insert([Oe]);if(Fn)throw Fn;let Jn=!1;if(WildeConvertBlockId)try{await oL(WildeConvertBlockId)}catch{Jn=!0}await F();W("success",Jn?"Booking saved; remove the old hold separately.":"Booking saved in Requests and dates reserved.")}else{const Oe=await rL(Ut(T.from,"yyyy-MM-dd"),Ut(T.to,"yyyy-MM-dd"),N||void 0);g(mt=>[...mt,Oe].sort((Mt,Fn)=>Mt.from_date.localeCompare(Fn.from_date)));W("success","Dates blocked.")}A(void 0);C("");WildeSetBookingEmail("");WildeSetBookingGuests(2);WildeSetConvertBlockId("")}catch(Oe){W("error",Oe.message||"Failed to save. Try again.")}finally{H(!1)}}',
)

replace_once(
    'if(await dL(re,Oe),w(mt=>mt.map(Mt=>Mt.id===re?{...Mt,status:Oe}:Mt)),Oe==="confirmed")',
    'if(await dL(re,Oe),await F(),Oe==="confirmed")',
)
replace_once(
    'await hL(re),w(Oe=>Oe.filter(mt=>mt.id!==re)),W("success","Request deleted.")',
    'await hL(re),await F(),W("success","Request deleted.")',
)
replace_once(
    'v.length===0?y.jsx("div",{"data-loc":"client/src/pages/Admin.tsx:545"',
    'v.filter(re=>re.label!=="Confirmed booking").length===0?y.jsx("div",{"data-loc":"client/src/pages/Admin.tsx:545"',
)
replace_once(
    'children:v.map(re=>y.jsxs(We.div,{"data-loc":"client/src/pages/Admin.tsx:551"',
    'children:v.filter(re=>re.label!=="Confirmed booking").map(re=>y.jsxs(We.div,{"data-loc":"client/src/pages/Admin.tsx:551"',
)
replace_once(
    '})]}),y.jsx("button",{"data-loc":"client/src/pages/Admin.tsx:565",onClick:()=>xe(re.id)',
    '})]}),y.jsx("button",{type:"button",onClick:()=>{A({from:Ir(re.from_date),to:Ir(re.to_date)});C(re.label||"");WildeSetConvertBlockId(re.id);document.getElementById("wilde-booking-form")?.scrollIntoView({behavior:"smooth",block:"center"})},className:"font-[\'Lato\'] text-xs text-teal-700 hover:underline whitespace-nowrap",children:"Record booking"}),y.jsx("button",{"data-loc":"client/src/pages/Admin.tsx:565",onClick:()=>xe(re.id)',
)
replace_once(
    'y.jsxs("form",{"data-loc":"client/src/pages/Admin.tsx:586",onSubmit:ie',
    'y.jsxs("form",{"data-loc":"client/src/pages/Admin.tsx:586",id:"wilde-booking-form",onSubmit:ie',
)
replace_once(
    'children:"Select a date range to mark as unavailable."',
    'children:"Select dates, then add a guest email to record a booking in Requests. Leave email blank for a calendar hold."',
)
replace_once(
    'children:"Label (optional)"',
    'children:"Guest name or hold label"',
)
replace_once(
    'placeholder:"e.g. Family vacation"',
    'placeholder:"e.g. Guest name or family vacation"',
)
replace_once(
    '})]}),y.jsxs("button",{"data-loc":"client/src/pages/Admin.tsx:623",type:"submit"',
    '})]}),y.jsxs("div",{children:[y.jsx("label",{className:"font-[\'Lato\'] text-[10px] tracking-[0.2em] uppercase text-[oklch(0.52_0.02_60)] block mb-1.5",children:"Guest email (for booking)"}),y.jsx("input",{type:"email",value:WildeBookingEmail,onChange:re=>WildeSetBookingEmail(re.target.value),placeholder:"guest@example.com",className:"w-full border border-[oklch(0.88_0.03_80)] rounded-md px-4 py-2.5 font-[\'Lato\'] text-sm bg-[oklch(0.97_0.015_85)]"}),WildeBookingEmail&&y.jsxs("div",{className:"mt-4",children:[y.jsx("label",{className:"font-[\'Lato\'] text-[10px] tracking-[0.2em] uppercase block mb-1.5",children:"Guests"}),y.jsx("input",{type:"number",min:1,max:20,value:WildeBookingGuests,onChange:re=>WildeSetBookingGuests(re.target.value),className:"w-full border border-[oklch(0.88_0.03_80)] rounded-md px-4 py-2.5 font-[\'Lato\'] text-sm bg-[oklch(0.97_0.015_85)]"})]})]}),y.jsxs("button",{"data-loc":"client/src/pages/Admin.tsx:623",type:"submit"',
)
replace_once(
    'z?"Saving…":"Block These Dates"',
    'z?"Saving…":WildeBookingEmail.trim()?"Record Booking":"Block These Dates"',
)
replace_once(
    'children:"Guest email (for booking)"',
    'children:WildeConvertBlockId?"Guest email (required to record this booking)":"Guest email (for booking)"',
)
replace_once(
    'WildeBookingEmail&&y.jsxs("div",{className:"mt-4",children:',
    'WildeConvertBlockId&&y.jsx("button",{type:"button",onClick:()=>{WildeSetConvertBlockId("");A(void 0);C("");WildeSetBookingEmail("")},className:"mt-2 text-xs text-teal-700 hover:underline",children:"Cancel conversion"}),WildeBookingEmail&&y.jsxs("div",{className:"mt-4",children:',
)

target.write_text(bundle)
old_src = "/assets/index-admin-auth-20261011.js"
new_src = "/assets/index-booking-sync-20261011.js"
for page_path in (root / "index.html", root / "404.html"):
    page = page_path.read_text()
    if page.count(old_src) == 1:
        page_path.write_text(page.replace(old_src, new_src, 1))
    elif page.count(new_src) != 1:
        raise RuntimeError(f"Expected one bundle reference in {page_path.name}")
