const CAT_LABEL={
  "fibra":"Fibra e Internet casa",
  "pay-tv":"Pay TV / Streaming TV",
  "streaming-sport":"Sport in streaming",
  "bundle-streaming":"Bundle TIMVISION",
  "tv-streaming":"TV streaming (estero)",
  "gaming":"Gaming"
};
const CAT_ORDER=["fibra","pay-tv","streaming-sport","bundle-streaming","tv-streaming","gaming"];
const FLAG={IT:"Italia",ES:"Spagna",DE:"Germania",BE:"Belgio",PT:"Portogallo",AT:"Austria",CH:"Svizzera"};
const esc=s=>String(s??"n/d").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const $=id=>document.getElementById(id);
const today=new Date().toISOString().slice(0,10);

function card(o){
  const exp=o.promo_until&&o.promo_until<today;
  const promo=o.is_promo&&!exp;
  return `<article class="card ${promo?'promo':''}">
    <span class="badge">${esc(FLAG[o.country]||o.country)}</span>
    ${promo?'<span class="badge p">PROMO</span>':''}
    ${exp?'<span class="badge x">SCADUTA</span>':''}
    <h4>${esc(o.name)}</h4>
    ${o.promo_price?`<div class="price">${esc(o.promo_price)}</div><div class="old">per ${esc(o.promo_duration||'n/d')}, poi ${esc(o.price_after||'n/d')} · listino ${esc(o.price)}</div>`:`<div class="price">${esc(o.price)}</div>`}
    <dl>
      <dt>Attivazione</dt><dd>${esc(o.activation)}</dd>
      <dt>Vincolo</dt><dd>${esc(o.vincolo)}</dd>
      ${o.category==="fibra"?`<dt>Chiamate</dt><dd>${esc(o.calls)}</dd><dt>Modem</dt><dd>${esc(o.modem)}</dd><dt>Velocità</dt><dd>${esc(o.speed)}</dd>`:""}
      ${o.promo_until?`<dt>Valida fino</dt><dd>${esc(o.promo_until.split("-").reverse().join("/"))}</dd>`:""}
    </dl>
    ${o.notes?`<div class="note">${esc(o.notes)}</div>`:""}
    <div class="src">Verificato: ${esc(o.checked)} · <a href="${esc(o.source)}" target="_blank" rel="noopener">fonte ufficiale</a></div>
  </article>`;
}

fetch("data.json?"+Date.now()).then(r=>r.json()).then(d=>{
  if($("upd")) $("upd").textContent=d.updated;

  if($("list")){
    const cats=[...new Set(d.offers.map(o=>o.category))];
    const ctys=[...new Set(d.offers.map(o=>o.country))];
    cats.forEach(c=>$("cat").insertAdjacentHTML("beforeend",`<option value="${c}">${CAT_LABEL[c]||c}</option>`));
    ctys.forEach(c=>$("cty").insertAdjacentHTML("beforeend",`<option value="${c}">${FLAG[c]||c}</option>`));

    const render=()=>{
      const q=$("q").value.toLowerCase(), c=$("cat").value, k=$("cty").value, p=$("onlyPromo").checked;
      const f=d.offers.filter(o=>(!c||o.category===c)&&(!k||o.country===k)&&(!p||o.is_promo)&&(!q||JSON.stringify(o).toLowerCase().includes(q)));

      const pr=f.filter(o=>o.is_promo&&!(o.promo_until&&o.promo_until<today));
      $("promos").innerHTML=pr.length
        ?`<h2 class="cat">Promozioni attive (${pr.length})</h2><div class="grid">${pr.map(card).join("")}</div>`:"";

      const nw=(d.news||[]).filter(n=>(!q||JSON.stringify(n).toLowerCase().includes(q))&&(!k||n.country===k)).slice(0,10);
      if($("news")) $("news").innerHTML=nw.length
        ?`<h2 class="cat">Novità rilevate</h2><div class="news-box"><table>${nw.map(n=>`<tr><td style="white-space:nowrap">${esc((n.date||"").slice(0,10).split("-").reverse().join("/"))}</td><td><span class="badge">${esc(n.service)} ${esc(n.country||"")}</span></td><td><a href="${esc(n.source)}" target="_blank" rel="noopener">${esc(n.text)}</a></td></tr>`).join("")}</table></div>`:"";

      const order=CAT_ORDER.filter(id=>f.some(o=>o.category===id)).concat([...new Set(f.map(o=>o.category))].filter(id=>!CAT_ORDER.includes(id)));
      $("toc").innerHTML=order.map(id=>`<a href="#cat-${id}">${esc(CAT_LABEL[id]||id)}</a>`).join("");

      let html="";
      for(const cat of order){
        const items=f.filter(o=>o.category===cat);
        if(!items.length) continue;
        html+=`<section id="cat-${cat}"><h2 class="cat">${esc(CAT_LABEL[cat]||cat)} <span style="color:var(--mut);font-weight:500;font-size:.9rem">(${items.length})</span></h2>`;
        const by={};
        items.forEach(o=>{const key=o.service+(o.country&&o.category!=="fibra"&&o.category!=="bundle-streaming"?` · ${FLAG[o.country]||o.country}`:""); (by[key]=by[key]||[]).push(o);});
        Object.entries(by).forEach(([prov,list])=>{
          html+=`<h3 class="prov">${esc(prov)} (${list.length})</h3><div class="grid">${list.map(card).join("")}</div>`;
        });
        html+=`</section>`;
      }
      $("list").innerHTML=html||`<p class="empty">Nessuna offerta con questi filtri.</p>`;
    };
    ["q","cat","cty","onlyPromo"].forEach(i=>$(i).addEventListener("input",render));
    render();
  }

  if($("h")){
    const rh=()=>{
      const q=$("hq").value.toLowerCase();
      $("h").innerHTML=(d.history||[]).filter(e=>!q||JSON.stringify(e).toLowerCase().includes(q)).map(e=>
        `<tr><td>${esc((e.date||"").slice(0,16).replace("T"," "))}</td><td>${esc(e.type)}</td><td>${esc(e.service||"")} ${esc(e.country||"")}</td><td>${esc(e.text)}</td><td>${e.source?`<a href="${esc(e.source)}" target="_blank" rel="noopener">fonte</a>`:""}</td></tr>`
      ).join("")||`<tr><td colspan="5" class="empty">Nessuna voce</td></tr>`;
    };
    $("hq").addEventListener("input",rh); rh();
    if($("s")) $("s").innerHTML=(d.sources||[]).map(s=>
      `<tr><td>${esc(s.service)}</td><td>${s.ok?"OK":"Errore: "+esc(s.error||"")}${s.note?" — "+esc(s.note):""}</td><td>${s.prices_found??"-"}</td><td><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc((s.url||"").slice(0,70))}</a></td></tr>`
    ).join("");
  }
});
