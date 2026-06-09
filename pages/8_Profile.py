import html

import pandas as pd
import streamlit as st

from utils.rewards import badge_from_points
from utils.storage import ensure_data_files, get_preferences, get_user_by_email
from utils.style import apply_style
from utils.translations import language_selector


LEVELS = [
    {"name": "Explorer", "emoji": "🧭", "min": 0, "color": "#FBBF24", "tone": "Start discovering calmer routes."},
    {"name": "Local Supporter", "emoji": "🌿", "min": 100, "color": "#34D399", "tone": "You are helping balance city flows."},
    {"name": "Sustainable Traveler", "emoji": "🚲", "min": 300, "color": "#38BDF8", "tone": "Your trips are becoming smarter and greener."},
    {"name": "CityFlow Ambassador", "emoji": "🏙️", "min": 600, "color": "#A78BFA", "tone": "You guide the city like a pro."},
    {"name": "Urban Hero", "emoji": "🏆", "min": 1000, "color": "#FB7185", "tone": "Top-tier impact across Barcelona."},
]


def safe(value):
    return html.escape(str(value or ""))


def points_to_level(points):
    current = LEVELS[0]
    next_level = None
    for index, level in enumerate(LEVELS):
        if points >= level["min"]:
            current = level
            next_level = LEVELS[index + 1] if index + 1 < len(LEVELS) else None
    if next_level:
        span = next_level["min"] - current["min"]
        progress = min(100, max(0, ((points - current["min"]) / span) * 100))
        remaining = max(0, next_level["min"] - points)
    else:
        progress = 100
        remaining = 0
    return current, next_level, progress, remaining


def stat_card(label, value, detail):
    return (
        '<div class="profile-stat-card">'
        f'<div class="profile-stat-value">{safe(value)}</div>'
        f'<div class="profile-stat-label">{safe(label)}</div>'
        f'<div class="profile-stat-detail">{safe(detail)}</div>'
        '</div>'
    )


def empty_state(message):
    return f'<div class="profile-empty">{safe(message)}</div>'


def clean_activity_table(df, columns):
    if df.empty:
        return df
    visible = [column for column in columns if column in df.columns]
    return df[visible].sort_values("created_at", ascending=False) if "created_at" in visible else df[visible]


st.set_page_config(page_title="Profile", page_icon="profile", layout="wide")
apply_style()
ensure_data_files()
t = language_selector(st)

