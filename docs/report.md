# Cyrus Unspoken: Representing Tacit Roles in Accounts of Cyrus the Great

## Abstract

This teaching project investigates whether short accounts of Cyrus can support traceable, source-specific interpretations. A curated set of 14 English paraphrases refers to three ancient works. A rule-based extractor detects explicit action cues; three declared mappings derive possible tacit roles: Restorer, Conqueror, and Ideal Ruler. Each passage also records its narrated historical setting separately from the later narrator's time and viewpoint. Three additional rules illustrate a prior condition and possible human or political consequences. An OWL vocabulary and RDF graph retain evidence and rule provenance. Six SPARQL queries answer evidence, context and comparison questions. Twelve passages trigger a role, two serve as negative examples. Internal action/role agreement with provisional hand labels is 14/14, but the labels and rules were designed together; this is a pipeline consistency check rather than independent validation.

## 1. Task and contribution

**Research question:** When a passage narrates an action by Cyrus, how can we represent a *possible implied characterization* with its evidence and perspective?

An action such as returning cult images is stated in the source. Calling Cyrus a *Restorer* is our interpretation. The model makes that extra step explicit and records its rule. The old Cyrus LODLAM project modelled entities and relations around Cyrus; this project addresses the distinct KRKE task of connecting textual cues to source-grounded interpretations. It supports the course's knowledge representation, extraction, reasoning, querying and evaluation aims (see `sources.md`).

## 2. Scope and corpus

There are 14 short, original paraphrases, each with a work, section/line locator and edition URL in `data/excerpts.csv`: four positive Cylinder examples plus one negative, four positive Herodotus examples plus one negative, and four Xenophon examples. Annotations are provisional human judgments made for this prototype. The English wording is curated for the method; the code does not read Akkadian or Greek, nor does it ingest whole source texts.

Genre matters. The Cylinder is a royal inscription, Herodotus gives a Greek narrative, and Xenophon constructs a literary model of leadership. A role is therefore attached to an **excerpt-specific depiction**, never asserted as `Cyrus rdf:type IdealRuler` or an unconditional historical fact.

Professor Gangemi's 1 October response approved the topic and asked us to consider the historical time and society of the actions alongside the later narrator's time and expectations. The two context tables make those variables visible in the graph. We use approximate periods and short, sourced interpretive notes, and do not claim to reconstruct all ancient expectations. See `docs/professor_feedback.md`.

## 3. Representation

The compact ontology has `Person`, `Source`, `Excerpt`, `Action`, `TacitRole`, `Depiction`, `Rule`, `HistoricalContext`, `NarratorContext` and `TacitImplication`. The action classes are `Restoration`, `Conquest`, and `GoodGovernance`. The role **individuals** are `Restorer`, `Conqueror`, and `IdealRuler`; they are not subclasses of Person. `Depiction` is the evidence-bearing node connecting a role to an excerpt, action, person and rule. The excerpt links to its historical setting, while the source links to the narrator context. A few `TacitImplication` nodes represent a possible consequence or presupposition tied to the excerpt and action.

Illustrative triples (shortened):

```turtle
cu:excerpt_E03 cu:fromSource cu:source_cylinder ;
               cu:depictsAction cu:action_E03 .
cu:action_E03 a cu:Restoration ; cu:hasAgent cu:Cyrus ;
              cu:matchedCue "returned" .
cu:depiction_E03 a cu:Depiction ;
                  cu:hasEvidence cu:excerpt_E03 ;
                  cu:hasSubject cu:Cyrus ;
                  cu:triggeredBy cu:action_E03 ;
                  cu:portraysAs cu:Restorer ;
                  cu:derivedBy cu:RuleRestoration .
```

The source link and exact line locator are properties of the excerpt. `output/explicit.ttl` contains evidence/action data; `output/inferred.ttl` contains derived depictions. `output/combined.ttl` joins both with the ontology. These named files make the boundary visible, though the merged output is an ordinary RDF graph rather than an RDF dataset with named graphs.

For example, E06 has a narrated mid sixth-century BCE Lydia campaign setting; Herodotus's source has a separate fifth-century BCE Greek narrator context. The claim about restricted freedom is a qualified implication of taking Croesus captive **in Herodotus's account**. The graph does not record it as an independently verified event.

## 4. Extraction and rules

