import streamlit as st

PURPLE = "#8B5CF6"
PURPLE_DARK = "#6D28D9"
PURPLE_LIGHT = "#C4B5FD"

DARK = {
    "bg": "#0E0B16",
    "card": "#1A1625",
    "text": "#F1EEF9",
    "muted": "#A79FC0",
    "border": "#2E2740",
}

LIGHT = {
    "bg": "#FAF9FC",
    "card": "#FFFFFF",
    "text": "#1E1B2E",
    "muted": "#6B6480",
    "border": "#E4DFF2",
}


def inject_theme(dark_mode: bool):
    t = DARK if dark_mode else LIGHT
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {t['bg']};
            color: {t['text']};
        }}
        section[data-testid="stSidebar"] {{
            background-color: {t['card']};
            border-right: 1px solid {t['border']};
        }}
        div[data-testid="stFileUploader"] {{
            background-color: {t['card']};
            border: 1.5px dashed {PURPLE};
            border-radius: 10px;
            padding: 10px;
        }}
        .app-card {{
            background-color: {t['card']};
            border: 1px solid {t['border']};
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        .chip-match {{
            display:inline-block; padding:5px 12px; margin:4px;
            border-radius:100px; border:1px solid #4ADE80; color:#4ADE80;
            font-size:12.5px;
        }}
        .chip-miss {{
            display:inline-block; padding:5px 12px; margin:4px;
            border-radius:100px; border:1px solid #F87171; color:#F87171;
            font-size:12.5px;
        }}
        .gauge-wrap {{
            background-color: {t['border']};
            border-radius: 100px;
            height: 14px;
            width: 100%;
            overflow: hidden;
            margin-top: 6px;
        }}
        .gauge-fill {{
            height: 100%;
            border-radius: 100px;
            background: linear-gradient(90deg, {PURPLE_DARK}, {PURPLE}, {PURPLE_LIGHT});
        }}
        .score-label {{
            font-size: 13px; color: {t['muted']}; text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .score-num {{
            font-size: 42px; font-weight: 700; color: {PURPLE};
        }}
        button[kind="primary"] {{
            background-color: {PURPLE} !important;
            border-color: {PURPLE} !important;
        }}

        /* Toggle switch (dark/light mode) — was invisible in light mode */
        [data-baseweb="switch"] {{
            background-color: {t['border']} !important;
        }}
        [data-baseweb="switch"][aria-checked="true"] {{
            background-color: {PURPLE} !important;
        }}

        /* Sidebar collapse arrow icon — was invisible in light mode */
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="collapsedControl"] svg,
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="baseButton-headerNoPadding"] svg {{
            fill: {t['text']} !important;
        }}

        /* Chat bubbles — fixes invisible chat in light mode */
        [data-testid="stChatMessage"] {{
            background-color: {t['card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 10px !important;
        }}
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] div,
        [data-testid="stChatMessage"] span {{
            color: {t['text']} !important;
        }}
        [data-testid="stChatInput"] textarea {{
            color: {t['text']} !important;
            background-color: {t['card']} !important;
        }}
    </style>
    """, unsafe_allow_html=True)