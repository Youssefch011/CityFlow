import streamlit as st

from utils.style import apply_style
from utils.translations import language_selector


st.set_page_config(page_title="Subscription", page_icon="subscription", layout="wide")
apply_style()
t = language_selector(st)

plans = [
    {
        "key": "trial",
        "name": t.get("sub_trial", "Free Trial"),
        "price": "0 €",
        "period": t.get("sub_trial_period", "for 1 month"),
        "badge": t.get("sub_start_badge", "Start here"),
        "description": t.get("sub_trial_desc", "Explore CityFlow Premium features before paying."),
        "features": [
            t.get("sub_feature_routes", "Premium smart route advisor"),
            t.get("sub_feature_map", "City Pulse crowd map"),
            t.get("sub_feature_reports", "Community reports and profile XP"),
        ],
        "featured": False,
    },
    {
        "key": "weekly",
        "name": t.get("sub_weekly", "Weekly"),
        "price": "4,99 €",
        "period": t.get("sub_weekly_period", "per week"),
        "badge": t.get("sub_flexible_badge", "Flexible"),
        "description": t.get("sub_weekly_desc", "Best for short visits, events, and weekends in Barcelona."),
        "features": [
            t.get("sub_feature_routes", "Premium smart route advisor"),
            t.get("sub_feature_recommendations", "AI-assisted calm alternatives"),
            t.get("sub_feature_rewards", "Impact rewards and status progression"),
        ],
        "featured": False,
    },
    {
        "key": "monthly",
        "name": t.get("sub_monthly", "Monthly"),
        "price": "6,99 €",
        "period": t.get("sub_monthly_period", "per month"),
        "badge": t.get("sub_popular_badge", "Most popular"),
        "description": t.get("sub_monthly_desc", "Best for regular residents, students, and city explorers."),
        "features": [
            t.get("sub_feature_routes", "Premium smart route advisor"),
            t.get("sub_feature_alerts", "Crowd-aware planning and alerts"),
            t.get("sub_feature_rewards", "Impact rewards and status progression"),
        ],
        "featured": True,
    },
    {
        "key": "yearly",
        "name": t.get("sub_yearly", "Yearly"),
        "price": "35,99 €",
        "period": t.get("sub_yearly_period", "per year"),
        "badge": t.get("sub_best_value_badge", "Best value"),
        "description": t.get("sub_yearly_desc", "Best for locals who use CityFlow all year."),
        "features": [
            t.get("sub_feature_routes", "Premium smart route advisor"),
            t.get("sub_feature_alerts", "Crowd-aware planning and alerts"),
            t.get("sub_feature_partner", "Partner rewards and future premium benefits"),
        ],
        "featured": False,
    },
]

