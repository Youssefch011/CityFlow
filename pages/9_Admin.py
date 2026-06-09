import pandas as pd
import plotly.express as px
import streamlit as st
import html

from utils.storage import delete_report_at_index, ensure_data_files
from utils.style import apply_style
from utils.translations import language_selector


st.set_page_config(page_title="Admin", page_icon="admin", layout="wide")
apply_style()
ensure_data_files()
t = language_selector(st)


def safe(value):
    return html.escape(str(value or ""))


def report_status_color(level):
    label = str(level or "").lower()
    if "crowd" in label:
        return "#FB7185"
    if "busy" in label:
        return "#FDBA74"
    if "moderate" in label:
        return "#67E8F9"
    return "#86EFAC"


def format_time(value):
    try:
        return pd.to_datetime(value).strftime("%b %d, %H:%M")
    except Exception:
        return "Unknown time"


st.markdown(
    """
    <style>
    .admin-report-card {
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 14px;
        padding: 16px;
        border-radius: 8px;
        background: rgba(8,20,38,0.76);
        border: 1px solid rgba(103,232,249,0.18);
        box-shadow: 0 14px 34px rgba(0,0,0,0.22);
        margin-bottom: 12px;
        color: #EAF7FF;
    }

    .admin-report-title {
        color: #FFFFFF;
        font-size: 17px;
        font-weight: 900;
        margin-bottom: 7px;
    }

    .admin-report-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 9px 0;
    }

    .admin-report-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 7px 9px;
        border-radius: 8px;
        background: rgba(255,255,255,0.065);
        border: 1px solid rgba(103,232,249,0.14);
        color: #D9F7FF;
        font-size: 12px;
        font-weight: 800;
    }

    .admin-report-message {
        max-width: 780px;
        color: #B7D4E8;
        line-height: 1.5;
        font-size: 14px;
    }

    .admin-report-actions {
        min-width: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 8px;
    }

    .admin-empty {
        padding: 18px;
        border-radius: 8px;
        background: rgba(34,197,94,0.10);
        border: 1px solid rgba(34,197,94,0.22);
        color: #BBF7D0;
        font-weight: 800;
    }

    @media (max-width: 760px) {
        .admin-report-card {
            grid-template-columns: 1fr;
        }

        .admin-report-actions {
            min-width: 0;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">' + t["admin"] + '</div>', unsafe_allow_html=True)
locations = pd.read_csv("data/locations.csv")
users = pd.read_csv("data/users.csv")
reports = pd.read_csv("data/reports.csv")
itineraries = pd.read_csv("data/itineraries.csv")
redemptions = pd.read_csv("data/redemptions.csv")

c1, c2, c3, c4 = st.columns(4)
c1.metric(t.get("locations", "Locations"), len(locations))
c2.metric(t.get("avg_crowd", "Avg crowd"), f"{locations['crowd_level'].mean():.1f}%")
c3.metric(t.get("reports", "Reports"), len(reports))
c4.metric(t.get("users", "Users"), len(users))

st.plotly_chart(
    px.bar(
        locations.sort_values("crowd_level", ascending=False),
        x="name",
        y="crowd_level",
        color="category",
        template="plotly_white",
        title="Crowd level by destination",
    ),
    use_container_width=True,
)

tabs = st.tabs([t.get("locations", "Locations"), t.get("users", "Users"), t.get("reports", "Reports"), t.get("itineraries", "Itineraries"), t.get("redemptions", "Redemptions")])
with tabs[0]:
    st.dataframe(locations, use_container_width=True)
with tabs[1]:
    st.dataframe(users, use_container_width=True)
with tabs[2]:
    st.markdown(f'<div class="section-title">{t.get("report_control_center", "Report Control Center")}</div>', unsafe_allow_html=True)
    if reports.empty:
        st.markdown(f'<div class="admin-empty">{t.get("no_reports_manage", "No community reports to manage.")}</div>', unsafe_allow_html=True)
    else:
        reports_view = reports.copy()
        reports_view["report_index"] = reports_view.index
        location_options = [t.get("all_locations", "All locations")] + sorted(reports_view["location"].dropna().unique().tolist())
        crowd_options = [t.get("all_levels", "All levels")] + sorted(reports_view["crowd_level"].dropna().unique().tolist())
        filter_cols = st.columns([1, 1, 0.7])
        with filter_cols[0]:
            selected_location = st.selectbox(t.get("filter_location", "Filter by location"), location_options)
        with filter_cols[1]:
            selected_level = st.selectbox(t.get("filter_crowd", "Filter by crowd level"), crowd_options)

        if selected_location != t.get("all_locations", "All locations"):
            reports_view = reports_view[reports_view["location"] == selected_location]
        if selected_level != t.get("all_levels", "All levels"):
            reports_view = reports_view[reports_view["crowd_level"] == selected_level]
        with filter_cols[2]:
            st.metric(t.get("visible_reports", "Visible reports"), len(reports_view))

        st.caption(t.get("delete_report_note", "Delete removes the report from data/reports.csv. This action is immediate."))
        for _, row in reports_view.sort_values("created_at", ascending=False).iterrows():
            color = report_status_color(row.get("crowd_level", ""))
            col_a, col_b = st.columns([1, 0.2])
            with col_a:
                st.markdown(
                    f"""
                    <div class="admin-report-card">
                        <div>
                            <div class="admin-report-title">{safe(row.get("location", "Unknown location"))}</div>
                            <div class="admin-report-meta">
                                <span class="admin-report-pill" style="border-color:{color};color:{color};">{safe(row.get("crowd_level", "Unknown"))}</span>
                                <span class="admin-report-pill">By {safe(row.get("name", "City Explorer"))}</span>
                                <span class="admin-report-pill">{safe(format_time(row.get("created_at", "")))}</span>
                                <span class="admin-report-pill">+{safe(row.get("points_awarded", 0))} XP</span>
                            </div>
                            <div class="admin-report-message">{safe(row.get("comment", "") or "No comment provided.")}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_b:
                st.write("")
                st.write("")
                if st.button(t.get("delete", "Delete"), key=f"delete_report_{int(row['report_index'])}", use_container_width=True):
                    if delete_report_at_index(int(row["report_index"])):
                        st.success(t.get("report_deleted", "Report deleted."))
                        st.rerun()
                    else:
                        st.error(t.get("delete_failed", "Could not delete this report."))

        with st.expander(t.get("raw_report_table", "Raw report table")):
            st.dataframe(reports_view.drop(columns=["report_index"]), use_container_width=True, hide_index=True)
with tabs[3]:
    st.dataframe(itineraries, use_container_width=True)
with tabs[4]:
    st.dataframe(redemptions, use_container_width=True)
