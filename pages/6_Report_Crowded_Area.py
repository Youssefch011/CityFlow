import pandas as pd
import streamlit as st
from pathlib import Path
from uuid import uuid4

from utils.rewards import badge_from_points, report_points
from utils.storage import ensure_data_files, save_report, update_location_crowd, update_user_points
from utils.style import apply_style
from utils.translations import language_selector


st.set_page_config(page_title="Report", page_icon="report", layout="wide")
apply_style()
ensure_data_files()
t = language_selector(st)

st.markdown(
    """
    <style>
    .report-photo-label {
        margin: 8px 0 6px;
        color: #EAF7FF;
        font-size: 13px;
        font-weight: 900;
    }

    .report-photo-helper {
        margin: -2px 0 8px;
        color: #B7D4E8;
        font-size: 12px;
        line-height: 1.35;
    }

    [data-testid="stFileUploader"] > label {
        display: none !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        min-height: 76px !important;
        padding: 0 !important;
        border: 1px dashed rgba(93,242,165,0.42) !important;
        border-radius: 18px !important;
        background:
            linear-gradient(135deg, rgba(34,197,94,0.13), rgba(14,165,233,0.10)),
            rgba(8,20,38,0.74) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 12px 26px rgba(0,0,0,0.18);
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        display: none !important;
    }

    [data-testid="stFileUploaderDropzone"] > span {
        width: 100% !important;
    }

    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] {
        width: 100% !important;
        min-height: 58px !important;
        border: 0 !important;
        border-radius: 16px !important;
        background: transparent !important;
        color: transparent !important;
        box-shadow: none !important;
        position: relative;
        font-size: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    [data-testid="stFileUploader"] button * {
        color: transparent !important;
        font-size: 0 !important;
    }

    [data-testid="stFileUploader"] button:before {
        content: "Add photo";
        display: block;
        color: #FFFFFF;
        font-size: 13px;
        font-weight: 900;
        line-height: 1;
        text-align: center;
    }

    [data-testid="stFileUploader"] button:after {
        content: "Camera or gallery";
        display: block;
        margin-top: 5px;
        color: #BBF7D0;
        font-size: 10px;
        font-weight: 800;
        text-align: center;
    }

    [data-testid="stFileUploader"] svg {
        display: none !important;
    }

    [data-testid="stImage"] img {
        border-radius: 16px;
        border: 1px solid rgba(103,232,249,0.22);
        box-shadow: 0 14px 30px rgba(0,0,0,0.24);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">' + t["report"] + '</div>', unsafe_allow_html=True)
locations = pd.read_csv("data/locations.csv")
location = st.selectbox(t.get("location", "Location"), locations["name"].tolist())
crowd = st.selectbox(t.get("observed_crowd_level", "Observed crowd level"), ["Calm", "Moderate", "Busy", "Very Crowded"])
comment = st.text_area(t.get("comment", "Comment"))
st.markdown(
    f"""
    <div class="report-photo-label">{t.get("report_photo", "Add a picture")}</div>
    <div class="report-photo-helper">{t.get("report_photo_help", "Optional: attach a crowd or place photo to support your report.")}</div>
    """,
    unsafe_allow_html=True,
)
photo = st.file_uploader(
    t.get("report_photo", "Add a picture"),
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)

if photo:
    st.image(photo, caption=t.get("photo_preview", "Photo preview"), use_container_width=True)

if st.button(t.get("submit_report", "Submit Report")):
    pts = report_points()
    st.session_state.points = int(st.session_state.get("points", 0)) + pts
    user = st.session_state.get("current_user") or {"name": "City Explorer", "email": ""}
    photo_path = ""
    if photo:
        photo_dir = Path("assets/report_photos")
        photo_dir.mkdir(parents=True, exist_ok=True)
        suffix = Path(photo.name).suffix.lower() or ".jpg"
        photo_path = str(photo_dir / f"report_{uuid4().hex}{suffix}").replace("\\", "/")
        Path(photo_path).write_bytes(photo.getbuffer())

    save_report(user.get("name", "City Explorer"), user.get("email", ""), location, crowd, comment, pts, photo_path)
    update_location_crowd(location, crowd)
    update_user_points(user.get("email", ""), st.session_state.points)
    if st.session_state.get("current_user"):
        st.session_state.current_user["points"] = st.session_state.points
        st.session_state.current_user["badge"] = badge_from_points(st.session_state.points)

    st.success(f"{t.get('report_success', 'Thank you. You earned impact points. The City Pulse crowd level was updated.')} +{pts}")
    st.info(f"{t['badge']}: {badge_from_points(st.session_state.points)}")
