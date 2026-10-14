import json, datetime, re, html, shutil
from zoneinfo import ZoneInfo
CAT = [("fibra","Fibra e Internet casa"),("pay-tv","Pay TV / Streaming TV"),("streaming-sport","Sport in streaming"),
       ("bundle-streaming","Bundle TIMVISION"),("tv-streaming","TV streaming (estero)"),("gaming","Gaming")]
FLAG = {"IT":"Italia","ES":"Spagna","DE":"Germania","BE":"Belgio","PT":"Portogallo","AT":"Austria","CH":"Svizzera"}
e = lambda s: html.escape(str(s if s not in (None,"") else "n/d"))
def dt(s): return "/".join(reversed(s.split("-"))) if s and re.match(r"^\d{4}-\d{2}(-\d{2})?$", s) else (s or "n/d")
def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
def prov_of(o):
    multi = o["category"] in ("streaming-sport","tv-streaming")
    name = o["service"] + (f" {FLAG.get(o['country'],o['country'])}" if multi else "")
    return name, slug(o["service"] + (f"-{o['country']}" if multi else ("-fibra" if o["category"]=="fibra" and o["service"] in ("TIM",) else "")))
def page(title, body, upd, depth=0, active=""):
    r = "../"*depth
    nav = "".join(f'<a class="{"on" if active==k else ""}" href="{r}{h}">{t}</a>' for k,h,t in
                  [("home","index.html","Categorie"),("novita","novita.html","Novità"),("storico","storico.html","Storico")])
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark"><title>{e(title)} – Monitor Offerte</title><link rel="stylesheet" href="{r}style.css"></head><body>
<header><div class="wrap"><div class="top"><h1><a href="{r}index.html" style="color:#fff;text-decoration:none">Monitor <span>Offerte</span></a></h1>
<nav>{nav}</nav><div class="upd">Ultimo aggiornamento: <b>{e(upd)}</b></div></div></div></header>
<main class="wrap">{body}</main><footer>Solo offerte da fonti ufficiali o fonti locali recenti, con data. Aggiornamento automatico ogni ora · “n/d” = dato non trovato.</footer>
<button class="totop l" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑ Sali su</button><button class="totop r" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑ Sali su</button>
<script src="{r}app.js"></script></body></html>'''
def card(o, today):
    exp = o.get("promo_until") and o["promo_until"] < today; pr = o.get("is_promo") and not exp
    rows = [("Attivazione",o.get("activation")),("Vincolo",o.get("vincolo"))]
    if o["category"]=="fibra": rows += [("Chiamate",o.get("calls")),("Modem",o.get("modem")),("Velocità",o.get("speed"))]
    if o.get("promo_until"): rows.append(("Valida fino",dt(o["promo_until"])))
    price = (f'<div class="price">{e(o["promo_price"])}</div><div class="old">per {e(o.get("promo_duration"))}, poi {e(o.get("price_after"))} · listino {e(o["price"])}</div>'
             if o.get("promo_price") else f'<div class="price">{e(o["price"])}</div>')
    extra = f' · <a href="{e(o["extra_source"])}" target="_blank" rel="noopener">conferma</a>' if o.get("extra_source") else ""
    return f'''<article class="card {"promo" if pr else ""}"><span class="badge">{e(FLAG.get(o["country"],o["country"]))}</span>{'<span class="badge p">PROMO</span>' if pr else ''}{'<span class="badge x">SCADUTA</span>' if exp else ''}
