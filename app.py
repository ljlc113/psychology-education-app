# app.py
import streamlit as st

# ----- Page / app config -----
st.set_page_config(page_title="Cognition Educational App", layout="wide")

# ----- Constants -----
PAGE_LANDING = "landing"
PAGE_PSYCHOMETRICS = "Psychometrics"
PAGE_ECONOMIC = "Economic Choices + Utility Curves"
PAGE_WORKING_MEMORY = "Working Memory"

# ----- Initialize session state -----
if "page" not in st.session_state:
    st.session_state.page = PAGE_LANDING

def go_to(page_name: str):
    """Set the current page in session state."""
    st.session_state.page = page_name

# ----- Landing left with big styled buttons (light blue + hover) -----
def render_landing_left():
    st.markdown("""
        <style>
        .big-button .stButton>button {
            width: 100% !important;
            padding: 16px 26px !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            margin-bottom: 14px !important;
            transition: all 0.15s ease-in-out !important;
        }

        .big-button .stButton>button:hover {
            background-color: #f0f0f0 !important;   /* subtle hover highlight */
            transform: translateY(-2px);
            box-shadow: 0px 4px 10px rgba(0,0,0,0.12);
        }
        </style>
    """, unsafe_allow_html=True)

    # Use on_click to ensure single-click navigation
    with st.container():
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        st.button(
            PAGE_PSYCHOMETRICS,
            key="btn_psych",
            on_click=go_to,
            args=(PAGE_PSYCHOMETRICS,)
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        st.button(
            PAGE_ECONOMIC,
            key="btn_econ",
            on_click=go_to,
            args=(PAGE_ECONOMIC,)
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        st.button(
            PAGE_WORKING_MEMORY,
            key="btn_working",
            on_click=go_to,
            args=(PAGE_WORKING_MEMORY,)
        )
        st.markdown('</div>', unsafe_allow_html=True)