`src/build.py` finds a **single cue** in each curated paraphrase with case-insensitive phrase patterns. Example patterns are `returned` or `rebuilt` for Restoration; `captured`, `entered Babylon` or `took Croesus captive` for Conquest; `freed`, `spared`, `supported`, `rewarded` or `visited sick` for GoodGovernance. The input has already been manually selected to keep Cyrus as the actor. The program rejects passages matching more than one cue rather than silently choosing one.

The materialization rules are:

1. Detected `Restoration` action by Cyrus → depiction as `Restorer` in the supporting excerpt.
2. Detected `Conquest` action by Cyrus → depiction as `Conqueror` in the supporting excerpt.
3. Detected `GoodGovernance` action by Cyrus → depiction as `IdealRuler` in the supporting excerpt.

These are **project-specific interpretive heuristics**, implemented in Python, not universal historical laws or automatic consequences of OWL. `IdealRuler` is an especially strong label; the model treats it as a narrow operational convention and exposes the underlying evidence for criticism. One could rename it `BenevolentLeadershipPortrayal` in a future group revision.

Three other phrase-specific rules demonstrate tacit knowledge beyond roles: `freed ... from forced service` suggests an earlier burden (E02); `took Croesus captive` implies a restriction of personal freedom (E06); `captured Sardis` suggests a change of political control (E05). These claims are qualified in `output/implications.csv` and attached to their evidence in RDF. The program records historical and narrator context for human review; it does not automatically decide how a narrator's social expectations should change a role label.

## 5. Competency questions and observed results

The actual queries are in `queries/`; their full output is in `output/query_results.md`.

| Question | Query | Result on this dataset |
|---|---|---:|
| Which roles appear? | `01_roles.sparql` | 3 role rows |
| Which passages support Restorer? | `02_restorer_evidence.sparql` | 2 passages, Cylinder lines 32 and 39–41 |
| How many portrayals per source and role? | `03_sources_by_role.sparql` | 6 source/role combinations |
| Which cue and rule produced each portrayal? | `04_rule_trace.sparql` | 12 trace rows |
| Which excerpts produce no role? | `05_explicit_without_tacit.sparql` | E13 and E14 |
| Which implications have historical and narrator context? | `06_context_and_impacts.sparql` | 3 traceable examples |

The source-role query illustrates perspective without forcing agreement: the Cylinder produces Restoration, Conquest and GoodGovernance depictions; Herodotus gives Conquest and GoodGovernance; Xenophon gives GoodGovernance in this *selected sample*. No source-wide claim follows from these counts.

## 6. Evaluation and critical analysis

`output/predictions.csv` exposes the provisional human label, extracted action, matched cue and derived role for every row. `output/evaluation.json` reports 14/14 exact agreement for action and role; twelve positives and two negatives. Every class has precision and recall 1.0 **within these deliberately curated paraphrases**. This number is expected to be optimistic because the annotations, wording and patterns were developed by the same author. It must not be presented as general accuracy, independent validation, or a measured property of the original ancient texts.

Concrete limits:

- A synonym such as “brought back” can evade the `returned` rule.
- Negation or another actor can cause a false positive; the extractor has no syntactic parser.
- A single passage can support multiple readings; the implementation picks at most one of three action classes.
- The role mappings are interpretive and genre dependent; “peaceful entry” can still trigger Conqueror by the project's explicit convention.
- The context notes are human-authored interpretations. This prototype does not validate them against an independent group annotation, nor does context automatically override role mappings.
- The three additional implication rules are narrow examples, not a general engine for physical, legal or geopolitical reasoning.
- The source links and paraphrases require group verification; no inter-annotator agreement has yet been measured.

A defensible next evaluation would have **two group members independently label unseen passages**, reconcile disagreements, freeze a gold set, then compare an unchanged extractor. This is proposed future work, not completed work.

## 7. Web and reproducibility

Open `web/index.html` directly to filter and trace all passages. It is self-contained, so it can also be published through a static host after the team reviews it. `README.md` supplies the three rebuild commands. The example.org namespace is a demonstrative URI and is not dereferenceable here. The separate ontology and graph files can be loaded into Protégé, but Python must run to materialize the interpretive rules.

## 8. Conclusion

The project demonstrates a complete, small text-to-graph chain with visible interpretive steps. Its strongest claim is **traceability**: every inferred portrayal has a source, section, paraphrase, action cue and named rule, while the narrator and historical times remain distinct. The group can extend or challenge each rule without losing its evidence trail.