st.markdown(
    """
    <style>
    .profile-hero {
        display: grid;
        grid-template-columns: 1.2fr 0.8fr;
        gap: 18px;
        align-items: stretch;
        margin-bottom: 18px;
    }

    .profile-level-card {
        padding: 26px;
        border-radius: 8px;
        background:
            linear-gradient(135deg, rgba(2,8,23,0.94), rgba(8,47,73,0.78)),
            radial-gradient(circle at 92% 12%, rgba(52,211,153,0.34), transparent 28%);
        border: 1px solid rgba(103,232,249,0.24);
        box-shadow: 0 20px 55px rgba(0,0,0,0.30);
        color: #EAF7FF;
        min-height: 300px;
    }

    .profile-avatar-row {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 18px;
    }

    .profile-avatar {
        width: 86px;
        height: 86px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 46px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.16);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
    }

    .profile-name {
        font-size: 34px;
        line-height: 1.05;
        font-weight: 900;
        color: #FFFFFF;
        margin-bottom: 8px;
    }

    .profile-level-pill {
        display: inline-flex;
        gap: 8px;
        align-items: center;
        padding: 8px 11px;
        border-radius: 8px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(103,232,249,0.22);
        color: #D9F7FF;
        font-weight: 900;
        font-size: 13px;
    }

    .profile-xp-row {
        display: flex;
        align-items: end;
        justify-content: space-between;
        gap: 12px;
        margin: 18px 0 10px;
    }

    .profile-xp-number {
        font-size: 42px;
        line-height: 1;
        font-weight: 900;
        color: #67E8F9;
    }

    .profile-xp-label {
        color: #B7D4E8;
        font-weight: 800;
        font-size: 13px;
        text-transform: uppercase;
    }

    .profile-progress-shell {
        height: 14px;
        border-radius: 999px;
        overflow: hidden;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.10);
    }

    .profile-progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #22C55E, #38BDF8, #FBBF24);
        box-shadow: 0 0 20px rgba(56,189,248,0.32);
    }

    .profile-level-road {
        padding: 22px;
        border-radius: 8px;
        background: rgba(8,20,38,0.74);
        border: 1px solid rgba(103,232,249,0.20);
        color: #EAF7FF;
    }

    .profile-road-item {
        display: grid;
        grid-template-columns: 42px 1fr auto;
        gap: 12px;
        align-items: center;
        padding: 11px 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    .profile-road-item:last-child { border-bottom: 0; }

    .profile-road-emoji {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.08);
        font-size: 21px;
    }

    .profile-road-name {
        font-weight: 900;
        color: #FFFFFF;
        line-height: 1.1;
    }

    .profile-road-points {
        color: #B7D4E8;
        font-size: 12px;
        font-weight: 800;
    }

    .profile-road-status {
        font-size: 12px;
        font-weight: 900;
        color: #86EFAC;
    }

    .profile-stats-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin: 16px 0 18px;
    }

    .profile-stat-card {
        padding: 18px;
        border-radius: 8px;
        background: rgba(8,20,38,0.72);
        border: 1px solid rgba(103,232,249,0.18);
        box-shadow: 0 14px 36px rgba(0,0,0,0.22);
    }

    .profile-stat-value {
        font-size: 30px;
        line-height: 1;
        font-weight: 900;
        color: #67E8F9;
    }

    .profile-stat-label {
        margin-top: 8px;
        color: #FFFFFF;
        font-weight: 900;
    }

    .profile-stat-detail {
        margin-top: 5px;
        color: #B7D4E8;
        font-size: 13px;
        line-height: 1.35;
    }

    .profile-empty {
        padding: 18px;
        border-radius: 8px;
        background: rgba(251,191,36,0.12);
        border: 1px solid rgba(251,191,36,0.24);
        color: #FDE68A;
        font-weight: 800;
    }

    .profile-summary-line {
        color: #B7D4E8;
        line-height: 1.55;
        margin-top: 12px;
        max-width: 760px;
    }

    @media (max-width: 900px) {
        .profile-hero,
        .profile-stats-grid {
            grid-template-columns: 1fr;
        }

        .profile-name {
            font-size: 28px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

session_user = st.session_state.get("current_user") or {"name": "City Explorer", "email": "", "phone": ""}
email = session_user.get("email", "")
csv_user = get_user_by_email(email) if email else None
user = csv_user or session_user
points = int(user.get("points", st.session_state.get("points", 0)) or 0)
prefs = get_preferences(email)

itineraries = pd.read_csv("data/itineraries.csv")
reports = pd.read_csv("data/reports.csv")
redemptions = pd.read_csv("data/redemptions.csv")

if email:
    my_reports = reports[reports["email"].fillna("").str.lower() == email.lower()]
    my_itineraries = itineraries[itineraries["email"].fillna("").str.lower() == email.lower()]
    my_redemptions = redemptions[redemptions["email"].fillna("").str.lower() == email.lower()]
else:
    my_reports = reports.iloc[0:0].copy()
    my_itineraries = itineraries.iloc[0:0].copy()
    my_redemptions = redemptions.iloc[0:0].copy()

unique_places = my_itineraries["place"].nunique() if "place" in my_itineraries else 0
calm_visits = 0
if not my_itineraries.empty and "crowd_level" in my_itineraries:
    calm_visits = int((pd.to_numeric(my_itineraries["crowd_level"], errors="coerce").fillna(100) < 50).sum())
earned_points = 0
for frame in [my_itineraries, my_reports]:
    if not frame.empty and "points_awarded" in frame:
        earned_points += int(pd.to_numeric(frame["points_awarded"], errors="coerce").fillna(0).sum())

st.session_state.points = points
if csv_user:
    st.session_state.current_user = csv_user

current_level, next_level, progress, remaining = points_to_level(points)
display_badge = badge_from_points(points)

preferences_text = ", ".join(prefs["interests"]) if prefs["interests"] else "Not set yet"
next_text = f"{remaining} XP to {next_level['name']}" if next_level else "Maximum level reached"

st.markdown(f'<div class="section-title">{safe(t.get("profile_title", "City Explorer Profile"))}</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="profile-hero">'
    '<div class="profile-level-card">'
    '<div class="profile-avatar-row">'
    f'<div class="profile-avatar">{current_level["emoji"]}</div>'
    '<div>'
    f'<div class="profile-name">{safe(user.get("name", "City Explorer"))}</div>'
    f'<div class="profile-level-pill">{current_level["emoji"]} Level · {safe(display_badge)}</div>'
    '</div>'
    '</div>'
    f'<div class="profile-summary-line">{safe(current_level["tone"])} Your profile grows when you choose calmer destinations, generate itineraries, report crowds, and redeem local rewards.</div>'
    '<div class="profile-xp-row">'
    '<div>'
    f'<div class="profile-xp-number">{points}</div>'
    '<div class="profile-xp-label">CityFlow XP</div>'
    '</div>'
    f'<div class="profile-level-pill">{safe(next_text)}</div>'
    '</div>'
    '<div class="profile-progress-shell">'
    f'<div class="profile-progress-fill" style="width:{progress:.1f}%"></div>'
    '</div>'
    f'<div class="profile-summary-line">Email: {safe(user.get("email", "") or "City Explorer mode")} · Phone: {safe(user.get("phone", "") or "Not set")} · Travel style: {safe(prefs["travel_style"])}</div>'
    '</div>'
    '<div class="profile-level-road">'
    f'<div style="font-weight:900;font-size:18px;margin-bottom:8px;">{safe(t.get("level_road", "Level Road"))}</div>'
    + "".join(
        '<div class="profile-road-item">'
        f'<div class="profile-road-emoji">{level["emoji"]}</div>'
        '<div>'
        f'<div class="profile-road-name">{safe(level["name"])}</div>'
        f'<div class="profile-road-points">{level["min"]}+ XP</div>'
        '</div>'
        f'<div class="profile-road-status">{"Unlocked" if points >= level["min"] else "Locked"}</div>'
        '</div>'
        for level in LEVELS
    )
    + '</div>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="profile-stats-grid">'
    + stat_card("Places planned", unique_places, "Unique destinations in your itineraries")
    + stat_card("Calm choices", calm_visits, "Stops below 50% crowd pressure")
    + stat_card("Crowd reports", len(my_reports), "Community updates submitted")
    + stat_card("Rewards used", len(my_redemptions), "Marketplace redemptions")
    + '</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1.1, 0.9])
with left:
    st.markdown(
        '<div class="glass-card">'
        f'<h3>{safe(t.get("mission_focus", "Mission Focus"))}</h3>'
        f'<p class="muted"><b>Preferences:</b> {safe(preferences_text)}</p>'
        f'<p class="muted"><b>Total earned through activity:</b> {earned_points} XP</p>'
        '<p class="muted">Best next move: plan one calm route, then report one live crowd update to move faster along the level road.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        '<div class="glass-card">'
        f'<h3>{safe(t.get("badge_collection", "Badge Collection"))}</h3>'
        '<div class="profile-summary-line">'
        + " ".join(
            f'{level["emoji"]} {safe(level["name"])}'
            for level in LEVELS
            if points >= level["min"]
        )
        + '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

tabs = st.tabs([t.get("activity", "Activity"), t.get("itineraries", "Itineraries"), t.get("reports", "Reports"), t.get("redemptions", "Redemptions")])
with tabs[0]:
    recent_items = []
    if not my_itineraries.empty:
        for _, row in my_itineraries.sort_values("created_at", ascending=False).head(4).iterrows():
            recent_items.append(f'🗺️ Planned {safe(row.get("place", ""))} · {safe(row.get("points_awarded", 0))} XP')
    if not my_reports.empty:
        for _, row in my_reports.sort_values("created_at", ascending=False).head(3).iterrows():
            recent_items.append(f'📍 Reported {safe(row.get("location", ""))} · {safe(row.get("points_awarded", 0))} XP')
    if not my_redemptions.empty:
        for _, row in my_redemptions.sort_values("created_at", ascending=False).head(3).iterrows():
            recent_items.append(f'🎁 Redeemed {safe(row.get("reward", ""))}')

    if recent_items:
        st.markdown(
            f'<div class="glass-card"><h3>{safe(t.get("recent_progress", "Recent Progress"))}</h3>'
            + "".join(f'<p class="muted">{item}</p>' for item in recent_items[:8])
            + '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(empty_state(t.get("no_activity", "No activity yet. Generate an itinerary or report a crowd update to start earning XP.")), unsafe_allow_html=True)

with tabs[1]:
    table = clean_activity_table(my_itineraries, ["created_at", "time", "place", "activity", "crowd_level", "area", "points_awarded"])
    if table.empty:
        st.markdown(empty_state(t.get("no_itineraries", "No saved itineraries yet.")), unsafe_allow_html=True)
    else:
        st.dataframe(table, use_container_width=True, hide_index=True)

with tabs[2]:
    table = clean_activity_table(my_reports, ["created_at", "location", "crowd_level", "comment", "points_awarded"])
    if table.empty:
        st.markdown(empty_state(t.get("no_crowd_reports", "No crowd reports yet.")), unsafe_allow_html=True)
    else:
        st.dataframe(table, use_container_width=True, hide_index=True)

with tabs[3]:
    table = clean_activity_table(my_redemptions, ["created_at", "reward", "cost", "status"])
    if table.empty:
        st.markdown(empty_state(t.get("no_redemptions", "No reward redemptions yet.")), unsafe_allow_html=True)
    else:
        st.dataframe(table, use_container_width=True, hide_index=True)

if not email:
    st.info(t.get("guest_activity_note", "City Explorer activity is stored for this session only. Create an account to persist profile activity."))

if st.button(t["logout"]):
    for key in ["logged_in", "guest", "current_user", "onboarding_done"]:
        st.session_state[key] = False if key in ["logged_in", "guest", "onboarding_done"] else None
    st.session_state.points = 0
    st.session_state.preferences = []
    st.rerun()
