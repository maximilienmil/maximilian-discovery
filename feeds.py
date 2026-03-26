"""
Feed configuration for the discovery engine.

OPML_DOMAINS: domains already covered by the user's RSS reader — articles dropped before scoring.
DISCOVERY_FEEDS: list of (url, source_type) tuples defining what to fetch.

Source types:
  - "technical"          → arXiv, ML research blogs, journals → "Research & Technical" section
  - "discovery"          → niche Substacks, think tanks, longform → main digest sections
  - "podcast"            → podcast episodes, score threshold 7+ → "Podcast Episodes" section
  - "podcast_selective"  → curated shows where only the best episodes matter, score threshold 8+
"""

# Domains from user's RSS reader — dropped before scoring
# NOTE: alignment.anthropic.com intentionally removed — user wants it surfaced
OPML_DOMAINS: set[str] = {
    "bwog.com", "reddit.com", "columbiaspectator.com", "sundial-cu.org",
    "news.columbia.edu", "grcglobalgroup.substack.com",
    "bain.com", "bcg.com", "bigthink.com", "letters.thedankoe.com",
    "hbr.org", "harvardbusiness.org", "mckinsey.com", "mitsloan.mit.edu",
    "gq.com", "wsj.com", "dowjones.io",
    "ft.com", "npr.org", "nytimes.com", "theatlantic.com", "vox.com",
    "nature.com", "sciencedirect.com", "pubmed.ncbi.nlm.nih.gov",
    "vivekmurthy.substack.com", "bair.berkeley.edu",
    "centerforhumanetechnology.substack.com", "mag.re-alignment.com",
    "jasmi.news", "9to5mac.com", "404media.co",
    "magazine.sebastianraschka.com", "normaltech.ai", "aiguide.substack.com",
    "anthropic.com",  # main anthropic.com/news excluded; alignment.anthropic.com is NOT excluded
    "spectrum.ieee.org",
    "bloomberg.com", "tools.eq4c.com", "futurism.com",
    "aleximas.substack.com", "github.com", "mshibanami.github.io",
    "deepmind.google", "deepmind.com", "ruben.substack.com",
    "iaps.ai", "importai.substack.com", "interconnects.ai",
    "lennysnewsletter.com", "news.mit.edu", "technologyreview.com",
    "feeds.npr.org", "oneusefulthing.org", "openai.com",
    "platformer.news", "producthunt.com", "restofworld.org",
    "sineadbovell.substack.com", "techpolicy.press",
    "techcrunch.com", "washingtonpost.com", "thegradient.pub",
    "sustainablemedia.substack.com", "theverge.com", "wired.com",
    "kill-the-newsletter.com",
}

