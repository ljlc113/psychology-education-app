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
    st.markdown(
        """
        <style>
        /* Robust selectors to target Streamlit button elements across versions */
        .big-button .stButton>button,
        .big-button div.stButton>button,
        .big-button button {
            width: 100% !important;
            padding: 16px 26px !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            margin-bottom: 14px !important;

            background-color: #cfe8ff !important;   /* light blue */
            color: #003366 !important;              /* navy text */
            border: 1px solid #8bb8e8 !important;   /* soft border */

            transition: all 0.18s ease-in-out !important;
        }

        .big-button .stButton>button:hover,
        .big-button div.stButton>button:hover,
        .big-button button:hover {
            background-color: #b3d9ff !important;
            border-color: #66a3e0 !important;
            transform: translateY(-2px);
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
        }

        .big-button .stButton>button:focus,
        .big-button div.stButton>button:focus,
        .big-button button:focus {
            outline: 3px solid #66a3e0 !important;
        }

        /* Optional: slightly separate menu from page content */
        .left-menu-spacer { margin-bottom: 10px; padding: 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Put each button in its own container/div so css only affects these
    with st.container():
        st.markdown('<div class="big-button left-menu-spacer">', unsafe_allow_html=True)
        st.button(
            PAGE_PSYCHOMETRICS,
            key="btn_psychometrics_big",
            on_click=go_to,
            args=(PAGE_PSYCHOMETRICS,),
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="big-button left-menu-spacer">', unsafe_allow_html=True)
        st.button(
            PAGE_ECONOMIC,
            key="btn_economic_big",
            on_click=go_to,
            args=(PAGE_ECONOMIC,),
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="big-button left-menu-spacer">', unsafe_allow_html=True)
        st.button(
            PAGE_WORKING_MEMORY,
            key="btn_working_big",
            on_click=go_to,
            args=(PAGE_WORKING_MEMORY,),
        )
        st.markdown('</div>', unsafe_allow_html=True)
