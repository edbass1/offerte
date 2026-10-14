#!/usr/bin/env python3
"""Aggiorna le offerte: scarica le pagine ufficiali, estrae i prezzi (best-effort),
rileva cambiamenti, aggiorna lo storico e rigenera il sito in docs/."""
import json, re, hashlib, datetime, pathlib, sys, html
from zoneinfo import ZoneInfo
import requests
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = ROOT / "config/services.json"
OFFERS = ROOT / "data/offers.json"
SNAP = ROOT / "data/snapshots.json"
HIST = ROOT / "data/history/history.jsonl"
LOG = ROOT / "data/last_run.json"
DOCS = ROOT / "docs"
TZ = ZoneInfo("Europe/Rome")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
      "Accept-Language": "it-IT,it;q=0.9,en;q=0.8"}
PRICE_RE = re.compile(r"(?:€\s?\d{1,4}(?:[.,]\d{2})?|\d{1,4}[.,]\d{2}\s?(?:€|EUR|euro)|CHF\s?\d{1,4}(?:[.,]\d{2})?)", re.I)
PROMO_RE = re.compile(r"(anzich[ée]|invece di|promo|sconto|offerta valida|oferta|promoci[óo]n|angebot|rabatt|campanha|desconto|aanbieding|offre)", re.I)

def now(): return datetime.datetime.now(TZ)
def load(p, d):
    try: return json.loads(p.read_text())
    except Exception: return d

def fetch_text(url):
    r = requests.get(url, headers=UA, timeout=25)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for t in soup(["script", "style", "noscript", "svg"]): t.decompose()
    return re.sub(r"\s+", " ", soup.get_text(" "))

def norm(p): return re.sub(r"\s+", "", p).replace("EUR", "€").replace("euro", "€")

def main():
    cfg, data, snaps = load(CFG, {}), load(OFFERS, {"offers": []}), load(SNAP, {})
    offers = {o["id"]: o for o in data["offers"]}
    ts = now()
    events, log = [], {"run": ts.isoformat(), "sources": []}
    for svc in cfg.get("services", []):
        for src in svc.get("sources", []):
            url = src["url"]; entry = {"service": svc["name"], "url": url}
            try:
                text = fetch_text(url)
                prices = sorted({norm(p) for p in PRICE_RE.findall(text)})
                promo_hits = len(PROMO_RE.findall(text))
                entry.update(ok=True, prices_found=len(prices), promo_words=promo_hits)
                old = snaps.get(url)
                if prices:
                    if old and set(old["prices"]) != set(prices):
                        added = sorted(set(prices) - set(old["prices"])); removed = sorted(set(old["prices"]) - set(prices))
                        events.append(dict(date=ts.isoformat(), type="pagina_prezzi_cambiati", service=svc["name"], source=url,
                                           text=f"Nuovi importi: {', '.join(added[:15]) or '-'} | Rimossi: {', '.join(removed[:15]) or '-'}",
                                           offer_ids=src.get("offer_ids", [])))
                    snaps[url] = {"prices": prices, "checked": ts.isoformat(), "promo_words": promo_hits}
                else:
                    entry["note"] = "nessun prezzo nel testo (pagina dinamica?) - mantenuti ultimi valori noti"
                for oid, rx in (src.get("patterns") or {}).items():
                    m = re.search(rx, text, re.I | re.S)
                    if m and oid in offers:
                        val = m.group(1).strip(); o = offers[oid]
                        if o.get("scraped_price") and o["scraped_price"] != val:
                            events.append(dict(date=ts.isoformat(), type="variazione_prezzo", offer_id=oid, service=svc["name"],
                                               text=f"{o['name']}: {o['scraped_price']} → {val}", source=url))
                        o["scraped_price"] = val; o["scraped_at"] = ts.isoformat()
                    elif oid in offers:
                        entry.setdefault("pattern_fail", []).append(oid)
                for oid in src.get("offer_ids", []):
                    if oid in offers: offers[oid]["source_ok"] = ts.isoformat()
            except Exception as e:
                entry.update(ok=False, error=str(e)[:200])
            log["sources"].append(entry)
    # promo scadute
    today = ts.date().isoformat()
    for o in offers.values():
        if o.get("promo_until") and o["promo_until"] < today and not o.get("expired_logged"):
            o["expired_logged"] = True
            events.append(dict(date=ts.isoformat(), type="promo_scaduta", offer_id=o["id"], service=o["service"],
                               text=f"{o['name']}: promo {o.get('promo_price') or ''} scaduta il {o['promo_until']}", source=o["source"]))
    HIST.parent.mkdir(parents=True, exist_ok=True)
    with open(HIST, "a") as f:
        for e in events: f.write(json.dumps(e, ensure_ascii=False) + "\n")
    data["offers"] = list(offers.values()); data["updated"] = ts.isoformat()
    OFFERS.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    SNAP.write_text(json.dumps(snaps, ensure_ascii=False, indent=1))
    log["events"] = len(events); LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1))
    build_site(data, log)
    ok = sum(1 for s in log["sources"] if s.get("ok")); print(f"fonti ok {ok}/{len(log['sources'])}, eventi {len(events)}")

def build_site(data, log):
    import build_site as b
    b.build(ROOT, data, log)

if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    main()