<h4>{e(o["name"])}</h4>{price}<dl>{"".join(f"<dt>{k}</dt><dd>{e(v)}</dd>" for k,v in rows)}</dl>
{f'<div class="note">{e(o["notes"])}</div>' if o.get("notes") else ""}
<div class="src">Verificato il: <b>{e(dt(o.get("checked")))}</b> · Data fonte: <b>{e(dt(o.get("source_date")))}</b><br><a href="{e(o["source"])}" target="_blank" rel="noopener">fonte</a>{extra}</div></article>'''
def build(root, data, log):
    docs = root/"docs"; docs.mkdir(exist_ok=True); (docs/"p").mkdir(exist_ok=True)
    for f in (docs/"p").glob("*.html"): f.unlink()
    hist = []
    hp = root/"data/history/history.jsonl"
    if hp.exists(): hist = [json.loads(l) for l in hp.read_text().splitlines() if l.strip()]
    hist.sort(key=lambda x: x.get("date",""), reverse=True)
    now = datetime.datetime.now(ZoneInfo("Europe/Rome")); today = now.date().isoformat()
    upd = datetime.datetime.fromisoformat(data["updated"]).astimezone(ZoneInfo("Europe/Rome")).strftime("%d/%m/%Y %H:%M") + " (ora di Roma)"
    news = json.loads((root/"data/news.json").read_text())["items"] if (root/"data/news.json").exists() else []
    (docs/"data.json").write_text(json.dumps({"updated":upd,"history":hist,"sources":log.get("sources",[])}, ensure_ascii=False))
    (docs/".nojekyll").write_text("")
    offers = data["offers"]; provs = {}
    for o in offers:
        n, s = prov_of(o); provs.setdefault(s, {"name":n,"cat":o["category"],"offers":[]})["offers"].append(o)
    # index
    body = '<p class="lead">Scegli una categoria e poi l\'operatore per vedere le sue offerte.</p><nav class="toc">' + \
           "".join(f'<a href="#cat-{c}">{t}</a>' for c,t in CAT if any(p["cat"]==c for p in provs.values())) + "</nav>"
    for c,t in CAT:
        ps = sorted([(s,p) for s,p in provs.items() if p["cat"]==c], key=lambda x: x[1]["name"])
        if not ps: continue
        body += f'<section id="cat-{c}"><h2 class="cat">{t}</h2><div class="pgrid">'
        for s,p in ps:
            npromo = sum(1 for o in p["offers"] if o.get("is_promo") and not (o.get("promo_until") and o["promo_until"]<today))
            body += (f'<a class="pcard" href="p/{s}.html"><span class="pname">{e(p["name"])}</span>'
                     f'<span class="pmeta">{len(p["offers"])} offerte{f" · <b class=pp>{npromo} promo</b>" if npromo else ""}</span></a>')
        body += "</div></section>"
    (docs/"index.html").write_text(page("Categorie", body, upd, 0, "home"))
    # provider pages
    for s,p in provs.items():
        ct = dict(CAT).get(p["cat"], p["cat"])
        os_ = sorted(p["offers"], key=lambda o: (not o.get("is_promo"), o["name"]))
        pn = [n for n in news if n["service"] in p["name"] or p["name"].startswith(n["service"])][:8]
        b = (f'<p class="back"><a href="../index.html#cat-{p["cat"]}">← Torna a {e(ct)}</a></p><h2 class="cat">{e(p["name"])} <small>({len(os_)} offerte)</small></h2>'
             f'<div class="grid">{"".join(card(o,today) for o in os_)}</div>')
        if pn: b += '<h3 class="prov">Novità recenti</h3><div class="news-box"><table>' + "".join(
            f'<tr><td class="nd">{e(dt(n["date"][:10]))}</td><td><a href="{e(n["source"])}" target="_blank" rel="noopener">{e(n["text"])}</a></td></tr>' for n in pn) + "</table></div>"
        (docs/"p"/f"{s}.html").write_text(page(p["name"], b, upd, 1))
    # novita
    b = '<h2 class="cat">Novità rilevate (ultimi 21 giorni)</h2><p class="lead">Articoli da testate locali di ciascun paese, filtrati per data di pubblicazione.</p><div class="news-box"><table><thead><tr><th>Data</th><th>Servizio</th><th>Titolo</th></tr></thead>' + \
        "".join(f'<tr><td class="nd">{e(dt(n["date"][:10]))}</td><td><span class="badge">{e(n["service"])} {e(n.get("country",""))}</span></td><td><a href="{e(n["source"])}" target="_blank" rel="noopener">{e(n["text"])}</a></td></tr>' for n in news) + "</table></div>"
    (docs/"novita.html").write_text(page("Novità", b, upd, 0, "novita"))
    b = ('<h2 class="cat">Storico variazioni e promo</h2><div class="ctrl"><input id="hq" placeholder="Filtra storico…"></div><div class="news-box"><table><thead><tr><th>Data</th><th>Tipo</th><th>Servizio</th><th>Dettaglio</th><th>Fonte</th></tr></thead><tbody id="h"></tbody></table></div>'
         '<h2 class="cat">Stato fonti ultimo controllo</h2><div class="news-box"><table><thead><tr><th>Servizio</th><th>Esito</th><th>Prezzi</th><th>URL</th></tr></thead><tbody id="s"></tbody></table></div>')
    (docs/"storico.html").write_text(page("Storico", b, upd, 0, "storico"))
