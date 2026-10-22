import os, json, re, html, datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
B="https://jsuwood-ops.github.io/psychready"
DISC='<p class="disclaimer"><strong>Educational use only.</strong> PsychReady content is for staff education and program planning. It is not clinical advice and is not a substitute for accredited training, local policy, or professional judgment.</p>'
NAV=[("index.html","Home"),("training/index.html","Training"),("training/modules.html","Modules"),("barriers.html","Barriers"),("for-educators.html","For Educators"),("newsletter.html","Newsletter"),("newsletter/index.html","Archive"),("pricing.html","Pricing"),("sponsors.html","Sponsors"),("about.html","About")]
LOGO='<svg class="logo" viewBox="0 0 40 40" width="36" height="36" aria-hidden="true"><rect width="40" height="40" rx="10" fill="#0f5c5a"/><path d="M8 21h6l3-7 5 14 3-7h7" fill="none" stroke="#f6c453" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def page(path,title,desc,body,ld=None,training=False,extra_head=""):
    d="../"*path.count("/")
    def here(h):
        if h==path: return True
        return h=="newsletter/index.html" and path.startswith("newsletter/")
    nav="".join(f'<li><a href="{d}{h}"{" aria-current=\"page\"" if here(h) else ""}>{t}</a></li>' for h,t in NAV)
    lds=[{"@context":"https://schema.org","@type":"Organization","name":"PsychReady","url":B+"/","logo":B+"/logo.svg"},
         {"@context":"https://schema.org","@type":"WebSite","name":"PsychReady","url":B+"/"}]+(ld or [])
    canon=path.replace("index.html","")
    # Absolute URL shared by canonical, og:url, and the sitemap. `d` only prefixes in-page links.
    abs_url=f"{B}/{canon}"
    html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<!-- BASE_URL = {B} -->
<title>{title} | PsychReady</title><meta name="description" content="{desc}">
<link rel="canonical" href="{abs_url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="PsychReady"><meta property="og:title" content="{title} | PsychReady"><meta property="og:description" content="{desc}"><meta property="og:url" content="{abs_url}"><meta property="og:image" content="{B}/assets/og.png">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title} | PsychReady"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{B}/assets/og.png">
{extra_head}<link rel="icon" href="{d}logo.svg" type="image/svg+xml"><link rel="stylesheet" href="{d}assets/style.css">
<link rel="alternate" type="text/markdown" href="{d}llms.txt" title="LLM summary">
<script type="application/ld+json">{json.dumps(lds)}</script></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap bar"><a class="brand" href="{d}index.html">{LOGO}<span>PsychReady</span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
<nav id="nav" aria-label="Main"><ul>{nav}</ul></nav></div></header>
<main id="main" class="wrap">{body}</main>
<footer class="site-footer"><div class="wrap">
<section class="sponsor-strip" aria-label="Sponsor slots"><h2 class="h6">Founding sponsor slots</h2><div class="slots"><a class="slot" href="{d}sponsors.html">Available</a><a class="slot" href="{d}sponsors.html">Available</a><a class="slot" href="{d}sponsors.html">Available</a></div></section>
{DISC if training else ""}
<p><a href="{d}contact.html">Contact</a> · <a href="{d}newsletter/index.html">Past issues</a> · <a href="{d}privacy.html">Privacy</a> · <a href="{d}sponsors.html">Sponsorship &amp; disclosure</a> · <a href="{d}llms.txt">llms.txt</a></p>
<p class="small">© 2026 PsychReady. Practical training for facility behavioral health teams.</p></div></footer>
<script src="{d}assets/site.js" defer></script></body></html>'''
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True); open(path,"w").write(html)
def cta(d=""):
    return f'<aside class="cta"><h2>Get the weekly brief</h2><p>One practical training idea, drill, or checklist for behavioral health teams each week.</p><a class="btn" href="{d}newsletter.html">Subscribe free</a></aside>'
def course(name,desc,url):
    return {"@context":"https://schema.org","@type":"Course","name":name,"description":desc,"url":B+"/"+url,"provider":{"@type":"Organization","name":"PsychReady"},"isAccessibleForFree":True,"educationalLevel":"Professional"}
MODS=[("de-escalation","De-escalation & crisis prevention","Verbal de-escalation, early warning signs, team roles, and safe escalation pathways with physical intervention only as a last resort."),
("suicide-risk","Suicide/self-harm risk & safety planning","Structured risk formulation, collaborative safety planning, means-safety counseling, and handoff documentation."),
("trauma-informed","Trauma-informed & equitable care","Safety, trust, choice, collaboration, and empowerment; recognizing bias; interpreter use; culturally responsive communication."),
("teamstepps","TeamSTEPPS-style teamwork in psych ED","Briefs, huddles, debriefs, SBAR, call-outs, closed-loop communication, and mutual support under pressure."),
("telepsychiatry","Telepsychiatry skills & limits","Virtual assessment etiquette, local tele-presenter roles, privacy, and when to escalate to in-person care (e.g. delirium, severe agitation, tech failure)."),
("restraint-alternatives","Restraint alternatives & human-rights aligned care","Prevention-first approaches, sensory and environmental strategies, least-restrictive practice, and post-incident review aligned with human-rights guidance."),
("physical-health","Physical health deterioration in psychiatric settings","Recognizing and escalating medical deterioration, early warning scores, medication adverse effects, and diagnostic overshadowing."),
("supervision","Clinical supervision competencies","Competency-based supervision, direct observation, structured feedback, gatekeeping high-risk skills, and reflective practice.")]

SRCL={'apa': ('APA Clinical Practice Guidelines', 'https://www.psychiatry.org/psychiatrists/practice/clinical-practice-guidelines'), 'apatele': ('APA Telepsychiatry resources', 'https://www.psychiatry.org/psychiatrists/practice/telepsychiatry'), 'crisis': ('SAMHSA National Behavioral Health Crisis Care Guidance', 'https://www.samhsa.gov/mental-health/national-behavioral-health-crisis-care'), 'tic': ('SAMHSA Trauma-Informed Approaches', 'https://www.samhsa.gov/mental-health/trauma-violence/trauma-informed-approaches-programs'), '988': ('SAMHSA 988 Suicide & Crisis Lifeline', 'https://www.samhsa.gov/mental-health/988'), 'sud': ('SAMHSA Substance Use Treatment Options', 'https://www.samhsa.gov/substance-use/treatment/options'), 'asq': ('NIMH Ask Suicide-Screening Questions (ASQ) Toolkit', 'https://www.nimh.nih.gov/research/research-conducted-at-nimh/asq-toolkit-materials'), 'nsp': ('NIMH Suicide Prevention', 'https://www.nimh.nih.gov/health/topics/suicide-prevention'), 'meds': ('NIMH Mental Health Medications', 'https://www.nimh.nih.gov/health/topics/mental-health-medications')}
ALIGN={'de-escalation': ('Aligns with SAMHSA crisis care guidance (least-restrictive, recovery-oriented response) and APA practice guidelines on evaluation and care.', ['crisis', 'apa']), 'suicide-risk': ("Uses NIMH's free ASQ screening toolkit for medical settings, NIMH suicide-prevention guidance, APA's Psychiatric Evaluation of Adults guideline, and SAMHSA's 988 Lifeline for follow-up.", ['asq', 'nsp', 'apa', '988']), 'trauma-informed': ("Built on SAMHSA's trauma-informed approach: safety; trustworthiness and transparency; peer support; collaboration; empowerment, voice and choice; and cultural, historical and gender issues.", ['tic']), 'teamstepps': ('Teamwork drills support the coordinated, no-wrong-door crisis response described in SAMHSA crisis care guidance.', ['crisis']), 'telepsychiatry': ('Reflects APA telepsychiatry resources for virtual practice.', ['apatele']), 'restraint-alternatives': ("Mirrors SAMHSA's trauma-informed and crisis care guidance, which favors prevention and least-restrictive options.", ['tic', 'crisis']), 'physical-health': ("Medication adverse-effect content draws on NIMH's plain-language medication guide and APA practice guidelines; co-occurring substance use links to SAMHSA treatment resources.", ['meds', 'apa', 'sud']), 'supervision': ('Supervisors check practice against APA practice guidelines and SAMHSA trauma-informed principles.', ['apa', 'tic'])}
def srclinks(keys,d=""):
    return ", ".join(f'<a href="{SRCL[k][1]}" rel="noopener">{SRCL[k][0]}</a>' for k in keys)
def standards():
    return ('<section class="standards" id="standards"><h2>Standards &amp; sources</h2><p>PsychReady modules are aligned with public guidance from three U.S. organizations. We summarize; we don\'t replace their documents or your local policy.</p><ul>'
     '<li><strong>American Psychiatric Association (APA)</strong>: '+srclinks(["apa","apatele"])+'</li>'
     '<li><strong>Substance Abuse and Mental Health Services Administration (SAMHSA)</strong>: '+srclinks(["crisis","tic","988","sud"])+'</li>'
     '<li><strong>National Institute of Mental Health (NIMH)</strong>: '+srclinks(["asq","nsp","meds"])+'</li></ul>'
     '<p class="small">PsychReady is independent and not endorsed by APA, SAMHSA, or NIMH.</p></section>')
def bullets(items):
    return "".join(f"<li>{x}</li>" for x in items)
def checklist(rows):
    body="".join(f"<tr><td>{x}</td><td>☐</td></tr>" for x in rows)
    return ('<table><caption>Observed skills (Yes / Not yet)</caption><thead><tr><th scope="col">Skill</th><th scope="col">Observed?</th></tr></thead><tbody>'
            +body+'</tbody></table><p class="small">Set your own mastery threshold, for example all safety items plus most others. Reassess at one month.</p>')
def skilltable(caption, rows):
    body=""
    for skill, slug, label in rows:
        shown=html.escape(skill, quote=False)
        lab=html.escape(skill, quote=True)
        body+=f'<tr><td>{shown}</td><td><a href="{slug}.html">{html.escape(label, quote=False)}</a></td><td><input type="checkbox" aria-label="Observed: {lab}"></td></tr>'
    return ('<table class="skills"><caption>'+html.escape(caption, quote=False)+'</caption><thead><tr>'
            '<th scope="col">Skill</th><th scope="col">Module</th><th scope="col">Observed?</th>'
            '</tr></thead><tbody>'+body+'</tbody></table>')
def source_line(slug):
    note, keys = ALIGN[slug]
    return f'<p class="small"><strong>Standards:</strong> {html.escape(note, quote=False)} Sources: {srclinks(keys)}.</p>'
def lesson(slug,h1,page_title,desc,meta,objectives,learn,practice,simulate,measure,reading,tail=""):
    note,keys=ALIGN[slug]
    body=f'''<article><h1>{h1}</h1><p class="meta">{meta}</p>
