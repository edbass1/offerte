const CAT={"pay-tv":"Pay TV","streaming-sport":"Streaming sport","tv-streaming":"TV in streaming","gaming":"Gaming","bundle-streaming":"Bundle streaming","fibra":"Fibra casa"};
const FLAG={IT:"🇮🇹 Italia",ES:"🇪🇸 Spagna",DE:"🇩🇪 Germania",BE:"🇧🇪 Belgio",PT:"🇵🇹 Portogallo",AT:"🇦🇹 Austria",CH:"🇨🇭 Svizzera"};
const esc=s=>String(s??"n/d").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const $=id=>document.getElementById(id);
const today=new Date().toISOString().slice(0,10);
function card(o){const exp=o.promo_until&&o.promo_until<today;
return `<div class="card ${o.is_promo&&!exp?'promo':''}"><span class="badge">${esc(FLAG[o.country]||o.country)}</span><span class="badge">${esc(CAT[o.category]||o.category)}</span>${o.is_promo&&!exp?'<span class="badge p">PROMO</span>':''}${exp?'<span class="badge x">SCADUTA</span>':''}
<h3>${esc(o.name)}</h3>${o.promo_price?`<div class="price">${esc(o.promo_price)}</div><div class="old">per ${esc(o.promo_duration)}, poi ${esc(o.price_after)} · listino ${esc(o.price)}</div>`:`<div class="price">${esc(o.price)}</div>`}
<dl><dt>Attivazione</dt><dd>${esc(o.activation)}</dd><dt>Vincolo</dt><dd>${esc(o.vincolo)}</dd>${o.category=="fibra"?`<dt>Chiamate</dt><dd>${esc(o.calls)}</dd><dt>Modem</dt><dd>${esc(o.modem)}</dd><dt>Velocità</dt><dd>${esc(o.speed)}</dd>`:""}
${o.promo_until?`<dt>Valida fino</dt><dd>${esc(o.promo_until.split("-").reverse().join("/"))}</dd>`:""}${o.notes?`<dt>Note</dt><dd>${esc(o.notes)}</dd>`:""}${o.scraped_price?`<dt>Rilevato auto</dt><dd>${esc(o.scraped_price)}</dd>`:""}</dl>
<div class="src">Verificato: ${esc(o.checked)} · <a href="${esc(o.source)}" target="_blank" rel="noopener">fonte</a></div></div>`}
fetch("data.json?"+Date.now()).then(r=>r.json()).then(d=>{$("upd").textContent=d.updated;
 if($("list")){const cats=[...new Set(d.offers.map(o=>o.category))],ctys=[...new Set(d.offers.map(o=>o.country))];
  cats.forEach(c=>$("cat").insertAdjacentHTML("beforeend",`<option value="${c}">${CAT[c]||c}</option>`));
  ctys.forEach(c=>$("cty").insertAdjacentHTML("beforeend",`<option value="${c}">${FLAG[c]||c}</option>`));
  const render=()=>{const q=$("q").value.toLowerCase(),c=$("cat").value,k=$("cty").value,p=$("onlyPromo").checked;
   const f=d.offers.filter(o=>(!c||o.category==c)&&(!k||o.country==k)&&(!p||o.is_promo)&&(!q||JSON.stringify(o).toLowerCase().includes(q)));
   const pr=f.filter(o=>o.is_promo&&!(o.promo_until&&o.promo_until<today));
   $("promos").innerHTML=pr.length?`<h2>🔥 Promozioni attive (${pr.length})</h2><div class="grid">${pr.map(card).join("")}</div>`:"";
   const by={};f.forEach(o=>(by[o.service]=by[o.service]||[]).push(o));
   $("list").innerHTML=Object.entries(by).map(([s,l])=>`<h2>${esc(s)} (${l.length})</h2><div class="grid">${l.map(card).join("")}</div>`).join("")||"<p>Nessun risultato.</p>"};
  ["q","cat","cty","onlyPromo"].forEach(i=>$(i).addEventListener("input",render));render()}
 if($("h")){const rh=()=>{const q=$("hq").value.toLowerCase();$("h").innerHTML=d.history.filter(e=>!q||JSON.stringify(e).toLowerCase().includes(q)).map(e=>`<tr><td>${esc((e.date||"").slice(0,16).replace("T"," "))}</td><td>${esc(e.type)}</td><td>${esc(e.service)} ${esc(e.country||"")}</td><td>${esc(e.text)}</td><td>${e.source?`<a href="${esc(e.source)}" target="_blank">link</a>`:""}</td></tr>`).join("")};
  $("hq").addEventListener("input",rh);rh();
  $("s").innerHTML=d.sources.map(s=>`<tr><td>${esc(s.service)}</td><td>${s.ok?"✅ ok":"⚠️ "+esc(s.error)}${s.note?" – "+esc(s.note):""}</td><td>${s.prices_found??"-"}</td><td><a href="${esc(s.url)}" target="_blank">${esc(s.url.slice(0,70))}</a></td></tr>`).join("")}});
