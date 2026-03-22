"""
All feed sources for the discovery engine.

OPML_DOMAINS: domains already covered by Maximilian's NetNewsWire — articles from these are dropped.
DISCOVERY_FEEDS: list of (url, source_type) tuples.
  source_type "technical" → arXiv, journals, ML research blogs → rendered in a separate digest section
  source_type "discovery" → think tanks, niche Substacks, policy, long-form → main digest sections
"""

# Domains from Subscriptions-iCloud.opml — dropped before scoring
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
    "kill-the-newsletter.com",
}

# Each entry is (url, source_type)
# source_type: "technical" | "discovery"
DISCOVERY_FEEDS = [

    # ══ TECHNICAL ═════════════════════════════════════════════════════════════
    # These go into the "Research & Technical" digest section, not the main one.

    # ── arXiv ─────────────────────────────────────────────────────────────────
    ("https://rss.arxiv.org/rss/cs.CY", "technical"),   # Computers & Society
    ("https://rss.arxiv.org/rss/cs.HC", "technical"),   # Human-Computer Interaction
    ("https://rss.arxiv.org/rss/cs.AI", "technical"),   # Artificial Intelligence
    ("https://export.arxiv.org/search/?query=youth+platform+governance&searchtype=all&order=-announced_date_first&format=rss", "technical"),
    ("https://export.arxiv.org/search/?query=algorithmic+harm+children&searchtype=all&order=-announced_date_first&format=rss", "technical"),
    ("https://export.arxiv.org/search/?query=child+rights+digital+AI&searchtype=all&order=-announced_date_first&format=rss", "technical"),
    ("https://export.arxiv.org/search/?query=social+media+adolescent+longitudinal&searchtype=all&order=-announced_date_first&format=rss", "technical"),
    ("https://export.arxiv.org/search/?query=AI+alignment+interpretability&searchtype=all&order=-announced_date_first&format=rss", "technical"),

    # ── Academic journals ─────────────────────────────────────────────────────
    ("https://firstmonday.org/ojs/index.php/fm/gateway/plugin/WebFeedGatewayPlugin/rss2", "technical"),
    ("https://journals.sagepub.com/action/showFeed?jc=boca&type=axatoc&feed=rss", "technical"),   # Big Data & Society
    ("https://journals.sagepub.com/action/showFeed?jc=nmsa&type=axatoc&feed=rss", "technical"),   # New Media & Society
    ("https://journals.sagepub.com/action/showFeed?jc=smsa&type=axatoc&feed=rss", "technical"),   # Social Media + Society
    ("https://www.tandfonline.com/action/showFeed?jc=rics20&type=axatoc&feed=rss", "technical"),  # Information, Communication & Society
    ("https://dl.acm.org/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=chi&type=axatoc&feed=rss", "technical"),  # ACM CHI
    ("https://academic.oup.com/rss/site_5504/advanceAccess_5504.xml", "technical"),  # Journal of Computer-Mediated Communication
    ("https://link.springer.com/search.rss?query=digital+media&search-within=Journal&facet-journal-id=10964", "technical"),  # Journal of Youth & Adolescence

    # ── ML research blogs ─────────────────────────────────────────────────────
    ("https://distill.pub/rss.xml", "technical"),                    # Distill — ML clarity, visualization
    ("https://www.offconvex.org/feed.xml", "technical"),             # Off the Convex Path — DL theory (Arora, Ge)
    ("https://www.inference.vc/rss/", "technical"),                  # Ferenc Huszár — ML, causality, inference
    ("https://ruder.io/rss/index.rss", "technical"),                 # Sebastian Ruder — NLP
    ("https://jalammar.github.io/feed.xml", "technical"),            # Jay Alammar — ML visualization
    ("https://huggingface.co/blog/feed.xml", "technical"),           # Hugging Face blog
    ("https://fchollet.substack.com/feed", "technical"),             # François Chollet — ARC, deep learning
    ("https://karpathy.github.io/feed.xml", "technical"),            # Andrej Karpathy
    ("https://colah.github.io/rss.xml", "technical"),                # Chris Olah — mechanistic interpretability
    ("https://lilianweng.github.io/index.xml", "technical"),         # Lilian Weng — AI research surveys
    ("https://blog.acolyer.org/feed/", "technical"),                 # The Morning Paper — CS research
    ("https://epochai.org/feed", "technical"),                       # Epoch AI — compute trends, forecasting
    ("https://bounded-regret.ghost.io/rss/", "technical"),           # Bounded Regret — ML research

    # ── AI Alignment technical ────────────────────────────────────────────────
    ("https://www.alignmentforum.org/feed.xml", "technical"),        # Alignment Forum
    ("https://www.lesswrong.com/feed.xml?view=curated-questions", "technical"),  # LessWrong curated
    ("https://intelligence.org/feed/", "technical"),                 # MIRI
    ("https://vkrakovna.wordpress.com/feed/", "technical"),          # Victoria Krakovna
    ("https://paulfchristiano.com/feed/", "technical"),              # Paul Christiano
    ("https://rohinshah.com/feed/", "technical"),                    # Rohin Shah — AI alignment
    ("https://gwern.net/feed", "technical"),                         # Gwern — empirical, AI, psychology


    # ══ DISCOVERY ═════════════════════════════════════════════════════════════
    # Main digest sections: Must Read and Worth a Look.

    # ── Think tanks & policy institutes ──────────────────────────────────────
    ("https://www.oii.ox.ac.uk/feed/", "discovery"),                 # Oxford Internet Institute
    ("https://cyber.harvard.edu/feeds/news", "discovery"),           # Berkman Klein Center
    ("https://ainowinstitute.org/feed", "discovery"),                # AI Now Institute
    ("https://www.adalovelaceinstitute.org/feed/", "discovery"),     # Ada Lovelace Institute
    ("https://www.turing.ac.uk/rss.xml", "discovery"),               # Alan Turing Institute
    ("https://datasociety.net/feed/", "discovery"),                  # Data & Society
    ("https://points.datasociety.net/feed", "discovery"),            # Data & Society: Points
    ("https://cdt.org/feed/", "discovery"),                          # Center for Democracy & Technology
    ("https://www.eff.org/rss/updates.xml", "discovery"),            # Electronic Frontier Foundation
    ("https://knightcolumbia.org/feed", "discovery"),                # Knight First Amendment Institute
    ("https://reutersinstitute.politics.ox.ac.uk/rss.xml", "discovery"),  # Reuters Institute
    ("https://futureoflife.org/feed/", "discovery"),                 # Future of Life Institute
    ("https://partnershiponai.org/feed/", "discovery"),              # Partnership on AI
    ("https://5rightsfoundation.com/feed/", "discovery"),            # 5Rights Foundation
    ("https://www.pewresearch.org/internet/feed/", "discovery"),     # Pew Research — Internet & Tech
    ("https://www.commonsensemedia.org/rss.xml", "discovery"),       # Common Sense Media research
    ("https://www.unicef-irc.org/feeds/publications.xml", "discovery"),  # UNICEF Innocenti
    ("https://techpolicyinstitute.org/feed/", "discovery"),          # Tech Policy Institute
    ("https://www.childrenscommissioner.gov.uk/feed/", "discovery"), # UK Children's Commissioner
    ("https://www.rand.org/content/dam/rand/sites/rss/research.xml", "discovery"),  # RAND
    ("https://joanganzcooneycenter.org/feed/", "discovery"),         # Joan Ganz Cooney Center
    ("https://clalliance.org/feed/", "discovery"),                   # Connected Learning Alliance
    ("https://youthandmedia.org/feed/", "discovery"),                # Youth and Media (Berkman Klein)
    ("https://globalnetworkinitiative.org/feed/", "discovery"),      # Global Network Initiative
    ("https://80000hours.org/feed/", "discovery"),                   # 80,000 Hours
    ("https://www.accessnow.org/feed/", "discovery"),                # Access Now — digital rights
    ("https://citizenlab.ca/feed/", "discovery"),                    # Citizen Lab — surveillance research
    ("https://privacyinternational.org/rss.xml", "discovery"),       # Privacy International
    ("https://www.internetsociety.org/feed/", "discovery"),          # Internet Society
    ("https://www.article19.org/feed/", "discovery"),                # Article 19 — freedom of expression
    ("https://dair-community.social/users/DAIR.rss", "discovery"),   # DAIR Institute (Timnit Gebru)

    # ── AI ethics & critical tech researchers ─────────────────────────────────
    ("https://aisnakeoil.substack.com/feed", "discovery"),           # AI Snake Oil — Arvind Narayanan
    ("https://garymarcus.substack.com/feed", "discovery"),           # Gary Marcus — AI skepticism
    ("https://thezvi.substack.com/feed", "discovery"),               # Zvi Mowshowitz — AI policy
    ("https://simonwillison.net/atom/everything/", "discovery"),     # Simon Willison — AI capabilities
    ("https://abebabirhane.substack.com/feed", "discovery"),         # Abeba Birhane — AI & cognition
    ("https://safiyaunoble.substack.com/feed", "discovery"),         # Safiya Umoja Noble
    ("https://datafeminism.io/feed/", "discovery"),                  # Data Feminism (D'Ignazio)
    ("https://www.ajl.org/feed", "discovery"),                       # Algorithmic Justice League
    ("https://joybuolamwini.substack.com/feed", "discovery"),        # Joy Buolamwini
    ("https://chinai.substack.com/feed", "discovery"),               # ChinAI — Jeffrey Ding

    # ── AI alignment & governance (non-technical, policy/ideas framing) ────────
    ("https://thealgorithmicbridge.substack.com/feed", "discovery"), # The Algorithmic Bridge
    ("https://www.collectiveintelligenceproject.org/feed/", "discovery"),  # Collective Intelligence Project
    ("https://sbubeck.substack.com/feed", "discovery"),              # Sebastian Bubeck — AI reasoning

    # ── Youth, social media & cognitive effects ────────────────────────────────
    ("https://www.zephoria.org/thoughts/feed", "discovery"),         # danah boyd — apophenia
    ("https://blogs.lse.ac.uk/parenting4digitalfuture/feed/", "discovery"),  # Sonia Livingstone, LSE
    ("https://psyche.co/feed", "discovery"),                         # Psyche Magazine — philosophy & psychology
    ("https://digest.bps.org.uk/feed/", "discovery"),                # BPS Research Digest — psychology

    # ── Long-form, ideas, futures ─────────────────────────────────────────────
    ("https://astralcodexten.substack.com/feed", "discovery"),       # Astral Codex Ten — Scott Alexander
    ("https://eugenewei.substack.com/feed", "discovery"),            # Eugene Wei — attention, platforms
    ("https://www.ribbonfarm.com/feed/", "discovery"),               # Ribbonfarm — Venkatesh Rao
    ("https://breakingsmart.substack.com/feed", "discovery"),        # Breaking Smart — Venkat Rao
    ("https://www.roughtype.com/?feed=rss2", "discovery"),           # Rough Type — Nick Carr (attention)
    ("https://craigmod.com/rss/essays/", "discovery"),               # Craig Mod — longform, media
    ("https://nesslabs.com/feed", "discovery"),                      # Ness Labs — cognitive tools
    ("https://meaningness.com/rss.xml", "discovery"),                # Meaningness — David Chapman
    ("https://www.worksinprogress.news/feed", "discovery"),          # Works in Progress
    ("https://asteriskmag.com/feed.xml", "discovery"),               # Asterisk Magazine — rigorous long-form
    ("https://reallifemag.com/feed/", "discovery"),                  # Real Life Magazine
    ("https://logicmag.io/feed.xml", "discovery"),                   # Logic Magazine — tech criticism
    ("https://culturedigitally.org/feed/", "discovery"),             # Culture Digitally — media studies

    # ── High-signal journalism (not in OPML) ──────────────────────────────────
    ("https://news.google.com/rss/search?q=site:themarkup.org&hl=en-US&gl=US&ceid=US:en", "discovery"),  # The Markup
    ("https://www.niemanlab.org/feed/", "discovery"),                # Nieman Lab
    ("https://undark.org/feed/", "discovery"),                       # Undark — science journalism
    ("https://www.prospectmagazine.co.uk/rss", "discovery"),         # Prospect Magazine

    # ── Niche Substacks ───────────────────────────────────────────────────────
    ("https://theconvivialsociety.substack.com/feed", "discovery"),  # L.M. Sacasas — tech & human flourishing
    ("https://joinreboot.org/feed", "discovery"),                    # Reboot — tech & power, by young people
    ("https://www.garbageday.email/feed", "discovery"),              # Garbage Day — internet culture signal
    ("https://www.densediscovery.com/feed", "discovery"),            # Dense Discovery
    ("https://www.exponentialview.co/feed", "discovery"),            # Exponential View — Azeem Azhar
    ("https://sentiers.media/rss/", "discovery"),                    # Sentiers — Patrick Tanguay
    ("https://mattersoftech.substack.com/feed", "discovery"),        # Matters of Tech
    ("https://multiversenewsletter.substack.com/feed", "discovery"), # Multiverse — interdisciplinary ethics
    ("https://ethanzuckerman.com/feed/", "discovery"),               # Ethan Zuckerman — media, internet governance
    ("https://thereboot.com/feed/", "discovery"),                    # The Reboot
    ("https://www.scopeofwork.net/rss/", "discovery"),               # Scope of Work — systems thinking
    ("https://theprepared.com/newsletter/rss", "discovery"),         # The Prepared — infrastructure

    # ── MIT Media Lab ─────────────────────────────────────────────────────────
    ("https://www.media.mit.edu/publications/rss/", "technical"),
    ("https://www.media.mit.edu/groups/lifelong-kindergarten/publications/rss/", "technical"),
    ("https://www.media.mit.edu/groups/social-machines/publications/rss/", "technical"),
    ("https://www.media.mit.edu/groups/personal-robots/publications/rss/", "technical"),
    ("https://www.media.mit.edu/groups/human-dynamics/publications/rss/", "technical"),
]