<section><h2>Learning objectives</h2><ul>{bullets(objectives)}</ul></section>
<section><h2>Learn</h2>{learn}<p class="small"><strong>Standards:</strong> {note} Sources: {srclinks(keys)}.</p></section>
<section><h2>Practice</h2>{practice}</section>
<section><h2>Simulate</h2>{simulate}</section>
<section><h2>Measure</h2>{checklist(measure)}</section>
<section><h2>Further reading</h2><ul>{bullets(reading)}</ul></section></article>
'''+standards()+tail
    page(f"training/{slug}.html",page_title,desc,body,[{"@context":"https://schema.org","@type":"LearningResource","name":h1.replace("&amp;","&"),"learningResourceType":"Lesson","educationalLevel":"Professional","audience":{"@type":"Audience","audienceType":"Behavioral health facility staff"},"url":B+f"/training/{slug}.html","isAccessibleForFree":True}],True)

# HOME
mods_cards="".join(f'<li class="card"><h3><a href="training/{a}.html">{t}</a></h3><p>{s}</p></li>' for a,t,s in MODS[:4])
page("index.html","Behavioral Health Staff Training for Facilities","Practical, competency-based training plans, drills, and checklists for hospital and clinic behavioral health and psychiatric teams.",f'''
<section class="hero"><h1>Practical training for facility behavioral health teams</h1>
<p class="lead">Competency-based modules, simulation drills, and program playbooks for nurses, psychiatrists, social workers, techs, security, and primary-care partners.</p>
<p><a class="btn" href="training/index.html">Start training</a> <a class="btn btn-ghost" href="pricing.html">See pricing</a> <a class="btn btn-ghost" href="newsletter.html">Get the weekly brief</a></p></section>
<section><h2>Who PsychReady is for</h2><ul class="grid3">
<li class="card"><h3>Educators &amp; nurse managers</h3><p>Ready-to-run lesson structures, a <a href="training/behavioral-health-staff-training-checklist.html">behavioral health staff training checklist</a>, and refresher calendars.</p></li>
<li class="card"><h3>ED leads &amp; C-L teams</h3><p>Teamwork drills, telepsychiatry workflows, and consult pathways.</p></li>
<li class="card"><h3>Facility leaders</h3><p>Solutions mapped to workforce, access, integration, and funding barriers.</p></li></ul></section>
<section><h2>Featured modules</h2><ul class="grid2">{mods_cards}</ul><p><a href="training/modules.html">See all eight modules →</a></p></section>
<section><h2>How the training works</h2><ol class="steps"><li><strong>Learn</strong> — short focused content per competency.</li><li><strong>Practice</strong> — Behavioral Skills Training: instruct, model, rehearse, feedback.</li><li><strong>Simulate</strong> — interprofessional scenarios with structured debrief.</li><li><strong>Measure</strong> — observed competence and operational outcomes, not just attendance.</li></ol></section>
<section><h2>Behavioral health staff training checklist</h2><p>Inpatient and residential teams can print one checklist for onboarding, annual competencies, and high-risk skills. Each item links to a free module. <a href="training/behavioral-health-staff-training-checklist.html">Open the checklist</a>.</p></section>
<section><h2>Fixing access barriers</h2><p>Staffing gaps, rural access, and siloed care limit psychiatric services. <a href="barriers.html">See solutions mapped to common facility barriers</a>.</p></section>
{cta()}''',[course("PsychReady Behavioral Health Staff Curriculum","Competency-based training for facility behavioral health teams.","training/")])

# TRAINING OVERVIEW
page("training/index.html","Competency-Based Behavioral Health Curriculum","Overview of the PsychReady curriculum: competency mapping, Behavioral Skills Training, simulation, mhGAP-style cascade training, and clinical supervision.",f'''
<h1>Curriculum overview</h1><p class="lead">PsychReady is built around observable competencies, not one-off lectures.</p>
<section><h2>1. Competency-based design</h2><p>Map role-specific competencies for each staff group — assessment, communication, de-escalation, risk, medication safety, trauma-informed care, and equity. Link each to a personal development plan and refresh at induction, annually, and after incidents.</p></section>
<section><h2>2. Behavioral Skills Training (BST)</h2><p>Instruction → modeling → rehearsal → feedback, repeated until staff meet a defined mastery standard on an observed checklist. Your facility sets the threshold.</p></section>
<section><h2>3. Simulation with structured debrief</h2><p>Standardized-patient or role-play scenarios covering aggression, suicide risk, capacity, and ED crises, followed by a structured debrief. Interprofessional scenarios bring nursing, psychiatry, social work, and security together. One published quality-improvement project in a psychiatric emergency setting reported fewer restraints and staff injuries after simulation-based training combined with crisis-prevention content. That is one site's result, and other facilities may not see the same.</p></section>
<section><h2>4. mhGAP-style cascade (“train the trainer”)</h2><p>The WHO mhGAP Intervention Guide and training manuals use cascade training: master trainers prepare local facilitators, who train frontline staff through role-play, case discussion, and skills assessment. This helps training outlast staff turnover.</p></section>
<section><h2>5. Clinical supervision as the backbone</h2><p>Regular, competency-based supervision with direct observation, documented feedback, and post-incident reflection that supports staff wellbeing.</p></section>
<section><h2>6. Aligned with APA, SAMHSA, and NIMH</h2><p>Each module maps to public guidance: APA practice guidelines for clinical care, SAMHSA for crisis care, trauma-informed care and substance use, and NIMH for suicide screening and medication basics. Modules list their sources.</p></section>
<section><h2>Behavioral health staff training checklist</h2><p>Track onboarding, annual competencies, and high-risk skills for inpatient and residential programs on one printable page. <a href="behavioral-health-staff-training-checklist.html">Open the behavioral health staff training checklist</a>. Each item links to a free module.</p></section>
<section><h2>Full lessons</h2><p>Each module is a full lesson: learn, practice, simulate, and measure.</p><ol>{"".join(f'<li><a href="{a}.html">{t}</a></li>' for a,t,_ in MODS)}</ol></section>
{standards()}<p><a class="btn" href="modules.html">Browse modules</a> <a class="btn btn-ghost" href="../pricing.html">See pricing</a></p>{cta("../")}''',[course("PsychReady Curriculum","Competency-based behavioral health staff curriculum.","training/")],True)

# MODULES
ml="".join(f'<section id="{a}" class="card module"><h2>{t}</h2><p>{s}</p><p class="small"><strong>Standards:</strong> {ALIGN[a][0]} Sources: {srclinks(ALIGN[a][1])}.</p><p><a href="{a}.html">Open the full lesson →</a></p></section>' for a,t,s in MODS)
toc="".join(f'<li><a href="#{a}">{t}</a></li>' for a,t,_ in MODS)
page("training/modules.html","Training Modules for Psychiatric & Behavioral Health Staff","Eight PsychReady modules: de-escalation, suicide risk, trauma-informed care, teamwork, telepsychiatry, restraint alternatives, physical health, and supervision.",f'<h1>Training modules</h1><p class="lead">The curriculum overview stays free. Each lesson below is a full module with practice, simulation, and a checklist. For one printable list, use the <a href="behavioral-health-staff-training-checklist.html">behavioral health staff training checklist</a>.</p><nav aria-label="Modules" class="toc"><ol>{toc}</ol></nav>{ml}{standards()}<p><a class="btn" href="../pricing.html">See pricing</a></p>{cta("../")}',
 [{"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"name":t,"url":f"{B}/training/{a}.html"} for i,(a,t,_) in enumerate(MODS)]}],True)

# LESSONS
lesson("de-escalation","De-escalation &amp; crisis prevention","De-escalation & Crisis Prevention Training Module","Lesson on verbal de-escalation and crisis prevention: learn, practice, simulate, measure, and the sources the module follows.","Module 1 · Audience: all direct-care staff, security · Suggested time: 90-minute skills lab plus a 20-minute e-module",
["Recognize early signs of escalating distress and agitation.","Use verbal and non-verbal de-escalation techniques.","Coordinate team roles during an escalating situation.","Explain when and how restrictive interventions may be used, only as a last resort under local policy.","Take part in post-incident debrief and support."],
'''<p>Agitation and aggression are common in emergency and inpatient psychiatric settings. They put patients and staff at risk, and restrictive interventions can cause harm and damage trust. Consensus guidance, such as the American Association for Emergency Psychiatry's Project BETA de-escalation workgroup, recommends verbal de-escalation as a first-line approach.</p>
<ol><li><strong>Respect personal space</strong>: keep a safe distance and an open exit for everyone.</li><li><strong>Avoid provocation</strong>: calm posture, hands visible, matched eye level.</li><li><strong>One communicator</strong>: a single designated staff member leads.</li><li><strong>Concise, simple language</strong>: short sentences, repeat as needed.</li><li><strong>Identify wants and feelings</strong>: ask, listen actively, reflect back.</li><li><strong>Agree or agree to disagree</strong>: find truth to align with.</li><li><strong>Set clear limits</strong>: respectfully, with consequences explained.</li><li><strong>Offer choices and optimism</strong>, including food, drink, quiet space, or medication by choice.</li><li><strong>Debrief</strong> the patient and the staff afterward.</li></ol>''',
'''<p>Use Behavioral Skills Training. Repeat until staff meet your facility's mastery standard on the checklist.</p><ol><li><strong>Instruct</strong> (10 min): review the core skills.</li><li><strong>Model</strong> (10 min): facilitators demonstrate a waiting-room escalation.</li><li><strong>Rehearse</strong> (40 min): rotating triads of patient, communicator, and observer.</li><li><strong>Feedback</strong> (20 min): the observer scores the checklist and the group debriefs what went well, what to change, and any safety concerns.</li></ol>''',
'''<p>Run interprofessional role-play, then a structured debrief. Suggested scenarios: ED boarding frustration, a family visitor conflict, and an intoxicated patient. In the team drill, call for help, assign roles, and run a closed-loop communication check. Physical intervention stays a last resort under local policy.</p>''',
["Positions safely with an exit route","Introduces self and uses a calm tone","Uses short, clear statements","Reflects the person's feelings or needs","Offers at least two genuine choices","Sets a respectful limit","Coordinates with the team using closed-loop communication","Participates in the debrief"],
["Richmond JS et al. Verbal De-escalation of the Agitated Patient: Consensus Statement of the AAEP Project BETA De-escalation Workgroup. <em>West J Emerg Med</em>, 2012.","NICE guideline NG10: Violence and aggression: short-term management in mental health, health and community settings.","WHO mhGAP Intervention Guide, version 2.0.",f"SAMHSA, {srclinks(['crisis'])}.",f"SAMHSA, {srclinks(['tic'])}.",f"APA, {srclinks(['apa'])}.","WHO QualityRights training materials on human-rights-aligned care."],
'''<section class="resources"><h2>Recommended training resources</h2><p class="small"><strong>Disclosure:</strong> PsychReady may in future earn a commission from some recommended resources. We'll label every such link clearly. No affiliate links are active today.</p><ul><li>Accredited crisis-prevention or de-escalation certification programs for your region. We'll list vetted options here.</li></ul></section>''')

