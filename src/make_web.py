"""Make a self-contained offline evidence browser; no web server required."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "excerpts.csv").open(encoding="utf-8", newline="") as f:
    passages = list(csv.DictReader(f))
with (ROOT / "data" / "sources.csv").open(encoding="utf-8", newline="") as f:
    sources = {row["source_id"]: row["title"] for row in csv.DictReader(f)}
with (ROOT / "data" / "narrator_context.csv").open(encoding="utf-8", newline="") as f:
    narrators = {row["source_id"]: row for row in csv.DictReader(f)}
with (ROOT / "data" / "historical_context.csv").open(encoding="utf-8", newline="") as f:
    settings = {row["id"]: row for row in csv.DictReader(f)}
with (ROOT / "output" / "predictions.csv").open(encoding="utf-8", newline="") as f:
    predictions = {row["id"]: row for row in csv.DictReader(f)}
with (ROOT / "output" / "implications.csv").open(encoding="utf-8", newline="") as f:
    implications = {row["id"]: row for row in csv.DictReader(f)}
for passage in passages:
    passage["source_title"] = sources[passage["source_id"]]
    passage.update(predictions[passage["id"]])
    passage["narrator_context"] = narrators[passage["source_id"]]
    passage["historical_context"] = settings[passage["id"]]
    passage["implication"] = implications.get(passage["id"])
data = json.dumps(passages, ensure_ascii=False).replace("<", "\\u003c")

page = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cyrus Unspoken · KRKE evidence browser</title>
<style>
:root{color-scheme:dark;--bg:#111821;--panel:#1b2835;--line:#354657;--ink:#f2eddf;--muted:#b9c4c9;--gold:#efc77f;--teal:#84ddc7}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 85% 0,#2c4350 0,transparent 45%),var(--bg);color:var(--ink);font:16px/1.55 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:48px 22px 90px}a{color:var(--teal)}h1,h2,h3{line-height:1.12}h1{font:clamp(48px,8vw,92px)/1.02 Georgia,serif;letter-spacing:-.055em;margin:14px 0 22px}h2{font:32px Georgia,serif;margin:0 0 18px}h3{font-size:19px;margin:0 0 8px}.eyebrow{letter-spacing:.2em;text-transform:uppercase;color:var(--gold);font-size:12px;font-weight:700}.lede{max-width:710px;color:var(--muted);font-size:20px}.hero{padding:20px 0 52px;border-bottom:1px solid var(--line)}.stats,.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin:30px 0}.stat,.step,.card,.note{background:var(--panel);border:1px solid var(--line);border-radius:15px;padding:20px}.stat strong{font-size:30px;color:var(--gold);display:block}.stat span,.small{color:var(--muted);font-size:14px}.step b{color:var(--gold)}section{margin:46px 0}.controls{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0}button{font:inherit;background:#17222d;color:var(--ink);border:1px solid var(--line);border-radius:30px;padding:8px 16px;cursor:pointer}button.active,button:hover{background:var(--teal);color:#112128;border-color:var(--teal)}.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.card{min-width:0}.top{display:flex;gap:10px;justify-content:space-between;align-items:center;color:var(--muted);font-size:13px}.badge{color:#112128;background:var(--gold);border-radius:30px;padding:3px 11px;font-size:12px;font-weight:700}.quote{font:20px/1.4 Georgia,serif;margin:22px 0}.chain{border-top:1px solid var(--line);padding-top:14px;color:var(--teal);font-size:14px}.meta{color:var(--muted);font-size:13px}.note{border-left:4px solid var(--gold);color:var(--muted)}.footer{border-top:1px solid var(--line);padding-top:24px;color:var(--muted);font-size:14px}@media(max-width:700px){main{padding:28px 16px 60px}.stats,.steps,.cards{grid-template-columns:1fr}.hero{padding-bottom:30px}}
</style></head><body><main>
<header class="hero"><div class="eyebrow">Knowledge Representation and Extraction · demonstration project</div>
<h1>Cyrus<br>Unspoken</h1><p class="lede">How do short accounts of Cyrus imply roles through the actions they describe? Explore the evidence, extraction cues, and source-specific interpretations.</p>
<div class="stats"><div class="stat"><strong>14</strong><span>curated paraphrases</span></div><div class="stat"><strong>3</strong><span>interpretive roles</span></div><div class="stat"><strong>3</strong><span>explicit rules</span></div></div></header>
<section><div class="eyebrow">The method</div><h2>A traceable interpretation</h2><div class="steps"><div class="step"><b>01 · Text</b><p>A short, original paraphrase tied to a section or line in a historical source.</p></div><div class="step"><b>02 · Action</b><p>A narrow phrase pattern identifies an explicit narrated action.</p></div><div class="step"><b>03 · Context and inference</b><p>A declared rule generates a possible portrayal. The graph retains the narrated time and the later narrator’s viewpoint.</p></div></div><div class="note">“Ideal ruler” is a narrow teaching label for selected care, mercy, relief and reward cues. Three passages also demonstrate a prior condition or possible human or political impact. These are interpretations of sources. The input texts are paraphrases, so this is a bounded demonstration.</div></section>
<section><div class="eyebrow">Evidence explorer</div><h2>Read each inference</h2><p class="small">Filter by role. “No inferred role” passages are deliberate negative examples. Every citation opens the supporting edition.</p><div class="controls" id="filters"></div><div class="cards" id="cards"></div></section>
<footer class="footer">The ontology, context graph, inferred triples, six SPARQL queries, evaluation and reproducible code are inside the project zip. Source texts include the Cyrus Cylinder, Herodotus’s <i>Histories</i>, and Xenophon’s <i>Cyropaedia</i>. Original English paraphrases © project team for this demonstration. The domain name example.org identifies a sample namespace only.</footer>
</main><script>
const rows = __DATA__;
const $ = id => document.getElementById(id);
const escapeHTML = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const filters = ['All','Restorer','Conqueror','IdealRuler','None']; let chosen='All';
function render(){
  $('filters').innerHTML = filters.map(f=>`<button type="button" class="${chosen===f?'active':''}" aria-pressed="${chosen===f}" data-filter="${f}">${f==='None'?'No inferred role':f==='IdealRuler'?'Ideal ruler':f}</button>`).join('');
  const filtered = rows.filter(r=>chosen==='All'||r.predicted_role===chosen);
  $('cards').innerHTML = filtered.map(r=>`<article class="card"><div class="top"><span>${escapeHTML(r.id)} · ${escapeHTML(r.source_title)} · ${escapeHTML(r.locator)}</span><span class="badge">${r.predicted_role==='None'?'No role':escapeHTML(r.predicted_role.replace('IdealRuler','Ideal ruler'))}</span></div><p class="quote">“${escapeHTML(r.paraphrase)}”</p><p class="chain">${r.predicted_action==='None'?'No cue → no target action → no role':`Cue “${escapeHTML(r.cue)}” → ${escapeHTML(r.predicted_action)} → ${escapeHTML(r.predicted_role.replace('IdealRuler','Ideal ruler'))}`}</p><p class="meta"><b>Narrated time:</b> ${escapeHTML(r.historical_context.narrated_period)}. <b>Narrator:</b> ${escapeHTML(r.narrator_context.narrator_period)}, ${escapeHTML(r.narrator_context.viewpoint)}.</p><p class="meta"><b>Historical setting:</b> ${escapeHTML(r.historical_context.social_setting)}</p><p class="meta"><b>Narrator context:</b> ${escapeHTML(r.narrator_context.expectations_context)}</p>${r.implication?`<p class="meta"><b>Other possible tacit knowledge (${escapeHTML(r.implication.kind)}):</b> ${escapeHTML(r.implication.claim)}</p>`:""}<p class="meta">${escapeHTML(r.annotation_note)} <a href="${escapeHTML(r.source_url)}" target="_blank" rel="noopener noreferrer">View source ↗</a></p></article>`).join('');
  $('filters').querySelectorAll('button').forEach(b=>b.onclick=()=>{chosen=b.dataset.filter;render()});
}
render();
</script></body></html>'''
(ROOT / "web" / "index.html").write_text(page.replace("__DATA__", data), encoding="utf-8")
print("Wrote web/index.html — open directly in a browser")
