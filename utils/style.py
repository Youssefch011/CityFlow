
from pathlib import Path
import inspect

import streamlit as st

def apply_style():
    mobile_preview = st.query_params.get("mobile", "0") == "1"
    page_map = {
        "1_Home": "home",
        "app": "home",
        "2_City_Pulse_Map": "map",
        "3_Recommendations": "places",
        "4_Itinerary": "route",
        "6_Report_Crowded_Area": "report",
        "8_Profile": "profile",
    }
    active_page = ""
    active_script = ""
    for frame in inspect.stack():
        page_name = Path(frame.filename).stem
        if page_name in page_map:
            active_page = page_map[page_name]
            active_script = page_name
            break
    mobile_preview_css = """
    [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {
        display: none !important;
    }

    header, [data-testid="stHeader"], button[kind="header"], header [data-testid="baseButton-headerNoPadding"] {
        display: none !important;
    }

    .block-container {
        padding: 0.62rem 0.72rem 5.4rem !important;
        max-width: 356px !important;
    }

    .section-title {
        font-size: 20px !important;
        line-height: 1.08 !important;
        margin: 6px 0 9px !important;
    }

    .stApp {
        background: linear-gradient(180deg, #020817 0%, #071E3D 100%) !important;
    }

    p, .muted, .small-muted {
        font-size: 11px !important;
        line-height: 1.35 !important;
    }

    h1, h2, h3 {
        letter-spacing: 0 !important;
    }

    .cityflow-landing {
        min-height: 112px !important;
        padding: 12px !important;
        margin-bottom: 8px !important;
    }

    .cityflow-landing h1 {
        font-size: 20px !important;
        line-height: 1.06 !important;
        max-width: 260px !important;
    }

    .cityflow-landing p {
        display: none !important;
    }

    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.42rem !important;
        flex-wrap: wrap !important;
    }

    .premium-card, .glass-card, .dark-card, .mini-card, .feature-card,
    .destination-card, .metric-premium, .metric-box, .cityflow-image-card {
        padding: 10px !important;
        margin-bottom: 8px !important;
        box-shadow: 0 10px 24px rgba(0,0,0,0.22) !important;
    }

    .metric-premium, .metric-box, div[data-testid="stMetric"] {
        padding: 9px 10px !important;
    }

    .metric-number, .metric-value {
        font-size: 22px !important;
    }

    .metric-label {
        font-size: 10px !important;
        margin-top: 5px !important;
    }

    div.stButton > button,
    div[data-testid="stLinkButton"] > a {
        min-height: 36px !important;
        padding: 0.42rem 0.66rem !important;
        font-size: 11px !important;
    }

    input, textarea, [data-baseweb="select"] {
        font-size: 11px !important;
    }

    [data-testid="stTextInput"] label,
    [data-testid="stTextArea"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stSlider"] label,
    [data-testid="stMultiSelect"] label,
    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label {
        font-size: 10.5px !important;
        margin-bottom: 2px !important;
    }

    .home-feature {
        min-height: 0 !important;
        display: block !important;
        padding: 12px !important;
        margin-bottom: 8px !important;
        background-position: center !important;
    }

    .home-feature-title {
        font-size: 22px !important;
        line-height: 1.05 !important;
        margin-bottom: 6px !important;
    }

    .home-feature-quote {
        font-size: 11.5px !important;
        line-height: 1.3 !important;
    }

    .home-feature-tags {
        gap: 5px !important;
        margin-top: 9px !important;
    }

    .home-feature-tag, .route-tag, .itinerary-pill, .cityflow-meta-pill,
    .community-meta-row span, .quick-chip {
        padding: 6px 7px !important;
        font-size: 10px !important;
    }

    .home-feature-panel {
        margin-top: 9px !important;
        padding: 10px !important;
    }

    .home-feature-pressure {
        font-size: 28px !important;
    }

    .home-journey, .home-section-grid, .pricing-grid, .advisor-metrics,
    .profile-hero, .profile-stats-grid, .route-command-shell,
    .route-cockpit-grid, .route-kpi-grid, .route-strip {
        grid-template-columns: 1fr !important;
        gap: 7px !important;
        margin: 8px 0 !important;
    }

    .home-journey-step, .home-insight-card, .pricing-card,
    .profile-level-card, .profile-level-road, .route-panel,
    .route-pressure-panel, .route-cockpit, .route-brief {
        padding: 10px !important;
        min-height: 0 !important;
    }

    .home-journey-number, .cityflow-journey-icon, .route-node-index {
        width: 30px !important;
        height: 30px !important;
        font-size: 13px !important;
    }

    .cityflow-card-image-wrap, .cityflow-card-image, .cityflow-image-placeholder {
        height: 132px !important;
    }

    .cityflow-card-content, .destination-body {
        padding: 10px !important;
    }

    .cityflow-card-title, .itinerary-title, .stop-title {
        font-size: 17px !important;
    }

    .cityflow-card-description {
        font-size: 12px !important;
        line-height: 1.38 !important;
    }

    .itinerary-card {
        display: block !important;
        padding: 10px !important;
        margin-bottom: 8px !important;
    }

    .itinerary-card img {
        width: 100% !important;
        height: 132px !important;
        margin-bottom: 8px !important;
    }

    .stop-side {
        margin-top: 10px !important;
        padding: 11px !important;
    }

    .route-hero, .subscription-hero, .advisor-hero {
        min-height: 0 !important;
        padding: 14px !important;
        margin-bottom: 8px !important;
    }

    .route-title, .subscription-title, .advisor-title {
        font-size: 24px !important;
        line-height: 1.06 !important;
    }

    .route-subtitle, .subscription-subtitle, .advisor-subtitle {
        font-size: 12px !important;
        line-height: 1.4 !important;
    }

    .route-score-number {
        font-size: 36px !important;
    }

    .route-kpi-value, .advisor-metric-value, .profile-stat-value {
        font-size: 24px !important;
    }

    .pricing-card {
        min-height: 0 !important;
    }

    .pricing-price {
        font-size: 31px !important;
    }

    .pricing-desc {
        min-height: 0 !important;
        font-size: 12px !important;
    }

    .pricing-features {
        gap: 7px !important;
        margin-bottom: 10px !important;
    }

    .pricing-features li {
        font-size: 11px !important;
    }

    .profile-avatar {
        width: 58px !important;
        height: 58px !important;
        font-size: 30px !important;
    }

    .profile-name {
        font-size: 25px !important;
    }

    .profile-xp-number {
        font-size: 32px !important;
    }

    .community-report-card {
        grid-template-columns: 40px 1fr !important;
        gap: 9px !important;
        padding: 11px !important;
    }

    .community-avatar, .community-avatar-wrap {
        width: 38px !important;
        height: 38px !important;
        font-size: 12px !important;
    }

    .community-bubble {
        padding: 9px 11px !important;
        font-size: 12px !important;
        border-radius: 15px 15px 15px 5px !important;
    }

    [data-testid="stDataFrame"] {
        font-size: 10px !important;
    }

    .block-container {
        padding-bottom: 86px !important;
    }

    .cityflow-mobile-nav {
        position: fixed;
        left: 50%;
        bottom: 18px;
        transform: translateX(-50%);
        z-index: 9999;
        width: calc(100% - 24px);
        max-width: 364px;
        height: 60px;
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 2px;
        align-items: center;
        padding: 6px 7px 5px;
        border-radius: 24px;
        background:
            linear-gradient(180deg, rgba(15,23,42,0.92), rgba(2,8,23,0.96)),
            radial-gradient(circle at 50% 0%, rgba(103,232,249,0.14), transparent 58%);
        border: 1px solid rgba(148, 163, 184, 0.22);
        box-shadow:
            0 20px 48px rgba(0,0,0,0.52),
            inset 0 1px 0 rgba(255,255,255,0.10),
            inset 0 -1px 0 rgba(15,23,42,0.92);
        backdrop-filter: blur(22px);
    }

    .cityflow-mobile-nav a {
        height: 48px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 4px;
        border-radius: 18px;
        color: #9FB6C8 !important;
        text-decoration: none !important;
        font-size: 8px;
        font-weight: 900;
        letter-spacing: 0;
        line-height: 1;
        position: relative;
        transition: background 0.18s ease, color 0.18s ease, transform 0.18s ease;
    }

    .cityflow-mobile-nav a:hover,
    .cityflow-mobile-nav a:focus,
    .cityflow-mobile-nav a.active {
        background: rgba(103,232,249,0.10);
        color: #FFFFFF !important;
        transform: translateY(-1px);
    }

    .cityflow-mobile-nav a.active {
        background:
            linear-gradient(180deg, rgba(20,184,166,0.22), rgba(14,165,233,0.12)),
            rgba(255,255,255,0.04);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.12), 0 10px 24px rgba(20,184,166,0.16);
    }

    .cityflow-mobile-nav a.active:before {
        content: "";
        width: 18px;
        height: 3px;
        border-radius: 999px;
        background: #5DF2A5;
        box-shadow: 0 0 12px rgba(93,242,165,0.70);
        position: absolute;
        top: 4px;
    }

    .cityflow-mobile-nav .nav-icon {
        width: 18px;
        height: 18px;
        display: grid;
        place-items: center;
        border-radius: 11px;
        color: #67E8F9;
        background: rgba(103,232,249,0.08);
        border: 1px solid rgba(103,232,249,0.12);
    }

    .cityflow-mobile-nav a:hover .nav-icon,
    .cityflow-mobile-nav a:focus .nav-icon,
    .cityflow-mobile-nav a.active .nav-icon {
        color: #FFFFFF;
        background: linear-gradient(135deg, rgba(14,165,233,0.30), rgba(20,184,166,0.24));
        border-color: rgba(103,232,249,0.30);
        box-shadow: 0 0 16px rgba(56,189,248,0.22);
    }

    .cityflow-mobile-nav svg {
        width: 12px;
        height: 12px;
        stroke: currentColor;
        stroke-width: 2.4;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }
    """ if mobile_preview else ""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background:
            radial-gradient(circle at 12% 10%, rgba(0,219,255,0.16), transparent 28%),
            radial-gradient(circle at 88% 18%, rgba(77,255,166,0.13), transparent 28%),
            radial-gradient(circle at 50% 90%, rgba(120,70,255,0.14), transparent 32%),
            linear-gradient(135deg, #020817 0%, #06172A 45%, #071E3D 100%);
        color: #EAF7FF;
    }

    .block-container { padding-top: 1.2rem; padding-bottom: 4rem; max-width: 1220px; }

    .logo-orb {
        width: 112px;
        height: 112px;
        border-radius: 28px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(103,232,249,0.35);
        box-shadow: 0 0 40px rgba(0,219,255,0.22);
        padding: 8px;
        object-fit: contain;
        margin-bottom: 12px;
    }

    .hero-premium {
        position: relative;
        padding: 44px;
        border-radius: 34px;
        color: white;
        background:
            linear-gradient(135deg, rgba(2,8,23,0.94), rgba(7,30,61,0.82)),
            radial-gradient(circle at 85% 20%, rgba(53,194,165,0.45), transparent 32%),
            radial-gradient(circle at 15% 80%, rgba(0,144,255,0.35), transparent 28%);
        border: 1px solid rgba(103,232,249,0.28);
        box-shadow: 0 30px 80px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.08);
        margin-bottom: 28px;
        overflow: hidden;
    }

    .hero-premium:before {
        content: "";
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
        background-size: 42px 42px;
        mask-image: linear-gradient(to bottom, black, transparent 85%);
        pointer-events: none;
    }

    .hero-title {
        font-size: 58px;
        line-height: 1.02;
        font-weight: 900;
        margin-bottom: 12px;
        letter-spacing: -1.5px;
        position: relative;
        z-index: 1;
    }

    .gradient-text {
        background: linear-gradient(90deg, #38BDF8, #34D399, #FBBF24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 19px;
        opacity: 0.92;
        max-width: 720px;
        line-height: 1.55;
        position: relative;
        z-index: 1;
        color: #D9F7FF;
    }

    .hero-pill {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(14,165,233,0.14);
        border: 1px solid rgba(103,232,249,0.38);
        color: #67E8F9;
        font-weight: 800;
        margin-bottom: 16px;
        position: relative;
        z-index: 1;
        box-shadow: 0 0 24px rgba(14,165,233,0.18);
    }

    .premium-card, .glass-card {
        padding: 24px;
        border-radius: 28px;
        background: rgba(8,20,38,0.74);
        border: 1px solid rgba(103,232,249,0.22);
        box-shadow: 0 18px 48px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.06);
        margin-bottom: 18px;
        backdrop-filter: blur(18px);
        color: #EAF7FF;
    }

    .dark-card {
        padding: 26px;
        border-radius: 28px;
        background:
            linear-gradient(135deg, rgba(15,23,42,0.96), rgba(12,74,110,0.65)),
            radial-gradient(circle at 90% 10%, rgba(52,211,153,0.25), transparent 32%);
        color: white;
        border: 1px solid rgba(103,232,249,0.25);
        box-shadow: 0 20px 60px rgba(0,0,0,0.30);
        margin-bottom: 18px;
    }

    .mini-card, .feature-card {
        padding: 20px;
        border-radius: 24px;
        background: rgba(15,23,42,0.72);
        border: 1px solid rgba(103,232,249,0.20);
        box-shadow: 0 14px 35px rgba(0,0,0,0.25);
        min-height: 150px;
        margin-bottom: 16px;
        color: #EAF7FF;
    }

    .destination-card {
        border-radius: 28px;
        background: rgba(15,23,42,0.78);
        border: 1px solid rgba(103,232,249,0.22);
        box-shadow: 0 18px 45px rgba(0,0,0,0.28);
        overflow: hidden;
        margin-bottom: 18px;
        color: #EAF7FF;
    }

    .destination-body { padding: 18px; }

    .badge-green, .badge-orange, .badge-red, .badge-blue, .badge-yellow {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        font-weight: 900;
        font-size: 12px;
        letter-spacing: .25px;
        margin: 4px 0 8px 0;
        border: 1px solid rgba(255,255,255,0.12);
    }

    .badge-green { background: rgba(34,197,94,0.18); color:#86EFAC; }
    .badge-orange { background: rgba(251,146,60,0.18); color:#FDBA74; }
    .badge-red { background: rgba(244,63,94,0.18); color:#FDA4AF; }
    .badge-blue { background: rgba(56,189,248,0.18); color:#7DD3FC; }
    .badge-yellow { background: rgba(250,204,21,0.18); color:#FDE68A; }

    .muted, .small-muted { color: #B7D4E8; font-size: 14px; line-height: 1.55; }

    .metric-premium, .metric-box {
        padding: 22px;
        border-radius: 24px;
        background: rgba(8,20,38,0.72);
        border: 1px solid rgba(103,232,249,0.22);
        box-shadow: 0 16px 40px rgba(0,0,0,0.25);
        text-align: left;
        color: #EAF7FF;
    }

    .metric-number, .metric-value {
        font-size: 34px;
        font-weight: 900;
        color: #67E8F9;
        line-height: 1;
        text-shadow: 0 0 22px rgba(103,232,249,0.22);
    }

    .metric-label {
        margin-top: 8px;
        font-size: 13px;
        font-weight: 800;
        color: #A7C7D9;
        text-transform: uppercase;
        letter-spacing: .5px;
    }

    .section-title {
        font-size: 30px;
        font-weight: 900;
        color: #EAF7FF;
        margin: 18px 0 12px 0;
        letter-spacing: -0.6px;
    }

    .neo-search {
        padding: 18px 22px;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(103,232,249,0.26);
        color: #B7D4E8;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
        max-width: 680px;
    }

    .quick-chip {
        display: inline-block;
        padding: 9px 13px;
        margin: 5px 5px 5px 0;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(103,232,249,0.22);
        color: #D9F7FF;
        font-size: 13px;
        font-weight: 700;
    }

    .guest-note {
        padding: 14px;
        border-radius: 18px;
        background: rgba(251,191,36,0.16);
        border: 1px solid rgba(251,191,36,0.40);
        color: #FDE68A;
        font-weight: 800;
        text-align: center;
        margin-top: 10px;
    }

    div.stButton > button {
        border-radius: 16px;
        padding: 0.78rem 1.35rem;
        font-weight: 900;
        border: 1px solid rgba(103,232,249,0.30);
        background: linear-gradient(135deg, #0EA5E9, #14B8A6, #22C55E);
        color: white;
        box-shadow: 0 0 28px rgba(20,184,166,0.28);
    }

    div.stButton > button:hover {
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 0 34px rgba(56,189,248,0.36);
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(2,8,23,0.98), rgba(7,30,61,0.98)),
            radial-gradient(circle at 50% 10%, rgba(14,165,233,0.20), transparent 35%);
        border-right: 1px solid rgba(103,232,249,0.20);
    }

    [data-testid="stSidebar"] * { color: #EAF7FF !important; }

    input, textarea {
        background-color: rgba(255,255,255,0.92) !important;
        color: #071E3D !important;
    }
    
    .cityflow-image-card {
        overflow: hidden;
        border-radius: 28px;
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(103,232,249,0.22);
        box-shadow: 0 18px 45px rgba(0,0,0,0.28);
        margin-bottom: 22px;
        color: #EAF7FF;
        transition: all 0.25s ease;
    }

    .cityflow-image-card:hover {
        transform: translateY(-4px);
        border-color: rgba(103,232,249,0.48);
        box-shadow: 0 0 38px rgba(14,165,233,0.22), 0 22px 55px rgba(0,0,0,0.34);
    }

    .cityflow-card-image-wrap {
        position: relative;
        width: 100%;
        height: 225px;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(14,165,233,0.20), rgba(34,197,94,0.12));
    }

    .cityflow-card-image {
        width: 100%;
        height: 225px;
        object-fit: cover;
        display: block;
        filter: saturate(1.12) contrast(1.05);
        transition: transform 0.4s ease;
    }

    .cityflow-image-card:hover .cityflow-card-image {
        transform: scale(1.05);
    }

    .cityflow-card-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(2,8,23,0.05) 0%, rgba(2,8,23,0.78) 100%);
    }

    .cityflow-card-category {
        position: absolute;
        top: 14px;
        left: 14px;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(2,8,23,0.62);
        border: 1px solid rgba(103,232,249,0.28);
        color: #D9F7FF;
        font-size: 12px;
        font-weight: 900;
        backdrop-filter: blur(12px);
    }

    .cityflow-card-content {
        padding: 20px;
    }

    .cityflow-card-title {
        font-size: 25px;
        line-height: 1.15;
        font-weight: 900;
        color: #FFFFFF;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }

    .cityflow-card-description {
        color: #B7D4E8;
        font-size: 15px;
        line-height: 1.55;
        margin: 12px 0 14px 0;
    }

    .cityflow-card-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
        margin-top: 12px;
        font-size: 13px;
        color: #D9F7FF;
    }

    .cityflow-meta-pill {
        padding: 7px 10px;
        border-radius: 999px;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(103,232,249,0.16);
        font-weight: 800;
    }

    .cityflow-image-placeholder {
        height: 225px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #B7D4E8;
        background:
            radial-gradient(circle at 30% 20%, rgba(14,165,233,0.22), transparent 30%),
            radial-gradient(circle at 70% 80%, rgba(34,197,94,0.16), transparent 35%),
            rgba(15,23,42,0.82);
        font-weight: 900;
        letter-spacing: 0.3px;
        text-align: center;
        padding: 20px;
    }

    /* Premium product polish overrides */
    .block-container {
        max-width: 1240px;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .premium-card, .glass-card, .dark-card, .mini-card, .feature-card,
    .destination-card, .metric-premium, .metric-box, .cityflow-image-card {
        border-radius: 8px !important;
    }

    .section-title {
        letter-spacing: 0 !important;
        margin-top: 8px;
    }

    .hero-title {
        letter-spacing: 0 !important;
    }

    .cityflow-meta-pill, .quick-chip, .hero-pill,
    .badge-green, .badge-orange, .badge-red, .badge-blue, .badge-yellow {
        border-radius: 8px !important;
    }

    div.stButton > button,
    div[data-testid="stLinkButton"] > a {
        border-radius: 8px !important;
        min-height: 44px;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }

    div[data-testid="stLinkButton"] > a {
        border: 1px solid rgba(103,232,249,0.30);
        background: linear-gradient(135deg, #0EA5E9, #14B8A6);
        color: #FFFFFF;
        font-weight: 900;
        text-decoration: none;
        box-shadow: 0 0 24px rgba(20,184,166,0.20);
    }

    div[data-testid="stMetric"] {
        padding: 14px 16px;
        border-radius: 8px;
        background: rgba(8,20,38,0.60);
        border: 1px solid rgba(103,232,249,0.14);
    }

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid rgba(103,232,249,0.18);
    }

    [data-testid="stTabs"] button {
        font-weight: 800;
    }

    [data-testid="stSidebarNav"] a {
        border-radius: 8px;
        margin: 2px 8px;
        font-weight: 800;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: rgba(103,232,249,0.10);
    }

    .stSelectbox, .stMultiSelect, .stTextInput, .stTextArea, .stSlider {
        margin-bottom: 4px;
    }

    @media (max-width: 800px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .section-title {
            font-size: 25px;
        }

        .metric-number, .metric-value {
            font-size: 28px;
        }
    }

    </style>
    """ + f"<style>{mobile_preview_css}</style>", unsafe_allow_html=True)

    show_mobile_nav = mobile_preview and (
        st.session_state.get("logged_in", False) or active_script != "app"
    )
    if show_mobile_nav:
        def nav_class(page):
            return ' class="active"' if active_page == page else ""

        st.markdown(
            f"""
            <nav class="cityflow-mobile-nav" aria-label="Mobile app navigation">
                <a{nav_class("home")} href="/Home?mobile=1" target="_self"><span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/></svg></span><span>Home</span></a>
                <a{nav_class("map")} href="/City_Pulse_Map?mobile=1" target="_self"><span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M9 18 3 21V6l6-3 6 3 6-3v15l-6 3-6-3Z"/><path d="M9 3v15"/><path d="M15 6v15"/></svg></span><span>Map</span></a>
                <a{nav_class("places")} href="/Recommendations?mobile=1" target="_self"><span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M12 21s7-5.2 7-11a7 7 0 0 0-14 0c0 5.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg></span><span>Places</span></a>
                <a{nav_class("route")} href="/Itinerary?mobile=1" target="_self"><span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M4 19c4 0 4-14 8-14s4 14 8 14"/><circle cx="4" cy="19" r="2"/><circle cx="12" cy="5" r="2"/><circle cx="20" cy="19" r="2"/></svg></span><span>Route</span></a>
                <a{nav_class("report")} href="/Report_Crowded_Area?mobile=1" target="_self"><span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 4.3 2.7 18a2 2 0 0 0 1.7 3h15.2a2 2 0 0 0 1.7-3L13.7 4.3a2 2 0 0 0-3.4 0Z"/></svg></span><span>Report</span></a>
                <a{nav_class("profile")} href="/Profile?mobile=1" target="_self"><span class="nav-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.6-4 4.3-6 8-6s6.4 2 8 6"/></svg></span><span>Profile</span></a>
            </nav>
            """,
            unsafe_allow_html=True,
        )

def status_badge(level):
    if level >= 80:
        return '<span class="badge-red">Overcrowded</span>'
    if level >= 60:
        return '<span class="badge-orange">Busy</span>'
    if level >= 40:
        return '<span class="badge-blue">Moderate</span>'
    return '<span class="badge-green">Calm</span>'

def level_badge(points):
    if points >= 1000:
        return '<span class="badge-red">Urban Hero</span>'
    if points >= 600:
        return '<span class="badge-orange">CityFlow Ambassador</span>'
    if points >= 300:
        return '<span class="badge-blue">Sustainable Traveler</span>'
    if points >= 100:
        return '<span class="badge-green">Local Supporter</span>'
    return '<span class="badge-yellow">Explorer</span>'
