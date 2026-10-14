const FLAG={IT:"Italia",ES:"Spagna",DE:"Germania",BE:"Belgio",PT:"Portogallo",AT:"Austria",CH:"Svizzera"};
const esc=s=>String(s??"n/d").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const dt=s=>s&&/^\d{4}-\d{2}(-\d{2})?/.test(s)?s.slice(0,10).split("-").reverse().join("/"):(s||"n/d");
const $=id=>document.getElementById(id);const today=new Date().toISOString().slice(0,10);
let D,st={cat:null,p:null};
const live=o=>o.is_promo&&!(o.promo_until&&o.promo_until<today);
function card(o,showProv){const exp=o.promo_until&&o.promo_until<today,pr=live(o);
 const rows=[["Attivazione",o.activation],["Vincolo",o.vincolo]];
 if(o.category==="fibra")rows.push(["Chiamate",o.calls],["Modem",o.modem],["Velocità",o.speed]);
 if(o.promo_until)rows.push(["Valida fino",dt(o.promo_until)]);
 return `<article class="card ${pr?"promo":""}"><div>${showProv?`<span class="badge">${esc(o.service)}</span>`:""}<span class="badge">${esc(FLAG[o.country]||o.country)}</span>${pr?'<span class="badge p">PROMO</span>':""}${exp?'<span class="badge x">SCADUTA</span>':""}</div>
 <h4>${esc(o.name)}</h4>${o.promo_price?`<div class="price">${esc(o.promo_price)}</div><div class="old">per ${esc(o.promo_duration)}, poi ${esc(o.price_after)} · listino ${esc(o.price)}</div>`:`<div class="price">${esc(o.price)}</div>`}
 <dl>${rows.map(([k,v])=>`<dt>${k}</dt><dd>${esc(v)}</dd>`).join("")}</dl>${o.notes?`<div class="note">${esc(o.notes)}</div>`:""}
 <div class="src">Verificato il <b>${esc(dt(o.checked))}</b> · Data fonte <b>${esc(dt(o.source_date))}</b><br><a href="${esc(o.source)}" target="_blank" rel="noopener">fonte</a>${o.extra_source?` · <a href="${esc(o.extra_source)}" target="_blank" rel="noopener">conferma</a>`:""}</div></article>`}
const grid=list=>list.length?`<div class="grid fade">${list.join("")}</div>`:`<p class="empty fade">Nessun risultato.</p>`;
function render(push=true){
 const q=$("q").value.trim().toLowerCase();const chips=$("chips"),v=$("view");
 if(q){chips.innerHTML="";const f=D.offers.filter(o=>JSON.stringify(o).toLowerCase().includes(q));
  v.innerHTML=`<h2 class="cat">Risultati per “${esc(q)}” (${f.length})</h2>`+grid(f.map(o=>card(o,true)));return}
 const c=D.cats.find(x=>x.id===st.cat);
 if(c){if(!c.providers.some(p=>p.id===st.p))st.p=c.providers[0].id;
  chips.innerHTML=c.providers.map(p=>{const n=D.offers.filter(o=>o._prov===p.id),pr=n.filter(live).length;
   return `<button role="tab" class="chip ${p.id===st.p?"on":""}" data-p="${p.id}">${esc(p.name)} <small>${n.length}</small>${pr?`<span class="dot" title="${pr} promo"></span>`:""}</button>`}).join("");
  const list=D.offers.filter(o=>o._prov===st.p).sort((a,b)=>live(b)-live(a));
  v.innerHTML=grid(list.map(o=>card(o,false)))}
 else if(st.cat==="novita"){chips.innerHTML="";
  v.innerHTML=`<h2 class="cat">Novità (ultimi 21 giorni)</h2><div class="tbl fade"><table>${D.news.map(n=>`<tr><td class="nd">${dt(n.date)}</td><td><span class="badge">${esc(n.service)} ${esc(n.country||"")}</span></td><td><a href="${esc(n.source)}" target="_blank" rel="noopener">${esc(n.text)}</a></td></tr>`).join("")}</table></div>`}
 else if(st.cat==="storico"){chips.innerHTML="";
  v.innerHTML=`<h2 class="cat">Storico variazioni e promo</h2><div class="tbl fade"><table><tr><th>Data</th><th>Tipo</th><th>Servizio</th><th>Dettaglio</th><th></th></tr>${D.history.map(e=>`<tr><td class="nd">${dt(e.date)}</td><td>${esc(e.type)}</td><td>${esc(e.service||"")} ${esc(e.country||"")}</td><td>${esc(e.text)}</td><td>${e.source?`<a href="${esc(e.source)}" target="_blank" rel="noopener">fonte</a>`:""}</td></tr>`).join("")}</table></div>
  <h2 class="cat">Stato fonti</h2><div class="tbl"><table>${D.sources.map(s=>`<tr><td>${esc(s.service)}</td><td>${s.ok?"OK":"Errore"}${s.note?" — "+esc(s.note):""}</td><td><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.url.slice(0,60))}</a></td></tr>`).join("")}</table></div>`}
 if(push)history.replaceState(null,"","#cat="+st.cat+(st.p&&c?"&p="+st.p:""));
}
function fromHash(){const h=new URLSearchParams(location.hash.slice(1));st.cat=h.get("cat")||D.cats[0].id;st.p=h.get("p");$("cat").value=st.cat}
fetch("data.json?"+Date.now()).then(r=>r.json()).then(d=>{D=d;$("upd").textContent=d.updated;
 $("cat").innerHTML=d.cats.map(c=>`<option value="${c.id}">${esc(c.label)}</option>`).join("")+`<option value="novita">📰 Novità</option><option value="storico">🕘 Storico</option>`;
 fromHash();render();
 $("cat").onchange=e=>{st.cat=e.target.value;st.p=null;$("q").value="";render()};
 $("chips").onclick=e=>{const b=e.target.closest(".chip");if(!b)return;st.p=b.dataset.p;render()};
 $("q").oninput=()=>render(false);
 window.onhashchange=()=>{fromHash();render(false)}});
