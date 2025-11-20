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
    /* Target Streamlit buttons inside our container for full-width styling */
    .big-button .stButton>button {
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

    .big-button .stButton>button:hover {
        background-color: #b3d9ff !important;
        border-color: #66a3e0 !important;
        transform: translateY(-2px);
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.12);
    }

    .big-button .stButton>button:focus {
        outline: 3px solid #66a3e0 !important;
    }

    /* Ensure the container itself doesn't add extra padding */
    .big-button { padding: 0; }
    </style>
    """, unsafe_allow_html=True)

    # Each button inside a div with class "big-button" so CSS only affects these
    with st.container():
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        if st.button(PAGE_PSYCHOMETRICS, key="btn_psychometrics_big"):
            go_to(PAGE_PSYCHOMETRICS)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        if st.button(PAGE_ECONOMIC, key="btn_economic_big"):
            go_to(PAGE_ECONOMIC)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        if st.button(PAGE_WORKING_MEMORY, key="btn_working_big"):
            go_to(PAGE_WORKING_MEMORY)
        st.markdown('</div>', unsafe_allow_html=True)


# ----- Layout and routing -----
left_col, right_col = st.columns([1.0, 3.5])

if st.session_state.page == PAGE_LANDING:
    with left_col:
        render_landing_left()

    with right_col:
        st.markdown("<h1 style='margin-bottom:8px;'>Cognition Educational App</h1>", unsafe_allow_html=True)
        st.write("Welcome — choose a topic from the left to continue.")
        st.write("This is the landing page for the educational app. Each button will open a simple page for that topic.")
        st.divider()

elif st.session_state.page == PAGE_PSYCHOMETRICS:
    with right_col:
        st.header(PAGE_PSYCHOMETRICS)
        st.write("Placeholder page for Psychometrics content.")
        st.divider()
        if st.button("← Back to landing", key="back_from_psych"):
            go_to(PAGE_LANDING)

    with left_col:
        st.markdown("### Navigation")
        if st.button("Home", key="home_from_psych"):
            go_to(PAGE_LANDING)

elif st.session_state.page == PAGE_ECONOMIC:
    with right_col:
        st.header(PAGE_ECONOMIC)
        st.write("Placeholder page for Economic Choices and Utility Curves.")
        st.divider()
        if st.button("← Back to landing", key="back_from_econ"):
            go_to(PAGE_LANDING)

    with left_col:
        st.markdown("### Navigation")
        if st.button("Home", key="home_from_econ"):
            go_to(PAGE_LANDING)

elif st.session_state.page == PAGE_WORKING_MEMORY:
    with right_col:
        st.header(PAGE_WORKING_MEMORY)
        st.write("Placeholder page for Working Memory content.")
        st.divider()
        if st.button("← Back to landing", key="back_from_working"):
            go_to(PAGE_LANDING)

    with left_col:
        st.markdown("### Navigation")
        if st.button("Home", key="home_from_working"):
            go_to(PAGE_LANDING)

else:
    st.error("Unknown page. Returning to home.")
    go_to(PAGE_LANDING)
