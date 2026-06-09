import streamlit as st
import pandas as pd
from html import escape

from utils.style import apply_style, status_badge
from utils.translations import language_selector
from utils.recommendation_engine import recommend_alternatives, sustainability_score
from utils.image import get_image_base64, get_missing_images


st.set_page_config(page_title="Recommendations", page_icon="*", layout="wide")
apply_style()
t = language_selector(st)

st.markdown(
    """
    <style>
    .cityflow-recommendation-toolbar {
        margin: 6px 0 18px 0;
    }

    .cityflow-image-card {
        height: 100%;
        overflow: hidden;
        border-radius: 8px;
        background:
            linear-gradient(180deg, rgba(15,23,42,0.88), rgba(8,20,38,0.92)),
            radial-gradient(circle at 85% 8%, rgba(20,184,166,0.16), transparent 32%);
        border: 1px solid rgba(103,232,249,0.22);
        box-shadow: 0 18px 45px rgba(0,0,0,0.28);
        margin-bottom: 22px;
        color: #EAF7FF;
        transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
    }

    .cityflow-image-card:hover {
        transform: translateY(-3px);
        border-color: rgba(103,232,249,0.48);
        box-shadow: 0 0 38px rgba(14,165,233,0.22), 0 22px 55px rgba(0,0,0,0.34);
    }

    .cityflow-featured-card {
        display: grid;
        grid-template-columns: minmax(320px, 1.05fr) minmax(320px, 0.95fr);
        align-items: stretch;
        min-height: 330px;
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

    .cityflow-featured-card .cityflow-card-image-wrap,
    .cityflow-featured-card .cityflow-card-image {
        height: 100%;
        min-height: 330px;
    }

    .cityflow-card-overlay {
        position: absolute;
        inset: 0;
        background:
            linear-gradient(180deg, rgba(2,8,23,0.02) 0%, rgba(2,8,23,0.78) 100%),
            linear-gradient(90deg, rgba(2,8,23,0.28), transparent 52%);
    }

    .cityflow-card-category,
    .cityflow-crowd-chip {
        position: absolute;
        padding: 8px 12px;
        border-radius: 8px;
        background: rgba(2,8,23,0.68);
        border: 1px solid rgba(103,232,249,0.26);
        color: #D9F7FF;
        font-size: 12px;
        font-weight: 900;
        backdrop-filter: blur(12px);
    }

    .cityflow-card-category {
        top: 14px;
        left: 14px;
    }

    .cityflow-crowd-chip {
        right: 14px;
        bottom: 14px;
        color: #FFFFFF;
    }

    .cityflow-card-content {
        display: flex;
        min-height: 265px;
        flex-direction: column;
        padding: 20px;
    }

    .cityflow-featured-card .cityflow-card-content {
        justify-content: center;
        padding: 28px;
    }

    .cityflow-card-heading {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 14px;
    }

    .cityflow-card-title {
        font-size: 25px;
        line-height: 1.15;
        font-weight: 900;
        color: #FFFFFF;
        margin-bottom: 10px;
        letter-spacing: 0;
    }

    .cityflow-featured-card .cityflow-card-title {
        font-size: 34px;
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
        margin-top: auto;
        font-size: 13px;
        color: #D9F7FF;
    }

    .cityflow-meta-pill {
        padding: 7px 10px;
        border-radius: 8px;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(103,232,249,0.16);
        font-weight: 800;
    }

    .cityflow-score-box {
        min-width: 72px;
        padding: 10px 12px;
        border-radius: 8px;
        background: linear-gradient(135deg, rgba(14,165,233,0.22), rgba(34,197,94,0.16));
        border: 1px solid rgba(103,232,249,0.24);
        text-align: center;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
    }

    .cityflow-score-box span {
        display: block;
        color: #FFFFFF;
        font-size: 24px;
        line-height: 1;
        font-weight: 900;
    }

    .cityflow-score-box small {
        display: block;
        margin-top: 4px;
        color: #B7D4E8;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
    }

    .cityflow-reason-row {
        display: grid;
        grid-template-columns: 1fr;
        gap: 6px;
        padding: 12px;
        border-radius: 8px;
        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(52,211,153,0.18);
        color: #CFFAE5;
        font-size: 13px;
        font-weight: 800;
        margin: 0 0 14px 0;
    }

    .cityflow-panel-label {
        margin: 8px 0 10px 0;
        color: #67E8F9;
        font-size: 12px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.6px;
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
        text-align: center;
        padding: 20px;
    }

    @media (max-width: 900px) {
        .cityflow-featured-card {
            display: block;
            min-height: 0;
        }

        .cityflow-featured-card .cityflow-card-image-wrap,
        .cityflow-featured-card .cityflow-card-image {
            height: 245px;
            min-height: 245px;
        }

        .cityflow-featured-card .cityflow-card-title {
            font-size: 28px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="section-title">{escape(t.get("recommendations", "AI-Assisted Recommendations"))}</div>',
    unsafe_allow_html=True,
)
st.caption(t.get("recommendations_caption", "Choose a crowded place and CityFlow recommends smarter, calmer alternatives."))

locations = pd.read_csv("data/locations.csv")

st.markdown('<div class="cityflow-recommendation-toolbar">', unsafe_allow_html=True)
control_cols = st.columns([1.35, 1, 1])
with control_cols[0]:
    selected = st.selectbox(t.get("select_place", "Select place"), locations["name"].tolist())
with control_cols[1]:
    max_crowd = st.slider(t.get("max_crowd_alternatives", "Maximum crowd for alternatives"), 20, 95, 70, 5)
with control_cols[2]:
    category_options = sorted(locations["category"].dropna().unique().tolist())
    preferred_categories = st.multiselect(t.get("preferred_categories", "Preferred categories"), category_options)
st.markdown("</div>", unsafe_allow_html=True)

if preferred_categories:
    st.session_state.preferences = preferred_categories

selected_row = locations[locations["name"] == selected].iloc[0]


def crowd_label(level):
    if level >= 80:
        return "Avoid peak hours"
    if level >= 60:
        return "Plan with care"
    if level >= 40:
        return "Balanced option"
    return "Low-crowd pick"


def build_image_card(row, featured=False):
    img_b64 = get_image_base64(row.get("image", ""))
    crowd_level = int(row["crowd_level"])
    sustainability = sustainability_score(crowd_level)
    title = escape(str(row["name"]))
    category = escape(str(row.get("category", "Destination")))
    area = escape(str(row.get("area", "")))
    description = escape(str(row.get("description", "")))
    card_classes = "cityflow-image-card cityflow-featured-card" if featured else "cityflow-image-card"

    if img_b64:
        image_html = (
            '<div class="cityflow-card-image-wrap">'
            f'<img src="data:image/jpeg;base64,{img_b64}" class="cityflow-card-image" alt="{title}">'
            '<div class="cityflow-card-overlay"></div>'
            f'<div class="cityflow-card-category">{category}</div>'
            f'<div class="cityflow-crowd-chip">{crowd_level}% crowd</div>'
            "</div>"
        )
    else:
        image_html = (
            '<div class="cityflow-image-placeholder">'
            f'Image not available yet<br>{escape(str(row.get("image", "")))}'
            "</div>"
        )

    ai_score = row.get("ai_score", None)
    ai_html = ""
    if ai_score is not None and pd.notna(ai_score):
        ai_html = (
            '<div class="cityflow-score-box">'
            f"<span>{int(ai_score)}</span>"
            "<small>AI match</small>"
            "</div>"
        )

    reason_html = ""
    if not featured:
        crowd_delta = max(int(selected_row["crowd_level"]) - crowd_level, 0)
        reason_html = (
            '<div class="cityflow-reason-row">'
            f"<span>{escape(crowd_label(crowd_level))}</span>"
            f'<span>{crowd_delta} points calmer than {escape(str(selected_row["name"]))}</span>'
            "</div>"
        )

    return (
        f'<div class="{card_classes}">'
        f"{image_html}"
        '<div class="cityflow-card-content">'
        '<div class="cityflow-card-heading">'
        "<div>"
        f'<div class="cityflow-card-title">{title}</div>'
        f"{status_badge(crowd_level)}"
        "</div>"
        f"{ai_html}"
        "</div>"
        f'<div class="cityflow-card-description">{description}</div>'
        f"{reason_html}"
        '<div class="cityflow-card-meta">'
        f'<span class="cityflow-meta-pill">Area: {area}</span>'
        f'<span class="cityflow-meta-pill">Crowd: {crowd_level}%</span>'
        f'<span class="cityflow-meta-pill">Type: {category}</span>'
        f'<span class="cityflow-meta-pill">Sustainability: {sustainability}/100</span>'
        "</div>"
        "</div>"
        "</div>"
    )


st.markdown(f'<div class="cityflow-panel-label">{escape(t.get("selected_crowded_place", "Selected crowded place"))}</div>', unsafe_allow_html=True)
st.markdown(build_image_card(selected_row, featured=True), unsafe_allow_html=True)

recommendation_pool = locations[
    (locations["name"] == selected) | (locations["crowd_level"] <= max_crowd)
]

alts = recommend_alternatives(
    recommendation_pool,
    selected,
    st.session_state.get("preferences", []),
)

st.markdown(f'<div class="section-title">{escape(t.get("smarter_alternatives", "Smarter Alternatives"))}</div>', unsafe_allow_html=True)

if alts.empty:
    st.info(t.get("no_alternatives", "No alternatives match the current filters. Raise the maximum crowd level or remove category preferences."))
else:
    summary_cols = st.columns(3)
    best = alts.iloc[0]
    summary_cols[0].metric("Best AI match", f"{int(best['ai_score'])}/100")
    summary_cols[1].metric("Calmest option", f"{int(alts['crowd_level'].min())}% crowd")
    summary_cols[2].metric(
        "Average sustainability",
        f"{int(alts['crowd_level'].apply(sustainability_score).mean())}/100",
    )

    cols = st.columns(min(3, len(alts)))
    for col, (_, row) in zip(cols, alts.iterrows()):
        with col:
            st.markdown(build_image_card(row), unsafe_allow_html=True)

with st.expander("Check missing images"):
    missing = get_missing_images(locations)

    if missing:
        st.warning(f"{len(missing)} {t.get('images_missing', 'images are missing from assets/images.')}")
        st.write(missing)
    else:
        st.success(t.get("images_available", "All images are available locally."))
