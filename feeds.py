"""
All feed sources for the discovery engine.
OPML_DOMAINS: domains already covered by Maximilian's NetNewsWire — excluded from discovery.
DISCOVERY_FEEDS: net-new sources he does not already subscribe to.
NITTER_ACCOUNTS: Twitter/X handles to pull per-account RSS from Nitter.
NITTER_QUERIES: search strings for Nitter dynamic layer.
"""

# Domains from Subscriptions-iCloud.opml — articles from these are dropped
OPML_DOMAINS = {
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
    "alignment.anthropic.com", "anthropic.com", "spectrum.ieee.org",
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
    "kill-the-newsletter.com",  # Every, Joanna Stern, Genius Filter newsletters
}

# All discovery feeds — net new only
DISCOVERY_FEEDS = [

    # ── arXiv (pre-publication research) ──────────────────────────────────────
    "https://rss.arxiv.org/rss/cs.CY",   # Computers and Society
    "https://rss.arxiv.org/rss/cs.HC",   # Human-Computer Interaction
    "https://export.arxiv.org/search/?query=youth+platform+governance&searchtype=all&order=-announced_date_first&format=rss",
    "https://export.arxiv.org/search/?query=algorithmic+harm+children&searchtype=all&order=-announced_date_first&format=rss",
    "https://export.arxiv.org/search/?query=child+rights+digital+AI&searchtype=all&order=-announced_date_first&format=rss",
    "https://export.arxiv.org/search/?query=social+media+adolescent+longitudinal&searchtype=all&order=-announced_date_first&format=rss",

    # ── Academic journals (not in OPML) ───────────────────────────────────────
    # First Monday — open access, underrated, long-running internet studies journal
    "https://firstmonday.org/ojs/index.php/fm/gateway/plugin/WebFeedGatewayPlugin/rss2",
    # Big Data & Society (Sage)
    "https://journals.sagepub.com/action/showFeed?jc=boca&type=axatoc&feed=rss",
    # New Media & Society (Sage)
    "https://journals.sagepub.com/action/showFeed?jc=nmsa&type=axatoc&feed=rss",
    # Social Media + Society (Sage)
    "https://journals.sagepub.com/action/showFeed?jc=smsa&type=axatoc&feed=rss",
    # Information, Communication & Society (Taylor & Francis)
    "https://www.tandfonline.com/action/showFeed?jc=rics20&type=axatoc&feed=rss",
    # ACM Digital Library: CHI and CSCW new publications
    "https://dl.acm.org/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=chi&type=axatoc&feed=rss",
    # Journal of Computer-Mediated Communication
    "https://academic.oup.com/rss/site_5504/advanceAccess_5504.xml",
    # Computers in Human Behavior (ScienceDirect already in OPML — skip)
    # Journal of Youth and Adolescence
    "https://link.springer.com/search.rss?query=digital+media&search-within=Journal&facet-journal-id=10964",

    # ── Think tanks & policy institutes (not in OPML) ────────────────────────
    # Oxford Internet Institute
    "https://www.oii.ox.ac.uk/feed/",
    # Berkman Klein Center
    "https://cyber.harvard.edu/feeds/news",
    # AI Now Institute
    "https://ainowinstitute.org/feed",
    # Ada Lovelace Institute
    "https://www.adalovelaceinstitute.org/feed/",
    # Alan Turing Institute
    "https://www.turing.ac.uk/rss.xml",
    # Data & Society
    "https://datasociety.net/feed/",
    "https://points.datasociety.net/feed",
    # Center for Democracy & Technology
    "https://cdt.org/feed/",
    # Electronic Frontier Foundation
    "https://www.eff.org/rss/updates.xml",
    # Knight First Amendment Institute
    "https://knightcolumbia.org/feed",
    # Reuters Institute for the Study of Journalism
    "https://reutersinstitute.politics.ox.ac.uk/rss.xml",
    # Future of Life Institute
    "https://futureoflife.org/feed/",
    # Partnership on AI
    "https://partnershiponai.org/feed/",
    # 5Rights Foundation
    "https://5rightsfoundation.com/feed/",
    # Pew Research — Internet & Tech
    "https://www.pewresearch.org/internet/feed/",
    # Common Sense Media research
    "https://www.commonsensemedia.org/rss.xml",
    # UNICEF Office of Research — Innocenti
    "https://www.unicef-irc.org/feeds/publications.xml",
    # Tech Policy Institute
    "https://techpolicyinstitute.org/feed/",
    # UK Children's Commissioner
    "https://www.childrenscommissioner.gov.uk/feed/",
    # RAND Corporation — technology & society
    "https://www.rand.org/content/dam/rand/sites/rss/research.xml",
    # Joan Ganz Cooney Center (Sesame Workshop research)
    "https://joanganzcooneycenter.org/feed/",
    # Connected Learning Alliance
    "https://clalliance.org/feed/",
    # Youth and Media (Berkman Klein)
    "https://youthandmedia.org/feed/",
    # Global Network Initiative
    "https://globalnetworkinitiative.org/feed/",
    # 80,000 Hours (EA-adjacent, AI risk policy depth)
    "https://80000hours.org/feed/",
    # Alignment Forum
    "https://www.alignmentforum.org/feed.xml",
    # LessWrong (AI safety reasoning)
    "https://www.lesswrong.com/feed.xml?view=curated-questions",

    # ── High-signal journalism (not in OPML) ─────────────────────────────────
    # The Markup — data-driven tech accountability (no RSS; replaced with Markup stories via Google News)
    "https://news.google.com/rss/search?q=site:themarkup.org&hl=en-US&gl=US&ceid=US:en",
    # Nieman Lab — journalism research
    "https://www.niemanlab.org/feed/",
    # Undark — science journalism
    "https://undark.org/feed/",
    # Prospect Magazine — long-form policy/ideas
    "https://www.prospectmagazine.co.uk/rss",

    # ── Researcher blogs (key AI/digital rights thinkers) ─────────────────────
    # Andrej Karpathy — neural nets, AI fundamentals
    "https://karpathy.github.io/feed.xml",
    # Simon Willison — AI capabilities, critical empirical takes
    "https://simonwillison.net/atom/everything/",
    # Arvind Narayanan — AI Snake Oil (already below as Substack, also has personal site)
    # Gary Marcus — AI skepticism, cognitive science
    "https://garymarcus.substack.com/feed",
    # Zvi Mowshowitz — AI policy, alignment
    "https://thezvi.substack.com/feed",
    # Astral Codex Ten (Scott Alexander) — empirical, long-form, counterintuitive
    "https://astralcodexten.substack.com/feed",
    # Eugene Wei — attention economy, platform design, social media
    "https://eugenewei.substack.com/feed",
    # The Morning Paper (Adrian Colyer) — CS research accessible summaries
    "https://blog.acolyer.org/feed/",
    # Gwern Branwen — AI, psychology, long-form empirical
    "https://gwern.net/feed",
    # Kate Crawford — AI and power (her institute blog via AI Now)
    # Timnit Gebru — DAIR Institute (Mastodon feed)
    "https://dair-community.social/users/DAIR.rss",
    # Abeba Birhane — cognitive science × AI
    "https://abebabirhane.substack.com/feed",
    # Safiya Umoja Noble — algorithmic oppression
    "https://safiyaunoble.substack.com/feed",
    # Chris Olah — mechanistic interpretability
    "https://colah.github.io/rss.xml",
    # Lilian Weng — AI research blog (OpenAI alum)
    "https://lilianweng.github.io/index.xml",
    # Sebastian Bubeck — AI reasoning, LLM theory
    "https://sbubeck.substack.com/feed",
    # AI Alignment Newsletter (Rohin Shah)
    "https://rohinshah.com/feed/",
    # Paul Christiano — alignment research
    "https://paulfchristiano.com/feed/",

    # ── Long-tail Substacks (obscure, high-signal, not in OPML) ──────────────
    # AI Snake Oil — Arvind Narayanan, skeptical empirical takes
    "https://aisnakeoil.substack.com/feed",
    # The Convivial Society — L.M. Sacasas, tech and human flourishing
    "https://theconvivialsociety.substack.com/feed",
    # Reboot — tech and power, written by young people
    "https://joinreboot.org/feed",
    # Works in Progress — long-form, original argument, evidence-based (moved to worksinprogress.news)
    "https://www.worksinprogress.news/feed",
    # Asterisk Magazine — rigorous empirical long-form
    "https://asteriskmag.com/feed.xml",
    # Real Life Magazine — technology and everyday life
    "https://reallifemag.com/feed/",
    # Logic Magazine — tech criticism
    "https://logicmag.io/feed.xml",
    # Scope of Work — adjacent technical thinking, systems
    "https://www.scopeofwork.net/rss/",
    # The Prepared — infrastructure and systems
    "https://theprepared.com/newsletter/rss",
    # Sentiers — curated futures writing, Patrick Tanguay
    "https://sentiers.media/rss/",
    # The Algorithmic Bridge — Alberto Romero, AI criticism
    "https://thealgorithmicbridge.substack.com/feed",
    # China AI Weekly (ChinAI) — Jeffrey Ding
    "https://chinai.substack.com/feed",
    # Bounded Regret — ML research blog
    "https://bounded-regret.ghost.io/rss/",
    # The Gradient Podcast blog (different from thegradient.pub which is in OPML)
    "https://thegradientpub.substack.com/feed",
    # Garbage Day — Ryan Broderick, internet culture signal
    "https://www.garbageday.email/feed",
    # Dense Discovery — design + tech
    "https://www.densediscovery.com/feed",
    # Exponential View — Azeem Azhar
    "https://www.exponentialview.co/feed",
    # The Reckoning — independent investigative
    "https://thereckoning.substack.com/feed",
    # Matters of Tech — policy angle
    "https://mattersoftech.substack.com/feed",
    # Multiverse — interdisciplinary tech ethics
    "https://multiversenewsletter.substack.com/feed",
    # The Intersection — Anjali Bhatt, youth + tech policy
    "https://theintersection.substack.com/feed",
    # Platformer (already in OPML — but keep for reference, dropped by OPML check)
    # Ethan Zuckerman — media, internet governance
    "https://ethanzuckerman.com/feed/",
    # danah boyd's apophenia blog
    "https://www.zephoria.org/thoughts/feed",
    # Sonia Livingstone (LSE) — children and digital media
    "https://blogs.lse.ac.uk/parenting4digitalfuture/feed/",
    # Shoshana Zuboff / surveillance capitalism adjacent
    "https://thereboot.com/feed/",

    # ── MIT Media Lab (specific groups, not just news feed) ───────────────────
    "https://www.media.mit.edu/publications/rss/",
    "https://www.media.mit.edu/groups/lifelong-kindergarten/publications/rss/",
    "https://www.media.mit.edu/groups/social-machines/publications/rss/",
    "https://www.media.mit.edu/groups/personal-robots/publications/rss/",
    "https://www.media.mit.edu/groups/human-dynamics/publications/rss/",
]

