#!/usr/bin/env python3
"""Costruisce il report HTML di un brand reputation audit a partire da data.json.

    python3 scripts/build_report.py output/brand-2026-09-21/data.json

Inietta i dati dentro assets/report_template.html e scrive report.html accanto al
file dati. Prima di scrivere esegue un controllo di coerenza sui dati e stampa gli
avvisi: sono quasi sempre errori veri, non falsi allarmi, perche' un grafico storto
nasce quasi sempre da un totale che non torna.

Nessuna dipendenza esterna, serve solo Python 3.8 o superiore.
"""

import argparse
import json
import pathlib
import sys
import webbrowser

SENTIMENT_KEYS = ("positive", "neutral", "negative", "mixed", "unclassified")
MAX_SERIES = 5        # la palette ha cinque colori validati e non si cicla
SPARSE_THRESHOLD = 30  # sotto questa soglia le quote di un periodo non reggono


def fail(msg):
    print("ERRORE: " + msg, file=sys.stderr)
    sys.exit(1)


def check(data):
    """Controlli di coerenza. Restituisce la lista degli avvisi."""
    warn = []
    meta = data.get("meta") or {}

    for field in ("brand", "collected_at"):
        if not meta.get(field):
            warn.append("meta.%s mancante: il report esce senza un'informazione che serve a chi lo legge." % field)

    # I totali per fonte devono coincidere con il sentiment dichiarato.
    declared = {s.get("name") or s.get("id"): s.get("items")
                for s in (data.get("sources") or []) if s.get("items") is not None}
    for row in data.get("sentiment_by_source") or []:
        name = row.get("source")
        total = sum(row.get(k) or 0 for k in SENTIMENT_KEYS)
        if name in declared and declared[name] != total:
            warn.append(
                "sentiment_by_source['%s'] somma %d contenuti ma sources dichiara %d. "
                "Il lettore attento lo verifica: allinea i due numeri o spiega lo scarto."
                % (name, total, declared[name]))
        if total == 0:
            warn.append("sentiment_by_source['%s'] e' tutto a zero: togli la riga invece di mostrarla vuota." % name)

    # Le quote vanno da 0 a 1, non in percentuale.
    def ratio(path, value):
        if value is None:
            return
        if not isinstance(value, (int, float)):
            warn.append("%s non e' un numero." % path)
        elif value > 1.0001:
            warn.append("%s vale %s: le quote si esprimono da 0 a 1, e' il template a formattare in percentuale."
                        % (path, value))

    for i, t in enumerate(data.get("themes") or []):
        ratio("themes[%d].share" % i, t.get("share"))
        if not t.get("quotes"):
            warn.append("themes[%d] ('%s') non ha citazioni: sono quelle che rendono il tema credibile."
                        % (i, t.get("name", "?")))
    llm = data.get("llm") or {}
    for i, r in enumerate(llm.get("share_of_voice") or []):
        ratio("llm.share_of_voice[%d].share" % i, r.get("share"))
        if r.get("runs") and r.get("mentions") is not None and r["mentions"] > r["runs"]:
            warn.append("llm.share_of_voice[%d]: le menzioni superano le esecuzioni." % i)
    for i, r in enumerate(llm.get("by_family") or []):
        ratio("llm.by_family[%d].brand_share" % i, r.get("brand_share"))
    # La vista per canale si costruisce da sola incrociando sentiment_by_source,
    # sources e i temi: qui controlliamo solo che i nomi combacino, perche' un
    # nome scritto in due modi diversi produce un canale fantasma e uno vuoto.
    src_names = {s.get("name") or s.get("id") for s in (data.get("sources") or [])}
    chan_names = {r.get("source") for r in (data.get("sentiment_by_source") or [])}
    orphans = sorted(n for n in chan_names - src_names if n)
    if src_names and orphans:
        warn.append("Canali presenti in sentiment_by_source ma non in sources: %s. I nomi devono combaciare, "
                    "altrimenti nella vista per canale mancano periodo e note." % ", ".join(orphans))
    for name in sorted(chan_names):
        if not name:
            continue
        covered = any((t.get("by_source") or {}).get(name) for t in (data.get("themes") or []))
        if data.get("themes") and not covered:
            warn.append("Nessun tema riporta contenuti per il canale '%s': la sua scheda resta senza la parte "
                        "piu' utile, cioe' di cosa si parla li'." % name)

    for i, c in enumerate(data.get("competitors") or []):
        ratio("competitors[%d].sov" % i, c.get("sov"))
        ratio("competitors[%d].sentiment_negative" % i, c.get("sentiment_negative"))

    if llm.get("share_of_voice") and not any(r.get("is_brand") for r in llm["share_of_voice"]):
        warn.append("In llm.share_of_voice nessuna riga ha is_brand: true, quindi il brand non viene evidenziato nel grafico.")

    # Oltre cinque serie la palette dovrebbe ciclare, e i colori smettono di distinguersi.
    if len(data.get("sentiment_by_source") or []) > MAX_SERIES + 3:
        warn.append("Troppe fonti in sentiment_by_source: raggruppa le minori sotto 'Altre fonti'.")
    vot = data.get("volume_over_time") or {}
    keys = set()
    for p in vot.get("points") or []:
        keys.update((p.get("by_source") or {}).keys())
    if len(keys) > MAX_SERIES:
        warn.append("volume_over_time ha %d serie ma la palette ne regge %d: aggrega le minori sotto 'Altre fonti', "
                    "le serie oltre la quinta non verranno disegnate." % (len(keys), MAX_SERIES))

    # Cronistoria: e' la sezione che distingue l'audit da un export, e anche
    # quella dove e' piu' facile far dire ai dati cose che non dicono.
    tl = data.get("timeline") or {}
    if not tl:
        warn.append("Nessun blocco timeline: il report resta una fotografia. La cronistoria e' la parte "
                    "che mostra se il brand sta migliorando o peggiorando, ed e' quella che fa agire.")
    else:
        if not tl.get("narrative"):
            warn.append("timeline.narrative mancante: i grafici da soli non raccontano il periodo.")
        sparse_auto = []
        for i, p in enumerate(tl.get("sentiment") or []):
            total = p.get("total")
            summed = sum(p.get(k) or 0 for k in SENTIMENT_KEYS)
            if total is not None and summed and total != summed:
                warn.append("timeline.sentiment[%d] (%s): total dice %s ma le categorie sommano %d."
                            % (i, p.get("date", "?"), total, summed))
            eff = total if total is not None else summed
            if eff and eff < SPARSE_THRESHOLD and not p.get("sparse"):
                sparse_auto.append(p.get("date", "?"))
        if sparse_auto:
            warn.append("Periodi con meno di %d contenuti senza sparse: true -> %s. Marcali, altrimenti il "
                        "report presenta come tendenze quote calcolate su pochi contenuti."
                        % (SPARSE_THRESHOLD, ", ".join(sparse_auto[:6])))
        if len(tl.get("themes") or []) > MAX_SERIES:
            warn.append("timeline.themes ha %d temi ma il grafico ne disegna %d: aggrega gli altri sotto "
                        "'Altri temi'." % (len(tl["themes"]), MAX_SERIES))
        for i, t in enumerate(tl.get("themes") or []):
            for j, pt in enumerate(t.get("points") or []):
                ratio("timeline.themes[%d].points[%d].share" % (i, j), pt.get("share"))
        if (tl.get("sentiment") or tl.get("themes")) and not tl.get("milestones"):
            warn.append("timeline.milestones vuoto: ogni picco visibile va spiegato, o dichiarato inspiegato.")
        vis = tl.get("llm_visibility") or {}
        ents = set()
        for p in vis.get("points") or []:
            ents.update((p.get("by_entity") or {}).keys())
        if len(ents) > MAX_SERIES:
            warn.append("timeline.llm_visibility ha %d entita' ma il grafico ne disegna %d."
                        % (len(ents), MAX_SERIES))

    # Trascrizioni video: senza minutaggio la citazione non e' verificabile.
    vm = data.get("video_mentions") or {}
    for i, it in enumerate(vm.get("items") or []):
        if not it.get("timestamp"):
            warn.append("video_mentions.items[%d] senza timestamp: chi legge non puo' verificare la citazione." % i)
        if not it.get("quote"):
            warn.append("video_mentions.items[%d] senza quote: l'unita' di analisi e' il passaggio, non il video." % i)
        if it.get("role") and it["role"] not in ("soggetto", "confronto", "citazione"):
            warn.append("video_mentions.items[%d].role = '%s': valori ammessi soggetto, confronto, citazione."
                        % (i, it["role"]))
    if vm.get("items") and vm.get("occurrences") and len(vm["items"]) > vm["occurrences"]:
        warn.append("video_mentions: gli item elencati superano le occorrenze dichiarate.")

    # Un audit senza limiti dichiarati e' un audit che non si puo' difendere.
    method = data.get("methodology") or {}
    cap = method.get("cap") or {}
    if cap.get("requested") and cap.get("collected") and cap["collected"] > cap["requested"]:
        warn.append("methodology.cap: raccolti %s contenuti contro un tetto di %s. Il tetto e' un impegno "
                    "preso con chi paga." % (cap["collected"], cap["requested"]))
    if not method.get("limits"):
        warn.append("methodology.limits e' vuoto: i limiti dichiarati rafforzano il report, non lo indeboliscono.")

    return warn


