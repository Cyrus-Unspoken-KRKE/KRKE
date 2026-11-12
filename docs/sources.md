# Sources and provenance

The corpus uses original English **paraphrases** written for this teaching project. Its `source_url` and `locator` fields point readers to the corresponding passages. The paraphrases are **not quotations** and do not preserve all detail or nuance in the translations.

| Work | Sections used | Reading link | Interpretive caution |
|---|---|---|---|
| Cyrus Cylinder | lines 20–26, 32, 39–41 | [Livius translation](https://www.livius.org/sources/content/cyrus-cylinder/cyrus-cylinder-translation/) | A royal inscription with a self-legitimating perspective; translation and damaged text need care. |
| Herodotus, *Histories* I | 1.84, 1.86–88 | [LacusCurtius, Book I middle](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Herodotus/1b*.html) | Reported narrative, including Croesus's pyre and its contested moral reading. |
| Herodotus, *Histories* I | 1.189, 1.191 | [LacusCurtius, Book I end](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Herodotus/1d*.html) | The Babylon entry narrative emphasizes tactics and conflict. |
| Xenophon, *Cyropaedia* | 8.2.1–3, 8.2.25 | [Perseus, Book 8 chapter 2](https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0204%3Abook%3D8%3Achapter%3D2) | Literary and political portrait, not a contemporary chronicle. |
| Xenophon, *Cyropaedia* | 6.2.5 | [Book 6 online text](https://www.cais-soas.com/CAIS/History/hakhamaneshian/xenophon/cyropaedia/xenophon_book_6.htm) | Leadership behaviour is described as a rhetorical example. |

The [University of Bologna KRKE course description](https://www.unibo.it/en/study/course-units-transferable-skills-moocs/course-unit-catalogue/course-unit/2026/533916) emphasizes knowledge graphs, reasoning, extraction, evaluation, Web publication, and a defensible group project. The [DHDKey projects catalogue](https://projects.dharc.unibo.it/dhdkey/projects) was used to understand the scale and variety of previous projects.

Context notes also consult the [British Museum's Cyrus Cylinder record](https://www.britishmuseum.org/collection/object/W_1880-0617-1941) for the conquest of Babylon in 539 BCE and the genre of its inscription; the [University of Melbourne Library's Herodotus essay](https://blogs.unimelb.edu.au/librarycollections/2018/10/15/herodotus-histories/) for the fifth-century BCE historian; and the [Metropolitan Museum of Art's Cyrus essay](https://www.metmuseum.org/it/perspectives/cyrus-the-great) for Xenophon's fourth-century BCE literary portrait. The `data/narrator_context.csv` notes about a narrator's expectations are **our interpretations of these works**, not direct quotations from those reference pages. Approximate event periods and societal descriptions are contextual labels rather than precise archaeological dates.

Prior work: Saman Abdolrashidi, *Cyrus the Great: Modelling Kingship, Memory, and Cultural Heritage in Linked Open Data* (earlier LODLAM class project, supplied by its author). That work mapped entities, texts and heritage objects. Here, the reuse is domain background and RDF experience; the 14 passage labels and role-inference pipeline are distinct.

Before academic submission, the team should check each paraphrase against the cited edition and record the reviewer and any changed wording in `data/excerpts.csv`. Prefer stable edition identifiers in a final published release if the host site provides them.
