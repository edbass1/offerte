# Monitor Offerte
Sito autoaggiornato (ogni ora) con offerte e prezzi di Sky TV, DAZN (ES/DE/BE/PT), Zattoo, Teleboy, PlayStation Plus, TIMVISION e fibra (TIM, WindTre, Vodafone, Fastweb, Iliad, Sky Wifi).
- `config/services.json` – servizi e pagine fonte da monitorare (aggiungi qui nuovi servizi; `patterns` opzionali per estrarre un prezzo preciso)
- `data/offers.json` – offerte correnti (dettagli: prezzo, promo, attivazione, vincoli, chiamate, modem, velocità, fonte)
- `data/history/history.jsonl` – storico append-only (variazioni, promo passate/scadute)
- `scripts/update.py` – scraper + rigenerazione sito in `docs/`
