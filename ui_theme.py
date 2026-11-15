"""Reusable Bio-Orbital Liquid Glass theme for Field Shift Streamlit views."""

import base64
import html
from pathlib import Path

import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "imgs"
BRAND_ICON_PATH = IMAGE_DIR / "green-planet-logo.jpg"

TOKENS = {
    "bg_void": "#040D0A",
    "emerald_core": "#10B981",
    "bio_neon": "#00FF9D",
    "orbital_cyan": "#00E5FF",
    "nasa_alert": "#FC3D21",
    "solar_amber": "#F59E0B",
}


@st.cache_data(show_spinner=False)
def get_img_base64(filename: str) -> str:
    """Return a local image as base64, or an empty string when unavailable."""
    try:
        image_root = Path(__file__).resolve().parent / "imgs"
        image_path = (Path(__file__).resolve().parent / "imgs" / filename).resolve()
        if image_root.resolve() not in image_path.parents or not image_path.is_file():
            return ""
        return base64.b64encode(image_path.read_bytes()).decode("ascii")
    except (OSError, ValueError, TypeError):
        return ""


def _image_uri(filename: str) -> str:
    encoded = get_img_base64(filename)
    if not encoded:
        return ""
    extension = Path(filename).suffix.lower()
    mime_type = "image/png" if extension == ".png" else "image/jpeg"
    return f"data:{mime_type};base64,{encoded}"