lesson("suicide-risk","Suicide/self-harm risk &amp; safety planning","Suicide and Self-Harm Risk Training Module","Lesson on suicide and self-harm risk for facility staff: screening, collaborative safety planning, means safety, handoff, and sources.","Module 2 · Audience: nurses, social workers, psychiatrists, and any staff who screen · Suggested time: 90-minute skills lab plus a 20-minute e-module",
["Use a structured screen, such as NIMH's Ask Suicide-Screening Questions (ASQ) toolkit, and explain that a screen is not a full assessment.","Ask directly about suicidal ideation, plan, intent, and recent behavior.","Build a collaborative safety plan and counsel on means safety.","Document the risk formulation and the handoff.","Name 988 or the local crisis resource, and follow local emergency policy when danger is immediate."],
f'''<p>NIMH publishes a free ASQ toolkit for medical settings ({srclinks(["asq"])}). A positive screen is a reason to stay with the person and complete a clinical evaluation under your policy. It is not a diagnosis and it does not by itself set a disposition.</p>
<p>Ask in plain language about thoughts of suicide, a plan, intent, and what has happened recently. Collaborative safety planning usually covers warning signs, ways to cope, people to contact, professionals to contact, making the environment safer, and reasons for living. Means-safety counseling is specific: which method is available, and what the person will do to put time and distance between themselves and that method. Do not promise that a plan removes risk.</p>
<p>The handoff names who was told, what the plan is, and when follow-up happens. In the United States, {srclinks(["988"])} is the 24-hour Suicide &amp; Crisis Lifeline. If someone is in immediate danger, follow your emergency policy rather than handing them a number and leaving.</p>''',
'''<p>Behavioral Skills Training:</p><ol><li><strong>Instruct</strong> the screen questions and the parts of a safety plan.</li><li><strong>Model</strong> a calm, direct question about suicide, then a pause for the answer.</li><li><strong>Rehearse</strong> in triads: an ED patient who says they cannot go on; an inpatient who has been saving medication; a primary-care partner calling about a positive screen.</li><li><strong>Feedback</strong> on whether the ask was direct, whether means safety was concrete, and whether anyone was left alone against policy.</li></ol>''',
'''<p>Interprofessional simulation: a nurse starts the screen, a social worker drafts the safety plan with the person, and a psychiatrist reviews the formulation. Security joins only if local policy calls for it. Debrief what was asked, what was missed, and whether the handoff would let the next clinician continue the plan.</p>''',
["Asks directly about thoughts of suicide","Asks about plan, intent, and recent behavior","Stays with the person when risk is acute, following local policy","Completes a collaborative safety plan with warning signs, coping steps, and contacts","Discusses means safety in concrete terms","Documents the formulation and the handoff","Names 988 or the local crisis resource","Does not treat the screen as a complete assessment"],
[f"NIMH, {srclinks(['asq'])}.",f"NIMH, {srclinks(['nsp'])}.",f"APA, {srclinks(['apa'])} (including evaluation of adults).",f"SAMHSA, {srclinks(['988'])}.","Stanley B, Brown GK. Safety Planning Intervention: a brief intervention to mitigate suicide risk. Cogn Behav Pract. 2012."])

