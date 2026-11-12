"""Rebuild the explicit graph, rule-derived depictions, and evaluation.

Run from the project root: python src/build.py
The input is a tiny, curated corpus of original paraphrases, not raw ancient text.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import DCTERMS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "output"
CU = Namespace("https://example.org/cyrus-unspoken/")  # Demonstration namespace, not a live endpoint

# Ordered, narrow phrase patterns for this hand-curated English paraphrase set.
# These detect explicit narrated actions. Their semantic role is added in a later step.
ACTION_PATTERNS = {
    "Restoration": [r"\breturned\b", r"\brebuilt\b"],
    "Conquest": [r"\bentered Babylon\b", r"\bcaptured\b", r"\btook Croesus captive\b"],
    "GoodGovernance": [r"\bfreed\b", r"\bspared\b", r"\bsupported\b", r"\brewarded\b", r"\bvisited sick\b"],
}
ROLE_RULES = {
    "Restoration": ("Restorer", "RuleRestoration"),
    "Conquest": ("Conqueror", "RuleConquest"),
    "GoodGovernance": ("IdealRuler", "RuleGovernance"),
}

# Three bounded examples of other tacit knowledge, based on textual cues.
# A consequence is attached to an excerpt and stays qualified as an interpretation.
IMPLICATION_RULES = (
    ("GoodGovernance", r"\bfreed Babylonian citizens from forced service\b",
     "PriorCondition", "Babylonian citizens", "The passage presupposes an earlier burden of forced service.", "RulePriorService"),
    ("Conquest", r"\btook Croesus captive\b",
     "HumanImpact", "Croesus", "Captivity implies a restriction of Croesus's personal freedom.", "RuleCaptivity"),
    ("Conquest", r"\bcaptured Sardis\b",
     "PoliticalImpact", "Sardis", "The city's capture suggests a change of political control in this narrative.", "RuleCityCapture"),
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def detect_action(text: str) -> tuple[str, str]:
    """Return one action class and its matched cue, or ('None', '')."""
    matches = [(kind, found.group(0)) for kind, patterns in ACTION_PATTERNS.items()
               for pattern in patterns if (found := re.search(pattern, text, re.I))]
    if len(matches) > 1:
        raise ValueError(f"Ambiguous action cue in curated excerpt: {text!r}: {matches}")
    return matches[0] if matches else ("None", "")


def bind(g: Graph) -> Graph:
    g.bind("cu", CU)
    g.bind("dcterms", DCTERMS)
    return g


def score(gold: list[str], predicted: list[str], label: str) -> dict:
    tp = sum(a == label and b == label for a, b in zip(gold, predicted))
    fp = sum(a != label and b == label for a, b in zip(gold, predicted))
    fn = sum(a == label and b != label for a, b in zip(gold, predicted))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision,
            "recall": recall, "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    sources = read_rows(DATA / "sources.csv")
    excerpts = read_rows(DATA / "excerpts.csv")
    narrator_context = {r["source_id"]: r for r in read_rows(DATA / "narrator_context.csv")}
    historical_context = {r["id"]: r for r in read_rows(DATA / "historical_context.csv")}
    if len({r["id"] for r in excerpts}) != len(excerpts):
        raise ValueError("Excerpt IDs must be unique")
    source_ids = {r["source_id"] for r in sources}
    if any(r["source_id"] not in source_ids for r in excerpts):
        raise ValueError("An excerpt refers to an unknown source")
    if set(narrator_context) != source_ids or set(historical_context) != {r["id"] for r in excerpts}:
        raise ValueError("Every source and excerpt needs exactly one context row")

    explicit, inferred = bind(Graph()), bind(Graph())
    for row in sources:
        subject = CU["source_" + row["source_id"]]
        explicit.add((subject, RDF.type, CU.Source))
        explicit.add((subject, DCTERMS.title, Literal(row["title"])))
        explicit.add((subject, DCTERMS.creator, Literal(row["author"])))
        explicit.add((subject, DCTERMS.identifier, URIRef(row["reference_url"])))
        context_row = narrator_context[row["source_id"]]
        narrator = CU["narrator_context_" + row["source_id"]]
        explicit.add((narrator, RDF.type, CU.NarratorContext))
        explicit.add((narrator, CU.narratorPeriod, Literal(context_row["narrator_period"])))
        explicit.add((narrator, CU.narratorViewpoint, Literal(context_row["viewpoint"])))
        explicit.add((narrator, CU.narratorExpectations, Literal(context_row["expectations_context"])))
        explicit.add((narrator, DCTERMS.source, URIRef(context_row["context_source"])))
        explicit.add((subject, CU.hasNarratorContext, narrator))

    predictions = []
    implications = []
    for row in excerpts:
        excerpt = CU["excerpt_" + row["id"]]
        explicit.add((excerpt, RDF.type, CU.Excerpt))
        explicit.add((excerpt, CU.fromSource, CU["source_" + row["source_id"]]))
        explicit.add((excerpt, CU.sourceLocator, Literal(row["locator"])))
        explicit.add((excerpt, CU.paraphrase, Literal(row["paraphrase"])))
        explicit.add((excerpt, DCTERMS.source, URIRef(row["source_url"])))
        historical_row = historical_context[row["id"]]
        setting = CU["historical_context_" + row["id"]]
        explicit.add((setting, RDF.type, CU.HistoricalContext))
        explicit.add((setting, CU.narratedPeriod, Literal(historical_row["narrated_period"])))
        explicit.add((setting, CU.socialSetting, Literal(historical_row["social_setting"])))
        explicit.add((excerpt, CU.hasHistoricalContext, setting))

        action_name, cue = detect_action(row["paraphrase"])
        role_name = ROLE_RULES[action_name][0] if action_name != "None" else "None"
        predictions.append({"id": row["id"], "gold_action": row["gold_action"],
                            "predicted_action": action_name, "cue": cue,
                            "gold_role": row["gold_role"], "predicted_role": role_name})
        if action_name == "None":
            continue
        action = CU["action_" + row["id"]]
        explicit.add((action, RDF.type, CU[action_name]))
        explicit.add((action, CU.hasAgent, CU.Cyrus))
        explicit.add((action, CU.matchedCue, Literal(cue)))
        explicit.add((excerpt, CU.depictsAction, action))

        role_name, rule_name = ROLE_RULES[action_name]
        depiction = CU["depiction_" + row["id"]]
        inferred.add((depiction, RDF.type, CU.Depiction))
        inferred.add((depiction, CU.hasEvidence, excerpt))
        inferred.add((depiction, CU.hasSubject, CU.Cyrus))
        inferred.add((depiction, CU.portraysAs, CU[role_name]))
        inferred.add((depiction, CU.triggeredBy, action))
        inferred.add((depiction, CU.derivedBy, CU[rule_name]))

        for required_action, pattern, implication_kind, bearer, claim, implication_rule in IMPLICATION_RULES:
            if action_name != required_action or not re.search(pattern, row["paraphrase"], re.I):
                continue
            implication = CU["implication_" + row["id"] + "_" + implication_kind]
            inferred.add((implication, RDF.type, CU.TacitImplication))
            inferred.add((implication, CU.implicationKind, CU[implication_kind]))
            inferred.add((implication, CU.affectedEntity, Literal(bearer)))
            inferred.add((implication, CU.implicationText, Literal(claim)))
            inferred.add((implication, CU.implicationTriggeredBy, action))
            inferred.add((implication, CU.implicationDerivedBy, CU[implication_rule]))
            inferred.add((excerpt, CU.hasImplication, implication))
            implications.append({"id": row["id"], "kind": implication_kind, "bearer": bearer,
                                 "claim": claim, "rule": implication_rule})

    with (OUT / "predictions.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(predictions[0]))
        writer.writeheader()
        writer.writerows(predictions)
    with (OUT / "implications.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["id", "kind", "bearer", "claim", "rule"])
        writer.writeheader()
        writer.writerows(implications)

    gold_action = [p["gold_action"] for p in predictions]
    pred_action = [p["predicted_action"] for p in predictions]
    gold_role = [p["gold_role"] for p in predictions]
    pred_role = [p["predicted_role"] for p in predictions]
    evaluation = {
        "note": "Illustrative internal agreement on 14 curated paraphrases. Gold labels and rules were designed by the same project author; this is not independent validation or a performance claim on historical text.",
        "rows": len(predictions),
        "exact_action_agreement": sum(a == b for a, b in zip(gold_action, pred_action)),
        "exact_role_agreement": sum(a == b for a, b in zip(gold_role, pred_role)),
        "action_by_class": {name: score(gold_action, pred_action, name) for name in ACTION_PATTERNS},
        "role_by_class": {name: score(gold_role, pred_role, name) for name, _ in ROLE_RULES.values()},
        "mismatches": [p for p in predictions if p["gold_action"] != p["predicted_action"] or p["gold_role"] != p["predicted_role"]],
    }
    (OUT / "evaluation.json").write_text(json.dumps(evaluation, indent=2) + "\n", encoding="utf-8")
    ontology = bind(Graph()).parse(ROOT / "ontology" / "cyrus_unspoken.ttl", format="turtle")
    combined = ontology + explicit + inferred
    for name, graph in (("explicit", explicit), ("inferred", inferred), ("combined", combined)):
        graph.serialize(destination=OUT / f"{name}.ttl", format="turtle")
    print(f"{len(excerpts)} excerpts; {len(explicit)} explicit triples; {len(inferred)} inferred triples; {len(combined)} combined triples")
    print(f"Tacit implications: {len(set(inferred.objects(predicate=CU.hasImplication)))}")
    print(f"Action agreement: {evaluation['exact_action_agreement']}/{len(excerpts)}; role agreement: {evaluation['exact_role_agreement']}/{len(excerpts)}")


if __name__ == "__main__":
    main()
