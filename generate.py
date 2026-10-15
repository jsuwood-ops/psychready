import os, json
B="https://jsuwood-ops.github.io/psychready"
DISC='<p class="disclaimer"><strong>Educational use only.</strong> PsychReady content is for staff education and program planning. It is not clinical advice and is not a substitute for accredited training, local policy, or professional judgment.</p>'
NAV=[("index.html","Home"),("training/index.html","Training"),("training/modules.html","Modules"),("barriers.html","Barriers"),("for-educators.html","For Educators"),("newsletter.html","Newsletter"),("sponsors.html","Sponsors"),("about.html","About")]
LOGO='<svg class="logo" viewBox="0 0 40 40" width="36" height="36" aria-hidden="true"><rect width="40" height="40" rx="10" fill="#0f5c5a"/><path d="M8 21h6l3-7 5 14 3-7h7" fill="none" stroke="#f6c453" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def page(path,title,desc,body,ld=None,training=False):
    d="../"*path.count("/")
    nav="".join(f'<li><a href="{d}{h}"{" aria-current=\"page\"" if h==path else ""}>{t}</a></li>' for h,t in NAV)
    lds=[{"@context":"https://schema.org","@type":"Organization","name":"PsychReady","url":B+"/","logo":B+"/logo.svg"},
         {"@context":"https://schema.org","@type":"WebSite","name":"PsychReady","url":B+"/"}]+(ld or [])
    canon=path.replace("index.html","")
    html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<!-- BASE_URL = {B} (pending real domain; canonicals are relative until then) -->
<title>{title} | PsychReady</title><meta name="description" content="{desc}">
<link rel="canonical" href="{d}{path}">
<meta property="og:type" content="website"><meta property="og:site_name" content="PsychReady"><meta property="og:title" content="{title} | PsychReady"><meta property="og:description" content="{desc}"><meta property="og:url" content="{B}/{canon}"><meta property="og:image" content="{B}/assets/og.svg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title} | PsychReady"><meta name="twitter:description" content="{desc}">
<link rel="icon" href="{d}logo.svg" type="image/svg+xml"><link rel="stylesheet" href="{d}assets/style.css">
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
<p><a href="{d}contact.html">Contact</a> · <a href="{d}privacy.html">Privacy</a> · <a href="{d}sponsors.html">Sponsorship &amp; disclosure</a> · <a href="{d}llms.txt">llms.txt</a></p>
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

# HOME
mods_cards="".join(f'<li class="card"><h3><a href="training/modules.html#{a}">{t}</a></h3><p>{s}</p></li>' for a,t,s in MODS[:4])
page("index.html","Behavioral Health Staff Training for Facilities","Practical, competency-based training plans, drills, and checklists for hospital and clinic behavioral health and psychiatric teams.",f'''
<section class="hero"><h1>Practical training for facility behavioral health teams</h1>
<p class="lead">Competency-based modules, simulation drills, and program playbooks for nurses, psychiatrists, social workers, techs, security, and primary-care partners.</p>
<p><a class="btn" href="training/index.html">Start training</a> <a class="btn btn-ghost" href="newsletter.html">Get the weekly brief</a></p></section>
<section><h2>Who PsychReady is for</h2><ul class="grid3">
<li class="card"><h3>Educators &amp; nurse managers</h3><p>Ready-to-run lesson structures, skills checklists, and refresher calendars.</p></li>
<li class="card"><h3>ED leads &amp; C-L teams</h3><p>Teamwork drills, telepsychiatry workflows, and consult pathways.</p></li>
<li class="card"><h3>Facility leaders</h3><p>Solutions mapped to workforce, access, integration, and funding barriers.</p></li></ul></section>
<section><h2>Featured modules</h2><ul class="grid2">{mods_cards}</ul><p><a href="training/modules.html">See all eight modules →</a></p></section>
<section><h2>How the training works</h2><ol class="steps"><li><strong>Learn</strong> — short focused content per competency.</li><li><strong>Practice</strong> — Behavioral Skills Training: instruct, model, rehearse, feedback.</li><li><strong>Simulate</strong> — interprofessional scenarios with structured debrief.</li><li><strong>Measure</strong> — observed competence and operational outcomes, not just attendance.</li></ol></section>
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
<p><a class="btn" href="modules.html">Browse modules</a></p>{cta("../")}''',[course("PsychReady Curriculum","Competency-based behavioral health staff curriculum.","training/")],True)