lesson("trauma-informed","Trauma-informed &amp; equitable care","Trauma-Informed and Equitable Care Training Module","Lesson on trauma-informed and equitable care using SAMHSA's principles: safety, trust, choice, collaboration, and cultural responsiveness.","Module 3 · Audience: all staff who meet patients and families · Suggested time: 75-minute skills lab plus a 20-minute e-module",
["Name SAMHSA's trauma-informed principles and give a unit example of each.","Offer real choices and explain what will happen before it happens.","Ask permission before touch and arrange an interpreter when one is needed.","Notice bias in language, assumptions, and who gets heard.","Avoid asking someone to retell a trauma story for staff curiosity."],
f'''<p>This module follows {srclinks(["tic"])}. SAMHSA describes six principles: safety; trustworthiness and transparency; peer support; collaboration and mutuality; empowerment, voice and choice; and cultural, historical, and gender issues.</p>
<p>On a unit, that looks like predictable routines, saying what you are about to do, offering two acceptable options instead of an order, and using a qualified interpreter rather than a family member when clinical information is shared. Peer support is a role, not a slogan: know how your facility involves peers. Equity work includes who is searched, who is believed, and whose language is treated as agitation.</p>''',
'''<p>Behavioral Skills Training:</p><ol><li><strong>Instruct</strong> the six principles with one facility example each.</li><li><strong>Model</strong> an approach from the side, an introduction, and a choice.</li><li><strong>Rehearse</strong> rewriting a commanding script into one that explains and offers a choice, including a scene that needs an interpreter.</li><li><strong>Feedback</strong> on whether the choice was genuine and whether the person was talked about as if they were not there.</li></ol>''',
'''<p>Scenarios: a person who startles when staff approach from behind; a family meeting in which staff talk over the person; a request to repeat a trauma history that is already in the record. Debrief safety, choice, and what staff could have explained first.</p>''',
["Explains what will happen before doing it","Offers at least one real choice","Asks permission before touch","Arranges a qualified interpreter when needed","Does not require a trauma story to be retold for staff curiosity","Names one assumption they checked"],
[f"SAMHSA, {srclinks(['tic'])}."])

lesson("teamstepps","TeamSTEPPS-style teamwork in the psych ED","Teamwork in the Psychiatric ED Training Module","Lesson on briefs, huddles, debriefs, SBAR, and closed-loop communication for psychiatric emergency teams.","Module 4 · Audience: ED and crisis-team clinicians, techs, and security · Suggested time: 60-minute drill plus a 15-minute e-module",
["Lead a short brief that assigns roles.","Give an SBAR that separates situation, background, assessment, and recommendation.","Use a call-out and a closed-loop check-back.","Call for help before the team is overwhelmed.","Join a debrief that includes what to change next time."],
f'''<p>TeamSTEPPS is the Agency for Healthcare Research and Quality teamwork program. This lesson borrows its tools for psychiatric emergency teams. It is not a substitute for an AHRQ course.</p>
<p>A <strong>brief</strong> assigns roles before the shift or the event. A <strong>huddle</strong> resets the plan when the situation changes. A <strong>debrief</strong> asks what went well and what to change. <strong>SBAR</strong> is situation, background, assessment, recommendation. A <strong>call-out</strong> says the critical fact out loud. <strong>Closed-loop</strong> communication means the receiver repeats the request and the sender confirms. These drills support the coordinated, no-wrong-door crisis response in {srclinks(["crisis"])}.</p>''',
'''<p>Behavioral Skills Training:</p><ol><li><strong>Instruct</strong> brief, huddle, debrief, SBAR, call-out, and check-back.</li><li><strong>Model</strong> a 60-second brief and a 30-second SBAR to psychiatry.</li><li><strong>Rehearse</strong> in groups of four, rotating leader and receiver.</li><li><strong>Feedback</strong> on whether the recommendation was explicit and whether the loop was closed.</li></ol>''',
'''<p>Simulation: an ED surge with one person who is agitated and also has a new medical complaint. Nursing, psychiatry, and security brief, then the nurse gives SBAR, then the team huddles when the person tries to leave. Debrief role clarity and whether anyone was left without a job.</p>''',
["Leads a brief that names roles","Gives SBAR with a clear recommendation","Uses a call-out for a critical fact","Closes the loop and confirms it","Calls for help before becoming overwhelmed","Joins the debrief and names one change"],
[f"SAMHSA, {srclinks(['crisis'])}.","Agency for Healthcare Research and Quality. TeamSTEPPS."])

lesson("telepsychiatry","Telepsychiatry skills &amp; limits","Telepsychiatry Skills Training Module","Lesson on virtual assessment etiquette, the on-site tele-presenter role, privacy, and when to convert to in-person care.","Module 5 · Audience: remote clinicians and on-site tele-presenters · Suggested time: 60-minute lab plus a 15-minute e-module",
["Open a visit by confirming identity, location, and who else is in the room.","Explain privacy limits of the video connection.","Describe the on-site tele-presenter's job.","Name situations that should move to in-person care, including delirium, severe agitation, and technology failure.","State the local escalation contact before the visit starts."],
f'''<p>Follow {srclinks(["apatele"])} for how virtual practice is framed. The remote clinician and the person on site both need to know where the person is, who can hear the visit, and what happens if the connection fails.</p>
<p>The tele-presenter is the local staff member who can see the room, call for help, and carry out an in-person task the remote clinician cannot. Convert to in-person care when you cannot examine what matters, when agitation cannot be managed through the screen, when delirium or another medical emergency is possible, or when the technology fails. Do not continue a visit you cannot safely complete.</p>''',
'''<p>Behavioral Skills Training:</p><ol><li><strong>Instruct</strong> the opening script: identity, location, others in the room, privacy, and the backup plan.</li><li><strong>Model</strong> that script, including a failed-connection plan.</li><li><strong>Rehearse</strong> the remote clinician and the tele-presenter together.</li><li><strong>Feedback</strong> on whether escalation was named before it was needed.</li></ol>''',
'''<p>Scenarios: the connection drops during a risk question; the person is more agitated than the local staff described; a family member is off camera and answering for the person. Debrief what the tele-presenter does in the room and when the visit stops.</p>''',
["Confirms identity and location","States who else is present","Explains privacy limits","Names the tele-presenter's role","Names a reason to convert to in-person care","Has a local escalation contact before starting"],
[f"APA, {srclinks(['apatele'])}."])

lesson("restraint-alternatives","Restraint alternatives &amp; human-rights aligned care","Restraint Alternatives Training Module","Lesson on prevention, sensory and environmental strategies, least-restrictive practice, and post-incident review.","Module 6 · Audience: direct-care staff and security · Suggested time: 75-minute lab plus a 15-minute e-module",
["Try prevention and environmental changes before any restrictive intervention.","Offer sensory, space, and choice-based options.","Explain a limit and why it exists.","Use restrictive measures only as a last resort under local policy.","Hold a post-incident review that includes the person when they can take part."],
f'''<p>{srclinks(["tic"])} and {srclinks(["crisis"])} favor prevention and the least restrictive response. Restrictive interventions can injure people and damage trust. This lesson does not authorize restraint or seclusion. Your facility policy, and the law where you practice, decide if and when those measures may be used.</p>
<p>Prevention includes noise, crowding, hunger, pain, fear, and unclear rules. Sensory and environmental options include a quieter space, a drink, a blanket, dimmer light, and a route that is not a dead end. After any incident, review what was tried, who was hurt or frightened, and what the team will change. Invite the person into that review when they are able to join.</p>''',
'''<p>Behavioral Skills Training:</p><ol><li><strong>Instruct</strong> a prevention checklist for the room and the first four non-restrictive options your unit actually has.</li><li><strong>Model</strong> offering two options before stating a limit.</li><li><strong>Rehearse</strong> an environmental scan: exits, noise, audience, and weapons or hazards.</li><li><strong>Feedback</strong> on whether restriction was discussed before other options were tried.</li></ol>''',
'''<p>Simulation: a person pacing and shouting in a crowded alcove. The team reduces the audience, offers space and a drink, assigns one communicator, and only then states a limit from policy. Debrief the order of those steps and the post-incident review.</p>''',
["Tries at least two non-restrictive options first","Reduces noise, crowding, or audience when possible","Explains the limit in plain language","Assigns one communicator","Documents what was tried","Plans a post-incident review that includes the person when possible"],
[f"SAMHSA, {srclinks(['tic'])}.",f"SAMHSA, {srclinks(['crisis'])}.","WHO QualityRights materials on human-rights-aligned care."])

