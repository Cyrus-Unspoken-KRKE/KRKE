"""Build the editable eight-slide defense deck with python-pptx."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parents[1]
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
blank = prs.slide_layouts[6]
BG, INK, MUTED, GOLD, TEAL, LINE = (RGBColor(17,24,33), RGBColor(245,238,224),
    RGBColor(193,204,207), RGBColor(239,199,127), RGBColor(132,221,199), RGBColor(76,94,106))

def box(slide, x, y, w, h, text, size=22, bold=False, color=INK, font="Aptos", align=None):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame; tf.clear(); tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(.02)
    tf.margin_top = tf.margin_bottom = Inches(.02)
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line; p.font.name = font; p.font.size = Pt(size); p.font.bold = bold; p.font.color.rgb = color
        p.space_after = Pt(10)
        if align: p.alignment = align
    return shape

def base(title, no):
    s = prs.slides.add_slide(blank)
    s.background.fill.solid(); s.background.fill.fore_color.rgb = BG
    box(s,.72,.35,11.7,.75,title,35,True,INK)
    box(s,12.1,.42,.5,.35,str(no).zfill(2),13,True,GOLD,align=PP_ALIGN.RIGHT)
    return s

def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

def line(slide, x1,y1,x2,y2,color=LINE):
    connector = slide.shapes.add_connector(1, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    connector.line.color.rgb = color; connector.line.width = Pt(2)

s=prs.slides.add_slide(blank); s.background.fill.solid(); s.background.fill.fore_color.rgb=BG
box(s,.8,.7,11.6,.45,"KNOWLEDGE REPRESENTATION AND EXTRACTION",15,True,GOLD)
box(s,.8,1.65,11.6,2.1,"Cyrus Unspoken",64,True,INK,"Georgia")
box(s,.85,4.0,10.5,1.2,"Representing source-specific tacit roles\nfrom narrated actions",28,False,MUTED)
box(s,.85,6.55,11.8,.4,"Group project prototype  •  University of Bologna  •  October 2026",14,False,MUTED)
notes(s,"Research question: How can explicit narrated actions be connected to implicit portrayals while preserving the source? Insert actual group names only after the group reviews the work.")

s=base("From narrated action to implied role",2)
box(s,.8,1.45,11.8,.9,"Cyrus returned divine images to their sanctuaries.",30,False,INK,"Georgia")
line(s,.8,2.62,12.4,2.62)
box(s,.9,3.0,5.4,.5,"EXPLICIT",15,True,TEAL)
box(s,.9,3.55,5.2,1.35,"A narrated return of cult images",27)
box(s,6.7,3.0,5.1,.5,"TACIT INTERPRETATION",15,True,GOLD)
box(s,6.7,3.55,5.2,1.35,"This passage portrays Cyrus as Restorer",27)
box(s,.9,6.15,11.5,.5,"The source does not need to use the word “Restorer” for the role to be inferred.",17,False,MUTED)
notes(s,"Example based on Cylinder line 32, paraphrased by us. This is a source-grounded interpretation, not an objective historical statement. Source: https://www.livius.org/sources/content/cyrus-cylinder/cyrus-cylinder-translation/")

s=base("A small corpus with three perspectives",3)
data=[("Cyrus Cylinder","5","Royal inscription"),("Herodotus, Histories I","5","Greek historical narrative"),("Xenophon, Cyropaedia","4","Literary political portrait")]
table=s.shapes.add_table(4,3,Inches(.82),Inches(1.55),Inches(11.7),Inches(3.55)).table
for i,w in enumerate([4.8,1.55,5.35]):table.columns[i].width=Inches(w)
for c,v in enumerate(["Source","Passages","Genre"]):table.cell(0,c).text=v
for r,row in enumerate(data,1):
    for c,v in enumerate(row):table.cell(r,c).text=v
for r in range(4):
    for c in range(3):
        cell=table.cell(r,c);cell.fill.solid();cell.fill.fore_color.rgb=RGBColor(31,44,56) if r%2 else BG
        cell.margin_left=Inches(.17);cell.margin_top=Inches(.12);cell.vertical_anchor=MSO_ANCHOR.MIDDLE
        for p in cell.text_frame.paragraphs:
            p.font.name="Aptos";p.font.size=Pt(20);p.font.bold=(r==0);p.font.color.rgb=GOLD if r==0 else INK
box(s,.9,5.6,11.5,1.1,"Each passage records the narrated historical setting; each source records the narrator’s later time and viewpoint.",21,False,MUTED)
notes(s,"Five Cylinder passages, five Herodotus, four Xenophon. Two negative examples. The Cylinder is near the Babylon campaign of 539 BCE; Herodotus wrote in the fifth century BCE; Xenophon in the fourth. These are approximate contexts, not precise event dating for every episode. British Museum: https://www.britishmuseum.org/collection/object/W_1880-0617-1941; Met Museum: https://www.metmuseum.org/it/perspectives/cyrus-the-great")

s=base("The ontology preserves evidence",4)
box(s,.85,1.35,11.6,.5,"One depiction connects the person, role, action, excerpt and rule.",24,False,MUTED)
data=[("Excerpt E03","Cylinder line 32"),("Action E03","Restoration"),("Depiction E03","portrays Cyrus as Restorer"),("Rule","Restoration suggests Restorer")]
for i,(head,sub) in enumerate(data):
    x=.9+(i%2)*6.1;y=2.3+(i//2)*1.7
    box(s,x,y,5.5,.45,head,19,True,TEAL if i<2 else GOLD)
    box(s,x,y+.5,5.4,.95,sub,25)
box(s,.9,6.13,11.6,.7,"The excerpt also links to its historical setting; the source links to the narrator’s context.",17,False,MUTED)
notes(s,"The central Depiction node retains source and evidence. The ontology is in ontology/cyrus_unspoken.ttl. Role labels are individuals of TacitRole. HistoricalContext and NarratorContext are separate to avoid confusing event and writing times.")

s=base("Three rules materialize portrayals",5)
rows=[("returned / rebuilt","Restoration","Restorer"),("captured / entered Babylon","Conquest","Conqueror"),("rewarded / spared / supported","GoodGovernance","Ideal ruler")]
box(s,.9,1.4,3.7,.5,"ENGLISH CUE",15,True,TEAL)
box(s,5.0,1.4,3.7,.5,"ACTION CLASS",15,True,TEAL)
box(s,9.2,1.4,3.2,.5,"TACIT ROLE",15,True,GOLD)
for i,row in enumerate(rows):
    y=2.25+i*1.24
    for x,w,v in [( .9,3.7,row[0]),(5.0,3.7,row[1]),(9.2,3.2,row[2])]:box(s,x,y,w,.9,v,22)
    line(s,.9,y+1.0,12.25,y+1.0)
box(s,.9,6.43,11.5,.45,"Three extra bounded rules model a prior condition and human or political effects.",16,False,MUTED)
notes(s,"The input is a curated paraphrase set. Phrase matching detects an explicit action; Python emits an evidence-bearing depiction. Three additional cue-specific rules infer prior forced service, Croesus's restricted freedom, and possible changed control of Sardis. Python applies these rules; OWL alone does not.")

s=base("Queries expose each interpretation",6)
box(s,.9,1.45,11.5,.6,"Which passages support the Restorer role?",29,False,INK,"Georgia")
box(s,.9,2.4,11.4,.8,"E03  ·  Cylinder line 32  ·  returned divine images",23,False,TEAL)
box(s,.9,3.35,11.4,.8,"E04  ·  Cylinder lines 39–41  ·  rebuilt quay wall",23,False,TEAL)
line(s,.9,4.45,12.3,4.45)
box(s,.9,4.75,11.4,1.2,"A sixth query shows three tacit implications beside event time and narrator time.",22)
box(s,.9,6.5,11.3,.4,"Live demo: open web/index.html and compare E02, E05 and E06.",16,False,MUTED)
notes(s,"Run the demo from the offline browser. Six SPARQL files and actual results are in queries/ and output/query_results.md. Compare the Cylinder's official voice to Herodotus's later Greek account. Context is annotated for human review, not an automatic override of role labels.")

s=base("Evaluation is an internal check",7)
box(s,.9,1.55,4.4,1.2,"14 / 14",56,True,GOLD)
box(s,5.0,1.65,7.1,.9,"Agreement with provisional labels",26)
line(s,.9,3.1,12.2,3.1)
box(s,.9,3.55,11.2,1.0,"The same author selected the paraphrases, labels and patterns.",27)
box(s,.9,4.85,11.5,1.0,"A synonym, negation or a different actor can break this extractor.",25,False,MUTED)
box(s,.9,6.35,11.5,.55,"Next validation: independent annotation of unseen passages by group members.",17,False,TEAL)
notes(s,"Twelve positive depictions and two negatives. The score evaluates action and role labels only in a designed corpus; context notes and three other implications were not independently scored. Never present it as 100% historical text extraction accuracy. See output/evaluation.json and docs/report.md.")

s=base("A defensible KRKE contribution",8)
box(s,.9,1.65,11.4,1.0,"A narrated action becomes a traceable, source-specific portrayal.",30,False,INK,"Georgia")
box(s,.9,3.0,11.2,.7,"Representation: small OWL vocabulary and evidence-bearing RDF graph",22)
box(s,.9,4.0,11.2,.7,"Extraction: declared English phrase patterns and three materialization rules",22)
box(s,.9,5.0,11.2,.7,"Investigation: five queries, offline browser and candid evaluation",22)
box(s,.9,6.38,11.4,.5,"Professor approved the topic; the group still needs to verify its annotations.",17,False,GOLD)
notes(s,"The earlier Cyrus LODLAM work supplies domain background. Professor Gangemi approved the topic on 1 October and suggested considering action time/social setting and the narrator's time/expectations. We added both context layers and three qualified non-role implications. Group contributions and final submission format still need review. The deck is editable.")

prs.save(ROOT / "presentation.pptx")
print("Wrote presentation.pptx with 8 editable slides")
