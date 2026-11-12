# Eight-slide defense guide (about 7–9 minutes)

The editable deck is `presentation.pptx`. Use these notes to learn the content; do not memorize sentences without understanding the data.

## 1. Cyrus Unspoken

**Say:** “We study how an account of Cyrus can imply a role through the action it describes. Our result is a small, traceable knowledge graph. The role belongs to a source-specific portrayal.”

## 2. Research question

**Say:** “The text reports that Cyrus returned divine images. That is an explicit narrated action. We interpret it as a portrayal of a Restorer. The word Restorer may not appear in the passage. Our problem is to represent that extra interpretive step and show its evidence.”

## 3. Corpus and source perspectives

**Say:** “We wrote 14 short English paraphrases tied to exact lines or sections: five from the Cylinder, five from Herodotus, and four from Xenophon. Two are negative examples. The graph records two time layers: when the narrated action is set and when the narrator describes it. The Cylinder is close to the Babylon events, whereas Herodotus and Xenophon wrote later from Greek perspectives.”

## 4. Ontology

**Say:** “The important node is Depiction. It links Cyrus, the role, the passage, the action and the rule. The passage also has a historical setting, and its source has a separate narrator context. Restorer is an individual of TacitRole, not a class that Cyrus belongs to. That keeps an interpretation attached to evidence and viewpoint.”

## 5. Extraction and inference

**Say:** “Python looks for narrow English cues such as returned, captured, or rewarded. Three rules then materialize Restorer, Conqueror or Ideal Ruler depictions. We also have three small examples of tacit knowledge beyond roles: a prior condition, a human consequence, and a political consequence. The OWL file defines the vocabulary; Python runs the rules.”

## 6. Query demonstration

**Show:** Open `web/index.html`, filter Restorer, click the two source links. Then show `output/query_results.md` or a SPARQL file.

**Say:** “One query returns the passage and source URL behind Restorer. Another traces cue, action and rule. The sixth query places three implications beside the action's narrated time and the narrator's later time. These make the interpretation inspectable.”

## 7. Evaluation and limitation

**Say:** “The pipeline agrees with our provisional labels on all 14 curated paraphrases, including two that produce no role. This is only an internal consistency check. The same author chose the labels and patterns, so it does not measure unseen-text performance. Synonyms, negation and actor resolution can break it. Two independent group annotations on held-out passages would be the proper next test.”

## 8. Contribution and next review

**Say:** “Compared with the earlier Cyrus LODLAM graph, this project adds a new task: from a narrated action to a documented, context-aware interpretation. Professor Gangemi approved the topic and suggested considering the action's time and social setting as well as the narrator's later expectations. We represent those variables, and we know the rule-based limits. Before submission, our group will verify the paraphrases and record who contributed what.”

## Likely defense questions

**What is tacit knowledge here?** A role a reader may infer from a narrated action even if the source does not explicitly name the role.

**Is Cyrus truly an ideal ruler?** The project does not claim that. `IdealRuler` names our narrow interpretation of some passages about care, mercy, relief or reward. It remains contestable.

**What does the ontology do?** It supplies types and relationships for sources, passages, action instances, role concepts and evidence-bearing depictions.

**Does an OWL reasoner infer your roles?** No. The Python script materializes three declared interpretation rules. Protégé displays the resulting triples and can reason about OWL class axioms separately.

**Why 14 passages?** A small corpus keeps source review and oral defense manageable. The size limits any claim about general performance.

**Why is the evaluation perfect?** The corpus, paraphrases and rules were developed together. Perfect internal agreement does not establish generalization.

**Is this the same as the LODLAM exam?** The Cyrus domain and RDF familiarity carry over. The passage-level tacit-role extraction and evidence trail are new.

**Can a passage express several roles?** Yes in principle. This teaching prototype chooses one action per paraphrase; multi-label representation is a sensible extension.

**How does the professor's feedback change the project?** Every excerpt now records its narrated time and social setting, while each work records the narrator's period and perspective. Three cases also show a prior condition or possible human/political consequence. These are visible in the graph and query 06.

**Does the program use narrator time to change the role automatically?** No. We retain it as evidence for critical interpretation. Our narrow role rules are transparent hypotheses; a group discussion may reject a label such as Ideal Ruler in a particular episode.