lesson("physical-health","Physical health deterioration in psychiatric settings","Physical Health Deterioration Training Module","Lesson on recognizing medical deterioration, medication adverse effects, diagnostic overshadowing, and when to escalate.","Module 7 · Audience: nurses, techs, and prescribing clinicians · Suggested time: 75-minute lab plus a 20-minute e-module",
["Check airway, breathing, circulation, and consciousness when someone looks unwell.","Avoid explaining new physical signs only by the psychiatric diagnosis.","Use the facility early-warning score and escalation policy.","Name common medication adverse effects using a plain-language source and the facility medication list.","Escalate co-occurring substance-use emergencies without delaying medical care."],
f'''<p>Diagnostic overshadowing means a physical problem is missed because staff attribute it to a psychiatric diagnosis or to behavior. New confusion, chest pain, trouble breathing, a stiff or very hot body, collapse, or a sudden change in alertness needs the same medical response you would use anywhere else.</p>
<p>Use your facility's early-warning score and the escalation steps that go with it. Do not invent a threshold for this lesson. {srclinks(["meds"])} is a plain-language overview of mental health medications and adverse effects, not a prescribing guide. For co-occurring substance use, {srclinks(["sud"])} describes treatment options. Withdrawal and overdose are medical emergencies first.</p>
<p>This lesson is for recognition and escalation. It is not a protocol for doses or for choosing a medicine.</p>''',
'''<p>Behavioral Skills Training:</p><ol><li><strong>Instruct</strong> a head-to-toe concern list: airway, breathing, circulation, consciousness, temperature, and glucose if that is in your policy.</li><li><strong>Model</strong> an escalation call that leads with the physical signs, not the diagnosis.</li><li><strong>Rehearse</strong> reading your own early-warning tool and stating the action it requires.</li><li><strong>Feedback</strong> on whether the psychiatric diagnosis delayed the medical call.</li></ol>''',
'''<p>Simulation: a person described as just anxious who is short of breath and sweaty, and a second scene in which new confusion is blamed on a medication the team has not checked. Debrief overshadowing, who was called, and what was documented.</p>''',
["Checks airway, breathing, circulation, and consciousness","Does not attribute new physical signs only to the psychiatric diagnosis","Uses the facility early-warning score and escalation policy","Names a medication adverse effect to watch for from the facility list","Treats possible overdose or severe withdrawal as a medical emergency","Documents the handoff to medical staff"],
[f"NIMH, {srclinks(['meds'])}.",f"APA, {srclinks(['apa'])}.",f"SAMHSA, {srclinks(['sud'])}."])

lesson("supervision","Clinical supervision competencies","Clinical Supervision Training Module","Lesson on competency-based supervision, direct observation, structured feedback, and gatekeeping high-risk skills.","Module 8 · Audience: preceptors, charge nurses, and clinical supervisors · Suggested time: 60-minute lab plus a 15-minute e-module",
["Observe a high-risk skill directly instead of counting attendance.","Give feedback as what went well, what to change, and one next step.","Withhold sign-off when safety items on the checklist are not met.","Invite the staff member's view of the same event.","Check practice against local policy, APA practice guidelines, and SAMHSA trauma-informed principles."],
f'''<p>Supervision is how the other modules stay in use after the class ends. High-risk skills for this curriculum are de-escalation, suicide response, and medical escalation. Sign-off means a supervisor saw the skill and the safety items were met. Attendance is not sign-off.</p>
<p>Structured feedback is short: what went well, what to change, and the next time you will look again. Reflective practice asks the staff member what they noticed before the supervisor adds their view. {srclinks(["apa"])} and {srclinks(["tic"])} are the external checks. Local policy still governs what staff may do.</p>''',
'''<p>Behavioral Skills Training for supervisors:</p><ol><li><strong>Instruct</strong> the three-part feedback script and which checklist items are safety items.</li><li><strong>Model</strong> a 10-minute feedback conversation after a role-play.</li><li><strong>Rehearse</strong> telling someone they are not yet signed off, without humiliating them.</li><li><strong>Feedback</strong> on whether the standard was named and whether a next observation was scheduled.</li></ol>''',
'''<p>Simulation: a supervisee wants you to sign off a colleague who missed the safety items on the de-escalation checklist but has finished the e-module. Practice the refusal, the coaching plan, and what you document. Debrief gatekeeping and respect.</p>''',
["Observes the skill directly","Uses what went well, what to change, and one next step","Withholds sign-off when safety items are not met","Invites the staff member's account of the event","Names the policy or standard being applied","Schedules the next observation"],
[f"APA, {srclinks(['apa'])}.",f"SAMHSA, {srclinks(['tic'])}."])

# CHECKLIST
def module_rows(slug, label, items):
    return [(item, slug, label) for item in items]
