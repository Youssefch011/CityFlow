from html import escape
from io import BytesIO
import base64

import folium
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import st_folium

from utils.image import get_image_path
from utils.maps import place_maps_url
from utils.recommendation_engine import crowd_color, crowd_label
from utils.style import apply_style, status_badge
from utils.translations import language_selector


st.set_page_config(page_title="Map", page_icon="map", layout="wide")
apply_style()
t = language_selector(st)

st.markdown(
    """
    <style>
    .cityflow-map-toolbar {
        margin: 4px 0 16px 0;
    }

    .cityflow-map-panel {
        padding: 20px;
        border-radius: 8px;
        background: rgba(8,20,38,0.76);
        border: 1px solid rgba(103,232,249,0.22);
        box-shadow: 0 18px 45px rgba(0,0,0,0.28);
        color: #EAF7FF;
        margin-bottom: 16px;
    }

    .cityflow-map-panel h3 {
        margin: 0 0 14px 0;
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 900;
    }

    .cityflow-legend {
        display: grid;
        grid-template-columns: 1fr;
        gap: 8px;
        margin-top: 12px;
    }

    .cityflow-legend-item {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #D9F7FF;
        font-size: 13px;
        font-weight: 800;
    }

    .cityflow-legend-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        box-shadow: 0 0 14px currentColor;
    }

    .cityflow-mini-destination {
        display: grid;
        grid-template-columns: 72px 1fr;
        gap: 12px;
        align-items: center;
        padding: 10px;
        border-radius: 8px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(103,232,249,0.14);
        margin-bottom: 10px;
    }

    .cityflow-mini-destination img {
        width: 72px;
        height: 54px;
        object-fit: cover;
        border-radius: 6px;
        display: block;
    }

    .cityflow-mini-title {
        color: #FFFFFF;
        font-size: 14px;
        font-weight: 900;
        line-height: 1.2;
    }

    .cityflow-mini-meta {
        color: #B7D4E8;
        font-size: 12px;
        margin-top: 4px;
        font-weight: 700;
    }

    .cityflow-map-note {
        color: #B7D4E8;
        font-size: 13px;
        line-height: 1.45;
        margin-top: 10px;
    }

    .confidence-ring {
        display: grid;
        grid-template-columns: 86px 1fr;
        gap: 14px;
        align-items: center;
        padding: 12px;
        border-radius: 8px;
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(103,232,249,0.16);
        margin: 10px 0 12px;
    }

    .confidence-score {
        width: 78px;
        height: 78px;
        border-radius: 50%;
        display: grid;
        place-items: center;
        color: #FFFFFF;
        font-size: 22px;
        font-weight: 900;
        background:
            radial-gradient(circle at center, #081426 54%, transparent 55%),
            conic-gradient(#5DF2A5 var(--confidence), rgba(255,255,255,0.10) 0);
        box-shadow: 0 0 24px rgba(93,242,165,0.16);
    }

    .confidence-title {
        color: #FFFFFF;
        font-weight: 900;
        line-height: 1.2;
    }

    .confidence-copy {
        color: #B7D4E8;
        font-size: 12px;
        line-height: 1.4;
        margin-top: 5px;
    }

    .signal-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }

    .signal-pill {
        padding: 9px;
        border-radius: 8px;
        background: rgba(34,197,94,0.09);
        border: 1px solid rgba(34,197,94,0.16);
        color: #BBF7D0;
        font-size: 11px;
        font-weight: 900;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(f'<div class="section-title">{escape(t["map"])}</div>', unsafe_allow_html=True)
st.caption(t.get("map_caption", "Explore live crowd pressure by destination. Click any marker to preview the place, image, and crowd status."))

locations = pd.read_csv("data/locations.csv")
reports = pd.read_csv("data/reports.csv")


@st.cache_data(show_spinner=False)
def get_thumbnail_base64(image_name, size=(420, 260), quality=72):
    image_path = get_image_path(image_name)
    if not image_path or not image_path.exists():
        return ""

    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.thumbnail(size)
        canvas = Image.new("RGB", size, (8, 20, 38))
        x = (size[0] - img.width) // 2
        y = (size[1] - img.height) // 2
        canvas.paste(img, (x, y))
        buffer = BytesIO()
        canvas.save(buffer, format="JPEG", quality=quality, optimize=True)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


def crowd_hex(level):
    if level >= 80:
        return "#F43F5E"
    if level >= 60:
        return "#FB923C"
    if level >= 40:
        return "#38BDF8"
    return "#22C55E"


def confidence_metrics(filtered_locations, reports_df):
    report_count = len(reports_df)
    visible_count = len(filtered_locations)
    if report_count:
        created = pd.to_datetime(reports_df["created_at"], errors="coerce")
        recent_reports = int((created >= (pd.Timestamp.now() - pd.Timedelta(days=1))).sum())
        report_bonus = min(22, report_count * 6)
        recent_bonus = min(16, recent_reports * 8)
    else:
        recent_reports = 0
        report_bonus = 0
        recent_bonus = 0

    coverage_bonus = min(20, visible_count * 0.8)
    time_signal = 18 if pd.Timestamp.now().hour in {11, 12, 13, 17, 18, 19} else 12
    confidence = int(min(94, round(42 + report_bonus + recent_bonus + coverage_bonus + time_signal)))
    source_text = (
        f"{visible_count} mapped places, {report_count} community reports, "
        f"{recent_reports} fresh signal{'s' if recent_reports != 1 else ''}, and time-of-day patterns."
    )
    confidence_label = "High confidence" if confidence >= 78 else "Medium confidence" if confidence >= 62 else "Prototype confidence"
    return confidence, confidence_label, source_text, recent_reports


def marker_icon(row):
    level = int(row["crowd_level"])
    color = crowd_hex(level)
    label = escape(str(row["name"]))
    return folium.DivIcon(
        html=f"""
        <div title="{label}" style="
            width: 46px;
            height: 46px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: 900;
            background: radial-gradient(circle at 35% 30%, rgba(255,255,255,0.28), transparent 32%), {color};
            border: 3px solid rgba(255,255,255,0.88);
            box-shadow: 0 10px 24px rgba(0,0,0,0.32), 0 0 18px {color};
        ">{level}%</div>
        """
    )


def popup_html(row):
    level = int(row["crowd_level"])
    label = escape(crowd_label(level))
    color = crowd_hex(level)
    title = escape(str(row["name"]))
    area = escape(str(row["area"]))
    category = escape(str(row["category"]))
    description = escape(str(row["description"]))
    maps_url = place_maps_url(row["name"], row["lat"], row["lon"])
    img = get_thumbnail_base64(row.get("image", ""), size=(360, 210), quality=68)
    image_html = ""
    if img:
        image_html = (
            f'<img src="data:image/jpeg;base64,{img}" '
            'style="width:100%;height:132px;object-fit:cover;display:block;">'
        )

    return f"""
    <div style="width:275px;border-radius:8px;overflow:hidden;background:#081426;color:#EAF7FF;font-family:Inter,Arial,sans-serif;">
        {image_html}
        <div style="padding:13px;">
            <div style="font-size:18px;font-weight:900;line-height:1.15;margin-bottom:8px;color:#FFFFFF;">{title}</div>
            <div style="display:inline-block;padding:6px 9px;border-radius:8px;background:{color};color:white;font-size:12px;font-weight:900;margin-bottom:9px;">
                {level}% crowd · {label}
            </div>
            <div style="font-size:12px;line-height:1.45;color:#B7D4E8;margin-bottom:10px;">{description}</div>
            <div style="display:flex;gap:6px;flex-wrap:wrap;font-size:11px;font-weight:800;color:#D9F7FF;">
                <span style="padding:6px 8px;border-radius:8px;background:rgba(255,255,255,0.08);">Area: {area}</span>
                <span style="padding:6px 8px;border-radius:8px;background:rgba(255,255,255,0.08);">Type: {category}</span>
            </div>
            <a href="{maps_url}" target="_blank" style="display:block;margin-top:10px;padding:8px 10px;border-radius:8px;background:#0EA5E9;color:white;text-decoration:none;text-align:center;font-weight:900;font-size:12px;">Open in Google Maps</a>
        </div>
    </div>
    """


st.markdown('<div class="cityflow-map-toolbar">', unsafe_allow_html=True)
filter_cols = st.columns([1, 1, 1])
with filter_cols[0]:
    categories = sorted(locations["category"].dropna().unique().tolist())
    selected_categories = st.multiselect(t.get("categories", "Categories"), categories)
with filter_cols[1]:
    max_crowd = st.slider(t.get("show_crowd_up_to", "Show crowd up to"), 20, 100, 100, 5)
with filter_cols[2]:
    focus_mode = st.selectbox(t.get("map_focus", "Map focus"), [t.get("all_destinations", "All destinations"), t.get("overcrowded_only", "Overcrowded only"), t.get("calm_alternatives_only", "Calm alternatives")])
st.markdown("</div>", unsafe_allow_html=True)

filtered = locations[locations["crowd_level"] <= max_crowd].copy()
if selected_categories:
    filtered = filtered[filtered["category"].isin(selected_categories)]
if focus_mode == t.get("overcrowded_only", "Overcrowded only"):
    filtered = filtered[filtered["crowd_level"] >= 80]
elif focus_mode == t.get("calm_alternatives_only", "Calm alternatives"):
    filtered = filtered[filtered["crowd_level"] < 50]

left, right = st.columns([1.65, 0.85])

with left:
    center = [41.3851, 2.1734]
    if not filtered.empty:
        center = [filtered["lat"].mean(), filtered["lon"].mean()]

    m = folium.Map(
        location=center,
        zoom_start=12,
        tiles="CartoDB dark_matter",
        control_scale=True,
    )

    for _, row in filtered.iterrows():
        level = int(row["crowd_level"])
        folium.Marker(
            [row["lat"], row["lon"]],
            icon=marker_icon(row),
            popup=folium.Popup(popup_html(row), max_width=300),
            tooltip=f"{row['name']} · {level}% · {crowd_label(level)}",
        ).add_to(m)

        folium.Circle(
            [row["lat"], row["lon"]],
            radius=120 + level * 8,
            color=crowd_color(level),
            fill=True,
            fill_color=crowd_color(level),
            fill_opacity=0.14,
            weight=1,
        ).add_to(m)

    st_folium(m, use_container_width=True, height=620, returned_objects=[])

with right:
    confidence, confidence_label, source_text, recent_reports = confidence_metrics(filtered, reports)
    st.markdown(
        f"""
        <div class="cityflow-map-panel">
            <h3>{escape(t.get("crowd_intelligence", "Crowd Intelligence"))}</h3>
            <div class="confidence-ring">
                <div class="confidence-score" style="--confidence:{confidence}%;">{confidence}%</div>
                <div>
                    <div class="confidence-title">{escape(confidence_label)}</div>
                    <div class="confidence-copy">{escape(source_text)}</div>
                </div>
            </div>
            <div class="signal-grid">
                <div class="signal-pill">Live reports: {len(reports)}</div>
                <div class="signal-pill">Fresh today: {recent_reports}</div>
                <div class="signal-pill">Time signal: active</div>
                <div class="signal-pill">Map coverage: {len(filtered)}</div>
            </div>
            <div class="cityflow-map-note">CityFlow combines community observations, destination baseline pressure, time-of-day behavior, and visible map filters. This is a prototype confidence model, not official sensor data.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="cityflow-map-panel"><h3>{escape(t.get("city_status", "City Status"))}</h3>', unsafe_allow_html=True)
    metric_cols = st.columns(2)
    metric_cols[0].metric("Visible", len(filtered))
    metric_cols[1].metric("Avg crowd", f"{filtered['crowd_level'].mean():.1f}%" if not filtered.empty else "0%")
    metric_cols[0].metric("Overcrowded", len(filtered[filtered["crowd_level"] >= 80]))
    metric_cols[1].metric("Calm", len(filtered[filtered["crowd_level"] < 50]))
    st.markdown(
        """
        <div class="cityflow-legend">
            <div class="cityflow-legend-item"><span class="cityflow-legend-dot" style="background:#F43F5E;color:#F43F5E;"></span> Overcrowded · 80%+</div>
            <div class="cityflow-legend-item"><span class="cityflow-legend-dot" style="background:#FB923C;color:#FB923C;"></span> Busy · 60-79%</div>
            <div class="cityflow-legend-item"><span class="cityflow-legend-dot" style="background:#38BDF8;color:#38BDF8;"></span> Moderate · 40-59%</div>
            <div class="cityflow-legend-item"><span class="cityflow-legend-dot" style="background:#22C55E;color:#22C55E;"></span> Calm · below 40%</div>
        </div>
        <div class="cityflow-map-note">Marker size and glow show live crowd pressure. Select a marker to open the image preview card.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="cityflow-map-panel"><h3>{escape(t.get("highest_crowd", "Highest Crowd"))}</h3>', unsafe_allow_html=True)
    for _, row in filtered.sort_values("crowd_level", ascending=False).head(4).iterrows():
        img = get_thumbnail_base64(row.get("image", ""), size=(160, 120), quality=70)
        img_html = f'<img src="data:image/jpeg;base64,{img}">' if img else ""
        st.markdown(
            f"""
            <div class="cityflow-mini-destination">
                {img_html}
                <div>
                    <div class="cityflow-mini-title">{escape(str(row["name"]))}</div>
                    <div class="cityflow-mini-meta">{int(row["crowd_level"])}% · {escape(crowd_label(int(row["crowd_level"])))} · {escape(str(row["area"]))}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f'<div class="cityflow-map-panel"><h3>{escape(t.get("calm_alternatives", "Calm Alternatives"))}</h3>', unsafe_allow_html=True)
    for _, row in filtered.sort_values("crowd_level", ascending=True).head(4).iterrows():
        img = get_thumbnail_base64(row.get("image", ""), size=(160, 120), quality=70)
        img_html = f'<img src="data:image/jpeg;base64,{img}">' if img else ""
        st.markdown(
            f"""
            <div class="cityflow-mini-destination">
                {img_html}
                <div>
                    <div class="cityflow-mini-title">{escape(str(row["name"]))}</div>
                    <div class="cityflow-mini-meta">{int(row["crowd_level"])}% · {escape(crowd_label(int(row["crowd_level"])))} · {escape(str(row["area"]))}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f'<div class="section-title">{escape(t.get("destination_cards", "Destination Crowd Cards"))}</div>', unsafe_allow_html=True)
card_cols = st.columns(3)
for i, (_, row) in enumerate(filtered.sort_values("crowd_level", ascending=False).iterrows()):
    img = get_thumbnail_base64(row.get("image", ""), size=(420, 260), quality=72)
    img_html = f'<img src="data:image/jpeg;base64,{img}" class="cityflow-card-image">' if img else ""
    maps_url = place_maps_url(row["name"], row["lat"], row["lon"])
    with card_cols[i % 3]:
        st.markdown(
            f"""
            <div class="cityflow-image-card">
                <div class="cityflow-card-image-wrap">
                    {img_html}
                    <div class="cityflow-card-overlay"></div>
                    <div class="cityflow-card-category">{escape(str(row["category"]))}</div>
                </div>
                <div class="cityflow-card-content">
                    <div class="cityflow-card-title">{escape(str(row["name"]))}</div>
                    {status_badge(int(row["crowd_level"]))}
                    <div class="cityflow-card-description">{escape(str(row["description"]))}</div>
                    <div class="cityflow-card-meta">
                        <span class="cityflow-meta-pill">Area: {escape(str(row["area"]))}</span>
                        <span class="cityflow-meta-pill">Crowd: {int(row["crowd_level"])}%</span>
                        <a class="cityflow-meta-pill" href="{maps_url}" target="_blank" rel="noopener noreferrer">Google Maps</a>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