def apply_theme() -> None:
    """Install the Bio-Orbital CSS theme in the active Streamlit page."""
    nebula_uri = _image_uri("emerald-nebula-bg.jpg")
    texture_uri = _image_uri("simple.jpg")
    texture_layer = f"url('{texture_uri}')" if texture_uri else "none"
    nebula_layer = f"url('{nebula_uri}')" if nebula_uri else "none"

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
        :root {{
            --bg-void: {TOKENS['bg_void']};
            --emerald-core: {TOKENS['emerald_core']};
            --bio-neon: {TOKENS['bio_neon']};
            --orbital-cyan: {TOKENS['orbital_cyan']};
            --nasa-alert: {TOKENS['nasa_alert']};
            --solar-amber: {TOKENS['solar_amber']};
            --glass-fill: linear-gradient(135deg, rgba(16, 42, 34, .50), rgba(6, 18, 24, .68));
            --glass-edge: rgba(0, 255, 157, .26);
            --text-main: #E8F7F1;
            --text-muted: #9BB5AA;
        }}
        html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        .stApp {{
            color: var(--text-main);
            background-color: var(--bg-void);
            background-image: linear-gradient(rgba(4, 13, 10, .74), rgba(4, 13, 10, .78)), {nebula_layer};
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{ background: rgba(4, 13, 10, .76); }}
        [data-testid="stSidebar"] {{
            background-color: rgba(4, 13, 10, .92);
            border-right: 1px solid rgba(0, 255, 157, .22);
        }}
        [data-testid="stSidebarContent"] {{ position:relative; isolation:isolate; }}
        [data-testid="stSidebarContent"]:before {{
            content:''; position:absolute; inset:0; z-index:-1; pointer-events:none;
            opacity:.05; mix-blend-mode:screen; background-image:{texture_layer};
            background-repeat:repeat; background-size:240px 240px;
        }}
        [data-testid="stSidebar"] * {{ color: var(--text-main); }}
        h1, h2, h3, h4, h5, h6 {{ color: var(--text-main) !important; }}
        h1, h2, h3 {{ font-family: 'Space Grotesk', sans-serif !important; }}
        p, label, [data-testid="stCaption"] {{ color: #C0D4CC; }}
        code, [data-testid="stMetricValue"], .telemetry-mono {{ font-family: 'JetBrains Mono', monospace !important; }}
        .stMarkdown p {{ font-size: 1rem; }}
        .liquid-glass-card {{
            position: relative;
            overflow: hidden;
            border: 1px solid var(--glass-edge);
            border-radius: 12px;
            background: var(--glass-fill);
            -webkit-backdrop-filter: blur(22px) saturate(180%);
            backdrop-filter: blur(22px) saturate(180%);
            box-shadow: inset 0 1px 1px rgba(255,255,255,.25), inset 0 -1px 1px rgba(0,229,255,.14), 0 14px 36px rgba(0,0,0,.58);
            transition: transform .28s ease, border-color .28s ease, box-shadow .28s ease;
        }}
        .liquid-glass-card:hover {{
            transform: translateY(-3px);
            border-color: rgba(0, 229, 255, .62);
            box-shadow: inset 0 1px 1px rgba(255,255,255,.30), 0 0 22px rgba(0,255,157,.12), 0 18px 42px rgba(0,0,0,.62);
        }}
        .liquid-glass-card > * {{ animation:fadeSlideUp .62s both; }}
        .liquid-glass-card > *:nth-child(2) {{ animation-delay:.1s; }}
        .liquid-glass-card > *:nth-child(3) {{ animation-delay:.2s; }}
        .brand-bar {{ display:flex; align-items:center; gap:12px; margin:4px 0 14px; }}
        .brand-emblem {{
            width:46px; height:46px; flex:none; border-radius:50%; object-fit:cover;
            border:1px solid rgba(0,255,157,.75); box-shadow:0 0 18px rgba(16,185,129,.45);
            animation:orbitalFloat 5s ease-in-out infinite;
        }}
        .brand-emblem-fallback {{ display:grid; place-items:center; color:var(--bio-neon); font:700 13px 'JetBrains Mono',monospace; }}
        .brand-label {{ color:var(--bio-neon); font:600 10px 'JetBrains Mono',monospace; }}
        .brand-name {{ color:var(--text-main); font:700 19px 'Space Grotesk',sans-serif; }}
        .mission-hero {{
            min-height:270px; margin:6px 0 16px; padding:28px 32px;
            display:flex; flex-direction:column; justify-content:center; gap:12px;
            background-color:#071510;
            background-image:linear-gradient(90deg, rgba(4,13,10,.92) 38%, rgba(4,13,10,.28) 100%), {f"url('{_image_uri('hero-agro-astronaut.png')}')" if _image_uri('hero-agro-astronaut.png') else 'none'};
            background-size:cover; background-position:center 42%;
            border:1px solid rgba(0,255,157,.38); box-shadow:inset 0 0 35px rgba(0,229,255,.08), 0 12px 35px rgba(0,0,0,.35);
        }}
        .mission-kicker {{ color:var(--bio-neon); font:600 10px 'JetBrains Mono',monospace; }}
        .mission-title {{ color:#fff; font:700 32px 'Space Grotesk',sans-serif; margin:0; }}
        .mission-subtitle {{ max-width:650px; color:#D5E7E0; margin:0; }}
        .mission-ticker {{ display:flex; flex-wrap:wrap; gap:8px; margin:0 0 18px; }}
        .mission-tag {{ padding:8px 10px; background:rgba(5,20,16,.78); border:1px solid rgba(0,229,255,.24); border-radius:999px; color:#DDF8EE; font:500 10px 'JetBrains Mono',monospace; }}
        .status-beacon {{ color:var(--bio-neon); animation:radarPulse 1.8s ease-out infinite; }}
        .section-title {{ margin:0 0 10px; color:var(--orbital-cyan); font:600 12px 'JetBrains Mono',monospace; text-transform:uppercase; }}
        .image-feature {{ display:grid; grid-template-columns:minmax(0, 1fr) minmax(0, 1.2fr); gap:18px; align-items:center; padding:16px; margin:0 0 16px; }}
        .feature-image {{ display:block; width:100%; max-height:190px; object-fit:cover; border-radius:8px; border:1px solid rgba(0,229,255,.35); filter:sepia(.18) hue-rotate(95deg) saturate(1.35); }}
        .feature-copy {{ color:#BDD2C9; font-size:12px; line-height:1.55; }}
        .feature-copy strong {{ display:block; color:var(--text-main); font:600 12px 'JetBrains Mono',monospace; margin-bottom:8px; }}
        .pipeline-card {{ padding:18px; margin:0 0 18px; }}
        .pipeline-content {{ display:grid; grid-template-columns:minmax(0, 1.25fr) minmax(180px, .75fr); gap:18px; align-items:center; }}
        .pipeline-steps {{ display:grid; grid-template-columns:1fr 22px 1fr 22px 1fr; gap:6px; align-items:stretch; }}
        .moisture-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; }}
        .pipeline-node {{ position:relative; overflow:hidden; padding:12px; border:1px solid rgba(0,255,157,.20); background:rgba(4,18,14,.62); border-radius:8px; animation:fadeSlideUp .65s both; }}
        .pipeline-node:nth-child(3) {{ animation-delay:.12s; }} .pipeline-node:nth-child(5) {{ animation-delay:.24s; }}
        .pipeline-node:after {{ content:''; position:absolute; inset:-60% -100%; background:linear-gradient(110deg, transparent 46%, rgba(0,229,255,.12) 50%, transparent 54%); animation:telemetryScan 5s linear infinite; pointer-events:none; }}
        .pipeline-node b {{ display:block; color:var(--bio-neon); font:600 9px 'JetBrains Mono',monospace; }}
        .pipeline-node span {{ display:block; margin-top:7px; color:var(--text-main); font-size:11px; line-height:1.4; }}
        .pipeline-node small {{ display:block; margin-top:6px; color:var(--text-muted); font:9px 'JetBrains Mono',monospace; }}
        .pipeline-arrow {{ align-self:center; color:var(--orbital-cyan); text-align:center; font:18px 'JetBrains Mono',monospace; }}
        .pipeline-image {{ width:100%; max-height:175px; object-fit:cover; border-radius:9px; border:1px solid rgba(16,185,129,.45); box-shadow:0 0 24px rgba(16,185,129,.12); }}
        .bridge-card {{ padding:16px; margin:0 0 16px; }}
        .bridge-svg {{ width:100%; height:auto; display:block; }}
        .bridge-beam {{ stroke-dasharray:5 7; animation:telemetryScan 1.4s linear infinite; }}
        .metric-card {{ position:relative; overflow:hidden; padding:15px; border-radius:10px; border:1px solid rgba(0,255,157,.22); background:linear-gradient(135deg,rgba(8,28,21,.90),rgba(6,18,24,.88)); backdrop-filter:blur(16px); }}
        .metric-card:before {{ content:''; position:absolute; inset:0; z-index:0; pointer-events:none; opacity:.05; mix-blend-mode:screen; background-image:{texture_layer}; background-repeat:repeat; background-size:180px 180px; }}
        .metric-card > * {{ position:relative; z-index:1; }}
        .metric-label {{ color:var(--text-muted); font:500 9px 'JetBrains Mono',monospace; }}
        .metric-value {{ margin-top:7px; color:var(--orbital-cyan); font:700 22px 'JetBrains Mono',monospace; }}
        .metric-ground .metric-value {{ color:var(--bio-neon); }} .metric-delta .metric-value {{ color:var(--nasa-alert); }}
        .metric-track {{ height:4px; margin-top:10px; overflow:hidden; background:rgba(145,181,165,.18); border-radius:4px; }}
        .metric-fill {{ height:100%; background:linear-gradient(90deg,var(--emerald-core),var(--orbital-cyan)); box-shadow:0 0 10px rgba(0,229,255,.45); }}
        .stress-alert {{ padding:13px 15px; margin:12px 0; color:#FFE2DC; background:rgba(252,61,33,.13); border:1px solid rgba(252,61,33,.72); border-radius:8px; font:600 11px 'JetBrains Mono',monospace; animation:criticalPulse 1.7s ease-out infinite; }}
        div.stButton > button {{ color:#04120D !important; background:var(--bio-neon); border:1px solid var(--bio-neon); border-radius:7px; font-weight:700; transition:all .22s ease; }}
        div.stButton > button:hover {{ color:var(--bio-neon) !important; background:rgba(0,255,157,.08); box-shadow:0 0 20px rgba(0,255,157,.25); transform:translateY(-1px); }}
        [data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {{ background:var(--bio-neon); }}
        [data-testid="stMetricValue"] {{ color:var(--orbital-cyan) !important; font-family:'JetBrains Mono',monospace !important; }}
        [data-testid="stAlert"] {{ border-radius:8px; }}
        iframe[title*="st_folium"] {{ max-width:100%; border:1px solid rgba(0,229,255,.32); border-radius:10px; box-shadow:0 0 20px rgba(0,229,255,.09); }}
        ::-webkit-scrollbar {{ width:8px; height:8px; }} ::-webkit-scrollbar-track {{ background:#06110D; }} ::-webkit-scrollbar-thumb {{ background:#1C5946; border-radius:8px; }}
        @keyframes fadeSlideUp {{ from {{ opacity:0; transform:translateY(12px); }} to {{ opacity:1; transform:translateY(0); }} }}
        @keyframes orbitalFloat {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-5px); }} }}
        @keyframes radarPulse {{ 0% {{ box-shadow:0 0 0 0 rgba(0,255,157,.24); }} 70% {{ box-shadow:0 0 0 8px rgba(0,255,157,0); }} 100% {{ box-shadow:0 0 0 0 rgba(0,255,157,0); }} }}
        @keyframes criticalPulse {{ 0% {{ box-shadow:0 0 0 0 rgba(252,61,33,.32); }} 70% {{ box-shadow:0 0 0 9px rgba(252,61,33,0); }} 100% {{ box-shadow:0 0 0 0 rgba(252,61,33,0); }} }}
        @keyframes telemetryScan {{ to {{ transform:translateX(100%); }} }}
        @media (max-width:760px) {{
            .mission-hero {{ min-height:290px; padding:20px; }} .mission-title {{ font-size:26px; }}
            .image-feature,.pipeline-content {{ grid-template-columns:1fr; }}
            .pipeline-steps {{ grid-template-columns:1fr; }} .pipeline-arrow {{ transform:rotate(90deg); }}
            .moisture-grid {{ grid-template-columns:1fr; }}
            .pipeline-image {{ max-height:150px; }}
        }}
    </style>
    """, unsafe_allow_html=True)


def render_brand_bar() -> str:
    logo_uri = _image_uri("green-planet-logo.jpg")
    emblem = (
        f'<img class="brand-emblem" src="{logo_uri}" alt="Field Shift brand emblem">'
        if logo_uri
        else '<div class="brand-emblem brand-emblem-fallback">FS</div>'
    )
    return f"""
    <div class="brand-bar">{emblem}<div>
        <div class="brand-label">BIO-ORBITAL AGRICULTURE SYSTEMS</div>
        <div class="brand-name">Field Shift</div>
    </div></div>
    """


def render_hero(subtitle: str) -> str:
    return f"""
    <section class="mission-hero liquid-glass-card">
        <div class="mission-kicker">FIELD SHIFT / ORBITAL TELEMETRY</div>
        <h1 class="mission-title">From Space to Roots</h1>
        <p class="mission-subtitle">{html.escape(subtitle)}</p>
    </section>
    """


def render_ticker() -> str:
    items = (
        "[ONLINE] ORBITAL LINK ACTIVE",
        "150 EGYPT CROPLAND NODES",
        "100,350 DAILY ROWS",
        "CATBOOST RMSE: 0.0648",
        "FAO-56 RAG: 959 VERIFIED CHUNKS",
    )
    tags = "".join(
        f'<span class="mission-tag">{html.escape(item)}</span>'
        if index
        else f'<span class="mission-tag"><span class="status-beacon">{html.escape(item)}</span></span>'
        for index, item in enumerate(items)
    )
    return f'<div class="mission-ticker">{tags}</div>'


def render_data_pillars() -> str:
    image_uri = _image_uri("a.jpg")
    visual = (
        f'<img class="feature-image" src="{image_uri}" alt="Aerospace observation visual">'
        if image_uri
        else '<div class="feature-image" role="img" aria-label="Aerospace observation visual"></div>'
    )
    return f"""
    <section class="liquid-glass-card image-feature">
        {visual}
        <div class="feature-copy">
            <strong>NASA MULTI-SOURCE DATA PILLARS</strong>
            NASA POWER API / NASA SMAP / MODIS via GEE / ISRIC SoilGrids
            <br><br><span class="telemetry-mono">150 EGYPT CROPLAND NODES / 100,350 DAILY ROWS</span>
            <br><small>SMAP and MODIS are project data pillars; the current live scan requests POWER and SoilGrids.</small>
        </div>
    </section>
    """


def render_pipeline() -> str:
    image_uri = _image_uri("astronaut-deep-green.jpg")
    visual = (
        f'<img class="pipeline-image" src="{image_uri}" alt="Astronaut in a deep green orbital environment">'
        if image_uri
        else '<div class="pipeline-image" role="img" aria-label="Orbital pipeline visual"></div>'
    )
    return f"""
    <section class="liquid-glass-card pipeline-card">
        <div class="section-title">3-Layer Zero-Hallucination Decision Pipeline</div>
        <div class="pipeline-content">
            <div class="pipeline-steps">
                <div class="pipeline-node"><b>LAYER 01 / DECIDE</b><span>Deterministic JSON Rules</span><small>crops_knowledge_base.json</small></div>
                <div class="pipeline-arrow">&gt;</div>
                <div class="pipeline-node"><b>LAYER 02 / RETRIEVE</b><span>FAO-56 FAISS RAG</span><small>959 indexed chunks</small></div>
                <div class="pipeline-arrow">&gt;</div>
                <div class="pipeline-node"><b>LAYER 03 / EXPLAIN</b><span>Grounded explanation</span><small>Gemini 3.1-Flash-Lite</small></div>
            </div>
            {visual}
        </div>
    </section>
    """


def render_bridge() -> str:
    return """
    <section class="liquid-glass-card bridge-card">
        <div class="section-title">Space-to-Roots Telemetry Bridge</div>
        <svg class="bridge-svg" viewBox="0 0 900 132" role="img" aria-label="Satellite telemetry beams down to a root-zone moisture sensor">
            <defs><linearGradient id="orbitalBeam" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#00E5FF"/><stop offset="1" stop-color="#00FF9D" stop-opacity=".35"/></linearGradient></defs>
            <path d="M0 92 Q220 80 450 92 T900 92" fill="none" stroke="#10B981" stroke-opacity=".42" stroke-width="2"/>
            <path d="M0 108 H900" stroke="#00FF9D" stroke-opacity=".16" stroke-dasharray="4 8"/>
            <path d="M408 98 Q429 91 450 98 T492 98 M408 104 Q429 97 450 104 T492 104" fill="none" stroke="#00E5FF" stroke-opacity=".62"><animate attributeName="stroke-opacity" values=".25;.8;.25" dur="2.6s" repeatCount="indefinite"/></path>
            <g transform="translate(450 22)" stroke="#D9FFF5" stroke-width="2" fill="#10352B"><rect x="-15" y="-8" width="30" height="16" rx="2"/><path d="M-42 -13 H-19 V13 H-42Z M19 -13 H42 V13 H19Z" fill="#0A2B31" stroke="#00E5FF"/></g>
            <path class="bridge-beam" d="M450 40 V105" stroke="url(#orbitalBeam)" stroke-width="3"/>
            <path d="M438 61 Q450 50 462 61 M432 70 Q450 54 468 70" fill="none" stroke="#00E5FF" stroke-opacity=".8"/>
            <g transform="translate(450 91)" stroke="#B6FFE3" stroke-width="2" fill="none"><path d="M0 0 V32 M-8 32 H8 M0 20 L-11 29 M0 23 L11 31"/><circle cx="0" cy="0" r="4" fill="#10B981"/></g>
            <circle cx="450" cy="53" r="3" fill="#00FF9D"><animate attributeName="cy" values="43;88;43" dur="2.2s" repeatCount="indefinite"/></circle>
            <text x="24" y="32" fill="#9BB5AA" font-size="10" font-family="JetBrains Mono">ORBITAL OBSERVATION</text>
            <text x="24" y="119" fill="#9BB5AA" font-size="10" font-family="JetBrains Mono">ROOT-ZONE MOISTURE</text>
        </svg>
    </section>
    """


def render_moisture_comparison(ai_value: float, sensor_value: float, deficit: float) -> str:
    ai_percent = ai_value * 100
    sensor_percent = sensor_value * 100
    delta_percent = -deficit * 100
    ai_width = max(0.0, min(100.0, ai_percent / 0.8))
    sensor_width = max(0.0, min(100.0, sensor_percent / 0.8))
    return f"""
    <section class="liquid-glass-card" style="padding:16px;margin:12px 0">
        <div class="section-title">Space vs. Ground Reality</div>
        <div class="moisture-grid">
            <div class="metric-card"><div class="metric-label">AI SPACE BASELINE / CATBOOST</div><div class="metric-value">{ai_percent:.1f}%</div><div class="metric-track"><div class="metric-fill" style="width:{ai_width:.1f}%"></div></div></div>
            <div class="metric-card"><div class="metric-label">LIVE GROUND IoT SENSOR</div><div class="metric-value" style="color:var(--bio-neon)">{sensor_percent:.1f}%</div><div class="metric-track"><div class="metric-fill" style="width:{sensor_width:.1f}%"></div></div></div>
            <div class="metric-card metric-delta"><div class="metric-label">GROUND DELTA / SENSOR - BASELINE</div><div class="metric-value">{delta_percent:+.1f}%</div><div class="metric-label">ALERT THRESHOLD: ±10.0%</div></div>
        </div>
    </section>
    """


def render_status_alert(status: str, deficit: float, message: str) -> str:
    delta_percent = -deficit * 100
    if status == "SEVERE WATER STRESS":
        return f'<div class="stress-alert">[ALERT] {delta_percent:+.1f}% DEFICIT / SEVERE WATER STRESS DETECTED<br><span>{html.escape(message)}</span></div>'
    if status == "OVER-IRRIGATION":
        return f'<div class="liquid-glass-card" style="padding:12px;margin:12px 0;border-color:rgba(245,158,11,.5)">[WARNING] {html.escape(message)}</div>'
    return f'<div class="liquid-glass-card" style="padding:12px;margin:12px 0">[OPTIMAL] {html.escape(message)}</div>'