DISCOVERY_FEEDS: list[tuple[str, str]] = [

    # ══ TECHNICAL ═════════════════════════════════════════════════════════════
    # Goes into "Research & Technical" section. Score threshold: 6+

    # ── arXiv — broad daily feeds ─────────────────────────────────────────────
    ("https://rss.arxiv.org/rss/cs.CY", "technical"),   # Computers & Society
    ("https://rss.arxiv.org/rss/cs.HC", "technical"),   # Human-Computer Interaction
    ("https://rss.arxiv.org/rss/cs.AI", "technical"),   # Artificial Intelligence
    ("https://rss.arxiv.org/rss/cs.LG", "technical"),   # Machine Learning

    # ── arXiv — targeted keyword searches ────────────────────────────────────
    ("https://export.arxiv.org/search/?query=mechanistic+interpretability+circuits&searchtype=all&order=-announced_date_first&format=rss", "technical"),
    ("https://export.arxiv.org/search/?query=RLHF+reinforcement+learning+human+feedback+alignment&searchtype=all&order=-announced_date_first&format=rss", "technical"),
    ("https://export.arxiv.org/search/?query=constitutional+AI+alignment+scalable+oversight&searchtype=all&order=-announced_date_first&format=rss", "technical"),
    ("https://export.arxiv.org/search/?query=HCI+children+youth+design+participatory&searchtype=all&order=-announced_date_first&format=rss", "technical"),
    ("https://export.arxiv.org/search/?query=large+language+model+cognition+attention+education&searchtype=all&order=-announced_date_first&format=rss", "technical"),
    ("https://export.arxiv.org/search/?query=social+media+adolescent+mental+health+longitudinal&searchtype=all&order=-announced_date_first&format=rss", "technical"),
    ("https://export.arxiv.org/search/?query=platform+governance+algorithmic+harm+audit&searchtype=all&order=-announced_date_first&format=rss", "technical"),
    ("https://export.arxiv.org/search/?query=foundation+model+evaluation+benchmark+capabilities&searchtype=all&order=-announced_date_first&format=rss", "technical"),

    # ── HCI & social computing journals ───────────────────────────────────────
    ("https://firstmonday.org/ojs/index.php/fm/gateway/plugin/WebFeedGatewayPlugin/rss2", "technical"),
    ("https://journals.sagepub.com/action/showFeed?jc=nmsa&type=axatoc&feed=rss", "technical"),   # New Media & Society
    ("https://journals.sagepub.com/action/showFeed?jc=smsa&type=axatoc&feed=rss", "technical"),   # Social Media + Society
    ("https://journals.sagepub.com/action/showFeed?jc=boca&type=axatoc&feed=rss", "technical"),   # Big Data & Society
    ("https://www.tandfonline.com/action/showFeed?jc=rics20&type=axatoc&feed=rss", "technical"),  # Information, Communication & Society
    ("https://www.tandfonline.com/action/showFeed?jc=hhci20&type=axatoc&feed=rss", "technical"),  # Human-Computer Interaction (journal)
    ("https://dl.acm.org/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=chi&type=axatoc&feed=rss", "technical"),   # ACM CHI
    ("https://dl.acm.org/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=cscw&type=axatoc&feed=rss", "technical"),  # ACM CSCW
    ("https://link.springer.com/search.rss?query=digital+media+youth&search-within=Journal&facet-journal-id=10964", "technical"),  # Journal of Youth & Adolescence

    # ── Anthropic alignment (re-added per user request) ───────────────────────
    ("https://news.google.com/rss/search?q=site:alignment.anthropic.com&hl=en-US&gl=US&ceid=US:en", "technical"),

    # ── Institutional AI research labs ────────────────────────────────────────
    ("https://machinelearning.apple.com/rss.xml", "technical"),              # Apple ML Research — original research (not in OPML)
    ("https://blog.ml.cmu.edu/feed/", "technical"),                          # CMU Machine Learning Blog
    ("https://hai.stanford.edu/news/feed", "technical"),                     # Stanford HAI — AI + human-centered research
    ("https://allenai.org/blog/feed", "technical"),                          # Allen Institute for AI (AI2) — NLP, reasoning, safety
    ("https://research.ibm.com/blog/feed", "technical"),                     # IBM Research — quantum, foundation models, enterprise AI
    ("https://humancompatible.ai/feed/", "technical"),                       # CHAI Berkeley (Stuart Russell) — value alignment
    ("https://mila.quebec/en/feed/", "technical"),                           # Mila (Yoshua Bengio) — deep learning, causal reasoning
    ("https://blog.eleutherai.org/rss/", "technical"),                       # EleutherAI — open-source LLMs, The Pile, evaluation harness
    ("https://ai.meta.com/blog/rss/", "technical"),                          # Meta AI Research (FAIR) — Llama, SAM, DINO
    ("https://mistral.ai/news/rss", "technical"),                            # Mistral AI — frontier open-weight models
    ("https://www.together.ai/blog/rss", "technical"),                       # Together AI (Percy Liang) — open models, distributed training

    # ── ML research blogs — interpretability & alignment ─────────────────────
    ("https://www.neelnanda.io/blog/feed.xml", "technical"),         # Neel Nanda — mechanistic interpretability
    ("https://colah.github.io/rss.xml", "technical"),                # Chris Olah — circuits, interpretability
    ("https://lilianweng.github.io/index.xml", "technical"),         # Lilian Weng — research surveys
    ("https://distill.pub/rss.xml", "technical"),                    # Distill — ML clarity
    ("https://www.offconvex.org/feed.xml", "technical"),             # Off the Convex Path — DL theory
    ("https://www.inference.vc/rss/", "technical"),                  # Ferenc Huszár — ML, causality
    ("https://bounded-regret.ghost.io/rss/", "technical"),           # Bounded Regret

    # ── ML research blogs — capabilities & engineering ────────────────────────
    ("https://karpathy.github.io/feed.xml", "technical"),            # Andrej Karpathy
    ("https://fchollet.substack.com/feed", "technical"),             # François Chollet — ARC, abstraction
    ("https://eugeneyan.com/feed.xml", "technical"),                 # Eugene Yan — applied ML, RecSys
    ("https://huyenchip.com/feed.xml", "technical"),                 # Chip Huyen — ML systems
    ("https://hamel.dev/feed.xml", "technical"),                     # Hamel Husain — LLM engineering
    ("https://www.fast.ai/feed", "technical"),                       # fast.ai — practical deep learning
    ("https://www.latent.space/feed", "technical"),                  # Latent Space — AI engineering
    ("https://ruder.io/rss/index.rss", "technical"),                 # Sebastian Ruder — NLP
    ("https://jalammar.github.io/feed.xml", "technical"),            # Jay Alammar — ML visualization
    ("https://huggingface.co/blog/feed.xml", "technical"),           # Hugging Face
    ("https://paperswithcode.com/feed", "technical"),                # Papers with Code — trending
    ("https://maggieappleton.com/rss.xml", "technical"),             # Maggie Appleton — HCI, tools for thought
    ("https://blog.acolyer.org/feed/", "technical"),                 # The Morning Paper
    ("https://epochai.org/feed", "technical"),                       # Epoch AI — compute trends

    # ── AI alignment & safety orgs ────────────────────────────────────────────
    ("https://www.alignmentforum.org/feed.xml", "technical"),        # Alignment Forum
    ("https://www.lesswrong.com/feed.xml?view=curated-questions", "technical"),
    ("https://metr.org/blog/rss/", "technical"),                     # METR (ARC Evals) — model eval
    ("https://aiimpacts.org/feed/", "technical"),                    # AI Impacts — forecasting
    ("https://intelligence.org/feed/", "technical"),                 # MIRI
    ("https://gwern.net/feed", "technical"),                         # Gwern — empirical, long-form
    ("https://vickiboykis.com/index.xml", "technical"),              # Vicki Boykis — LLM internals, embeddings, cuts through hype
    ("https://paulfchristiano.com/feed/", "technical"),              # Paul Christiano
    ("https://vkrakovna.wordpress.com/feed/", "technical"),          # Victoria Krakovna
    ("https://rohinshah.com/feed/", "technical"),                    # Rohin Shah


    # ══ DISCOVERY ═════════════════════════════════════════════════════════════
    # Goes into "Must Read" (8+) and "Worth a Look" (5-7) sections.

    # ── AI ethics & critical tech — researchers, not advocacy orgs ────────────
    ("https://aisnakeoil.substack.com/feed", "discovery"),           # AI Snake Oil — Narayanan (empirical skepticism)
    ("https://garymarcus.substack.com/feed", "discovery"),           # Gary Marcus — AI criticism
    ("https://thezvi.substack.com/feed", "discovery"),               # Zvi Mowshowitz — alignment policy
    ("https://simonwillison.net/atom/everything/", "discovery"),     # Simon Willison — capabilities
    ("https://abebabirhane.substack.com/feed", "discovery"),         # Abeba Birhane — AI & cognition
    ("https://chinai.substack.com/feed", "discovery"),               # ChinAI — Jeffrey Ding
    ("https://thealgorithmicbridge.substack.com/feed", "discovery"), # Alberto Romero — AI criticism
    ("https://www.cold-takes.com/rss/", "discovery"),                # Holden Karnofsky — AI risk, Open Phil

    # ── Youth, social media & cognitive effects — actual researchers ───────────
    ("https://www.zephoria.org/thoughts/feed", "discovery"),         # danah boyd
    ("https://blogs.lse.ac.uk/parenting4digitalfuture/feed/", "discovery"),  # Sonia Livingstone
    ("https://safiyaunoble.substack.com/feed", "discovery"),         # Safiya Umoja Noble
    ("https://joybuolamwini.substack.com/feed", "discovery"),        # Joy Buolamwini
    ("https://datafeminism.io/feed/", "discovery"),                  # Data Feminism (D'Ignazio)

    # ── Cognition, attention, tools for thought ────────────────────────────────
    ("https://www.roughtype.com/?feed=rss2", "discovery"),           # Rough Type — Nick Carr (attention, The Shallows)
    ("https://theconvivialsociety.substack.com/feed", "discovery"),  # L.M. Sacasas — tech & human flourishing
    ("https://nesslabs.com/feed", "discovery"),                      # Ness Labs — cognitive tools, metacognition
    ("https://eugenewei.substack.com/feed", "discovery"),            # Eugene Wei — attention economy, social mechanics
    ("https://craigmod.com/rss/essays/", "discovery"),               # Craig Mod — technology, attention, craft
    ("https://psyche.co/feed", "discovery"),                         # Psyche Magazine — philosophy & psychology longform
    ("https://digest.bps.org.uk/feed/", "discovery"),                # BPS Research Digest — psychology

    # ── Longform ideas & futures ───────────────────────────────────────────────
    ("https://astralcodexten.substack.com/feed", "discovery"),       # Scott Alexander — empirical, counterintuitive
    ("https://www.ribbonfarm.com/feed/", "discovery"),               # Ribbonfarm — Venkatesh Rao
    ("https://breakingsmart.substack.com/feed", "discovery"),        # Breaking Smart — Venkat Rao
    ("https://meaningness.com/rss.xml", "discovery"),                # Meaningness — David Chapman
    ("https://www.worksinprogress.news/feed", "discovery"),          # Works in Progress — evidence-based longform
    ("https://asteriskmag.com/feed.xml", "discovery"),               # Asterisk — rigorous longform
    ("https://reallifemag.com/feed/", "discovery"),                  # Real Life — technology & everyday life
    ("https://logicmag.io/feed.xml", "discovery"),                   # Logic — tech criticism
    ("https://joinreboot.org/feed", "discovery"),                    # Reboot — tech & power, by young people
    ("https://www.exponentialview.co/feed", "discovery"),            # Azeem Azhar — Exponential View
    ("https://sentiers.media/rss/", "discovery"),                    # Sentiers — Patrick Tanguay
    ("https://culturedigitally.org/feed/", "discovery"),             # Culture Digitally — media studies

    # ── Think tanks — keep only those producing original analysis ──────────────
    ("https://www.oii.ox.ac.uk/feed/", "discovery"),                 # Oxford Internet Institute
    ("https://cyber.harvard.edu/feeds/news", "discovery"),           # Berkman Klein Center
    ("https://ainowinstitute.org/feed", "discovery"),                # AI Now Institute
    ("https://www.adalovelaceinstitute.org/feed/", "discovery"),     # Ada Lovelace Institute
    ("https://www.turing.ac.uk/rss.xml", "discovery"),               # Alan Turing Institute
    ("https://datasociety.net/feed/", "discovery"),                  # Data & Society
    ("https://cdt.org/feed/", "discovery"),                          # CDT — tech policy analysis
    ("https://www.eff.org/rss/updates.xml", "discovery"),            # EFF — tech law, surveillance
    ("https://knightcolumbia.org/feed", "discovery"),                # Knight First Amendment Institute
    ("https://5rightsfoundation.com/feed/", "discovery"),            # 5Rights Foundation
    ("https://www.childrenscommissioner.gov.uk/feed/", "discovery"), # UK Children's Commissioner
    ("https://80000hours.org/feed/", "discovery"),                   # 80,000 Hours
    ("https://citizenlab.ca/feed/", "discovery"),                    # Citizen Lab — surveillance, spyware research
    ("https://dair-community.social/users/DAIR.rss", "discovery"),   # DAIR Institute

    # ── Miscellaneous high-signal ─────────────────────────────────────────────
    ("https://www.densediscovery.com/feed", "discovery"),
    ("https://mattersoftech.substack.com/feed", "discovery"),
    ("https://www.scopeofwork.net/rss/", "discovery"),


    # ══ PODCASTS ══════════════════════════════════════════════════════════════
    # Goes into "Podcast Episodes" section.
    # "podcast"           → score threshold 7+ (surfaced if genuinely insightful)
    # "podcast_selective" → score threshold 8+ (only best episodes from curated shows)
    #
    # NOT included (already in NetNewsWire or excluded by user preference):
    #   Dan Koe's podcast, Sinead Bovell's I Got Questions, Hard Fork,
    #   Lenny's Podcast, AI & I

    # ── Selective — only best episodes surface (score 8+) ─────────────────────
    ("http://feeds.harvardbusiness.org/harvardbusiness/ideacast", "podcast_selective"),  # HBR IdeaCast
    ("https://www.omnycontent.com/d/playlist/708664bd-6843-4623-8066-aede00ce0c8a/a7ee33f2-d500-4226-b99c-af04013945d6/36587f70-89f9-4631-ac19-af04013945e0/podcast.rss", "podcast_selective"),  # McKinsey Inside the Strategy Room

    # ── AI, alignment & technical — broad interest ─────────────────────────
    ("https://lexfridman.com/feed/podcast/", "podcast"),                     # Lex Fridman — AI researchers, scientists, philosophers
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCXl4i9dYBrFOabk0xGmbkRA", "podcast"),  # Dwarkesh Podcast (YouTube)
    ("https://feeds.transistor.fm/future-of-life-institute-podcast-4e4d1fa5-a878-4cb2-91be-91c3ce266dfd", "podcast"),  # Future of Life Institute — AI safety, existential risk
    ("https://anchor.fm/s/1e4a0eac/podcast/rss", "podcast"),                # Machine Learning Street Talk — technical ML
    ("https://twimlai.com/feed/podcast/", "podcast"),                        # TWIML AI — researcher interviews, ML breadth
    ("https://changelog.com/practicalai/feed", "podcast"),                   # Practical AI — applied ML, broad accessible coverage
    ("https://feeds.buzzsprout.com/2057836.rss", "podcast"),                 # Cognitive Revolution (Nathan Labenz) — frontier AI capabilities
    ("https://feeds.buzzsprout.com/2022960.rss", "podcast"),                 # The Inside View (Michaël Trazzi / Redwood Research) — AI safety
    ("https://feeds.buzzsprout.com/2037297.rss", "podcast"),                 # Alignment Forum Podcast — AF posts in audio format
    ("https://braininspired.co/feed/podcast/", "podcast"),                   # Brain Inspired (Paul Middlebrooks) — neuroscience × AI
    ("https://feeds.buzzsprout.com/1532009.rss", "podcast"),                 # The Robot Brains (Pieter Abbeel) — robotics, RL
    ("https://feeds.simplecast.com/PkHMJpkS", "podcast"),                    # Gradient Dissent (W&B) — ML practitioners & researchers

    # ── YouTube — paper walkthroughs & lectures ──────────────────────────────
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCZHmQk67mSJgfCCTn7xBfew", "podcast"),  # Yannic Kilcher — paper walkthroughs (interpretability, alignment)
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCXUPKJO5MZQRRVSB7kRCF_A", "podcast_selective"),  # Andrej Karpathy — deep-dive tutorials (Neural Networks: Zero to Hero)
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCYO_jab_esuFRV4b17AJtAg", "podcast_selective"),  # 3Blue1Brown — neural nets, transformers (visual, mathematical)
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCbfYPyITQ-7l4upoX8nvctg", "podcast_selective"),  # Two Minute Papers — AI research in 2 minutes
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UC9-y-6csu5WGm29I7JiwpnA", "podcast_selective"),  # Computerphile — CS fundamentals, AI concepts
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCBa5G_ESCn8Yd4vw5U-gIcg", "podcast_selective"),  # Stanford Online — CS229/CS224N/CS231N lecture recordings
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCnUYZLuoy1rq1aVMwx4aTzw", "podcast_selective"),  # Google DeepMind — AlphaFold, Gemini, research talks
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCj8shE7aIn4Yawwbo2FceCQ", "podcast"),  # Aleksa Gordić (AI Epiphany) — GNN, transformer walkthroughs
    ("https://www.youtube.com/feeds/videos.xml?channel_id=UCF9O8Vj-FEbRDA5DcDGz-Pg", "podcast_selective"),  # Yann LeCun — rare but high-signal talks

    # ── Ideas, cognition & knowledge ────────────────────────────────────────
    ("https://rss.art19.com/sean-carrolls-mindscape", "podcast"),            # Sean Carroll's Mindscape — physics, philosophy, complexity
    ("https://cowenconvos.libsyn.com/rss", "podcast"),                       # Conversations with Tyler — wide-ranging intellectual
    ("https://feeds.simplecast.com/wgl4xEgL", "podcast"),                    # EconTalk — economics, ideas, incentives
    ("https://feeds.transistor.fm/80000-hours-podcast", "podcast"),          # 80,000 Hours — AI safety, career impact, EA
]
