"""Dati iniziali verificati manualmente il 2026-10-14. Eseguire una sola volta (o per reimpostare)."""
import json, pathlib
D = "2026-10-14"
ND = "n/d"
def o(id, service, cat, country, name, price, promo_price=None, promo_duration=None, price_after=None,
      activation=ND, vincolo=ND, calls=ND, modem=ND, speed=ND, notes="", source="", promo_until=None):
    return dict(id=id, service=service, category=cat, country=country, name=name, price=price,
                promo_price=promo_price, promo_duration=promo_duration, price_after=price_after,
                activation=activation, vincolo=vincolo, calls=calls, modem=modem, speed=speed,
                notes=notes, source=source, checked=D, promo_until=promo_until,
                is_promo=promo_price is not None)
SKY="https://www.sky.it/offerte"
SKYSC="https://www.sky.it/offerte/sky-sport-sky-calcio-insieme"
DES="https://www.dazn.com/es-ES/help/articles/16184063399709-planes-precios-y-contenidos-de-dazn"
DESW="https://www.dazn.com/es-ES/welcome"
DDE="https://www.dazn.com/de-DE/help/articles/16184063399709-dazn-plane-und-preise"
DDEP="https://www.dazn.com/de-DE/news/fussball/dazn-angebot-zur-champions-league-jetzt-unlimited-fuer-2499-euro-sichern/175va0epjd8z31wm00qk8bx2p4"
DBE="https://www.dazn.com/en-BE/help/articles/16184063399709-dazn-plans-and-pricing"
DPT="https://www.dazn.com/pt-PT/help/articles/16184063399709-planos-e-precos-dazn"
PS="https://www.mondomobileweb.it/320325-playstation-plus-aumento-di-prezzo-per-tutti-i-piani-in-versione-mensile-e-trimestrale/"
TV="https://www.tim.it/offerte-tv"
SEL="https://selectra.net/internet/guida/offerte/fibra-ottica"
offers = [
 # SKY TV ITALIA
 o("sky-tv-calcio-sport","Sky TV","pay-tv","IT","Sky TV + Sky Sport + Sky Calcio (Sky Smart)","59,90 €/mese (listino)","37,99 €/mese","18 mesi","59,90 €/mese (listino Sky Open)",
   activation="19 €", vincolo="18 mesi (Sky Smart); recesso anticipato = restituzione sconti", notes="Promo 1 anno Amazon Prime in regalo (06/10–08/11/2026)", source=SKYSC, promo_until="2026-10-25"),
 o("sky-tv-calcio-cinema","Sky TV","pay-tv","IT","Sky TV + Sky Calcio + Sky Cinema (Sky Smart)","33 €/mese (listino)","19,90 €/mese","18 mesi","33 €/mese",
   vincolo="18 mesi (Sky Smart)", notes="Include Paramount+ in Sky Cinema", source="https://www.sky.it/tv/sky-calcio", promo_until="2026-10-25"),
 o("sky-tv-sport","Sky TV","pay-tv","IT","Sky TV + Sky Sport","51,90 €/mese (listino)","29,99 €/mese","18 mesi","51,90 €/mese",
   vincolo="18 mesi (Sky Smart)", notes="Sky TV 14,90 € (anziché 25 €) + Sky Sport 15,09 € (anziché 26,90 €)", source="https://www.sky.it/tv/sky-calcio", promo_until="2026-10-25"),
 o("sky-tv-netflix","Sky TV","pay-tv","IT","Intrattenimento Plus (Sky TV + Netflix Std con pubblicità)","31,99 €/mese","16,99 €/mese","18 mesi","31,99 €/mese",
   vincolo="18 mesi (Sky Smart)", notes="Con Netflix Standard 23,99 € (anziché 38,99 €); Premium 29,99 € (anziché 44,99 €)", source=SKY, promo_until="2026-10-25"),
 o("sky-glass-plus-cinema-calcio","Sky TV","pay-tv","IT","Sky Glass: Intrattenimento Plus + Cinema + Calcio","53,99 €/mese (31,99+14+8)","26,98 €/mese","18 mesi","listino Sky Open",
   vincolo="18 mesi", notes="33,98 € con Netflix Standard, 39,98 € con Premium; Sky Sport aggiungibile a 22,90 € (anziché 26,90 €)",
   source="https://assets.contentstack.io/v3/assets/blta6c52b9cd5519be3/blt6fcd00c0e78c8200/6ab3de3358e0687e0788233b/SkySmart_SkyGlass_OffertaSpeciale_IntrattenimentoPlus_SkyCinema_SkyCalcio_28092026.pdf", promo_until="2026-10-25"),
 o("sky-stream-wifi","Sky TV","pay-tv","IT","Sky TV + Cinema (Sky Stream, per chi attiva Sky Wifi)","39 €/mese (25+14)","15 €/mese","18 mesi","39 €/mese",
   vincolo="18 mesi", notes="Sky TV 10 € + Cinema 5 €; Calcio +8 €, Sport +22,90 €",
   source="https://assets.contentstack.io/v3/assets/blta6c52b9cd5519be3/blt542d685bce191bb0/6ab3de4bace1f2dd26cde92c/SkySmart_SkyStream_perclientichesottoscrivonoSkyWifi_OF_SkyTV_SkyCinema_28092026.pdf", promo_until="2026-11-30"),
 # DAZN SPAGNA
 *[o(f"dazn-es-{k}","DAZN","streaming-sport","ES",f"DAZN {n}",f"{m} €/mese (mensile) · {a} €/mese (annuale rate) · {u} € (annuale unico)",
     pp, "12 mesi" if pp else None, f"{a} €/mese" if pp else None, activation="0 €", vincolo="Mensile: preavviso 30 gg; annuale: 12 mesi",
     calls="—", modem="—", speed="—", notes=nt, source=DESW if pp else DES)
   for k,n,m,a,u,pp,nt in [("futbol","Fútbol","29,99","19,99","219,99","14,99 €/mese (annuale)","Promo sito ufficiale"),
                       ("motor","Motor","29,99","19,99","219,99",None,""),
                       ("premium","Premium","44,99","31,99","351,99","25,99 €/mese (annuale)","Promo sito ufficiale"),
                       ("baloncesto","Baloncesto","14,99","9,99","109,99",None,""),
                       ("usa","Made in USA","7,99","4,99","54,99",None,"")]],
 # DAZN GERMANIA
 o("dazn-de-mobile","DAZN","streaming-sport","DE","DAZN Mobile Pass","9,99 €/mese (flessibile)",activation="0 €",vincolo="nessuno (preavviso 30 gg)",calls="—",modem="—",speed="—",notes="Solo smartphone",source=DDE),
 o("dazn-de-super","DAZN","streaming-sport","DE","DAZN Super Sports","24,99 €/mese flessibile · 19,99 €/mese annuale",activation="0 €",vincolo="annuale 12 mesi",calls="—",modem="—",speed="—",notes="Senza Champions League",source=DDE),
 o("dazn-de-unlimited","DAZN","streaming-sport","DE","DAZN Unlimited","44,99 €/mese flessibile · 34,99 €/mese annuale","24,99 €/mese","24 mesi","n/d",activation="0 €",vincolo="24 mesi",calls="—",modem="—",speed="—",notes="Offerta Champions League pubblicata 13/10/2026",source=DDEP),
 o("dazn-de-unlimited-plus","DAZN","streaming-sport","DE","DAZN Unlimited Plus","54,99 €/mese (solo annuale)",activation="0 €",vincolo="12 mesi",calls="—",modem="—",speed="—",source=DDE),
 # DAZN BELGIO
 o("dazn-be-total","DAZN","streaming-sport","BE","DAZN Total","29,99 €/mese flessibile · 24,99 €/mese (12 mesi)",activation="0 €",vincolo="12 mesi o flessibile (30 gg)",calls="—",modem="—",speed="—",
   notes="Alcune fonti indicano 34,99 € per il flessibile. Pass extra: NFL da 9,99 €, Rally TV 10,99 €",source=DBE),
 # DAZN PORTOGALLO
 o("dazn-pt-motores","DAZN","streaming-sport","PT","DAZN Motores","9,99 €/mese · 7,99 €/mese annuale rate · 79,99 €/anno",activation="0 €",vincolo="mensile o 12 mesi",calls="—",modem="—",speed="—",source=DPT),
 o("dazn-pt-base","DAZN","streaming-sport","PT","DAZN Base","21,99 €/mese · 17,99 €/mese annuale rate · 189,99 €/anno",activation="0 €",vincolo="mensile o 12 mesi",calls="—",modem="—",speed="—",
   notes="Fonti terze (04/10/2026) indicano 24,99 / 19,99 / 199,99 € dopo l'aumento di agosto 2026: verificare",source=DPT),
 o("dazn-pt-total","DAZN","streaming-sport","PT","DAZN Total","30,99 €/mese · 25,99 €/mese annuale rate · 249,99 €/anno",activation="0 €",vincolo="mensile o 12 mesi",calls="—",modem="—",speed="—",source=DPT),
 # ZATTOO / TELEBOY
 o("zattoo-de-smart","Zattoo","tv-streaming","DE","Zattoo Smart HD","6,99 €/mese",source="https://zattoo.com/de/en/offers",calls="—",modem="—",speed="—",notes="Non disponibile in Italia"),
 o("zattoo-de-premium","Zattoo","tv-streaming","DE","Zattoo Premium","9,99 €/mese",source="https://zattoo.com/de/en/offers",calls="—",modem="—",speed="—"),
 o("zattoo-de-ultimate","Zattoo","tv-streaming","DE","Zattoo Ultimate","13,99 €/mese",source="https://zattoo.com/de/en/offers",calls="—",modem="—",speed="—"),
 o("zattoo-at-premium","Zattoo","tv-streaming","AT","Zattoo Premium","11,99 €/mese",source="https://zattoo.com/at/en/offers",calls="—",modem="—",speed="—"),
 o("zattoo-at-ultimate","Zattoo","tv-streaming","AT","Zattoo Ultimate","14,99 €/mese",source="https://zattoo.com/at/en/offers",calls="—",modem="—",speed="—"),
 o("teleboy-tv","Teleboy","tv-streaming","CH","Teleboy TV","CHF 14.90/mese","CHF 11.90/mese","permanente (sconto 20%)","CHF 14.90",calls="—",modem="—",speed="—",notes="Lo sconto esclude la funzione Skip-Ad",source="https://www.teleboy.ch/tv"),
 # PLAYSTATION PLUS
 *[o(f"psplus-{k}","PlayStation Plus","gaming","IT",f"PS Plus {n}",f"{m} €/mese · {t} €/3 mesi · {y} €/anno",activation="0 €",vincolo="nessuno (rinnovo automatico)",calls="—",modem="—",speed="—",
     notes="Prezzi mensili/trimestrali aumentati dal 20/05/2026; annuale invariato",source=PS)
   for k,n,m,t,y in [("essential","Essential","9,99","27,99","71,99"),("extra","Extra","15,99","43,99","125,99"),("premium","Premium","18,99","54,99","151,99")]],
 # TIM
 o("timvision-base","TIM","bundle-streaming","IT","TIMVISION (Netflix + HBO Max)","14,99 €/mese","8 €/mese","12 mesi","14,99 €/mese",source=TV,calls="—",modem="—",speed="—"),
 o("timvision-m","TIM","bundle-streaming","IT","TIMVISION M (+ Disney+)","18,99 €/mese","12 €/mese","12 mesi","18,99 €/mese",source=TV,calls="—",modem="—",speed="—"),
 o("timvision-l","TIM","bundle-streaming","IT","TIMVISION L (+ Amazon Prime)","20,99 €/mese","14 €/mese","12 mesi","20,99 €/mese",source=TV,calls="—",modem="—",speed="—"),
 o("timvision-m-myclub","TIM","bundle-streaming","IT","TIMVISION M + DAZN MyClubPass","n/d","27 €/mese","12 mesi","n/d",source=TV,calls="—",modem="—",speed="—"),
 o("timvision-l-myclub","TIM","bundle-streaming","IT","TIMVISION L + DAZN MyClubPass","n/d","29 €/mese","12 mesi","n/d",source=TV,calls="—",modem="—",speed="—"),
 o("timvision-m-dazn","TIM","bundle-streaming","IT","TIMVISION M + DAZN Full","n/d","42 €/mese","12 mesi","n/d",source=TV,calls="—",modem="—",speed="—"),
 o("timvision-l-dazn","TIM","bundle-streaming","IT","TIMVISION L + DAZN Full","n/d","44 €/mese","12 mesi","n/d",source=TV,calls="—",modem="—",speed="—"),
 o("timvision-dazn-prime","TIM","bundle-streaming","IT","TIMVISION con DAZN e Prime","36,99 €/mese","29,99 €/mese","8 mesi","36,99 €/mese",calls="—",modem="—",speed="—",
   notes="Fonte stampa (TecnoAndroid)",source="https://www.tecnoandroid.it/news/timvision-con-dazn-e-prime-sconto-per-8-mesi-da-2499-euro-1982326/"),
 o("timvision-myclub-prime","TIM","bundle-streaming","IT","TIMVISION con MyClubPass e Prime","29,99 €/mese","24,99 €/mese","8 mesi","29,99 €/mese",calls="—",modem="—",speed="—",
   notes="Fonte stampa (TecnoAndroid)",source="https://www.tecnoandroid.it/news/timvision-con-dazn-e-prime-sconto-per-8-mesi-da-2499-euro-1982326/"),
 # FIBRA
 o("tim-wifi-casa","TIM","fibra","IT","TIM WiFi Casa","29,90 €/mese",activation="39,90 €",vincolo="24 mesi",calls="n/d",modem="incluso",speed="fino a 2,5 Gbps (FTTH)",
   notes="Promo WiFi Casa + TV in scadenza 24/10/2026",source="https://www.tim.it/fisso-e-mobile/fibra-e-adsl/fibra-calcio"),
 o("tim-premium-base","TIM","fibra","IT","TIM Premium Base","25,90 €/mese",vincolo="24 mesi (prezzo bloccato)",calls="No (a consumo 0,19 €/min + 0,19 € scatto)",modem="incluso",speed="1 Gbps / 300 Mbps",source=SEL,promo_until="2026-10-31"),
 o("windtre-super-fibra","WindTre","fibra","IT","WindTre Super Fibra","29,99 €/mese","24,99 €/mese","12 mesi","29,99 €/mese",activation="1,99 €/mese x 24 mesi",vincolo="24 mesi; anticipo modem 10 €",
   calls="No (a consumo, 0,23 € scatto)",modem="incluso (anticipo 10 €)",speed="2,5 Gbps / 500 Mbps",notes="Amazon Prime 12 mesi + Giga illimitati su SIM WindTre",
   source="https://www.windtre.it/Document/trasparenza-tariffaria/privati/fisso/20261001/20261001_zip_Allegato%20_1_del%20252_SUPER_FIBRA.pdf"),
 o("vodafone-casa-start","Vodafone","fibra","IT","Vodafone Casa Start","27,95 €/mese",activation="0 €",vincolo="nessuno",modem="Vodafone Station inclusa",speed="fino a 2,5 Gbps",source=SEL,promo_until="2026-10-31"),
 o("vodafone-casa-pro","Vodafone","fibra","IT","Vodafone Casa Pro","29,95 €/mese",modem="Vodafone Station inclusa",speed="fino a 2,5 Gbps",source=SEL),
 o("fastweb-casa-start","Fastweb","fibra","IT","Fastweb Casa Start","27,95 €/mese",activation="0 €",vincolo="nessuno",modem="FASTGate incluso",speed="fino a 2,5 Gbps",source=SEL),
 o("fastweb-casa-pro","Fastweb","fibra","IT","Fastweb Casa Pro","29,95 €/mese",vincolo="nessuno",calls="Sì, illimitate nazionali",modem="incluso (comodato)",speed="2,5 Gbps / 300 Mbps",source=SEL),
 o("fastweb-casa-ultra","Fastweb","fibra","IT","Fastweb Casa Ultra","36,95 €/mese",vincolo="nessuno",calls="Sì, illimitate nazionali",modem="incluso (comodato)",speed="2,5 Gbps / 300 Mbps",source=SEL),
 o("iliadbox","Iliad","fibra","IT","Iliadbox","26,99 €/mese (22,99 € per clienti mobile Iliad)",vincolo="nessuno",calls="Sì, illimitate fissi e mobili nazionali",modem="incluso (comodato gratuito)",speed="5 Gbps / 700 Mbps (solo FTTH)",
   source="https://www.iliad.it/scopri-offerte-internet-casa.html"),
 o("iliadbox-super","Iliad","fibra","IT","Iliadbox Super","34,99 €/mese (29,99 € clienti mobile)",vincolo="nessuno",modem="incluso",speed="n/d",source=SEL),
 o("sky-wifi-fibra","Sky Wifi","fibra","IT","Sky Wifi Fibra 100%","19,90 €/mese",activation="gratuita",vincolo="24 mesi",modem="Sky Hub",speed="FTTH Open Fiber (fino a 1 Gbps)",
   source="https://assets.contentstack.io/v3/assets/blta6c52b9cd5519be3/bltb9a7e1413f65c87b/6abe09c66464887150ec945e/NOWWIFI_19_90_OF_20261001.pdf"),
]
# Storico: promo passate/retroattive trovate con fonte
past = [
 dict(date="2026-08-15", type="promo_passata", offer_id="dazn-es-futbol", service="DAZN", country="ES",
      text="Promo inizio LaLiga: Plan Fútbol anuale a 14,99 €/mese fino al 20/09/2026 (anziché 19,99 €); Fútbol anuale pagamento unico 164,99 €; Premium annuale 285,99 € (anziché 351,99 €)",
      source="https://cincodias.elpais.com/companias/2026-08-15/los-operadores-encarecen-hasta-un-5-el-precio-del-futbol-en-television-ante-el-arranque-de-laliga.html"),
 dict(date="2026-07-27", type="promo_passata", offer_id="dazn-be-total", service="DAZN", country="BE",
      text="Start of season offer: da 14,99 €/mese per 3 mesi, poi 24,99 € per 9 mesi (27/07–21/09/2026, solo nuovi clienti, vincolo 12 mesi)", source=DBE),
 dict(date="2026-07-30", type="promo_passata", offer_id="dazn-be-total", service="DAZN", country="BE",
      text="Mobile Vikings DAZN Viking Pass: 30 €/mese con 5 € di sconto in bolletta = 25 € netti, senza vincolo",
      source="https://callmepower.be/fr/telecom/actualites/mobile-vikings-dazn-viking-pass-foot-belge"),
 dict(date="2026-08-01", type="variazione_prezzo", offer_id="dazn-pt-base", service="DAZN", country="PT",
      text="Aumento DAZN Base su MEO dal 01/08/2026: +3 € mensile, +2 € annuale", source="https://conteudos.meo.pt/meo/Documentos/Ajuda-Suporte/20260629_AumentoPre%C3%A7osCanaisDesporto.pdf"),
 dict(date="2026-05-20", type="variazione_prezzo", offer_id="psplus-essential", service="PlayStation Plus", country="IT",
      text="Aumento prezzi PS Plus mensili e trimestrali (annuali invariati)", source=PS),
 dict(date="2026-04-17", type="promo_passata", offer_id="dazn-be-total", service="DAZN", country="BE",
      text="End of Season Pass a 49,99 € (pagamento unico) valido fino al 17/04/2026", source="https://www.dazn.com/nl-BE/help/articles/16184063399709-dazn-plannen-en-prijzen"),
]
root = pathlib.Path(__file__).resolve().parent.parent
(root/"data/offers.json").write_text(json.dumps({"offers": offers}, ensure_ascii=False, indent=1))
with open(root/"data/history/history.jsonl","w") as f:
    for p in past: f.write(json.dumps(p, ensure_ascii=False)+"\n")
print(len(offers), "offerte")
