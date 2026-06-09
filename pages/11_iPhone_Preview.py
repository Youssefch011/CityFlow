import streamlit as st
import streamlit.components.v1 as components

from utils.image import get_image_base64
from utils.style import apply_style


st.set_page_config(page_title="iPhone Preview", page_icon="phone", layout="wide")
apply_style()
logo_image = get_image_base64("assets/cityflow_logo.png")
logo_src = f"data:image/png;base64,{logo_image}" if logo_image else ""

st.markdown(
    """
    <style>
    :root {
        --cityflow-preview-bg: #063B2B;
    }

    header,
    [data-testid="stHeader"],
    button[kind="header"],
    header [data-testid="baseButton-headerNoPadding"] {
        display: none !important;
    }

    [data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 10000 !important;
        width: 18rem !important;
        min-width: 18rem !important;
        max-width: 18rem !important;
        flex: 0 0 18rem !important;
        background: transparent !important;
        border-right: 1px solid rgba(187,247,208,0.14) !important;
        box-shadow: inset -1px 0 0 rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(20px) !important;
    }

    [data-testid="stSidebar"] * {
        visibility: visible !important;
    }

    [data-testid="stSidebar"] > div {
        width: 18rem !important;
        min-width: 18rem !important;
        max-width: 18rem !important;
        background: transparent !important;
    }

    [data-testid="stSidebar"] section,
    [data-testid="stSidebar"] nav,
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNav"] ul,
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        background: transparent !important;
    }

    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="collapsedControl"] button {
        background: rgba(2,20,14,0.22) !important;
        border: 1px solid rgba(187,247,208,0.16) !important;
        color: #EFFFF7 !important;
    }

    [data-testid="stSidebarNav"] a {
        background: rgba(255,255,255,0.055) !important;
        border: 1px solid rgba(187,247,208,0.10) !important;
        color: #EFFFF7 !important;
    }

    [data-testid="stSidebarNav"] a:hover,
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(34,197,94,0.18) !important;
        border-color: rgba(187,247,208,0.26) !important;
    }

    .stApp {
        background: var(--cityflow-preview-bg) !important;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background: transparent !important;
    }

    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

preview_html = """
    <div class="launch-badge">
        <div class="app-icon">
            <img src="__LOGO_SRC__" alt="CityFlow app icon">
        </div>
        <div class="launch-copy">
            <div class="brand">CityFlow</div>
            <div class="coming">Coming soon on</div>
            <div class="stores">
                <span>App Store</span>
                <span>Google Play</span>
            </div>
        </div>
    </div>
    <div class="phone-stage">
        <div class="iphone-frame">
            <div class="iphone-side left"></div>
            <div class="iphone-side right"></div>
            <div class="iphone-top">
                <div class="speaker"></div>
                <div class="camera"></div>
            </div>
            <iframe src="/?mobile=1" title="CityFlow mobile preview"></iframe>
            <div class="home-indicator"></div>
        </div>
    </div>
    <style>
        html, body {
            margin: 0;
            background: #063B2B;
            font-family: Inter, system-ui, sans-serif;
            overflow: hidden;
        }

        .launch-badge {
            position: fixed;
            top: 28px;
            right: 30px;
            z-index: 20;
            display: flex;
            align-items: center;
            gap: 13px;
            padding: 12px 14px 12px 12px;
            border-radius: 22px;
            color: #F0FFF7;
            background:
                linear-gradient(135deg, rgba(2,8,23,0.72), rgba(6,78,59,0.62)),
                radial-gradient(circle at 20% 0%, rgba(74,222,128,0.30), transparent 50%);
            border: 1px solid rgba(187,247,208,0.30);
            box-shadow: 0 22px 54px rgba(0,0,0,0.34), inset 0 1px 0 rgba(255,255,255,0.12);
            backdrop-filter: blur(20px);
        }

        .app-icon {
            width: 58px;
            height: 58px;
            border-radius: 18px;
            display: grid;
            place-items: center;
            overflow: hidden;
            background: linear-gradient(135deg, #04111F, #064E3B);
            border: 1px solid rgba(187,247,208,0.35);
            box-shadow: 0 12px 28px rgba(34,197,94,0.22);
        }

        .app-icon img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .launch-copy {
            min-width: 158px;
        }

        .brand {
            font-size: 16px;
            line-height: 1;
            font-weight: 900;
            letter-spacing: 0;
        }

        .coming {
            margin-top: 5px;
            color: #BBF7D0;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }

        .stores {
            margin-top: 8px;
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }

        .stores span {
            padding: 6px 8px;
            border-radius: 9px;
            color: #ECFDF5;
            background: rgba(2,8,23,0.52);
            border: 1px solid rgba(187,247,208,0.20);
            font-size: 10px;
            font-weight: 900;
            white-space: nowrap;
        }

        .phone-stage {
            position: relative;
            width: 100%;
            height: 735px;
            min-height: 735px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
            box-sizing: border-box;
            background: #063B2B;
        }

        .phone-stage:before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
            background-size: 42px 42px;
            mask-image: radial-gradient(circle at 50% 42%, black 0%, transparent 72%);
            pointer-events: none;
            display: none;
        }

        .phone-stage:after {
            content: "";
            position: absolute;
            width: 470px;
            height: 470px;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            border-radius: 50%;
            background: radial-gradient(circle, rgba(34,197,94,0.30), transparent 68%);
            filter: blur(20px);
            pointer-events: none;
            display: none;
        }

        .iphone-frame {
            position: relative;
            width: 356px;
            height: 690px;
            padding: 13px;
            border-radius: 48px;
            background:
                linear-gradient(145deg, #111827, #020617 45%, #0F172A);
            border: 1px solid rgba(255,255,255,0.18);
            box-shadow:
                0 38px 90px rgba(0,0,0,0.45),
                inset 0 1px 0 rgba(255,255,255,0.22),
                inset 0 -1px 0 rgba(0,0,0,0.60);
            overflow: hidden;
        }

        .iphone-frame:before {
            content: "";
            position: absolute;
            inset: 6px;
            border-radius: 42px;
            border: 1px solid rgba(255,255,255,0.08);
            pointer-events: none;
            z-index: 3;
        }

        .iphone-top {
            position: absolute;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            width: 118px;
            height: 31px;
            border-radius: 0 0 20px 20px;
            background: #020617;
            z-index: 5;
            box-shadow: 0 3px 10px rgba(0,0,0,0.4);
        }

        .speaker {
            position: absolute;
            top: 10px;
            left: 37px;
            width: 43px;
            height: 5px;
            border-radius: 999px;
            background: #1F2937;
        }

        .camera {
            position: absolute;
            top: 8px;
            right: 22px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #38BDF8, #0F172A 55%);
            border: 1px solid #111827;
        }

        .iphone-side {
            position: absolute;
            width: 4px;
            border-radius: 999px;
            background: #111827;
            z-index: 1;
        }

        .iphone-side.left {
            left: -2px;
            top: 118px;
            height: 72px;
        }

        .iphone-side.right {
            right: -2px;
            top: 154px;
            height: 104px;
        }

        iframe {
            position: relative;
            width: 100%;
            height: 100%;
            border: 0;
            border-radius: 34px;
            background: #020817;
            overflow: hidden;
            z-index: 2;
        }

        .home-indicator {
            position: absolute;
            bottom: 22px;
            left: 50%;
            transform: translateX(-50%);
            width: 112px;
            height: 5px;
            border-radius: 999px;
            background: rgba(255,255,255,0.78);
            z-index: 5;
        }

        @media (max-width: 520px) {
            .phone-stage {
                align-items: flex-start;
                min-height: 700px;
            }

            .iphone-frame {
                transform: scale(0.94);
                transform-origin: top center;
            }

            .launch-badge {
                top: 12px;
                right: 12px;
                transform: scale(0.78);
                transform-origin: top right;
            }

        }
    </style>
    """

components.html(
    preview_html.replace("__LOGO_SRC__", logo_src),
    height=735,
    scrolling=False,
)