# MODULES
ml="".join(f'<section id="{a}" class="card module"><h2>{t}</h2><p>{s}</p>{"<p><a href=\"de-escalation.html\">Open the full sample lesson →</a></p>" if a=="de-escalation" else "<p class=\"small\">Full lesson coming soon. <a href=\"../newsletter.html\">Get notified</a>.</p>"}</section>' for a,t,s in MODS)
toc="".join(f'<li><a href="#{a}">{t}</a></li>' for a,t,_ in MODS)
page("training/modules.html","Training Modules for Psychiatric & Behavioral Health Staff","Eight PsychReady modules: de-escalation, suicide risk, trauma-informed care, teamwork, telepsychiatry, restraint alternatives, physical health, and supervision.",f'<h1>Training modules</h1><nav aria-label="Modules" class="toc"><ol>{toc}</ol></nav>{ml}{cta("../")}',
 [{"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"name":t,"url":f"{B}/training/modules.html#{a}"} for i,(a,t,_) in enumerate(MODS)]}],True)

# DE-ESCALATION
page("training/de-escalation.html","De-escalation & Crisis Prevention Training Module","Sample lesson on verbal de-escalation and crisis prevention for facility behavioral health staff: objectives, core skills, drills, and an assessment checklist.",'''
<article><h1>De-escalation &amp; crisis prevention</h1><p class="meta">Module 1 · Audience: all direct-care staff, security · Suggested time: 90-minute skills lab plus a 20-minute e-module</p>
<section><h2>Learning objectives</h2><ul><li>Recognize early signs of escalating distress and agitation.</li><li>Use verbal and non-verbal de-escalation techniques.</li><li>Coordinate team roles during an escalating situation.</li><li>Explain when and how restrictive interventions may be used, only as a last resort under local policy.</li><li>Take part in post-incident debrief and support.</li></ul></section>
<section><h2>Why it matters</h2><p>Agitation and aggression are common in emergency and inpatient psychiatric settings. They put patients and staff at risk, and restrictive interventions can cause harm and damage trust. Consensus guidance, such as the American Association for Emergency Psychiatry's Project BETA de-escalation workgroup, recommends verbal de-escalation as a first-line approach.</p></section>
<section><h2>Core skills</h2><ol><li><strong>Respect personal space</strong>: keep a safe distance and an open exit for everyone.</li><li><strong>Avoid provocation</strong>: calm posture, hands visible, matched eye level.</li><li><strong>One communicator</strong>: a single designated staff member leads.</li><li><strong>Concise, simple language</strong>: short sentences, repeat as needed.</li><li><strong>Identify wants and feelings</strong>: ask, listen actively, reflect back.</li><li><strong>Agree or agree to disagree</strong>: find truth to align with.</li><li><strong>Set clear limits</strong>: respectfully, with consequences explained.</li><li><strong>Offer choices and optimism</strong>, including food, drink, quiet space, or medication by choice.</li><li><strong>Debrief</strong> the patient and the staff afterward.</li></ol></section>
<section><h2>Practice drills (BST format)</h2><ol><li><strong>Instruct</strong> (10 min): review the core skills.</li><li><strong>Model</strong> (10 min): facilitators demonstrate the "waiting room escalation" scenario.</li><li><strong>Rehearse</strong> (40 min): rotating triads of patient, communicator, and observer across three scenarios (ED boarding frustration, family visitor conflict, intoxicated patient).</li><li><strong>Feedback</strong> (20 min): the observer scores the checklist and the group debriefs (what went well, what to change, safety concerns).</li><li><strong>Team drill</strong> (10 min): call for help, assign roles, and run a closed-loop communication check.</li></ol></section>
<section><h2>Assessment checklist</h2><table><caption>Observed skills (Yes / Not yet)</caption><thead><tr><th scope="col">Skill</th><th scope="col">Observed?</th></tr></thead><tbody>
<tr><td>Positions safely with exit route</td><td>☐</td></tr><tr><td>Introduces self, uses calm tone</td><td>☐</td></tr><tr><td>Uses short, clear statements</td><td>☐</td></tr><tr><td>Reflects the patient's feelings or needs</td><td>☐</td></tr><tr><td>Offers at least two genuine choices</td><td>☐</td></tr><tr><td>Sets a respectful limit</td><td>☐</td></tr><tr><td>Coordinates with team using closed-loop communication</td><td>☐</td></tr><tr><td>Participates in debrief</td><td>☐</td></tr></tbody></table><p class="small">Set your own mastery threshold, for example all safety items plus most others. Reassess at one month.</p></section>
<section><h2>Further reading</h2><ul><li>Richmond JS et al. "Verbal De-escalation of the Agitated Patient: Consensus Statement of the AAEP Project BETA De-escalation Workgroup." <em>West J Emerg Med</em>, 2012.</li><li>NICE guideline NG10: Violence and aggression: short-term management in mental health, health and community settings.</li><li>WHO mhGAP Intervention Guide, version 2.0.</li><li>WHO QualityRights training materials on human-rights-aligned care.</li></ul></section></article>
<section class="resources"><h2>Recommended training resources</h2><p class="small"><strong>Disclosure:</strong> PsychReady may in future earn a commission from some recommended resources. We'll label every such link clearly. No affiliate links are active today.</p><ul><li>Accredited crisis-prevention or de-escalation certification programs for your region. We'll list vetted options here.</li></ul></section>''',
 [{"@context":"https://schema.org","@type":"LearningResource","name":"De-escalation & crisis prevention","learningResourceType":"Lesson","educationalLevel":"Professional","audience":{"@type":"Audience","audienceType":"Behavioral health facility staff"},"url":B+"/training/de-escalation.html","isAccessibleForFree":True}],True)

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
<ol class="steps big"><li><h2>Induction</h2><p>Within the first weeks, cover core modules: de-escalation, suicide risk, trauma-informed care, and physical-health escalation. Pair each new hire with a preceptor and a competency checklist.</p></li>
<li><h2>Refreshers</h2><p>Hold annual skills labs and run 10-minute micro-learning huddles on the unit. After incidents, run targeted refreshers.</p></li>
<li><h2>Simulation</h2><p>Run interprofessional scenarios quarterly or more often, always with structured debrief. Small and rural sites can share regional simulation days.</p></li>
<li><h2>Supervision</h2><p>Use direct observation, documented feedback, and reflective practice, and gatekeep high-risk skills.</p></li>
<li><h2>Measure outcomes</h2><p>Track confidence and observed competence before training, after it, and at one month. Link results to operational measures such as restraint and seclusion events, staff injuries, time-to-consult, and incident themes. Run booster sessions when metrics slip.</p></li></ol>
<section><h2>Build local capacity</h2><p>Use mhGAP-style cascade training: develop master trainers who coach unit educators so the program survives turnover.</p></section>{cta()}''')

# NEWSLETTER
page("newsletter.html","Weekly Behavioral Health Training Brief","Subscribe to the PsychReady weekly brief: one practical drill, checklist, or training idea for facility behavioral health teams.",'''
<h1>The PsychReady weekly brief</h1><p class="lead">One practical, five-minute read each week: a drill, a checklist, a barrier fix, or a summary of new evidence.</p>
<form class="form" action="mailto:hello@jsuwood-ops.github.io?subject=Newsletter%20signup" method="post" enctype="text/plain">
<label for="n">Name</label><input id="n" name="name" autocomplete="name" required>
<label for="e">Work email</label><input id="e" name="email" type="email" autocomplete="email" required>
<label class="check"><input type="checkbox" name="consent" required> I agree to receive the weekly brief and can unsubscribe anytime.</label>
<button class="btn" type="submit">Subscribe</button></form>
<p class="small">For now, signup opens your email app. We don't store anything on a server yet. See our <a href="privacy.html">privacy policy</a>.</p>''')

# SPONSORS
page("sponsors.html","Sponsor PsychReady","Sponsorship tiers and disclosure policy for PsychReady. Open for founding sponsors supporting free behavioral health staff training.",'''
<h1>Sponsorship</h1><p class="lead"><strong>Open for founding sponsors.</strong> PsychReady has no current sponsors.</p>
<section><h2>Tiers (placeholder)</h2><div class="grid3"><div class="card"><h3>Supporter</h3><p>Footer slot and newsletter mention.</p></div><div class="card"><h3>Partner</h3><p>Footer slot, a monthly newsletter feature, and a sponsor page listing.</p></div><div class="card"><h3>Founding sponsor</h3><p>Everything in Partner, plus "supported by" credit on one module.</p></div></div><p>Pricing on request.</p></section>
<section><h2>How sponsorship works</h2><ul><li>Sponsors never control or review clinical or educational content.</li><li>All sponsored placements are clearly labeled.</li><li>We don't accept sponsors whose products conflict with patient safety or human-rights-aligned care.</li></ul></section>
<section><h2>Disclosure</h2><p>Any sponsorship or affiliate relationship will be disclosed on this page and next to the relevant content.</p></section>
<p><a class="btn" href="contact.html">Enquire about sponsorship</a></p>''')

page("about.html","About PsychReady","PsychReady's mission, evidence sources (WHO mhGAP, inpatient mental health standards, simulation research), and educational disclaimer.",f'''
<h1>About PsychReady</h1><section><h2>Mission</h2><p>Help facilities build confident, competent, and humane behavioral health teams through practical, evidence-informed training.</p></section>
<section><h2>What our content is based on</h2><ul><li>WHO mhGAP Intervention Guide and training manuals</li><li>Inpatient mental health quality standards (for example, Royal College of Psychiatrists' quality networks)</li><li>NICE guidance on violence and aggression</li><li>Published research on simulation and Behavioral Skills Training in psychiatric education</li><li>Collaborative care and telepsychiatry literature</li><li>WHO QualityRights human-rights guidance</li></ul><p>We avoid made-up statistics. When we cite results, we name the setting and its limits.</p></section>
<section><h2>Disclaimer</h2>{DISC}</section>''')
page("contact.html","Contact PsychReady","Contact PsychReady about training, feedback, corrections, or sponsorship.",'<h1>Contact</h1><p>Email: <a href="mailto:hello@jsuwood-ops.github.io">hello@jsuwood-ops.github.io</a> (placeholder until the domain is live)</p><p>We welcome corrections, feedback, and module requests.</p>')
page("privacy.html","Privacy Policy","PsychReady privacy policy covering newsletter signups and future analytics.",'''
<h1>Privacy policy</h1><p class="meta">Last updated: October 15, 2026</p>
<h2>Newsletter</h2><p>If you subscribe, we use your name and email only to send the brief. We'll name our email provider here once we choose one. You can unsubscribe at any time.</p>
<h2>Analytics</h2><p>We don't currently use analytics or cookies. If we add analytics later, we'll prefer privacy-friendly, cookie-less tools and update this page first.</p>
<h2>Your rights</h2><p>To access or delete your data, email hello@jsuwood-ops.github.io.</p>
<h2>No health data</h2><p>Please don't send patient information to PsychReady.</p>''')
page("404.html","Page not found","The page you requested could not be found.",'<h1>Page not found</h1><p>Try the <a href="index.html">home page</a> or <a href="training/modules.html">modules</a>.</p>')