CHECK_TITLE="Behavioral Health Staff Training Checklist"
CHECK_DESC="Printable behavioral health staff training checklist for inpatient and residential facilities, covering onboarding, annual competencies, and high-risk skills."
check_path="training/behavioral-health-staff-training-checklist.html"
check_url=B+"/training/behavioral-health-staff-training-checklist.html"
onboarding_table=skilltable("Onboarding in the first weeks",[
("Positions safely, uses a calm tone and short statements, and offers at least two genuine choices before setting a limit.","de-escalation","De-escalation"),
("Asks directly about thoughts of suicide, a plan, intent, and recent behavior, and does not treat the screen as a complete assessment.","suicide-risk","Suicide risk"),
("Completes a collaborative safety plan with warning signs, coping steps, contacts, and concrete means safety, and documents the handoff.","suicide-risk","Suicide risk"),
("Explains what will happen before doing it, offers a real choice, and asks permission before touch.","trauma-informed","Trauma-informed care"),
("Checks airway, breathing, circulation, and consciousness, and escalates new physical signs with the facility early-warning policy.","physical-health","Physical health"),
("Names a preceptor, who observes a high-risk skill directly and withholds sign-off when a safety item is not met.","supervision","Supervision")])
annual_table=skilltable("Annual competencies",[
("Re-observe safe positioning, one communicator, choices, a respectful limit, and the debrief.","de-escalation","De-escalation"),
("Re-observe a direct question about suicide, a collaborative safety plan, means safety, and the handoff.","suicide-risk","Suicide risk"),
("Re-observe an explanation before action, a real choice, permission before touch, and a qualified interpreter when clinical information is shared.","trauma-informed","Trauma-informed care"),
("Re-observe at least two non-restrictive options before a limit, and a plan for post-incident review.","restraint-alternatives","Restraint alternatives"),
("If the role includes video visits, re-observe identity, location, privacy, and a reason to convert to in-person care.","telepsychiatry","Telepsychiatry"),
("Re-observe a brief that names roles, an SBAR with a recommendation, and a closed-loop check-back.","teamstepps","Teamwork"),
("Re-observe early-warning escalation so new physical signs are not attributed only to the psychiatric diagnosis.","physical-health","Physical health"),
("If the person precepts others, re-observe direct observation, three-part feedback, and withholding sign-off when safety items are not met.","supervision","Supervision"),
("After an incident, run a targeted refresher on the skill involved instead of waiting for the annual lab.","supervision","Supervision")])
HIGH=[
("skill-de-escalation","De-escalation and crisis prevention","de-escalation","De-escalation",
"<p>Physical intervention stays a last resort under local policy.</p>",
["Positions safely with an exit route","Introduces self and uses a calm tone","Uses short, clear statements","Reflects the person's feelings or needs","Offers at least two genuine choices","Sets a respectful limit","Coordinates with the team using closed-loop communication","Participates in the debrief"]),
("skill-suicide-risk","Suicide risk screening and safety planning","suicide-risk","Suicide risk",
"<p>Use a structured screen, such as NIMH's ASQ toolkit, and explain that a screen is not a full assessment. If someone is in immediate danger, follow your emergency policy rather than handing them a number and leaving.</p>",
["Asks directly about thoughts of suicide","Asks about plan, intent, and recent behavior","Stays with the person when risk is acute, following local policy","Completes a collaborative safety plan with warning signs, coping steps, and contacts","Discusses means safety in concrete terms","Documents the formulation and the handoff","Names 988 or the local crisis resource","Does not treat the screen as a complete assessment"]),
("skill-trauma-informed","Trauma-informed care","trauma-informed","Trauma-informed care",
"<p>Explain what will happen before it happens, and offer a real choice. Use a qualified interpreter rather than a family member when clinical information is shared.</p>",
["Explains what will happen before doing it","Offers at least one real choice","Asks permission before touch","Arranges a qualified interpreter when needed","Does not require a trauma story to be retold for staff curiosity","Names one assumption they checked"]),
("skill-restraint","Restraint and seclusion safety","restraint-alternatives","Restraint alternatives",
"<p>These items are prevention and least-restrictive practice. This checklist does not authorize restraint or seclusion. Your facility policy, and the law where you practice, decide if and when those measures may be used.</p>",
["Tries at least two non-restrictive options first","Reduces noise, crowding, or audience when possible","Explains the limit in plain language","Assigns one communicator","Documents what was tried","Plans a post-incident review that includes the person when possible"]),
("skill-telepsychiatry","Telepsychiatry","telepsychiatry","Telepsychiatry",
"<p>Use this table only when the role includes video visits. Stop the visit when you cannot examine what matters, when agitation cannot be managed through the screen, when delirium or another medical emergency is possible, or when the technology fails.</p>",
["Confirms identity and location","States who else is present","Explains privacy limits","Names the tele-presenter's role","Names a reason to convert to in-person care","Has a local escalation contact before starting"]),
("skill-supervision","Supervision","supervision","Supervision",
"<p>Sign-off means a supervisor saw the skill and the safety items were met. Attendance is not sign-off.</p>",
["Observes the skill directly","Uses what went well, what to change, and one next step","Withholds sign-off when safety items are not met","Invites the staff member's account of the event","Names the policy or standard being applied","Schedules the next observation"]),
("skill-teamwork","Teamwork","teamstepps","Teamwork",
"<p>These items borrow brief, huddle, debrief, SBAR, call-out, and closed-loop tools from TeamSTEPPS, the Agency for Healthcare Research and Quality teamwork program. They are not a substitute for an AHRQ course. Use them on inpatient units, in residential programs, and in the psychiatric emergency department.</p>",
["Leads a brief that names roles","Gives SBAR with a clear recommendation","Uses a call-out for a critical fact","Closes the loop and confirms it","Calls for help before becoming overwhelmed","Joins the debrief and names one change"]),
("skill-physical-health","Medical escalation","physical-health","Physical health",
"<p>The supervision module names medical escalation, with de-escalation and suicide response, as a high-risk skill. This table is recognition and escalation. It is not a protocol for doses or for choosing a medicine. Use the facility early-warning score and the steps that go with it.</p>",
["Checks airway, breathing, circulation, and consciousness","Does not attribute new physical signs only to the psychiatric diagnosis","Uses the facility early-warning score and escalation policy","Names a medication adverse effect to watch for from the facility list","Treats possible overdose or severe withdrawal as a medical emergency","Documents the handoff to medical staff"])]
high_html=""
for sid, heading, slug, label, intro, items in HIGH:
    high_html+=f'<section id="{sid}"><h3><a href="{slug}.html">{html.escape(heading)}</a></h3>{intro}{source_line(slug)}{skilltable(heading, module_rows(slug, label, items))}</section>'
check_body=f'''<article>
<h1>Behavioral health staff training checklist</h1>
<p class="lead">A printable checklist for staff training in inpatient and residential behavioral health facilities. Use it for onboarding, annual competencies, and direct observation of high-risk skills.</p>
<p class="no-print"><button class="btn" type="button" data-print>Print this checklist</button></p>
<p class="meta">Staff name _______________ &nbsp; Role _______________ &nbsp; Unit _______________<br>
Date _______________ &nbsp; Preceptor _______________</p>
<p>Check a box only after a preceptor has seen the skill. Reading a module is not sign-off. Your facility sets the mastery threshold, for example all safety items plus most others. Reassess at one month. Refresh at induction, annually, and after incidents.</p>
<p>The onboarding and annual tables are the program record: one mark when observation of that competency is done. The high-risk tables are the skills the preceptor watches. Skip any row the role does not perform. Marks stay in this browser tab and are not sent to PsychReady. Print a copy if you need a record.</p>
<p>This checklist is a training aid. It is not a regulation, and it does not replace local policy, accredited training, or the public sources linked below.</p>
<nav class="toc" aria-label="Checklist"><ol>
<li><a href="#onboarding">Onboarding</a></li>
<li><a href="#annual">Annual competencies</a></li>
<li><a href="#high-risk">High-risk skills</a></li>
</ol></nav>
<section id="onboarding"><h2>Onboarding</h2>
<p>In the first weeks, cover de-escalation, suicide and self-harm risk, trauma-informed care, and physical-health escalation. Pair each new hire with a preceptor. When the role includes crisis teamwork, video visits, or a situation where restriction might be considered, observe those high-risk tables during orientation as well.</p>
{onboarding_table}
</section>
<section id="annual"><h2>Annual competencies</h2>
<p>Hold an annual skills lab and re-observe the competencies this role uses. Between labs, a 10-minute huddle can rehearse one skill. After an incident, run a targeted refresher rather than waiting for the next annual date.</p>
{annual_table}
</section>
<section id="high-risk"><h2>High-risk skills</h2>
<p>Use these tables while you watch. Check a box only for a skill you saw. For de-escalation, suicide response, and medical escalation, withhold sign-off when a safety item is not met.</p>
{high_html}
</section>
</article>
'''+standards()+cta("../")
page(check_path, CHECK_TITLE, CHECK_DESC, check_body, [
{"@context":"https://schema.org","@type":"LearningResource","name":"Behavioral health staff training checklist","description":CHECK_DESC,"learningResourceType":"Checklist","educationalLevel":"Professional","audience":{"@type":"Audience","audienceType":"Inpatient and residential behavioral health facility staff"},"url":check_url,"isAccessibleForFree":True},
{"@context":"https://schema.org","@type":"ItemList","name":"Behavioral health staff training checklist","itemListElement":[
{"@type":"ListItem","position":1,"name":"Onboarding","url":check_url+"#onboarding"},
{"@type":"ListItem","position":2,"name":"Annual competencies","url":check_url+"#annual"},
{"@type":"ListItem","position":3,"name":"High-risk skills","url":check_url+"#high-risk"}]}], True)

# BARRIERS
BAR=[("Workforce shortages",["Hub-and-spoke telepsychiatry for ED and inpatient consults.","Expand the team with psychiatric mental health nurse practitioners and clearly defined roles.","Regional training pipelines and rural residency or fellowship tracks.","Retention: flexible schedules, wellbeing support, shared caseloads."]),
("Rural & underserved access",["Telepsychiatry with local nursing or tech support and in-person backup.","Task-shifting screening and follow-up to trained primary-care and community staff (mhGAP approach).","Partnerships with community mental health, peer support, and mobile crisis teams."]),
("Integration with primary care, ED & medical floors",["Collaborative care: screening, care manager, scheduled psychiatric case review.","Shared protocols and interdisciplinary huddles.","Consultation-liaison services, on-site or virtual."]),
("Pathways & continuity",["Standardized ED and inpatient triage, disposition, and medication-start protocols.","Formal referral agreements with closed-loop handoffs.","Care navigators and follow-up after discharge."]),
("Funding & reimbursement",["Use billable collaborative-care and telehealth codes where available.","Track boarding hours, readmissions, and time-to-consult to build the business case.","Grants, state behavioral health funds, and quality incentive programs."]),
("Stigma & culture",["Facility-wide training on recognizing and responding to mental illness.","Patient and family involvement in service design.","Leadership champions who keep behavioral health a visible priority."]),
("Technology & infrastructure",["Reliable video, EHR integration, and interpreter access.","Simple workflows that busy staff will actually use.","Continuous monitoring of access and outcome metrics."])]
bb="".join(f'<section class="card"><h2>{t}</h2><ul>{"".join(f"<li>{x}</li>" for x in xs)}</ul></section>' for t,xs in BAR)
page("barriers.html","Solutions to Barriers in Psychiatric Services","Practical solutions mapped to common facility barriers to psychiatric care: workforce, rural access, integration, pathways, funding, stigma, and technology.",f'<h1>Solutions to barriers in psychiatric services</h1><p class="lead">Approaches drawn from WHO guidance, collaborative care models, and telepsychiatry literature. Adapt them to your local context and regulations.</p>{bb}<p>Training gaps underlie many of these barriers. <a href="training/index.html">See the curriculum</a>.</p>{cta()}')

