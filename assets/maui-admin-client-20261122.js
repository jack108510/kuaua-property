(function(){
'use strict';
const BASE='https://wildemaui-admin-api.wildejack1010.chatgpt.site';
const KEY='wilde_maui_admin_session_v1';
function saved(){try{return JSON.parse(sessionStorage.getItem(KEY)||'null');}catch{return null;}}
function expire(){sessionStorage.removeItem(KEY);window.dispatchEvent(new Event('maui-admin-expired'));}
async function call(path,body,token){
 let response;try{response=await fetch(BASE+path,{method:body?'POST':'GET',headers:{'Content-Type':'application/json',...(token?{Authorization:'Bearer '+token}:{})},...(body?{body:JSON.stringify(body)}:{}),signal:AbortSignal.timeout(20000)});}catch{throw Error('Could not reach Maui admin. Check your connection and try again.');}
 const result=await response.json().catch(()=>({error:{message:'Maui admin returned an unexpected response.'}}));
 if(!response.ok){if(token&&response.status===401)expire();throw Object.assign(Error(result.error?.message||'Maui admin request failed.'),{status:response.status,code:result.error?.code});}
 return result;
}
class Query {
 constructor(table){this.body={table,op:'select',filters:[]};this.pending=null;}
 select(columns='*'){this.body.columns=columns;return this;}
 insert(values){this.body.op='insert';this.body.values=values;return this;}
 upsert(values,options={}){this.body.op='upsert';this.body.values=values;this.body.onConflict=options.onConflict;return this;}
 update(values){this.body.op='update';this.body.values=values;return this;}
 delete(){this.body.op='delete';return this;}
 eq(column,value){this.body.filters.push([column,value]);return this;}
 order(column,options={}){this.body.order={column,ascending:options.ascending!==false};return this;}
 maybeSingle(){this.body.one=true;return this;}
 then(resolve,reject){if(!this.pending)this.pending=call('/query',this.body,saved()?.token).catch(error=>({data:null,error:{message:error.message,code:error.code||'NETWORK_ERROR',status:error.status}}));return this.pending.then(resolve,reject);}
}
window.MauiAdminBridge=Object.freeze({
 active:()=>!!saved()?.token,
 async login(password){const result=await call('/login',{password});sessionStorage.setItem(KEY,JSON.stringify(result));return true;},
 async restore(){const session=saved();if(!session?.token)return false;if(session.expires_at*1000<=Date.now()){expire();return false;}try{await call('/session',null,session.token);return true;}catch{return false;}},
 logout:expire,
 from:table=>new Query(table)
});
})();
