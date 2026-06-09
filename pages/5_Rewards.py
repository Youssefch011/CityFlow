import pandas as pd
import streamlit as st

from utils.rewards import badge_from_points, reward_marketplace
from utils.storage import ensure_data_files, save_redemption, update_user_points
from utils.style import apply_style, level_badge
from utils.translations import language_selector


st.set_page_config(page_title="Rewards", page_icon="rewards", layout="wide")
apply_style()
ensure_data_files()
t = language_selector(st)

points = int(st.session_state.get("points", 0))
email = (st.session_state.get("current_user") or {}).get("email", "")

st.markdown('<div class="section-title">' + t.get("rewards", "Rewards") + '</div>', unsafe_allow_html=True)
a, b = st.columns([0.8, 1.2])
with a:
    st.markdown(
        f'<div class="dark-card"><h2>{points} Points</h2>{level_badge(points)}'
        f'<p>Your current status: <b>{badge_from_points(points)}</b></p></div>',
        unsafe_allow_html=True,
    )
    st.progress(min(points / 1000, 1.0))
with b:
    st.markdown(
        '<div class="premium-card"><h3>How points create value</h3>'
        '<p class="muted">Points motivate residents and visitors to help the city: report crowded areas, choose calmer alternatives, use public transport, and support local businesses. Partner rewards can be redeemed directly from this page.</p></div>',
        unsafe_allow_html=True,
    )

st.markdown(f'<div class="section-title">{t.get("reward_marketplace", "Reward Marketplace")}</div>', unsafe_allow_html=True)
cols = st.columns(4)
for idx, item in enumerate(reward_marketplace()):
    with cols[idx % 4]:
        available = points >= item["cost"]
        status = "Available" if available else "Locked"
        st.markdown(
            f'<div class="mini-card"><h2>{item.get("emoji", "Gift")}</h2><h3>{item["reward"]}</h3>'
            f'<p class="muted">{item.get("desc", "CityFlow partner reward.")}</p>'
            f'<b>{item["cost"]} points</b><br>{status}</div>',
            unsafe_allow_html=True,
        )
        if st.button(t.get("redeem", "Redeem"), key=f"redeem_{idx}", disabled=not available):
            points -= int(item["cost"])
            st.session_state.points = points
            update_user_points(email, points)
            save_redemption(email, item["reward"], item["cost"], "Redeemed")
            if st.session_state.get("current_user"):
                st.session_state.current_user["points"] = points
                st.session_state.current_user["badge"] = badge_from_points(points)
            st.success(f"{t.get('redeem', 'Redeem')}: {item['reward']}")
            st.rerun()

redemptions = pd.read_csv("data/redemptions.csv")
if email and not redemptions.empty:
    mine = redemptions[redemptions["email"].fillna("").str.lower() == email.lower()]
    if not mine.empty:
        st.markdown(f'<div class="section-title">{t.get("your_redemptions", "Your Redemptions")}</div>', unsafe_allow_html=True)
        st.dataframe(mine.sort_values("created_at", ascending=False), use_container_width=True)