st.markdown(
    """
    <style>
    .subscription-hero {
        padding: 34px;
        border-radius: 8px;
        background:
            linear-gradient(135deg, rgba(2,8,23,0.95), rgba(8,47,73,0.78)),
            radial-gradient(circle at 88% 16%, rgba(52,211,153,0.28), transparent 32%);
        border: 1px solid rgba(103,232,249,0.24);
        box-shadow: 0 24px 70px rgba(0,0,0,0.34);
        margin-bottom: 18px;
        color: #EAF7FF;
    }

    .subscription-eyebrow {
        display: inline-flex;
        padding: 8px 10px;
        border-radius: 8px;
        background: rgba(103,232,249,0.11);
        border: 1px solid rgba(103,232,249,0.22);
        color: #67E8F9;
        font-size: 12px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 14px;
    }

    .subscription-title {
        color: #FFFFFF;
        font-size: 48px;
        line-height: 1.04;
        font-weight: 900;
        margin: 0 0 12px;
    }

    .subscription-subtitle {
        color: #B7D4E8;
        max-width: 760px;
        font-size: 16px;
        line-height: 1.55;
    }

    .pricing-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin: 18px 0;
    }

    .pricing-card {
        position: relative;
        display: flex;
        flex-direction: column;
        min-height: 420px;
        padding: 20px;
        border-radius: 8px;
        background: rgba(8,20,38,0.78);
        border: 1px solid rgba(103,232,249,0.18);
        box-shadow: 0 18px 46px rgba(0,0,0,0.28);
        color: #EAF7FF;
    }

    .pricing-card.featured {
        border-color: rgba(52,211,153,0.48);
        box-shadow: 0 0 34px rgba(52,211,153,0.16), 0 22px 55px rgba(0,0,0,0.32);
        background:
            linear-gradient(180deg, rgba(8,47,73,0.80), rgba(8,20,38,0.86)),
            rgba(8,20,38,0.78);
    }

    .pricing-badge {
        align-self: flex-start;
        padding: 7px 9px;
        border-radius: 8px;
        background: rgba(103,232,249,0.10);
        border: 1px solid rgba(103,232,249,0.18);
        color: #67E8F9;
        font-size: 12px;
        font-weight: 900;
        margin-bottom: 14px;
    }

    .pricing-card.featured .pricing-badge {
        background: rgba(34,197,94,0.12);
        border-color: rgba(34,197,94,0.24);
        color: #BBF7D0;
    }

    .pricing-name {
        color: #FFFFFF;
        font-size: 22px;
        line-height: 1.1;
        font-weight: 900;
        margin-bottom: 10px;
    }

    .pricing-price {
        color: #FFFFFF;
        font-size: 42px;
        line-height: 1;
        font-weight: 900;
        margin-bottom: 6px;
    }

    .pricing-period {
        color: #67E8F9;
        font-size: 13px;
        font-weight: 900;
        margin-bottom: 14px;
    }

    .pricing-desc {
        color: #B7D4E8;
        font-size: 14px;
        line-height: 1.48;
        min-height: 62px;
        margin-bottom: 16px;
    }

    .pricing-features {
        display: grid;
        gap: 10px;
        margin: 0 0 18px;
        padding: 0;
        list-style: none;
    }

    .pricing-features li {
        color: #D9F7FF;
        font-size: 13px;
        line-height: 1.35;
        font-weight: 800;
    }

    .pricing-features li:before {
        content: "✓";
        color: #5DF2A5;
        font-weight: 900;
        margin-right: 8px;
    }

    .subscription-note {
        padding: 18px;
        border-radius: 8px;
        background: rgba(251,191,36,0.10);
        border: 1px solid rgba(251,191,36,0.22);
        color: #FDE68A;
        font-weight: 800;
        line-height: 1.45;
        margin-top: 14px;
    }

    @media (max-width: 1050px) {
        .pricing-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 700px) {
        .pricing-grid {
            grid-template-columns: 1fr;
        }

        .subscription-title {
            font-size: 34px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="subscription-hero">
        <div class="subscription-eyebrow">{t.get("subscription_eyebrow", "CityFlow Premium")}</div>
        <div class="subscription-title">{t.get("subscription_title", "Choose your CityFlow plan.")}</div>
        <div class="subscription-subtitle">{t.get("subscription_subtitle", "Unlock smarter routes, crowd-aware decisions, impact rewards, and a more useful Barcelona experience for residents and visitors.")}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="pricing-grid">', unsafe_allow_html=True)
cols = st.columns(4)
for col, plan in zip(cols, plans):
    with col:
        featured_class = " featured" if plan["featured"] else ""
        st.markdown(
            f"""
            <div class="pricing-card{featured_class}">
                <div class="pricing-badge">{plan["badge"]}</div>
                <div class="pricing-name">{plan["name"]}</div>
                <div class="pricing-price">{plan["price"]}</div>
                <div class="pricing-period">{plan["period"]}</div>
                <div class="pricing-desc">{plan["description"]}</div>
                <ul class="pricing-features">
                    {''.join(f'<li>{feature}</li>' for feature in plan["features"])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(t.get("sub_choose_plan", "Choose plan"), key=f"choose_{plan['key']}", use_container_width=True):
            st.session_state.subscription_plan = plan["key"]
            st.success(f'{t.get("sub_selected", "Selected plan")}: {plan["name"]} - {plan["price"]}')
st.markdown('</div>', unsafe_allow_html=True)

selected = st.session_state.get("subscription_plan")
if selected:
    selected_plan = next(plan for plan in plans if plan["key"] == selected)
    st.markdown(
        f'<div class="premium-card"><div class="section-title">{t.get("sub_current_choice", "Current choice")}</div>'
        f'<p class="muted"><b>{selected_plan["name"]}</b> · {selected_plan["price"]} · {selected_plan["period"]}</p></div>',
        unsafe_allow_html=True,
    )

st.markdown(
    f'<div class="subscription-note">{t.get("sub_note", "Prototype note: payment is not connected yet. These plans are displayed for product simulation and can later be connected to Stripe or another payment provider.")}</div>',
    unsafe_allow_html=True,
)
