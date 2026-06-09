import pandas as pd
import streamlit as st

from utils.image import get_image_base64
from utils.storage import (
    ensure_data_files,
    get_preferences,
    get_user_by_email,
    save_preferences,
    save_user,
)
from utils.style import apply_style, level_badge
from utils.translations import language_selector


st.set_page_config(page_title="CityFlow", page_icon="CF", layout="wide")
apply_style()
ensure_data_files()
t = language_selector(st)
mobile_preview = st.query_params.get("mobile", "0") == "1"

for key, value in {
    "logged_in": False,
    "guest": False,
    "points": 0,
    "preferences": [],
    "current_user": None,
    "onboarding_done": False,
    "travel_style": "Balanced",
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

locations = pd.read_csv("data/locations.csv")
reports = pd.read_csv("data/reports.csv")
hero_image = get_image_base64("assets/images/sagrada_familia.jpg")
logo_image = get_image_base64("assets/cityflow_logo.png")

if not st.session_state.get("logged_in", False):
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {
            display: none !important;
        }
        button[kind="header"], header [data-testid="baseButton-headerNoPadding"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if mobile_preview:
        st.markdown(
            """
            <style>
            .cityflow-landing {
                min-height: 104px !important;
                padding: 12px !important;
                margin-bottom: 7px !important;
                background-position: center top !important;
            }

            .cityflow-mobile-nav {
                display: none !important;
            }

            .cityflow-landing h1 {
                font-size: 21px !important;
                line-height: 1.02 !important;
                max-width: 248px !important;
            }

            .cityflow-landing .cityflow-landing-kicker {
                display: none !important;
            }

            .cityflow-landing p,
            .premium-card,
            .cityflow-journey,
            .metric-premium {
                display: none !important;
            }

            .cityflow-login-shell {
                padding: 10px !important;
                margin-top: 0 !important;
            }

            .cityflow-brand-lockup {
                margin-bottom: 7px !important;
                padding: 6px !important;
                gap: 8px !important;
            }

            .cityflow-brand-lockup img {
                width: 38px !important;
                height: 38px !important;
            }

            .cityflow-brand-name {
                font-size: 13px !important;
            }

            .cityflow-brand-tagline {
                font-size: 9px !important;
            }

            .section-title {
                font-size: 19px !important;
                margin: 4px 0 7px !important;
            }

            .gmail-connect-note,
            .guest-note {
                padding: 7px !important;
                font-size: 9.5px !important;
                margin: 5px 0 !important;
            }

            [data-testid="stRadio"] {
                margin-top: 4px !important;
            }

            [data-testid="stTextInput"] {
                margin-bottom: 2px !important;
            }

            [data-testid="stCheckbox"] {
                margin: 2px 0 4px !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

hero_bg = f"data:image/jpeg;base64,{hero_image}" if hero_image else ""
logo_html = f'<img src="data:image/png;base64,{logo_image}" alt="CityFlow logo">' if logo_image else ""
brand_lockup = (
    '<div class="cityflow-brand-lockup">'
    f'{logo_html}'
    '<div>'
    '<div class="cityflow-brand-name">CITYFLOW</div>'
    '<div class="cityflow-brand-tagline">Live the City</div>'
    '</div>'
    '</div>'
)
st.markdown(
    f"""
    <style>
    .cityflow-landing {{
        min-height: 430px;
        padding: 42px;
        border-radius: 8px;
        margin-bottom: 22px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(103,232,249,0.26);
        background:
            linear-gradient(90deg, rgba(2,8,23,0.92) 0%, rgba(2,8,23,0.76) 48%, rgba(2,8,23,0.22) 100%),
            url("{hero_bg}") center/cover no-repeat;
        box-shadow: 0 24px 70px rgba(0,0,0,0.34);
    }}
    .cityflow-landing h1 {{
        margin: 0;
        max-width: 760px;
        color: #FFFFFF;
        font-size: 64px;
        line-height: 1.02;
        letter-spacing: 0;
        font-weight: 900;
    }}
    .cityflow-landing p {{
        max-width: 690px;
        margin: 18px 0 0 0;
        color: #D9F7FF;
        font-size: 18px;
        line-height: 1.55;
    }}
    .cityflow-landing-kicker {{
        display: inline-flex;
        gap: 8px;
        align-items: center;
        padding: 8px 11px;
        margin-bottom: 16px;
        border-radius: 8px;
        color: #67E8F9;
        background: rgba(14,165,233,0.12);
        border: 1px solid rgba(103,232,249,0.24);
        font-size: 12px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    .cityflow-login-shell {{
        padding: 22px;
        border-radius: 8px;
        background: rgba(8,20,38,0.82);
        border: 1px solid rgba(103,232,249,0.22);
        box-shadow: 0 18px 45px rgba(0,0,0,0.28);
    }}
    .gmail-connect-note {{
        padding: 10px 12px;
        border-radius: 8px;
        margin: 8px 0 12px;
        color: #D9F7FF;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(103,232,249,0.16);
        font-size: 12px;
        line-height: 1.4;
        font-weight: 700;
    }}
    .cityflow-brand-lockup {{
        display: inline-flex;
        align-items: center;
        gap: 12px;
        padding: 8px 10px 8px 8px;
        margin-bottom: 20px;
        border-radius: 8px;
        background: rgba(2,8,23,0.58);
        border: 1px solid rgba(103,232,249,0.24);
        backdrop-filter: blur(14px);
    }}
    .cityflow-brand-lockup img {{
        width: 46px;
        height: 46px;
        border-radius: 8px;
        object-fit: contain;
        background: rgba(255,255,255,0.08);
        padding: 4px;
    }}
    .cityflow-brand-name {{
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 900;
        line-height: 1;
    }}
    .cityflow-brand-tagline {{
        color: #67E8F9;
        font-size: 11px;
        font-weight: 900;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .cityflow-journey {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin: 18px 0 22px;
    }}
    .cityflow-journey-step {{
        padding: 18px;
        border-radius: 8px;
        background: rgba(8,20,38,0.74);
        border: 1px solid rgba(103,232,249,0.18);
        box-shadow: 0 14px 34px rgba(0,0,0,0.22);
        min-height: 150px;
    }}
    .cityflow-journey-step b {{
        display: block;
        color: #FFFFFF;
        font-size: 16px;
        margin: 9px 0 7px;
    }}
    .cityflow-journey-icon {{
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(103,232,249,0.12);
        border: 1px solid rgba(103,232,249,0.22);
        font-size: 19px;
    }}
    .cityflow-journey-step span {{
        color: #B7D4E8;
        font-size: 13px;
        line-height: 1.45;
    }}
    @media (max-width: 900px) {{
        .cityflow-journey {{
            grid-template-columns: 1fr;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.logged_in:
    st.markdown(
        f"""
        <div class="cityflow-landing">
            {brand_lockup}<br>
            <div class="cityflow-landing-kicker">CityFlow MVP · Smart Tourism Operations</div>
            <h1>{t.get("home_quote_title", "Barcelona feels better when the city can breathe.")}</h1>
            <p>{t.get("subtitle", "AI-assisted city flow management for balanced, sustainable local and visitor experiences.")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.1, 0.9])
    with left:
        a, b, c = st.columns(3)
        a.markdown(f'<div class="metric-premium"><div class="metric-number">{len(locations)}</div><div class="metric-label">Tracked Places</div></div>', unsafe_allow_html=True)
        b.markdown(f'<div class="metric-premium"><div class="metric-number">{len(locations[locations["crowd_level"] >= 80])}</div><div class="metric-label">Crowded Zones</div></div>', unsafe_allow_html=True)
        c.markdown(f'<div class="metric-premium"><div class="metric-number">{len(reports)}</div><div class="metric-label">Live Reports</div></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="premium-card">
                <div class="section-title">{t.get("how_cityflow_helps", "How CityFlow Helps")}</div>
                <p class="muted">{t.get("home_quote", "Choose the calmer move, keep the experience beautiful, and leave space for everyone else.")}</p>
            </div>
            <div class="cityflow-journey">
                <div class="cityflow-journey-step"><div class="cityflow-journey-icon">1</div><b>{t.get("journey_1_title", "Avoid pressure")}</b><span>{t.get("journey_1_text", "Start from the places that feel too crowded and understand the risk before going.")}</span></div>
                <div class="cityflow-journey-step"><div class="cityflow-journey-icon">2</div><b>{t.get("journey_2_title", "Discover better places")}</b><span>{t.get("journey_2_text", "Find calmer alternatives that still match your interests and available time.")}</span></div>
                <div class="cityflow-journey-step"><div class="cityflow-journey-icon">3</div><b>{t.get("journey_3_title", "Help the city")}</b><span>{t.get("journey_3_text", "Send live crowd reports so other residents and visitors can make smarter choices.")}</span></div>
                <div class="cityflow-journey-step"><div class="cityflow-journey-icon">4</div><b>{t.get("journey_4_title", "Earn rewards")}</b><span>{t.get("journey_4_text", "Turn positive movement choices into points, profile levels, and local benefits.")}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="cityflow-login-shell">', unsafe_allow_html=True)
        st.markdown(brand_lockup, unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{t.get("login", "Login")}</div>', unsafe_allow_html=True)
        if st.button(t.get("continue_with_google", "Continue with Google / Gmail"), use_container_width=True, key="google_quick_login"):
            google_email = "cityflow.user@gmail.com"
            existing_user = get_user_by_email(google_email)
            user = save_user(
                (existing_user or {}).get("name", "") or "Google City Explorer",
                google_email,
                "",
                st.session_state.language,
                st.session_state.points,
                daily_alerts=True,
            )
            prefs = get_preferences(google_email)
            st.session_state.logged_in = True
            st.session_state.guest = False
            st.session_state.current_user = user
            st.session_state.points = int(user.get("points", 0))
            st.session_state.preferences = prefs["interests"]
            st.session_state.travel_style = prefs["travel_style"]
            st.session_state.onboarding_done = bool(existing_user or prefs["interests"])
            st.rerun()

        if st.button(t.get("guest", "Continue as City Explorer"), use_container_width=True, key="guest_quick_login"):
            st.session_state.logged_in = True
            st.session_state.guest = True
            st.session_state.current_user = {"name": "City Explorer", "email": "", "phone": "", "points": 0}
            st.session_state.points = 0
            st.session_state.preferences = []
            st.session_state.travel_style = "Balanced"
            st.session_state.onboarding_done = True
            st.rerun()

        mode = st.radio(t.get("user_type", "User type"), [t.get("existing_user", "Existing user"), t.get("new_user", "New user")], horizontal=True)
        is_existing = mode == t.get("existing_user", "Existing user")
        name = "Demo City Explorer"
        email = st.text_input(t.get("email", "Email"), value="tourist@cityflow.com" if is_existing else "")
        phone = st.text_input(t.get("phone", "Phone"), value="+34 600 000 000" if is_existing else "")
        st.text_input(t.get("password", "Password"), type="password", value="demo123" if is_existing else "")
        if not is_existing:
            name = st.text_input(t.get("full_name", "Full name"), value="")
        daily_alerts = st.checkbox(
            t.get("daily_alerts_opt_in", "Send me a CityFlow crowd alert email every 24 hours"),
            value=True,
            help=t.get("daily_alerts_help", "Daily emails include crowded zones, calmer alternatives, and one recommended move for the day."),
        )

        if st.button(t.get("continue_with_google", "Continue with Google / Gmail"), use_container_width=True, key="google_login"):
            google_email = email.strip() or "cityflow.user@gmail.com"
            existing_user = get_user_by_email(google_email)
            user = save_user(
                (existing_user or {}).get("name", "") or name or "Google City Explorer",
                google_email,
                phone,
                st.session_state.language,
                st.session_state.points,
                daily_alerts=daily_alerts,
            )
            prefs = get_preferences(google_email)
            st.session_state.logged_in = True
            st.session_state.guest = False
            st.session_state.current_user = user
            st.session_state.points = int(user.get("points", 0))
            st.session_state.preferences = prefs["interests"]
            st.session_state.travel_style = prefs["travel_style"]
            st.session_state.onboarding_done = bool(existing_user or prefs["interests"])
            st.rerun()

        st.markdown(
            f'<div class="gmail-connect-note">{t.get("gmail_demo_note", "Prototype mode: Google sign-in creates or opens a Gmail-based CityFlow profile. Real OAuth can be connected later with Google Cloud credentials.")}</div>',
            unsafe_allow_html=True,
        )

        if st.button(t.get("enter", "Enter CityFlow") if is_existing else t.get("create_account", "Create Account"), use_container_width=True, key="email_login"):
            if not email.strip():
                st.error(t.get("email_required", "Please enter an email address."))
            else:
                existing_user = get_user_by_email(email)
                user_name = (
                    existing_user.get("name", "Demo City Explorer")
                    if existing_user and is_existing
                    else name or "Demo City Explorer"
                )
                user = save_user(
                    user_name,
                    email,
                    phone,
                    st.session_state.language,
                    st.session_state.points,
                    daily_alerts=daily_alerts,
                )
                prefs = get_preferences(email)
                st.session_state.logged_in = True
                st.session_state.guest = False
                st.session_state.current_user = user
                st.session_state.points = int(user.get("points", 0))
                st.session_state.preferences = prefs["interests"]
                st.session_state.travel_style = prefs["travel_style"]
                st.session_state.onboarding_done = bool(existing_user or prefs["interests"])
                st.rerun()

        st.markdown(f'<div class="guest-note">{t.get("guest_note", "City Explorer mode lets you explore the prototype without email alerts or saved profile history.")}</div>', unsafe_allow_html=True)
        if st.button(t.get("guest", "Continue as City Explorer"), use_container_width=True, key="guest_login"):
            st.session_state.logged_in = True
            st.session_state.guest = True
            st.session_state.current_user = {"name": "City Explorer", "email": "", "phone": "", "points": 0}
            st.session_state.points = 0
            st.session_state.preferences = []
            st.session_state.travel_style = "Balanced"
            st.session_state.onboarding_done = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    user = st.session_state.current_user or {"name": "City Explorer"}
    if not st.session_state.onboarding_done:
        st.markdown(f'<div class="section-title">{t.get("preferences", "City Preferences")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="premium-card"><p class="muted">{t.get("preferences_intro", "Set your interests so recommendations and itineraries can prioritize what matters to you.")}</p></div>', unsafe_allow_html=True)
        category_options = sorted(locations["category"].dropna().unique().tolist())
        interests = st.multiselect(t.get("preferences", "Preferences"), category_options, default=st.session_state.get("preferences", []))
        style_options = ["Calm and local", "Balanced", "Iconic attractions"]
        current_style = st.session_state.get("travel_style", "Balanced")
        style = st.radio(t.get("travel_style", "Travel style"), style_options, horizontal=True, index=style_options.index(current_style if current_style in style_options else "Balanced"))
        if st.button(t.get("save", "Save"), use_container_width=True):
            st.session_state.preferences = interests
            st.session_state.travel_style = style
            save_preferences((st.session_state.current_user or {}).get("email", ""), interests, style)
            st.session_state.onboarding_done = True
            st.rerun()
    else:
        overcrowded = len(locations[locations["crowd_level"] >= 80])
        calm = len(locations[locations["crowd_level"] < 50])
        st.markdown(
            f"""
            <div class="cityflow-landing">
                {brand_lockup}<br>
                <div class="cityflow-landing-kicker">{t.get("home", "Home Dashboard")}</div>
                <h1>Welcome, {user.get("name", "City Explorer")}.</h1>
                <p>{t.get("dashboard_intro", "Use the sidebar to monitor crowd pressure, generate meaningful routes, report live observations, and manage your impact rewards.")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        a, b, c, d = st.columns(4)
        a.markdown(f'<div class="metric-premium"><div class="metric-number">{len(locations)}</div><div class="metric-label">{t.get("locations", "Locations")}</div></div>', unsafe_allow_html=True)
        b.markdown(f'<div class="metric-premium"><div class="metric-number">{overcrowded}</div><div class="metric-label">{t.get("crowded_zones", "Crowded Zones")}</div></div>', unsafe_allow_html=True)
        c.markdown(f'<div class="metric-premium"><div class="metric-number">{calm}</div><div class="metric-label">{t.get("calm_alternatives", "Calm Alternatives")}</div></div>', unsafe_allow_html=True)
        d.markdown(f'<div class="metric-premium"><div class="metric-number">{st.session_state.points}</div><div class="metric-label">{t.get("points", "Points")}</div></div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="premium-card"><div class="section-title">{t.get("impact_status", "Your Impact Status")}</div>{level_badge(int(st.session_state.points))}<p class="muted">{t.get("preferences", "City Preferences")}: {", ".join(st.session_state.get("preferences", [])) or "not set yet"}.</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="cityflow-journey">
                <div class="cityflow-journey-step"><div class="cityflow-journey-icon">1</div><b>{t.get("journey_1_title", "Avoid pressure")}</b><span>{t.get("journey_1_text", "Start from the places that feel too crowded and understand the risk before going.")}</span></div>
                <div class="cityflow-journey-step"><div class="cityflow-journey-icon">2</div><b>{t.get("journey_2_title", "Discover better places")}</b><span>{t.get("journey_2_text", "Find calmer alternatives that still match your interests and available time.")}</span></div>
                <div class="cityflow-journey-step"><div class="cityflow-journey-icon">3</div><b>{t.get("journey_3_title", "Help the city")}</b><span>{t.get("journey_3_text", "Send live crowd reports so other residents and visitors can make smarter choices.")}</span></div>
                <div class="cityflow-journey-step"><div class="cityflow-journey-icon">4</div><b>{t.get("journey_4_title", "Earn rewards")}</b><span>{t.get("journey_4_text", "Turn positive movement choices into points, profile levels, and local benefits.")}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        link_cols = st.columns(4)
        link_cols[0].page_link("pages/2_City_Pulse_Map.py", label=t.get("open_map", "Open Map"))
        link_cols[1].page_link("pages/4_Itinerary.py", label=t.get("plan_route", "Plan Route"))
        link_cols[2].page_link("pages/6_Report_Crowded_Area.py", label=t.get("report_crowd", "Report Crowd"))
        link_cols[3].page_link("pages/5_Rewards.py", label=t.get("view_rewards", "Rewards"))
