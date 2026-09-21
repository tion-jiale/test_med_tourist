"""Project introduction page. Save as pages/0_Introduction.py."""
from html import escape

import streamlit as st
from streamlit.errors import StreamlitAPIException

from shared import GROUP_NAME, PROJECT_TITLE, render_sidebar

st.set_page_config(page_title="Introduction", page_icon="📖", layout="wide")
render_sidebar()

# ---- Fill these in ----------------------------------------------------------
TEAM_MEMBERS = ["Shaza Nurayuni binti Shamsul Anuar", "Tion Jia Le", "Yip Yoong Eng", "Ain Mardhiah binti Abdul Hamid"]
HOOK = "Malaysia medical cost is cheap? A stereotype or a fact?"
# Edit these two to match the file names in your pages/ folder. If a path is
# wrong, the link is left out instead of crashing the page.
PAGE_RECOMMENDATION = "pages/1_Hospital_Recommendation.py"
PAGE_RECOVERY = "pages/2_Recovery_Plan.py"
# -----------------------------------------------------------------------------


def render(markup: str) -> None:
    """Render HTML. Lines are stripped and joined so Markdown never treats
    indented HTML as a code block."""
    flat = " ".join(line.strip() for line in markup.strip().splitlines())
    st.markdown(flat, unsafe_allow_html=True)


def page_link(path: str, label: str) -> None:
    try:
        st.page_link(path, label=label)
    except StreamlitAPIException:
        pass


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Source+Sans+3:wght@400;500;600&display=swap');

:root {
  --mc-ink: #F4F8F7;
  --mc-muted: rgba(244, 248, 247, .78);
  --mc-line: rgba(244, 248, 247, .2);
  --mc-sand: #F2C879;
  --mc-mint: #8FE0CB;
  --mc-serif: 'Fraunces', Georgia, serif;
  --mc-sans: 'Source Sans 3', 'Source Sans Pro', system-ui, sans-serif;
}

.block-container,
[data-testid="stMainBlockContainer"] {
  max-width: 1040px !important;
  margin: 0 auto !important;
  padding-top: 3.5rem !important;
  padding-bottom: 5rem !important;
}

/* Hero */
.mc-hero { margin-bottom: 3rem; }
.mc-pill {
  display: inline-block;
  padding: .25rem .85rem;
  margin-bottom: 1.3rem;
  border: 1px solid var(--mc-line);
  border-radius: 999px;
  font-family: var(--mc-sans);
  font-weight: 500;
  font-size: .88rem;
  color: var(--mc-muted);
}
.mc-title {
  font-family: var(--mc-serif);
  font-weight: 600;
  font-size: clamp(2.1rem, 5.2vw, 3.9rem);
  line-height: 1.05;
  letter-spacing: -.015em;
  text-wrap: balance;
  color: var(--mc-ink);
}
.mc-subtitle {
  margin-top: 1rem;
  font-family: var(--mc-serif);
  font-weight: 500;
  font-size: clamp(1.15rem, 2.2vw, 1.55rem);
  line-height: 1.3;
  color: var(--mc-ink);
}
.mc-lede {
  max-width: 52ch;
  margin-top: .9rem;
  font-family: var(--mc-sans);
  font-size: 1.2rem;
  line-height: 1.6;
  color: var(--mc-muted);
}

/* Text */
.mc-h2 {
  margin: 3.2rem 0 1rem;
  font-family: var(--mc-serif);
  font-weight: 500;
  font-size: 1.75rem;
  line-height: 1.2;
  color: var(--mc-ink);
}
.mc-p {
  max-width: 64ch;
  margin: 0 0 1rem;
  font-family: var(--mc-sans);
  font-size: 1.08rem;
  line-height: 1.65;
  color: var(--mc-muted);
}
.mc-p b { color: var(--mc-ink); font-weight: 600; }

/* Timeline */
.mc-timeline {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.6rem;
  margin: 2rem 0 2.2rem;
}
.mc-tl {
  position: relative;
  padding-top: 1.5rem;
  border-top: 2px solid var(--mc-line);
}
.mc-tl::before {
  content: '';
  position: absolute;
  top: -7px;
  left: 0;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--mc-sand);
}
.mc-tl-year {
  margin-bottom: .5rem;
  font-family: var(--mc-serif);
  font-weight: 600;
  font-size: 1.9rem;
  line-height: 1;
  color: var(--mc-sand);
}
.mc-tl-text {
  font-family: var(--mc-sans);
  font-size: .98rem;
  line-height: 1.5;
  color: var(--mc-muted);
}

