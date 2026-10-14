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
    hist = []
    hp = root/"data/history/history.jsonl"
    if hp.exists(): hist = [json.loads(l) for l in hp.read_text().splitlines() if l.strip()]
    hist.sort(key=lambda x: x.get("date",""), reverse=True)
    upd = datetime.datetime.fromisoformat(data["updated"]).astimezone(ZoneInfo("Europe/Rome")).strftime("%d/%m/%Y %H:%M") + " (ora di Roma)"
    news = json.loads((root/"data/news.json").read_text())["items"] if (root/"data/news.json").exists() else []
    offers = data["offers"]; provs = {}
    for o in offers:
        n, s = prov_of(o); o["_prov"] = s
        provs.setdefault(s, {"id":s,"name":n,"cat":o["category"]})
    cats = [{"id":c,"label":t,"providers":sorted([p for p in provs.values() if p["cat"]==c], key=lambda p:p["name"])} for c,t in CAT]
    cats = [c for c in cats if c["providers"]]
    (docs/"data.json").write_text(json.dumps({"updated":upd,"offers":offers,"cats":cats,"news":news,"history":hist,
        "sources":log.get("sources",[])}, ensure_ascii=False))
    (docs/".nojekyll").write_text("")
    for f in (docs/"p").glob("*.html"): f.unlink()
    for p in provs.values():
        (docs/"p"/f"{p['id']}.html").write_text(f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../index.html#cat={p["cat"]}&p={p["id"]}"><script>location.replace("../index.html#cat={p["cat"]}&p={p["id"]}")</script>')
    for old in ("novita","storico"):
        (docs/f"{old}.html").write_text(f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=index.html#cat={old}"><script>location.replace("index.html#cat={old}")</script>')