# EDUCATORS
page("for-educators.html","How to Run a Behavioral Health Training Program","A playbook for educators: induction, refreshers, simulation, supervision, and measuring outcomes for behavioral health staff training.",f'''
<h1>For educators: running your program</h1>
<ol class="steps big"><li><h2>Induction</h2><p>Within the first weeks, cover core modules: de-escalation, suicide risk, trauma-informed care, and physical-health escalation. Pair each new hire with a preceptor and the <a href="training/behavioral-health-staff-training-checklist.html">behavioral health staff training checklist</a>.</p></li>
<li><h2>Refreshers</h2><p>Hold annual skills labs and run 10-minute micro-learning huddles on the unit. After incidents, run targeted refreshers.</p></li>
<li><h2>Simulation</h2><p>Run interprofessional scenarios quarterly or more often, always with structured debrief. Small and rural sites can share regional simulation days.</p></li>
<li><h2>Supervision</h2><p>Use direct observation, documented feedback, and reflective practice, and gatekeep high-risk skills.</p></li>
<li><h2>Measure outcomes</h2><p>Track confidence and observed competence before training, after it, and at one month. Link results to operational measures such as restraint and seclusion events, staff injuries, time-to-consult, and incident themes. Run booster sessions when metrics slip.</p></li></ol>
<section><h2>Build local capacity</h2><p>Use mhGAP-style cascade training: develop master trainers who coach unit educators so the program survives turnover.</p></section>{cta()}''')

# PRICING
page("pricing.html","Pricing","PsychReady pricing. The curriculum overview is free. Facility seats, the Module Pack, and the Program Playbook are paid.",'''
<h1>Pricing</h1>
<p id="seat-thanks" class="disclaimer" hidden><strong>Thank you.</strong> Check your email for the receipt and onboarding next steps.</p>
<p class="lead">The curriculum overview remains free. Paid plans unlock facility seats and packs.</p>
<div class="grid2">
<section class="card"><h2>Facility Seat Access</h2><p><strong>$35/month per seat</strong></p><p>The seat count can be chosen at checkout.</p><p><a class="btn" href="https://buy.stripe.com/aFa6oI4tK3sA8jzaVl0Fi02" rel="noopener">Buy seats (monthly)</a></p></section>
<section class="card"><h2>Facility Seat Access (Annual)</h2><p><strong>$350/year per seat</strong></p><p>The seat count can be chosen at checkout.</p><p><a class="btn" href="https://buy.stripe.com/5kQfZigcsfbi0R7d3t0Fi03" rel="noopener">Buy seats (annual)</a></p></section>
<section class="card"><h2>Module Pack</h2><p><strong>$79 one-time</strong></p><p><a class="btn" href="https://buy.stripe.com/aFa7sM1hy7IQ43j6F50Fi00" rel="noopener">Buy Module Pack</a></p></section>
<section class="card"><h2>Program Playbook</h2><p><strong>$149 one-time</strong></p><p><a class="btn" href="https://buy.stripe.com/4gM3cw2lC7IQeHXd3t0Fi01" rel="noopener">Buy Program Playbook</a></p></section>
</div>
<p class="small">Questions? <a href="mailto:psychready@mail.grokbot.com?subject=Facility%20seats%20inquiry">psychready@mail.grokbot.com</a></p>
''')

# NEWSLETTER
page("newsletter.html","Weekly Behavioral Health Training Brief","Subscribe to the PsychReady weekly brief: one practical drill, checklist, or training idea for facility behavioral health teams.",'''
<h1>The PsychReady weekly brief</h1><p class="lead">One practical, five-minute read each week: a drill, a checklist, a barrier fix, or a summary of new evidence.</p>
<form class="form" action="mailto:psychready@mail.grokbot.com?subject=Subscribe%20me%20to%20the%20PsychReady%20newsletter" method="post" enctype="text/plain">
<label for="n">Name</label><input id="n" name="name" autocomplete="name" required>
<label for="e">Work email</label><input id="e" name="email" type="email" autocomplete="email" required>
<label class="check"><input type="checkbox" name="consent" required> I agree to receive the weekly brief and can unsubscribe anytime.</label>
<button class="btn" type="submit">Subscribe</button></form>
<p class="small">For now, signup opens your email app. We don't store anything on a server yet. See our <a href="privacy.html">privacy policy</a>.</p>
<p><a href="newsletter/index.html">Read past issues</a></p>''')

# SPONSORS
page("sponsors.html","Sponsor PsychReady","Sponsorship tiers and disclosure policy for PsychReady. Open for founding sponsors supporting free behavioral health staff training.",'''
<h1>Sponsorship</h1><p class="lead"><strong>Open for founding sponsors.</strong> PsychReady has no current sponsors.</p>
<section><h2>Tiers (placeholder)</h2><div class="grid3"><div class="card"><h3>Supporter</h3><p>Footer slot and newsletter mention.</p></div><div class="card"><h3>Partner</h3><p>Footer slot, a monthly newsletter feature, and a sponsor page listing.</p></div><div class="card"><h3>Founding sponsor</h3><p>Everything in Partner, plus "supported by" credit on one module.</p></div></div><p>Pricing on request.</p></section>
<section><h2>How sponsorship works</h2><ul><li>Sponsors never control or review clinical or educational content.</li><li>All sponsored placements are clearly labeled.</li><li>We don't accept sponsors whose products conflict with patient safety or human-rights-aligned care.</li></ul></section>
<section><h2>Disclosure</h2><p>Any sponsorship or affiliate relationship will be disclosed on this page and next to the relevant content.</p></section>
<p><a class="btn" href="contact.html">Enquire about sponsorship</a></p>''')

page("about.html","About PsychReady","PsychReady's mission and evidence sources, including APA, SAMHSA, NIMH, WHO mhGAP, and simulation research.",f'''
<h1>About PsychReady</h1><section><h2>Mission</h2><p>Help facilities build confident, competent, and humane behavioral health teams through practical, evidence-informed training.</p></section>
<section><h2>What our content is based on</h2><p>Training modules are aligned first with three U.S. organizations:</p><ul>
<li><strong>American Psychiatric Association (APA)</strong> &mdash; {srclinks(["apa","apatele"])}</li>
<li><strong>Substance Abuse and Mental Health Services Administration (SAMHSA)</strong> &mdash; {srclinks(["crisis","tic","988","sud"])}</li>
<li><strong>National Institute of Mental Health (NIMH)</strong> &mdash; {srclinks(["asq","nsp","meds"])}</li>
<li>WHO mhGAP Intervention Guide and training manuals</li>
<li>Inpatient mental health quality standards (for example, Royal College of Psychiatrists' quality networks)</li>
<li>NICE guidance on violence and aggression</li>
<li>Published research on simulation and Behavioral Skills Training in psychiatric education</li>
<li>Collaborative care and telepsychiatry literature</li>
<li>WHO QualityRights human-rights guidance</li></ul>
<p>We avoid made-up statistics. When we cite results, we name the setting and its limits. PsychReady is independent and not endorsed by APA, SAMHSA, or NIMH.</p></section>
{standards()}
<section><h2>Disclaimer</h2>{DISC}</section>''')
page("contact.html","Contact PsychReady","Contact PsychReady about training, feedback, corrections, or sponsorship.",'<h1>Contact</h1><p>Email: <a href="mailto:psychready@mail.grokbot.com?subject=Facility%20seats%20inquiry">psychready@mail.grokbot.com</a></p><p>We welcome corrections, feedback, and module requests.</p>')
page("privacy.html","Privacy Policy","PsychReady privacy policy covering newsletter signups and future analytics.",'''
<h1>Privacy policy</h1><p class="meta">Last updated: October 15, 2026</p>
<h2>Newsletter</h2><p>If you subscribe, we use your name and email only to send the brief. We'll name our email provider here once we choose one. You can unsubscribe at any time.</p>
<h2>Analytics</h2><p>We don't currently use analytics or cookies. If we add analytics later, we'll prefer privacy-friendly, cookie-less tools and update this page first.</p>
<h2>Your rights</h2><p>To access or delete your data, email <a href="mailto:psychready@mail.grokbot.com">psychready@mail.grokbot.com</a>.</p>
<h2>No health data</h2><p>Please don't send patient information to PsychReady.</p>''')
page("404.html","Page not found","The page you requested could not be found.",'<h1>Page not found</h1><p>Try the <a href="index.html">home page</a> or <a href="training/modules.html">modules</a>.</p>')

