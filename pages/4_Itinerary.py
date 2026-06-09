import html

import pandas as pd
import streamlit as st

from utils.image import get_image_base64
from utils.itinerary_generator import generate_itinerary
from utils.maps import directions_maps_url, place_maps_url
from utils.rewards import badge_from_points, calculate_points
from utils.storage import ensure_data_files, save_itinerary, update_user_points
from utils.style import apply_style
from utils.translations import language_selector


def safe(value):
    return html.escape(str(value or ""))


def pressure_color(level):
    if level >= 80:
        return "#FF5B7A"
    if level >= 60:
        return "#FFB057"
    if level >= 40:
        return "#42D5FF"
    return "#5DF2A5"


def pressure_label(level):
    if level >= 80:
        return "High"
    if level >= 60:
        return "Busy"
    if level >= 40:
        return "Balanced"
    return "Calm"


def kpi_card(label, value, detail):
    return (
        '<div class="route-kpi">'
        f'<div class="route-kpi-value">{safe(value)}</div>'
        f'<div class="route-kpi-label">{safe(label)}</div>'
        f'<div class="route-kpi-detail">{safe(detail)}</div>'
        '</div>'
    )


def route_node(index, item):
    color = pressure_color(item["projected_crowd"])
    return (
        '<div class="route-node">'
        f'<div class="route-node-index" style="border-color:{color};">{index}</div>'
        '<div>'
        f'<div class="route-node-name">{safe(item["place"])}</div>'
        f'<div class="route-node-meta">{int(item["projected_crowd"])}% pressure · {safe(item["time"])}</div>'
        '</div>'
        '</div>'
    )


