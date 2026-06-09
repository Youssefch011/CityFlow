import pandas as pd
import streamlit as st
import html

from utils.image import get_image_base64
from utils.rewards import badge_from_points
from utils.storage import ensure_data_files
from utils.style import apply_style, level_badge
from utils.translations import language_selector


st.set_page_config(page_title="Home", page_icon="home", layout="wide")
apply_style()
ensure_data_files()
t = language_selector(st)


def safe(value):
    return html.escape(str(value or ""))


def report_emoji(level):
    label = str(level or "").lower()
    if "calm" in label:
        return "🌿"
    if "moderate" in label:
        return "🚶"
    if "busy" in label:
        return "⚠️"
    if "crowd" in label:
        return "🔥"
    return "📍"


def initials(name):
    parts = [part for part in str(name or "City Explorer").split() if part]
    if not parts:
        return "CE"
    return "".join(part[0].upper() for part in parts[:2])


def format_report_time(value):
    try:
        dt = pd.to_datetime(value)
        return dt.strftime("%b %d · %H:%M")
    except Exception:
        return "Just now"


def report_card(row):
    name = row.get("name", "City Explorer") or "City Explorer"
    location = row.get("location", "Barcelona")
    crowd = row.get("crowd_level", "Update")
    comment = row.get("comment", "")
    message = comment if str(comment).strip() else f"{location} feels {str(crowd).lower()} right now."
    points = row.get("points_awarded", 0)
    created = format_report_time(row.get("created_at", ""))
    emoji = report_emoji(crowd)
    photo = get_image_base64(row.get("photo_path", ""))
    photo_html = f'<img class="community-report-photo" src="data:image/jpeg;base64,{photo}" alt="Report photo">' if photo else ""
    return (
        '<div class="community-report-card">'
        '<div class="community-avatar-wrap">'
        f'<div class="community-avatar">{safe(initials(name))}</div>'
        f'<div class="community-emoji">{emoji}</div>'
        '</div>'
        '<div class="community-report-body">'
        '<div class="community-report-head">'
        f'<div><b>{safe(name)}</b><span>{safe(location)} · {safe(created)}</span></div>'
        f'<div class="community-points">+{safe(points)} XP</div>'
        '</div>'
        f'<div class="community-bubble">{safe(message)}</div>'
        f'{photo_html}'
        '<div class="community-meta-row">'
        f'<span>{emoji} {safe(crowd)}</span>'
        f'<span>{safe(t.get("community_signal", "Community signal"))}</span>'
        '</div>'
        '</div>'
        '</div>'
    )

locations = pd.read_csv("data/locations.csv")
reports = pd.read_csv("data/reports.csv")
points = int(st.session_state.get("points", 0))
overcrowded = len(locations[locations["crowd_level"] >= 80])
calm = len(locations[locations["crowd_level"] < 50])
barceloneta = locations[locations["name"] == "Barceloneta Beach"].iloc[0]
barceloneta_image = get_image_base64(barceloneta.get("image", ""))
barceloneta_bg = f"data:image/jpeg;base64,{barceloneta_image}" if barceloneta_image else ""
calmest = locations.sort_values("crowd_level").head(3)
highest = locations.sort_values("crowd_level", ascending=False).head(3)