# NEWSLETTER ARCHIVE
# Add an issue: create content/newsletter/YYYY-MM-DD-slug.md with title, date, and summary
# front matter (date must match the filename). Then run: python3 generate.py
RSS_HEAD='<link rel="alternate" type="application/rss+xml" title="PsychReady weekly brief" href="{href}">'
def md_inline(s):
    s=html.escape(s)
    def link(m):
        href=m.group(2)
        if not re.match(r"^(https://|http://|mailto:|\.{0,2}/)", href):
            return m.group(0)
        return f'<a href="{href}">{m.group(1)}</a>'
    s=re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, s)
    s=re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s=re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s
def md_html(body):
    out=[]; para=[]; list_tag=None
    ol=re.compile(r"^\d+\. (.*)$")
    def flush():
        nonlocal para
        if para:
            out.append("<p>"+md_inline(" ".join(para))+"</p>"); para=[]
    def close_list():
        nonlocal list_tag
        if list_tag:
            out.append(f"</{list_tag}>"); list_tag=None
    def open_list(tag):
        nonlocal list_tag
        if list_tag!=tag:
            close_list(); out.append(f"<{tag}>"); list_tag=tag
    for line in body.splitlines():
        numbered=ol.match(line)
        if line.startswith("### "):
            flush(); close_list(); out.append(f"<h3>{md_inline(line[4:])}</h3>")
        elif line.startswith("## "):
            flush(); close_list(); out.append(f"<h2>{md_inline(line[3:])}</h2>")
        elif line.startswith("# "):
            flush(); close_list(); out.append(f"<h2>{md_inline(line[2:])}</h2>")
        elif line.strip() in ("---","***","___"):
            flush(); close_list(); out.append("<hr>")
        elif line.startswith("- "):
            flush(); open_list("ul"); out.append(f"<li>{md_inline(line[2:])}</li>")
        elif numbered:
            flush(); open_list("ol"); out.append(f"<li>{md_inline(numbered.group(1))}</li>")
        elif not line.strip():
            flush(); close_list()
        else:
            close_list(); para.append(line.strip())
    flush(); close_list()
    return "\n".join(out)
def load_issues():
    issues=[]
    for path in sorted(Path("content/newsletter").glob("*.md")):
        text=path.read_text()
        if not text.startswith("---\n"):
            raise SystemExit(f"{path} needs front matter (title, date, summary)")
        _,fm,body=text.split("---",2)
        meta={}
        for line in fm.strip().splitlines():
            if ":" not in line: continue
            k,v=line.split(":",1)
            meta[k.strip()]=v.strip().strip('"')
        for key in ("title","date","summary"):
            if key not in meta:
                raise SystemExit(f"{path} is missing {key}")
        m=re.match(r"^(\d{4}-\d{2}-\d{2})-(.+)$", path.stem)
        if not m or m.group(1)!=meta["date"]:
            raise SystemExit(f"{path} filename date must match the date field")
        datetime.date.fromisoformat(meta["date"])
        issues.append({"title":meta["title"],"date":meta["date"],"summary":meta["summary"],"slug":path.stem,"body":body.strip()})
    issues.sort(key=lambda x: x["date"], reverse=True)
    return issues
def pretty_date(iso):
    return datetime.date.fromisoformat(iso).strftime("%-d %B %Y")
def rfc822(iso):
    return datetime.datetime.strptime(iso,"%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 GMT")
def sync_sitemap(issues):
    text=Path("sitemap.xml").read_text()
    text=re.sub(r"\n<url><loc>"+re.escape(B)+r"/newsletter/.*?</url>","",text)
    newest=issues[0]["date"] if issues else "2026-10-18"
    block=f'<url><loc>{B}/newsletter/</loc><lastmod>{newest}</lastmod></url>\n'
    block+=f'<url><loc>{B}/newsletter/feed.xml</loc><lastmod>{newest}</lastmod></url>\n'
    for iss in issues:
        block+=f'<url><loc>{B}/newsletter/{iss["slug"]}.html</loc><lastmod>{iss["date"]}</lastmod></url>\n'
    text,n=re.subn(r"(<url><loc>"+re.escape(B)+r"/newsletter\.html</loc><lastmod>[^<]+</lastmod></url>\n)", r"\1"+block, text, count=1)
    if n!=1:
        raise SystemExit("sitemap.xml is missing the newsletter.html entry")
    Path("sitemap.xml").write_text(text)
def sync_llms(issues):
    lines=["## Newsletter archive", f"- [Archive]({B}/newsletter/): past issues of the weekly brief, newest first", f"- [RSS]({B}/newsletter/feed.xml)"]
    for iss in issues:
        lines.append(f'- [{iss["title"]}]({B}/newsletter/{iss["slug"]}.html) ({iss["date"]}): {iss["summary"]}')
    block="\n".join(lines)+"\n"
    text=Path("llms.txt").read_text()
    if "## Newsletter archive\n" in text:
        text=re.sub(r"## Newsletter archive\n(?:- .*\n)*", block, text)
    else:
        text=text.rstrip()+"\n\n"+block
    Path("llms.txt").write_text(text)
def build_newsletter():
    src=Path("content/newsletter")
    if not src.is_dir():
        return
    issues=load_issues()
    rss=RSS_HEAD.format(href="feed.xml")
    for iss in issues:
        shown=pretty_date(iss["date"])
        body=f'''<article>
<p class="meta">Weekly brief · <time datetime="{iss["date"]}">{shown}</time></p>
<h1>{html.escape(iss["title"])}</h1>
<p class="lead">{html.escape(iss["summary"])}</p>
{md_html(iss["body"])}
<p><a href="index.html">All issues</a> · <a href="feed.xml">RSS</a> · <a href="../newsletter.html">Subscribe</a></p>
</article>'''
        page(f'newsletter/{iss["slug"]}.html', iss["title"], iss["summary"], body, [{"@context":"https://schema.org","@type":"BlogPosting","headline":iss["title"],"datePublished":iss["date"],"description":iss["summary"],"url":f'{B}/newsletter/{iss["slug"]}.html',"author":{"@type":"Organization","name":"PsychReady"}}], False, rss)
    cards="".join(
        f'<li class="card"><p class="meta"><time datetime="{i["date"]}">{pretty_date(i["date"])}</time></p><h2><a href="{i["slug"]}.html">{html.escape(i["title"])}</a></h2><p>{html.escape(i["summary"])}</p><p><a href="{i["slug"]}.html">Read this issue</a></p></li>'
        for i in issues) or '<li class="card"><p>No issues yet.</p></li>'
    page("newsletter/index.html","Newsletter archive","Past issues of the PsychReady weekly brief for facility behavioral health teams.",
        f'''<h1>Newsletter archive</h1><p class="lead">Past issues of the weekly brief, newest first. One practical training idea, drill, or checklist for behavioral health teams.</p>
<p><a href="../newsletter.html">Subscribe</a> · <a href="feed.xml">RSS feed</a></p>
<ul class="grid2">{cards}</ul>''', None, False, rss)
    items="".join(
        f'''<item><title>{xml_escape(i["title"])}</title><link>{B}/newsletter/{i["slug"]}.html</link><guid isPermaLink="true">{B}/newsletter/{i["slug"]}.html</guid><pubDate>{rfc822(i["date"])}</pubDate><description>{xml_escape(i["summary"])}</description></item>\n'''
        for i in issues)
    Path("newsletter/feed.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>PsychReady weekly brief</title>
<link>{B}/newsletter/</link>
<description>One practical training idea, drill, or checklist for facility behavioral health teams each week.</description>
<language>en</language>
{items}</channel></rss>
''')
    sync_sitemap(issues)
    sync_llms(issues)
build_newsletter()
