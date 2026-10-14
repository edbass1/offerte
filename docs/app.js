const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const $=id=>document.getElementById(id);
if($("h")){fetch("data.json?"+Date.now()).then(r=>r.json()).then(d=>{
 const rh=()=>{const q=$("hq").value.toLowerCase();$("h").innerHTML=d.history.filter(e=>!q||JSON.stringify(e).toLowerCase().includes(q)).map(e=>`<tr><td class="nd">${esc((e.date||"").slice(0,10).split("-").reverse().join("/"))}</td><td>${esc(e.type)}</td><td>${esc(e.service)} ${esc(e.country||"")}</td><td>${esc(e.text)}</td><td>${e.source?`<a href="${esc(e.source)}" target="_blank" rel="noopener">fonte</a>`:""}</td></tr>`).join("")};
 $("hq").addEventListener("input",rh);rh();
 $("s").innerHTML=d.sources.map(s=>`<tr><td>${esc(s.service)}</td><td>${s.ok?"OK":"Errore: "+esc(s.error)}${s.note?" — "+esc(s.note):""}</td><td>${s.prices_found??"-"}</td><td><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.url.slice(0,70))}</a></td></tr>`).join("")})}