def build(data_path, out_path=None, open_browser=False, strict=False):
    data_path = pathlib.Path(data_path).resolve()
    if not data_path.is_file():
        fail("file dati non trovato: %s" % data_path)

    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail("data.json non e' un JSON valido: %s" % e)

    template = pathlib.Path(__file__).resolve().parent.parent / "assets" / "report_template.html"
    if not template.is_file():
        fail("template non trovato in %s" % template)

    warnings = check(data)
    for w in warnings:
        print("Avviso: " + w, file=sys.stderr)
    if warnings and strict:
        fail("%d avvisi con --strict attivo: correggi data.json e rilancia." % len(warnings))

    # "</" spezzerebbe il tag script. La barra rovesciata e' un escape JSON valido.
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    brand = (data.get("meta") or {}).get("brand", "Brand")
    html = template.read_text(encoding="utf-8")
    html = html.replace("__AUDIT_DATA__", payload)
    html = html.replace("__TITLE__", "Brand Reputation Audit %s" % brand)

    out = pathlib.Path(out_path).resolve() if out_path else data_path.parent / "report.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

    size = out.stat().st_size / 1024
    print("Report scritto: %s (%.0f KB)" % (out, size))
    if size > 4096:
        print("Avviso: il report supera i 4 MB. Sposta le citazioni lunghe nei file grezzi.", file=sys.stderr)
    if open_browser:
        webbrowser.open(out.as_uri())
    return out


def main():
    ap = argparse.ArgumentParser(description="Genera il report HTML del brand reputation audit.")
    ap.add_argument("data", help="percorso di data.json")
    ap.add_argument("--out", help="percorso del file HTML da scrivere (default: report.html accanto ai dati)")
    ap.add_argument("--open", action="store_true", dest="open_browser", help="apri il report nel browser")
    ap.add_argument("--strict", action="store_true", help="interrompi se ci sono avvisi di coerenza")
    a = ap.parse_args()
    build(a.data, a.out, a.open_browser, a.strict)


if __name__ == "__main__":
    main()