/* The gap */
.mc-gap {
  margin: 2.4rem 0 0;
  padding: 1.7rem 1.9rem;
  border-left: 4px solid var(--mc-sand);
  border-radius: 0 12px 12px 0;
  background: rgba(255, 255, 255, .06);
}
.mc-gap-lead {
  margin-bottom: 1.1rem;
  font-family: var(--mc-serif);
  font-weight: 500;
  font-size: clamp(1.3rem, 2.6vw, 1.75rem);
  line-height: 1.3;
  color: var(--mc-ink);
}
.mc-gap-cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.8rem;
}
.mc-gap .mc-p { margin: 0; max-width: none; }

/* App steps */
.mc-step {
  padding: 1.4rem 1.5rem;
  border: 1px solid var(--mc-line);
  border-radius: 12px;
  background: rgba(255, 255, 255, .05);
}
.mc-step-head {
  display: flex;
  align-items: center;
  gap: .8rem;
  margin-bottom: .7rem;
}
.mc-step-num {
  flex: none;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: var(--mc-mint);
  font-family: var(--mc-sans);
  font-weight: 600;
  color: #06424B;
}
.mc-step-name {
  font-family: var(--mc-serif);
  font-weight: 500;
  font-size: 1.3rem;
  color: var(--mc-ink);
}
.mc-step .mc-p { margin: 0; max-width: none; }

/* Data layers */
.mc-layers { border-bottom: 1px solid var(--mc-line); }
.mc-layer {
  display: grid;
  grid-template-columns: 8rem 1fr;
  gap: 1.2rem;
  align-items: start;
  padding: 1.2rem 0;
  border-top: 1px solid var(--mc-line);
}
.mc-fig {
  font-family: var(--mc-serif);
  font-weight: 600;
  font-size: 2.5rem;
  line-height: 1;
  color: var(--mc-ink);
}
.mc-fig-unit {
  margin-top: .3rem;
  font-family: var(--mc-sans);
  font-size: .85rem;
  color: var(--mc-muted);
}
.mc-layer-real .mc-fig { color: var(--mc-mint); }
.mc-layer-curated .mc-fig { color: var(--mc-sand); }
.mc-tag {
  display: inline-block;
  margin-bottom: .5rem;
  padding: .15rem .7rem;
  border-radius: 999px;
  font-family: var(--mc-sans);
  font-weight: 600;
  font-size: .82rem;
}
.mc-tag-real { border: 1px solid var(--mc-mint); color: var(--mc-mint); }
.mc-tag-public { border: 1px solid var(--mc-ink); color: var(--mc-ink); }
.mc-tag-curated { border: 1px dashed var(--mc-sand); color: var(--mc-sand); }
.mc-layer .mc-p { margin: 0; max-width: 60ch; }

/* Team */
.mc-team {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 2rem;
  border-bottom: 1px solid var(--mc-line);
}
.mc-member {
  padding: .9rem 0;
  border-top: 1px solid var(--mc-line);
  font-family: var(--mc-sans);
  font-size: 1.05rem;
  color: var(--mc-ink);
}

@media (max-width: 760px) {
  .mc-timeline { grid-template-columns: 1fr; gap: 1.4rem; }
  .mc-tl {
    padding: 0 0 0 1.4rem;
    border-top: none;
    border-left: 2px solid var(--mc-line);
  }
  .mc-tl::before { top: .35rem; left: -7px; }
  .mc-gap-cols, .mc-team { grid-template-columns: 1fr; }
  .mc-layer { grid-template-columns: 5.5rem 1fr; }
  .mc-fig { font-size: 2rem; }
}
</style>
"""

render(CSS)

# ---------------------------------------------------------------- Hero
title_main, _, title_sub = PROJECT_TITLE.partition(":")
subtitle = (
    f'<div class="mc-subtitle">{escape(title_sub.strip())}</div>'
    if title_sub.strip()
    else ""
)
render(f"""
<div class="mc-hero">
  <div class="mc-pill">Group: {escape(GROUP_NAME)}</div>
  <div class="mc-title" role="heading" aria-level="1">{escape(title_main.strip())}</div>
  {subtitle}
  <div class="mc-lede">{escape(HOOK)}</div>
</div>
""")

# ---------------------------------------------------------- Background
render("""
<div class="mc-h2" role="heading" aria-level="2">Background</div>
<div class="mc-p">Malaysia is one of Southeast Asia's fastest-growing medical tourism hubs, known for low-cost, high-quality care and English-speaking doctors. The industry grew through deliberate policy:</div>