st.markdown(
    """
    <style>
    .home-feature {
        min-height: 360px;
        display: grid;
        grid-template-columns: minmax(0, 1fr) 330px;
        gap: 18px;
        align-items: end;
        padding: 28px;
        margin-bottom: 18px;
        border-radius: 8px;
        overflow: hidden;
        position: relative;
        border: 1px solid rgba(103,232,249,0.24);
        box-shadow: 0 24px 70px rgba(0,0,0,0.34);
        background:
            linear-gradient(90deg, rgba(2,8,23,0.94), rgba(2,8,23,0.68), rgba(2,8,23,0.18)),
            var(--home-beach-image) center/cover no-repeat;
    }

    .home-feature-title {
        color: #FFFFFF;
        font-size: 44px;
        line-height: 1.04;
        font-weight: 900;
        max-width: 740px;
        margin-bottom: 12px;
    }

    .home-feature-quote {
        max-width: 660px;
        color: #D9F7FF;
        font-size: 18px;
        line-height: 1.55;
        font-weight: 700;
    }

    .home-feature-panel {
        padding: 18px;
        border-radius: 8px;
        background: rgba(8,20,38,0.76);
        border: 1px solid rgba(103,232,249,0.22);
        backdrop-filter: blur(14px);
    }

    .home-feature-pressure {
        color: #FFFFFF;
        font-size: 46px;
        line-height: 1;
        font-weight: 900;
    }

    .home-feature-label {
        color: #B7D4E8;
        font-size: 13px;
        font-weight: 800;
        margin-top: 7px;
    }

    .home-pressure-bar {
        height: 10px;
        border-radius: 999px;
        overflow: hidden;
        background: rgba(255,255,255,0.13);
        margin: 13px 0;
    }

    .home-pressure-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #FDBA74, #FB7185);
    }

    .home-feature-tags,
    .home-priority-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 12px;
    }

    .home-feature-tag {
        padding: 8px 10px;
        border-radius: 8px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(103,232,249,0.18);
        color: #D9F7FF;
        font-size: 12px;
        font-weight: 900;
    }

    .home-section-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin: 18px 0;
    }

    .home-insight-card {
        padding: 20px;
        border-radius: 8px;
        background: rgba(8,20,38,0.76);
        border: 1px solid rgba(103,232,249,0.18);
        box-shadow: 0 14px 34px rgba(0,0,0,0.22);
        color: #EAF7FF;
    }

    .home-insight-card h3 {
        margin: 0 0 12px 0;
        color: #FFFFFF;
        font-size: 20px;
    }

    .home-place-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    .home-place-row:last-child {
        border-bottom: 0;
    }

    .home-place-name {
        color: #FFFFFF;
        font-weight: 900;
        line-height: 1.15;
    }

    .home-place-area {
        color: #B7D4E8;
        font-size: 12px;
        margin-top: 4px;
        font-weight: 700;
    }

    .home-place-score {
        white-space: nowrap;
        padding: 7px 9px;
        border-radius: 8px;
        background: rgba(103,232,249,0.10);
        border: 1px solid rgba(103,232,249,0.20);
        color: #67E8F9;
        font-size: 12px;
        font-weight: 900;
    }

    .community-feed {
        display: grid;
        gap: 12px;
        margin-bottom: 18px;
    }

    .home-journey {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin: 16px 0 20px;
    }

    .home-journey-step {
        padding: 18px;
        border-radius: 8px;
        background: rgba(8,20,38,0.76);
        border: 1px solid rgba(103,232,249,0.18);
        box-shadow: 0 14px 34px rgba(0,0,0,0.22);
        color: #EAF7FF;
        min-height: 150px;
    }

    .home-journey-number {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(103,232,249,0.12);
        border: 1px solid rgba(103,232,249,0.22);
        color: #67E8F9;
        font-weight: 900;
        margin-bottom: 10px;
    }

    .home-journey-step b {
        display: block;
        color: #FFFFFF;
        font-size: 16px;
        margin-bottom: 7px;
    }

    .home-journey-step span {
        color: #B7D4E8;
        font-size: 13px;
        line-height: 1.45;
    }

    .community-report-card {
        display: grid;
        grid-template-columns: 54px 1fr;
        gap: 13px;
        align-items: start;
        padding: 16px;
        border-radius: 8px;
        background: rgba(8,20,38,0.76);
        border: 1px solid rgba(103,232,249,0.18);
        box-shadow: 0 14px 36px rgba(0,0,0,0.24);
        color: #EAF7FF;
    }

    .community-avatar-wrap {
        position: relative;
        width: 48px;
        height: 48px;
    }

    .community-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #0EA5E9, #14B8A6);
        color: #FFFFFF;
        font-weight: 900;
        font-size: 15px;
        border: 1px solid rgba(255,255,255,0.20);
        box-shadow: 0 10px 28px rgba(14,165,233,0.22);
    }

    .community-emoji {
        position: absolute;
        right: -4px;
        bottom: -4px;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #071E3D;
        border: 1px solid rgba(103,232,249,0.22);
        font-size: 13px;
    }

    .community-report-head {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 8px;
    }

    .community-report-head b {
        display: block;
        color: #FFFFFF;
        font-size: 15px;
        line-height: 1.1;
    }

    .community-report-head span {
        display: block;
        color: #B7D4E8;
        font-size: 12px;
        margin-top: 4px;
        font-weight: 700;
    }

    .community-points {
        white-space: nowrap;
        padding: 6px 8px;
        border-radius: 8px;
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.24);
        color: #BBF7D0;
        font-size: 12px;
        font-weight: 900;
    }

    .community-bubble {
        position: relative;
        display: inline-block;
        max-width: min(720px, 100%);
        padding: 12px 15px;
        border-radius: 18px 18px 18px 5px;
        background: linear-gradient(135deg, #34C759, #20D67D);
        color: #FFFFFF;
        font-weight: 800;
        line-height: 1.45;
        box-shadow: 0 12px 28px rgba(34,197,94,0.20);
    }

    .community-bubble:before {
        content: "";
        position: absolute;
        left: -6px;
        bottom: 0;
        width: 14px;
        height: 14px;
        background: #34C759;
        border-bottom-right-radius: 12px;
        clip-path: polygon(100% 0, 0 100%, 100% 100%);
    }

    .community-report-photo {
        width: 100%;
        max-height: 190px;
        object-fit: cover;
        display: block;
        margin: 8px 0 4px;
        border-radius: 14px;
        border: 1px solid rgba(187,247,208,0.20);
        box-shadow: 0 12px 28px rgba(0,0,0,0.22);
    }

    .community-meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 9px;
    }

    .community-meta-row span {
        padding: 6px 8px;
        border-radius: 8px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(103,232,249,0.14);
        color: #D9F7FF;
        font-size: 12px;
        font-weight: 800;
    }

    @media (max-width: 720px) {
        .home-feature,
        .home-section-grid {
            grid-template-columns: 1fr;
        }

        .home-feature-title {
            font-size: 32px;
        }

        .home-journey {
            grid-template-columns: 1fr;
        }

        .community-report-card {
            grid-template-columns: 44px 1fr;
            padding: 13px;
        }

        .community-avatar,
        .community-avatar-wrap {
            width: 42px;
            height: 42px;
        }

        .community-report-head {
            flex-direction: column;
            gap: 6px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="home-feature" style="--home-beach-image:url('{barceloneta_bg}');">
        <div>
            <div class="home-feature-title">{safe(t.get("home_quote_title", "Barcelona feels better when the city can breathe."))}</div>
            <div class="home-feature-quote">{safe(t.get("home_quote", '"Choose the calmer move, keep the experience beautiful, and leave space for everyone else."'))}</div>
            <div class="home-feature-tags">
                <span class="home-feature-tag">{safe(t.get("avoid_pressure", "Avoid pressure"))}</span>
                <span class="home-feature-tag">{safe(t.get("discover_alternatives", "Discover alternatives"))}</span>
                <span class="home-feature-tag">{safe(t.get("report_live", "Report live"))}</span>
                <span class="home-feature-tag">{safe(t.get("earn_impact", "Earn impact"))}</span>
            </div>
        </div>
        <div class="home-feature-panel">
            <div class="home-feature-pressure">{int(barceloneta["crowd_level"])}%</div>
            <div class="home-feature-label">{safe(t.get("barceloneta_pressure", "Barceloneta Beach crowd pressure"))}</div>
            <div class="home-pressure-bar"><div class="home-pressure-fill" style="width:{int(barceloneta["crowd_level"])}%;"></div></div>
            <p class="muted">{safe(t.get("barceloneta_note", "A beautiful place, but often a pressure point. CityFlow helps users find nearby calmer choices before the visit becomes frustrating."))}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
a, b, c, d = st.columns(4)
a.markdown(f'<div class="metric-premium"><div class="metric-number">{overcrowded}</div><div class="metric-label">{safe(t.get("crowded_zones", "Crowded Zones"))}</div></div>', unsafe_allow_html=True)
b.markdown(f'<div class="metric-premium"><div class="metric-number">{calm}</div><div class="metric-label">{safe(t.get("calm_alternatives", "Calm Alternatives"))}</div></div>', unsafe_allow_html=True)
c.markdown(f'<div class="metric-premium"><div class="metric-number">{points}</div><div class="metric-label">{t.get("points", "Points")}</div></div>', unsafe_allow_html=True)
d.markdown(f'<div class="metric-premium"><div class="metric-number">{len(reports)}</div><div class="metric-label">{safe(t.get("community_reports", "Community Reports"))}</div></div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="premium-card"><div class="section-title">{safe(t.get("impact_status", "Your Impact Status"))}</div>{level_badge(points)}'
    f'<p class="muted">{safe(t.get("current_badge", "Current badge"))}: <b>{badge_from_points(points)}</b>. {safe(t.get("impact_status_text", "Earn points by reporting crowded areas, choosing low-crowd itineraries, using public transport, and supporting local neighborhoods."))}</p></div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="section-title">{safe(t.get("how_cityflow_helps", "How CityFlow Helps"))}</div>
    <div class="home-journey">
        <div class="home-journey-step"><div class="home-journey-number">1</div><b>{safe(t.get("journey_1_title", "Avoid pressure"))}</b><span>{safe(t.get("journey_1_text", "Start from the places that feel too crowded and understand the risk before going."))}</span></div>
        <div class="home-journey-step"><div class="home-journey-number">2</div><b>{safe(t.get("journey_2_title", "Discover better places"))}</b><span>{safe(t.get("journey_2_text", "Find calmer alternatives that still match your interests and available time."))}</span></div>
        <div class="home-journey-step"><div class="home-journey-number">3</div><b>{safe(t.get("journey_3_title", "Help the city"))}</b><span>{safe(t.get("journey_3_text", "Send live crowd reports so other residents and visitors can make smarter choices."))}</span></div>
        <div class="home-journey-step"><div class="home-journey-number">4</div><b>{safe(t.get("journey_4_title", "Earn rewards"))}</b><span>{safe(t.get("journey_4_text", "Turn positive movement choices into points, profile levels, and local benefits."))}</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)
action_cols = st.columns(4)
action_cols[0].page_link("pages/2_City_Pulse_Map.py", label=t.get("open_map", "Open Map"))
action_cols[1].page_link("pages/4_Itinerary.py", label=t.get("plan_route", "Plan Route"))
action_cols[2].page_link("pages/6_Report_Crowded_Area.py", label=t.get("report_crowd", "Report Crowd"))
action_cols[3].page_link("pages/5_Rewards.py", label=t.get("view_rewards", "Rewards"))

def place_rows(frame, calm_mode):
    rows = []
    for _, item in frame.iterrows():
        label = "calm" if calm_mode else "pressure"
        rows.append(
            '<div class="home-place-row">'
            '<div>'
            f'<div class="home-place-name">{safe(item["name"])}</div>'
            f'<div class="home-place-area">{safe(item["area"])} · {safe(item["category"])}</div>'
            '</div>'
            f'<div class="home-place-score">{int(item["crowd_level"])}% {label}</div>'
            '</div>'
        )
    return "".join(rows)


st.markdown(
    '<div class="home-section-grid">'
    f'<div class="home-insight-card"><h3>{safe(t.get("best_calm_moves", "Best Calm Moves Now"))}</h3>'
    + place_rows(calmest, True)
    + '</div>'
    f'<div class="home-insight-card"><h3>{safe(t.get("pressure_points", "Pressure Points To Reroute"))}</h3>'
    + place_rows(highest, False)
    + '</div>'
    '</div>',
    unsafe_allow_html=True,
)

if not reports.empty:
    st.markdown(f'<div class="section-title">{safe(t.get("latest_reports", "Latest Community Reports"))}</div>', unsafe_allow_html=True)
    latest_reports = reports.tail(5).iloc[::-1]
    st.markdown(
        '<div class="community-feed">'
        + "".join(report_card(row) for _, row in latest_reports.iterrows())
        + '</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    f'<div class="premium-card"><div class="section-title">{safe(t.get("cityflow_concept", "CityFlow Concept"))}</div>'
    f'<p class="muted">{safe(t.get("cityflow_concept_text", "The platform transforms city movement from consumption-based navigation into impact-based exploration. Residents and visitors receive daily alerts, contribute crowd reports, avoid saturated spaces, and unlock sustainable rewards."))}</p></div>',
    unsafe_allow_html=True,
)