st.set_page_config(page_title="Smart Route Advisor", page_icon="itinerary", layout="wide")
apply_style()
ensure_data_files()
t = language_selector(st)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1320px;
    }

    .route-hero {
        min-height: 360px;
        border-radius: 8px;
        overflow: hidden;
        position: relative;
        border: 1px solid rgba(103,232,249,0.24);
        box-shadow: 0 26px 80px rgba(0,0,0,0.36);
        margin-bottom: 18px;
        background:
            linear-gradient(90deg, rgba(2,8,23,0.96) 0%, rgba(2,8,23,0.82) 46%, rgba(2,8,23,0.24) 100%),
            var(--route-hero-image) center/cover no-repeat;
    }

    .route-hero-inner {
        position: relative;
        z-index: 1;
        padding: 34px;
        max-width: 780px;
    }

    .route-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 10px;
        border-radius: 8px;
        background: rgba(103,232,249,0.11);
        border: 1px solid rgba(103,232,249,0.24);
        color: #67E8F9;
        font-size: 12px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 18px;
    }

    .route-title {
        color: #FFFFFF;
        font-size: 56px;
        line-height: 1.02;
        font-weight: 900;
        letter-spacing: 0;
        margin: 0;
    }

    .route-subtitle {
        color: #D9F7FF;
        font-size: 17px;
        line-height: 1.55;
        margin-top: 16px;
        max-width: 680px;
    }

    .route-command-shell {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 340px;
        gap: 16px;
        align-items: stretch;
        margin-bottom: 18px;
    }

    .route-panel,
    .route-pressure-panel,
    .route-cockpit,
    .route-brief {
        border-radius: 8px;
        background: rgba(8,20,38,0.78);
        border: 1px solid rgba(103,232,249,0.20);
        box-shadow: 0 18px 48px rgba(0,0,0,0.28);
        color: #EAF7FF;
    }

    .route-panel {
        padding: 22px;
    }

    .route-pressure-panel {
        padding: 22px;
        background:
            linear-gradient(180deg, rgba(8,20,38,0.84), rgba(15,23,42,0.88)),
            radial-gradient(circle at 80% 18%, rgba(251,191,36,0.18), transparent 32%);
    }

    .route-panel-title {
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 900;
        margin-bottom: 12px;
    }

    .pressure-big {
        font-size: 62px;
        line-height: 1;
        font-weight: 900;
        color: #FFFFFF;
        margin: 6px 0 8px;
    }

    .pressure-bar {
        height: 11px;
        border-radius: 999px;
        background: rgba(255,255,255,0.10);
        overflow: hidden;
        margin: 12px 0;
    }

    .pressure-fill {
        height: 100%;
        border-radius: 999px;
    }

    .route-tag-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 12px;
    }

    .route-tag {
        padding: 8px 10px;
        border-radius: 8px;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(103,232,249,0.16);
        color: #D9F7FF;
        font-size: 12px;
        font-weight: 800;
        text-decoration: none;
    }

    .route-cockpit {
        padding: 24px;
        margin-bottom: 18px;
    }

    .route-cockpit-grid {
        display: grid;
        grid-template-columns: 220px 1fr;
        gap: 22px;
        align-items: stretch;
    }

    .route-score-card {
        min-height: 206px;
        border-radius: 8px;
        padding: 22px;
        background:
            linear-gradient(135deg, rgba(14,165,233,0.20), rgba(34,197,94,0.12)),
            rgba(255,255,255,0.05);
        border: 1px solid rgba(103,232,249,0.22);
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }

    .route-score-number {
        font-size: 64px;
        line-height: 0.95;
        font-weight: 900;
        color: #FFFFFF;
    }

    .route-score-label {
        color: #67E8F9;
        font-weight: 900;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 0.5px;
        margin-top: 10px;
    }

    .route-kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
    }

    .route-kpi {
        border-radius: 8px;
        padding: 17px;
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(103,232,249,0.15);
        min-height: 100px;
    }

    .route-kpi-value {
        color: #67E8F9;
        font-size: 29px;
        line-height: 1;
        font-weight: 900;
    }

    .route-kpi-label {
        color: #FFFFFF;
        font-weight: 900;
        margin-top: 9px;
    }

    .route-kpi-detail {
        color: #B7D4E8;
        font-size: 13px;
        line-height: 1.35;
        margin-top: 5px;
    }

    .route-brief {
        padding: 21px;
        margin-bottom: 18px;
    }

    .route-brief h3,
    .route-panel-title h3 {
        margin-top: 0;
    }

    .route-strip {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin-bottom: 18px;
    }

    .route-node {
        display: grid;
        grid-template-columns: 42px 1fr;
        gap: 12px;
        align-items: center;
        padding: 14px;
        border-radius: 8px;
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(103,232,249,0.15);
    }

    .route-node-index {
        width: 38px;
        height: 38px;
        border-radius: 8px;
        border: 2px solid #67E8F9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        color: #FFFFFF;
        background: rgba(2,8,23,0.72);
    }

    .route-node-name {
        color: #FFFFFF;
        font-weight: 900;
        line-height: 1.12;
    }

    .route-node-meta {
        color: #B7D4E8;
        font-size: 12px;
        margin-top: 4px;
        font-weight: 700;
    }

    .itinerary-card {
        display: grid;
        grid-template-columns: 280px 1fr 210px;
        gap: 18px;
        padding: 16px;
        border-radius: 8px;
        background: rgba(8,20,38,0.82);
        border: 1px solid rgba(103,232,249,0.20);
        box-shadow: 0 18px 45px rgba(0,0,0,0.28);
        margin-bottom: 16px;
        color: #EAF7FF;
    }

    .itinerary-card img {
        width: 280px;
        height: 220px;
        border-radius: 8px;
        object-fit: cover;
        display: block;
    }

    .stop-kicker {
        color: #67E8F9;
        font-size: 12px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stop-title {
        color: #FFFFFF;
        font-size: 27px;
        font-weight: 900;
        line-height: 1.08;
        margin: 7px 0 10px;
    }

    .stop-copy {
        color: #B7D4E8;
        font-size: 14px;
        line-height: 1.5;
        margin: 8px 0;
    }

    .stop-side {
        border-radius: 8px;
        padding: 15px;
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(103,232,249,0.15);
    }

    .stop-pressure-value {
        font-size: 42px;
        line-height: 1;
        font-weight: 900;
        color: #FFFFFF;
    }

    .swap-list {
        display: grid;
        gap: 8px;
        margin-top: 10px;
    }

    .swap-chip {
        padding: 9px;
        border-radius: 8px;
        background: rgba(34,197,94,0.10);
        border: 1px solid rgba(34,197,94,0.20);
        color: #BBF7D0;
        font-size: 12px;
        font-weight: 800;
    }

    .decision-note {
        margin: 11px 0;
        padding: 11px 12px;
        border-radius: 8px;
        background: rgba(93,242,165,0.09);
        border: 1px solid rgba(93,242,165,0.20);
        color: #DFFFEA;
        font-size: 13px;
        line-height: 1.45;
        font-weight: 800;
    }

    .confidence-mini {
        margin-top: 10px;
        padding: 10px;
        border-radius: 8px;
        background: rgba(103,232,249,0.08);
        border: 1px solid rgba(103,232,249,0.16);
        color: #D9F7FF;
        font-size: 12px;
        font-weight: 900;
    }

    @media (max-width: 1050px) {
        .route-command-shell,
        .route-cockpit-grid,
        .itinerary-card {
            grid-template-columns: 1fr;
        }

        .route-kpi-grid,
        .route-strip {
            grid-template-columns: 1fr;
        }

        .itinerary-card img {
            width: 100%;
            height: 240px;
        }

        .route-title {
            font-size: 38px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

locations = pd.read_csv("data/locations.csv")
category_options = sorted(locations["category"].dropna().unique().tolist())
saved_preferences = st.session_state.get("preferences", [])
crowded_default = locations.sort_values("crowd_level", ascending=False)["name"].iloc[0]
default_row = locations[locations["name"] == crowded_default].iloc[0]
hero_image = get_image_base64(default_row.get("image", ""))
hero_bg = f"data:image/jpeg;base64,{hero_image}" if hero_image else ""

st.markdown(
    f"""
    <div class="route-hero" style="--route-hero-image:url('{hero_bg}');">
        <div class="route-hero-inner">
            <div class="route-eyebrow">{safe(t.get("route_eyebrow", "CityFlow Route Intelligence"))}</div>
            <h1 class="route-title">{safe(t.get("route_title", "Plan the better move."))}</h1>
            <div class="route-subtitle">
                {safe(t.get("route_subtitle", "A premium route advisor for residents and visitors: avoid the pressure point, keep the experience meaningful, and understand the city impact before you move."))}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="route-command-shell">', unsafe_allow_html=True)
left_col, right_col = st.columns([1, 0.43])
with left_col:
    st.markdown(f'<div class="route-panel-title">{safe(t.get("route_command", "Route Command"))}</div>', unsafe_allow_html=True)
    control_cols = st.columns([1.2, 0.65, 0.65])
    with control_cols[0]:
        selected = st.selectbox(
            t.get("planned_destination", "Planned destination"),
            locations["name"].tolist(),
            index=locations["name"].tolist().index(crowded_default),
        )
    with control_cols[1]:
        start_hour = st.slider(t.get("start", "Start"), 8, 20, 10)
    with control_cols[2]:
        duration_hours = st.slider(t.get("hours", "Hours"), 2, 8, 4)

    strategy_cols = st.columns([1, 0.8, 0.9])
    with strategy_cols[0]:
        focus = st.selectbox(
            t.get("goal", "Goal"),
            [
                "Avoid queues",
                "Smart balanced",
                "Local discovery",
                "Culture and architecture",
                "Beach reset",
                "Family friendly",
                "Iconic Barcelona",
            ],
        )
    with strategy_cols[1]:
        pace = st.selectbox(t.get("pace", "Pace"), ["Balanced", "Relaxed", "Fast"])
    with strategy_cols[2]:
        transport = st.checkbox(t.get("walk_transit", "Walk / transit first"), value=True)

    interests = st.multiselect(
        t.get("keep_interests", "Keep these interests"),
        category_options,
        default=[item for item in saved_preferences if item in category_options],
    )
    avoid_overcrowded = st.toggle(t.get("avoid_80", "Avoid stops above 80% pressure"), value=True)

with right_col:
    selected_row = locations[locations["name"] == selected].iloc[0]
    selected_pressure = int(selected_row["crowd_level"])
    selected_color = pressure_color(selected_pressure)
    st.markdown(
        f"""
        <div class="route-pressure-panel">
            <div class="route-panel-title">{safe(t.get("live_pressure_preview", "Live Pressure Preview"))}</div>
            <div class="pressure-big">{selected_pressure}%</div>
            <div class="muted">{safe(selected)} is currently marked as {safe(pressure_label(selected_pressure).lower())} pressure.</div>
            <div class="pressure-bar"><div class="pressure-fill" style="width:{selected_pressure}%;background:{selected_color};"></div></div>
            <div class="route-tag-row">
                <span class="route-tag">{safe(selected_row["area"])}</span>
                <span class="route-tag">{safe(selected_row["category"])}</span>
                <span class="route-tag">Goal: {safe(focus)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown('</div>', unsafe_allow_html=True)

generate = st.button(t.get("build_premium_route", "Build Premium Route"), use_container_width=True)

if generate:
    itinerary, insights = generate_itinerary(
        locations,
        selected,
        interests=interests,
        start_hour=start_hour,
        duration_hours=duration_hours,
        pace=pace,
        focus=focus,
        avoid_overcrowded=avoid_overcrowded,
        transport=transport,
    )

    if not itinerary:
        st.warning(t.get("no_route", "No route could be generated with these filters. Try a longer window or a different goal."))
        st.stop()

    total = 0
    points_by_place = {}

    st.markdown(
        '<div class="route-cockpit">'
        '<div class="route-cockpit-grid">'
        '<div class="route-score-card">'
        f'<div class="route-score-number">{insights["impact_score"]}</div>'
        f'<div class="route-score-label">{safe(t.get("impact_score", "Impact Score"))}</div>'
        '</div>'
        '<div>'
        '<div class="route-kpi-grid">'
        + kpi_card(t.get("crowd_avoided", "Crowd Avoided"), f'-{insights["pressure_reduction"]}%', f'Compared with {safe(selected)}')
        + kpi_card(t.get("average_pressure", "Average Pressure"), f'{insights["avg_crowd"]}%', f'Busiest stop: {safe(insights["busiest_stop"])}')
        + kpi_card(t.get("movement_cost", "Movement Cost"), f'{insights["total_travel"]} min', f'{insights["total_distance"]} km route distance')
        + '</div>'
        '<div class="route-strip">'
        + "".join(route_node(index, item) for index, item in enumerate(itinerary, start=1))
        + '</div>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    avoided_text = ", ".join(insights["avoided_hotspots"]) if insights.get("avoided_hotspots") else "none"
    st.markdown(
        f"""
        <div class="route-brief">
            <h3>{safe(t.get("route_decision_brief", "Route Decision Brief"))}</h3>
            <p class="muted">{safe(insights["summary"])}</p>
            <p class="muted"><b>{safe(t.get("why_cityflow_changed_route", "Why CityFlow changed the route"))}:</b> {safe(insights.get("smart_explanation", ""))}</p>
            <p class="muted"><b>{safe(t.get("hotspots_monitored", "Hotspots monitored"))}:</b> {safe(avoided_text)}.</p>
            <p class="muted"><b>{safe(t.get("city_benefit", "City benefit"))}:</b> movement is redirected toward lower-pressure areas without stripping the route of useful Barcelona context.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    start_row = locations[locations["name"] == selected].iloc[0]
    maps_route_url = directions_maps_url(selected, start_row["lat"], start_row["lon"], itinerary)
    st.link_button(t.get("open_google_route", "Open Full Route in Google Maps"), maps_route_url, use_container_width=True)

    for index, item in enumerate(itinerary, start=1):
        earned = calculate_points(item["projected_crowd"], transport)
        points_by_place[item["place"]] = earned
        total += earned
        row = locations[locations["name"] == item["place"]].iloc[0]
        img = get_image_base64(row.get("image", ""))
        image_html = f'<img src="data:image/jpeg;base64,{img}" alt="{safe(item["place"])}">' if img else ""
        maps_url = place_maps_url(item["place"], item["lat"], item["lon"])
        color = pressure_color(item["projected_crowd"])
        alternatives_html = "".join(
            f'<div class="swap-chip">{safe(alt["name"])} - {int(alt["crowd_level"])}%</div>'
            for alt in item.get("alternatives", [])
        )
        if not alternatives_html:
            alternatives_html = '<div class="swap-chip">No better nearby swap found</div>'

        st.markdown(
            f"""
            <div class="itinerary-card">
                {image_html}
                <div>
                    <div class="stop-kicker">{safe(t.get("stop", "Stop"))} {index} · {safe(item["time"])}</div>
                    <div class="stop-title">{safe(item["place"])}</div>
                    <p class="stop-copy"><b>{safe(t.get("why_belongs", "Why it belongs"))}:</b> {safe(item["reason"])}</p>
                    <div class="decision-note">{safe(item.get("decision_note", ""))}</div>
                    <p class="stop-copy"><b>{safe(t.get("local_move", "Local move"))}:</b> {safe(item["local_tip"])}</p>
                    <p class="stop-copy"><b>{safe(t.get("best_window", "Best window"))}:</b> {safe(item["best_time"])}</p>
                    <div class="route-tag-row">
                        <span class="route-tag">Area: {safe(item["area"])}</span>
                        <span class="route-tag">Type: {safe(item["category"])}</span>
                        <span class="route-tag">Travel: {int(item["travel_minutes"])} min</span>
                        <span class="route-tag">Impact: +{earned}</span>
                        <a class="route-tag" href="{maps_url}" target="_blank" rel="noopener noreferrer">{safe(t.get("google_maps", "Google Maps"))}</a>
                    </div>
                </div>
                <div class="stop-side">
                    <div class="stop-kicker">{safe(t.get("expected_pressure", "Expected pressure"))}</div>
                    <div class="stop-pressure-value">{int(item["projected_crowd"])}%</div>
                    <div class="pressure-bar"><div class="pressure-fill" style="width:{int(item["projected_crowd"])}%;background:{color};"></div></div>
                    <p class="stop-copy">{safe(item["crowd_label"]).title()}</p>
                    <div class="confidence-mini">Decision confidence: {int(item.get("confidence", 72))}%</div>
                    <div class="stop-kicker" style="margin-top:14px;">{safe(t.get("smart_swaps", "Smart swaps"))}</div>
                    <div class="swap-list">{alternatives_html}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.session_state.points = int(st.session_state.get("points", 0)) + total
    email = (st.session_state.get("current_user") or {}).get("email", "")
    save_itinerary(email, itinerary, points_by_place)
    update_user_points(email, st.session_state.points)
    if st.session_state.get("current_user"):
        st.session_state.current_user["points"] = st.session_state.points
        st.session_state.current_user["badge"] = badge_from_points(st.session_state.points)

    st.success(f"+{total} {t['points']} {t.get('route_points_success', 'added for choosing a lower-pressure route.')}")
    st.info(f"{t['badge']}: {badge_from_points(st.session_state.points)}")
