import pandas as pd
import streamlit as st

from utils.storage import ensure_data_files
from utils.style import apply_style
from utils.translations import language_selector


st.set_page_config(page_title="Leaderboard", page_icon="leaderboard", layout="wide")
apply_style()
ensure_data_files()
t = language_selector(st)

st.markdown('<div class="section-title">' + t["leaderboard"] + '</div>', unsafe_allow_html=True)
users = pd.read_csv("data/users.csv")
if users.empty:
    st.info(t.get("no_users", "No users yet."))
else:
    users["points"] = users["points"].fillna(0).astype(int)
    ranked = users.sort_values("points", ascending=False).reset_index(drop=True)
    ranked.insert(0, "rank", ranked.index + 1)
    st.dataframe(ranked[["rank", "name", "email", "points", "badge", "language"]], use_container_width=True)
