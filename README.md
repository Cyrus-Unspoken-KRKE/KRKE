# Cyrus Unspoken

**A small, reproducible KRKE project about source-grounded tacit roles in accounts of Cyrus the Great.**

The research question is: **How can explicit narrated actions be connected to implicit portrayals of a historical figure without treating those portrayals as historical facts?**

The package contains 14 short, original English paraphrases linked to passages in the Cyrus Cylinder, Herodotus, and Xenophon; a small OWL ontology; phrase-based explicit action extraction; three role rules and three bounded implication examples; historical and narrator context; a source-grounded RDF graph; six SPARQL questions; a transparent internal evaluation; and an offline evidence browser.

## Start here

1. Double-click `web/index.html` to explore the evidence in any modern browser. Internet is only needed if you click external source links.
2. Read `docs/professor_feedback.md` and `docs/report.md` for the academic explanation, then `docs/presentation.md` for the defense.
3. Inspect `data/excerpts.csv`, `ontology/cyrus_unspoken.ttl`, and `output/query_results.md`.

## Rebuild from source files

From the root of this extracted folder:

```bash
python -m pip install -r requirements.txt
python src/build.py
python src/run_queries.py
python src/make_web.py
```

On Windows, `py -m pip install -r requirements.txt` and `py src/build.py` may be needed. If PowerShell blocks a launcher, use Command Prompt. `web/index.html` and all generated RDF/queries are already in the zip, so no installation is needed simply to review the project. Open `ontology/cyrus_unspoken.ttl` or `output/combined.ttl` in Protégé; query `output/combined.ttl` with the bundled Python runner or an RDF tool.

## Folder map

| Path | Purpose |
|---|---|
| `data/sources.csv` | The three works and editions |
| `data/excerpts.csv` | Paraphrases, line/section references, source links, provisional human labels |
| `data/historical_context.csv`, `data/narrator_context.csv` | Time and social setting of the narrated events; later narrator's time and viewpoint |
| `src/build.py` | Detects explicit action cues, applies three role rules, builds graphs and evaluates |
| `ontology/cyrus_unspoken.ttl` | Classes, properties, individuals and rule descriptions |
| `output/explicit.ttl` | Detected excerpts/actions with provenance |
| `output/inferred.ttl` | Materialized source-specific depictions |
| `output/combined.ttl` | Ontology plus explicit and inferred triples |
| `queries/*.sparql` | Five competency questions |
| `output/query_results.md` | Their actual local results |
| `output/predictions.csv`, `output/implications.csv`, `output/evaluation.json` | Internal demonstration evaluation and three bounded implications |
| `web/index.html` | Self-contained evidence browser |
| `docs/` | Report, talk notes, contribution and approval checklist |

## Precise scope

- The corpus comprises **paraphrases of cited passages**, not verbatim primary-source excerpts or an ancient-language processing system.
- `IdealRuler` is a deliberately narrow teaching label inferred from selected relief, mercy, care and reward actions; another scholar can disagree.
- The six rules are **Python graph materialization rules**. Three assign roles and three illustrate a prior condition or possible impact. Protégé's OWL reasoner alone will not execute the Python rules or generate `inferred.ttl`.
- The contextual notes are human interpretations, supported by linked editions and collection essays. The program displays them for critical review; it does **not** automatically prove which societal expectation governed a narrator or modify the role rules on that basis.
- The namespace `https://example.org/cyrus-unspoken/` is illustrative and does not claim a published endpoint. The Web-ready, self-contained page can be hosted as static files after group review.
- The labels and rules were prepared by the same author. The reported 14/14 agreement is a **sanity check on this designed corpus**, not independent evidence of model accuracy on unseen passages.
- Professor Gangemi approved the topic on 1 October 2026 and suggested considering historical and narrator context. Group names, real division of work and any course-specific submission format still need group review.

## Provenance and reuse

This project builds on the **domain and workflow** of Saman Abdolrashidi's earlier Cyrus LODLAM project. It does not copy its dataset into the KRKE graph. The new contribution is an explicit-action-to-source-specific-tacit-role pipeline. See `docs/report.md` and `docs/sources.md` for attribution and citations.
