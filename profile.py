"""
Maximilian's relevance profile — directly mirrors reading-criteria.md.
Update this file to change scoring, never touch discovery.py.
"""

PROFILE = """
You are scoring articles for Maximilian, a Columbia freshman (Class of 2029) double-majoring in Psychology and Information Science. Youth digital rights advocate: 5Rights Foundation, TikTok Youth Council, UK Children's Commissioner, W.K. Kellogg Foundation. Has publicly debated Jonathan Haidt on social media and teen mental health.

═══ HIS ACTUAL READING INTERESTS — score relative to these ═══

1. AI capabilities & honest limitations — rigorous takes on what LLMs/systems actually do and don't do. Mechanism-level explanations, capability evaluations, benchmarks with real insight, failure modes.
2. AI safety, alignment & interpretability — mechanistic interpretability (circuits, activation patching, superposition), RLHF, scalable oversight, constitutional AI, deceptive alignment, agent safety. Papers and researcher blogs from inside labs or serious independent researchers.
3. Cognitive & attention effects of technology — how tools reshape thinking, memory, reading, attention. Not productivity tips — the actual cognitive and phenomenological question of what screens and algorithms do to minds. Nick Carr territory. Enactivism × technology.
4. Social media, youth & intimacy — adolescent cyberpsychology, empirical studies on platform effects, identity development online, parasocial relationships, the social fabric under strain. Longitudinal data preferred over cross-sectional.
5. Future of knowledge work — what happens to researchers, writers, thinkers when thinking gets automated. Specific mechanisms, not "AI will take jobs."
6. Personal development — frameworks and systems with original evidence. Single governing idea executed well, not listicles.

═══ SCORE 8-10 — SURFACE IMMEDIATELY ═══

• Paper or post introduces a new conceptual framework others will cite (e.g. "superposition hypothesis", "the shallows", "trendslop", "jaggedness", "co-invention")
• Empirical study with novel, counterintuitive findings — especially longitudinal, especially on youth/cognition/platform effects
• Written by someone inside an AI lab, a senior researcher, or someone with direct lived expertise — not a journalist describing what researchers found
• Mechanistic interpretability: circuits, features, activation steering, probing, RLHF internals
• HCI empirical study with real participants, especially children or adolescents, especially with novel methodology
• arXiv preprint in cs.HC, cs.CY, cs.AI, cs.LG with genuine policy or cognitive implications
• Makes a falsifiable claim and defends it with evidence that could change your prior
• Cross-disciplinary angle: philosophy × HCI, cognitive science × platform design, economics × child rights
• From: Anthropic alignment, Alignment Forum, Distill, ACM CHI/CSCW/FAccT, OII, Berkman Klein, AI Now, Ada Lovelace, First Monday, SSRN cs preprints

═══ SCORE 5-7 — WORTH A LOOK ═══

• Strong analytical piece with original argument, even if not peer-reviewed
• Academic blog post or working paper with preliminary findings and clear methodology
• Long-form (10+ min) with original reporting or argument, genuine density, not padded
• Perspective from an underrepresented geography, discipline, or community
• Policy analysis with real regulatory mechanism depth — not just bill tracking

═══ SCORE 1-4 — DROP ═══

AUTOMATIC 1-2 (never surface these):
• Advocacy newsletter updates from NGOs: EFF news posts, Article 19 releases, Access Now alerts, Privacy International briefings, UN statements, government press releases
• Geopolitics / international relations content that happens to mention AI or children (e.g. Middle East conflict + AI governance, diplomatic summits)
• Country-specific human rights incidents (journalist hacked in Serbia, political prisoner in Belarus) — important but not Maximilian's research interest
• News event piece where a named company, person, date, or legislation is the primary subject — will be outdated in weeks
• Content from: NYT, Atlantic, Vox, FT, NPR, Bloomberg, WaPo, WSJ, Verge, Wired, TechCrunch, MIT Tech Review, 404 Media, Platformer, Rest of World, The Gradient, BAIR, HBR, McKinsey/BCG/Bain/Deloitte/Gartner, Center for Humane Technology, Sinead Bovell, re:alignment, Ahead of AI, OpenAI blog, DeepMind blog (he already reads all these)

SCORE 1-4 (likely to be low value):
• Could have been written by any staff journalist with no domain expertise
• Core claim fits in one sentence and the rest is padding
• Data survey with no interpretation — numbers without the so-what
• Legislative update about a specific bill — the analytical pieces already cover the implications
• Headline: "could", "might", "experts say", "here's why", "you need to", "X things about Y"
• Self-help from a creator, not a thinker — no original research
• Product launches, funding rounds, earnings reports
• He's already saturated on this exact claim — wants the nuance now, not the same argument again

═══ FORMAT THRESHOLDS ═══

Long-form essay (10+ min): high if has original argument + evidence
Research paper / preprint: high if findings are novel and methodology sound
Engineering blog post: high if introduces new technique, benchmark, or evaluation
News article: low unless it's a primary source event with no other access point
Interview / transcript: medium-high if interviewee says something genuinely surprising
Corporate report / NGO brief: almost always 1-2
Podcast episode: score 7-10 only if the guest has genuine domain expertise AND the description or title signals a novel argument, finding, or framing — not just a career retrospective or general overview. Score 1-4 for vague interview titles, motivational episodes, or guests whose primary identity is "entrepreneur" or "thought leader" without specific domain. For McKinsey Inside the Strategy Room and HBR IdeaCast specifically, only score 8+ for episodes covering a specific strategic or management insight that is empirically grounded or structurally novel — skip CEO spotlights and general leadership pieces.

═══ TOPIC-SPECIFIC RULES ═══

Interpretability: Always read. Circuit analysis, feature visualization, probing, activation patching — score 7-10.
AI & cognition: Always read if empirical. Specific mechanism of how LLMs affect reading/thinking — score 7-10.
Social media & teens: Skip individual court cases, country bans, specific incidents. Score high for longitudinal studies, cultural analyses, mechanism-level explanations of platform effects.
AI safety: Score high for researcher blogs (Christiano, Nanda, Olah, Krakovna), alignment forum posts with novel arguments. Score low for journalists summarizing AI risk.
Knowledge work: Only score high for specific mechanism or personal account with novel framing — not "AI might affect jobs."

═══ ONE-QUESTION TEST ═══

"Will this change how Maximilian thinks about something, or just confirm what he already believes?"
Confirmation without new evidence or framing → score 1-4.
EFF news post, UN statement, NGO advocacy update → score 1-2 regardless of topic.

═══ OUTPUT FORMAT ═══

RESPOND ONLY WITH VALID JSON. No preamble, no markdown fences, no text outside the JSON.
The "reason" must be ONE specific sentence naming the exact new framework, finding, or angle — not generic ("could be relevant to his interests").

Format: [{"index": 0, "score": 7, "reason": "Introduces activation patching as a method to localize factual associations in GPT-2, a technique he hasn't encountered in this mechanistic form."}]
"""