<div class="mc-timeline">
  <div class="mc-tl">
    <div class="mc-tl-year">1998</div>
    <div class="mc-tl-text">The National Committee for the Promotion of Health Tourism is formed, and 35 private hospitals are identified for promotion.</div>
  </div>
  <div class="mc-tl">
    <div class="mc-tl-year">2001</div>
    <div class="mc-tl-text">Medical tourism gets dedicated budget under the Eighth Malaysia Plan. Malaysia treats 75,210 foreign patients.</div>
  </div>
  <div class="mc-tl">
    <div class="mc-tl-year">2006</div>
    <div class="mc-tl-text">Foreign patients reach 296,687, generating RM203 million in revenue.</div>
  </div>
  <div class="mc-tl">
    <div class="mc-tl-year">2024</div>
    <div class="mc-tl-text">Malaysia welcomes 37.96 million foreign visitors overall, up 31.1% from 2023.</div>
  </div>
</div>

<div class="mc-p">Later growth came from international accreditation such as JCI and new specialist centres for cardiology, oncology, fertility and orthopaedics. Green Lanes at main entry points also speed up immigration clearance for medical travellers.</div>

<div class="mc-gap">
  <div class="mc-gap-lead">Malaysia still has no centralised, data-driven way to compare hospital-level treatment capability across states.</div>
  <div class="mc-gap-cols">
    <div class="mc-p">Patients choose by word of mouth and reputation. A few well-known hospitals stay visible and busy, while equally capable hospitals outside the main hubs go unnoticed.</div>
    <div class="mc-p">Changes in tax policy and cost structures raise the price of a poor match, so pairing each patient with a hospital that fits their treatment matters more than ever.</div>
  </div>
</div>
""")

# ------------------------------------------------------ How it works
render('<div class="mc-h2" role="heading" aria-level="2">How MediMatch works</div>')

col_rec, col_plan = st.columns(2, gap="large")

with col_rec:
    render("""
    <div class="mc-step">
      <div class="mc-step-head">
        <div class="mc-step-num">1</div>
        <div class="mc-step-name">Hospital Recommendation</div>
      </div>
      <div class="mc-p">Ranks hospitals by specialty and state using a rule-based approach built on accreditation, membership tier and international patient services.</div>
    </div>
    """)
    page_link(PAGE_RECOMMENDATION, "Open Hospital Recommendation")

with col_plan:
    render("""
    <div class="mc-step">
      <div class="mc-step-head">
        <div class="mc-step-num">2</div>
        <div class="mc-step-name">Recovery Plan</div>
      </div>
      <div class="mc-p">Takes the chosen hospital and treatment and suggests where the patient can recover. Major surgery keeps patients close to the treating hospital for follow-up. Minor procedures and wellness stays can move to rural destinations.</div>
    </div>
    """)
    page_link(PAGE_RECOVERY, "Open Recovery Plan")

# ------------------------------------------------------- Data and method
render("""
<div class="mc-h2" role="heading" aria-level="2">Data and method</div>
<div class="mc-layers">
  <div class="mc-layer mc-layer-real">
    <div>
      <div class="mc-fig">91</div>
      <div class="mc-fig-unit">hospitals</div>
    </div>
    <div>
      <div class="mc-tag mc-tag-real">Real data</div>
      <div class="mc-p"><b>Hospital dataset.</b> Coordinates, accreditation, membership tier, specialist listings and international patient service details.</div>
    </div>
  </div>

  <div class="mc-layer mc-layer-public">
    <div>
      <div class="mc-fig">5</div>
      <div class="mc-fig-unit">public sources</div>
    </div>
    <div>
      <div class="mc-tag mc-tag-public">Public sources</div>
      <div class="mc-p"><b>Used for the wider study.</b> MHTC, OpenDOSM, KKMNOW (MOH data catalogue), data.gov.my and Tourism Malaysia.</div>
    </div>
  </div>

  <div class="mc-layer mc-layer-curated">
    <div>
      <div class="mc-fig">27</div>
      <div class="mc-fig-unit">specialty categories</div>
    </div>
    <div>
      <div class="mc-tag mc-tag-curated">Curated / heuristic</div>
      <div class="mc-p"><b>Specialty groupings.</b> Specialist names are normalised into 27 categories, and treatment intensity per specialty is a heuristic default.</div>
    </div>
  </div>

  <div class="mc-layer mc-layer-curated">
    <div>
      <div class="mc-fig">14</div>
      <div class="mc-fig-unit">rural destinations</div>
    </div>
    <div>
      <div class="mc-tag mc-tag-curated">Curated / heuristic</div>
      <div class="mc-p"><b>Rural destinations.</b> Hand-curated and matched to hospital states.</div>
    </div>
  </div>
</div>
""")

# ------------------------------------------------------------------ Team
members = "".join(f'<div class="mc-member">{escape(name)}</div>' for name in TEAM_MEMBERS)
render(f"""
<div class="mc-h2" role="heading" aria-level="2">Team</div>
<div class="mc-team">{members}</div>
""")
