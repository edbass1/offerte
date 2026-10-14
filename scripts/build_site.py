import json, datetime
from zoneinfo import ZoneInfo
def build(root, data, log):
    docs = root / "docs"; docs.mkdir(exist_ok=True)
    hist = []
    p = root / "data/history/history.jsonl"
    if p.exists():
        hist = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    hist.sort(key=lambda e: e.get("date", ""), reverse=True)
    upd = datetime.datetime.fromisoformat(data["updated"]).astimezone(ZoneInfo("Europe/Rome"))
    out = {"updated": upd.strftime("%d/%m/%Y %H:%M") + " (ora di Roma)", "offers": data["offers"],
           "history": hist, "sources": log.get("sources", []),
           "news": (json.loads((root/"data/news.json").read_text())["items"][:60] if (root/"data/news.json").exists() else [])}
    (docs / "data.json").write_text(json.dumps(out, ensure_ascii=False))
    (docs / ".nojekyll").write_text("")