# Twitter/X accounts to follow via Nitter per-account RSS
# Fetched as: {nitter_instance}/{handle}/rss
# Covers Maximilian's ~150/193 X follows in AI, digital rights, academia
NITTER_ACCOUNTS = [
    # ── AI/ML Researchers ──────────────────────────────────────────────────────
    "karpathy",           # Andrej Karpathy — neural nets, AI education
    "AndrewYNg",          # Andrew Ng — AI education, industry
    "ylecun",             # Yann LeCun — deep learning, AI debate
    "GaryMarcus",         # Gary Marcus — AI skepticism, neurosymbolic
    "ESYudkowsky",        # Eliezer Yudkowsky — AI alignment
    "DanHendrycks",       # Dan Hendrycks — AI safety, benchmarks
    "paulfchristiano",    # Paul Christiano — alignment research
    "tegmark",            # Max Tegmark — FLI, AI existential risk
    "random_walker",      # Arvind Narayanan — AI Snake Oil
    "ZviMowshowitz",      # Zvi Mowshowitz — AI policy, alignment
    "drfeifei",           # Fei-Fei Li — AI and humanity
    "yoshuabengio",       # Yoshua Bengio — deep learning, AI safety
    "ilyasut",            # Ilya Sutskever — AI research
    "percyliang",         # Percy Liang — foundation models, HELM
    "chelseabfinn",       # Chelsea Finn — meta-learning, robotics
    "pabbeel",            # Pieter Abbeel — robotics, RL
    "srussell_ai",        # Stuart Russell — AI safety, CAIS
    "sama",               # Sam Altman — OpenAI
    "demishassabis",      # Demis Hassabis — DeepMind/Google
    "mmitchell_ai",       # Margaret Mitchell — AI ethics, documentation
    "zacharylipton",      # Zachary Lipton — ML criticism
    "ylecun",             # (already listed — deduplicated at runtime)
    "natashajaques",      # Natasha Jaques — social learning, RL
    "jacobandreas",       # Jacob Andreas — language + grounding
    "seb_ruder",          # Sebastian Ruder — NLP, transfer learning
    "colinraffel",        # Colin Raffel — T5, data curation
    "ClementDelangue",    # Clement Delangue — Hugging Face
    "rasbt",              # Sebastian Raschka — already in OPML but signal on novel papers

    # ── AI Ethics / Critical Tech ──────────────────────────────────────────────
    "timnitGebru",        # Timnit Gebru — DAIR, algorithmic harm
    "emilymbender",       # Emily Bender — NLP ethics, stochastic parrots
    "katecrawford",       # Kate Crawford — AI and power
    "jovialjoy",          # Joy Buolamwini — algorithmic bias, Poet of Code
    "safiyanoble",        # Safiya Umoja Noble — algorithmic oppression
    "mireillemoret",      # Mireille Moret — AI governance
    "math_babe",          # Cathy O'Neil — Weapons of Math Destruction
    "zephoria",           # danah boyd — youth, social media, identity
    "FrancesHaugen",      # Frances Haugen — Facebook whistleblower
    "juliapowles",        # Julia Powles — tech law and regulation
    "benedictevans",      # Benedict Evans — tech analysis, strategic
    "azeem",              # Azeem Azhar — Exponential View
    "zeynep",             # Zeynep Tufekci — social media, technology critique
    "mlcassidy",          # Meredith Broussard — tech journalism, anti-solutionism
    "abebab",             # Abeba Birhane — cognition, AI, ethics

    # ── Youth / Digital Rights / Policy ───────────────────────────────────────
    "5rightsfdn",         # 5Rights Foundation
    "childrencomm",       # UK Children's Commissioner
    "harari_yuval",       # Yuval Noah Harari — AI and humanity
    "profbowers",         # C. Thi Nguyen — games, echo chambers
    "Snowden",            # Edward Snowden — surveillance, privacy
    "EVanDijck",          # José van Dijck — platform society
    "MarkAndreessen",     # Marc Andreessen (counterpoint reading)
    "katelosse",          # Kate Losse — Facebook memoir, tech criticism
    "tante",              # Joerg Ruediger Sack — tech ethics, German perspective
    "hypervisible",       # Ruha Benjamin — race + technology
    "alondra",            # Alondra Nelson — science, tech, social policy

    # ── Science / Empirical Thinking ──────────────────────────────────────────
    "AndrewPSullivan",    # Andrew Sullivan — long-form political culture
    "sapinker",           # Steven Pinker — cognitive science, language
    "JohnHaidt",          # Jonathan Haidt — social psychology (Maximilian's debate opponent)
    "JeanTwenge",         # Jean Twenge — iGen, social media + teens research
    "AmyOrben",           # Amy Orben — screen time research, Oxford
    "przybylski_a",       # Andrew Przybylski — screens and teens, empirical
    "LenoreKenig",        # Lenore Skenazy — free-range kids, helicopter parenting
    "RebekahLundman",     # Rebekah Lundman — youth mental health research

    # ── Journalism / Long-form ────────────────────────────────────────────────
    "karaswisher",        # Kara Swisher — tech accountability
    "benedictevans",      # (already listed)
    "EzraKlein",          # Ezra Klein — ideas, AI, society
    "reckless",           # Max Read — internet culture, media
    "ryanbroderick",      # Ryan Broderick — Garbage Day
    "robinsloan",         # Robin Sloan — media, technology, fiction
    "warrenellis",        # Warren Ellis — futures thinking
    "tcarmody",           # Tim Carmody — media theory
]

# Nitter dynamic search queries — discovery-oriented, not account-following
NITTER_QUERIES = [
    "platform governance youth empirical 2025",
    "algorithmic harm children longitudinal study",
    "child rights digital policy research",
    "HCI youth participatory design",
    "cyberpsychology identity adolescent",
    "AI literacy pedagogy critique",
    "DSA DMA enforcement children",
    "AADC age appropriate design code implementation",
    "online safety act mechanics critique",
    "generative AI cognitive load study",
    "attention economy mechanism research",
    "youth digital wellbeing measurement",
    "platform accountability youth audit",
    "digital rights framework youth",
]

# Nitter instance sources — fetch live list from these, test, rotate
NITTER_LIST_SOURCES = [
    "https://raw.githubusercontent.com/wiki/zedeus/nitter/Instances.md",
    "https://raw.githubusercontent.com/xnaas/nitter-instances/master/instances.json",
]

NITTER_HARDCODED_FALLBACKS = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.catsarch.com",
    "https://nitter.unixfr.org",
    "https://nitter.1d4.us",
]
