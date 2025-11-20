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

# ----- Helper: render landing left buttons -----
def render_landing_left():
    """
    Render the three landing buttons on the left column.
    Each button navigates to its page.
    """
    st.markdown("### Menu")
    # Use individual buttons with on_click callbacks to persist navigation
    if st.button(PAGE_PSYCHOMETRICS, key="btn_psychometrics"):
        go_to(PAGE_PSYCHOMETRICS)
    if st.button(PAGE_ECONOMIC, key="btn_economic"):
        go_to(PAGE_ECONOMIC)
    if st.button(PAGE_WORKING_MEMORY, key="btn_working"):
        go_to(PAGE_WORKING_MEMORY)

# ----- Layout and routing -----
# Create two columns: narrow left for navigation, wide right for content
left_col, right_col = st.columns([1.0, 3.5])

# Landing page layout
if st.session_state.page == PAGE_LANDING:
    with left_col:
        # Show the three buttons on the left
        render_landing_left()

    with right_col:
        # Right side landing title
        st.markdown("<h1 style='margin-bottom:8px;'>Cognition Educational App</h1>", unsafe_allow_html=True)
        st.write("Welcome — choose a topic from the left to continue.")
        st.write("This is the landing page for the educational app. Each button will open a simple page for that topic.")
        st.divider()

# Psychometrics page
elif st.session_state.page == PAGE_PSYCHOMETRICS:
    # Content column: show page title and a back arrow
    with right_col:
        st.header(PAGE_PSYCHOMETRICS)
        st.write("Placeholder page for Psychometrics content.")
        st.write("Add visualizations, interactive exercises, or theory here.")
        st.divider()
        # Back button
        if st.button("← Back to landing", key="back_from_psych"):
            go_to(PAGE_LANDING)

    # Left column can optionally offer the same landing buttons for quick jumps
    with left_col:
        st.markdown("### Navigation")
        # Small navigation convenience: optional quick links (do not override primary flow)
        if st.button("Home", key="home_from_psych"):
            go_to(PAGE_LANDING)

# Economic Choices + Utility Curves page
elif st.session_state.page == PAGE_ECONOMIC:
    with right_col:
        st.header(PAGE_ECONOMIC)
        st.write("Placeholder page for Economic Choices and Utility Curves content.")
        st.write("Add diagrams of utility curves, choice tasks, or interactive widgets here.")
        st.divider()
        if st.button("← Back to landing", key="back_from_econ"):
            go_to(PAGE_LANDING)

    with left_col:
        st.markdown("### Navigation")
        if st.button("Home", key="home_from_econ"):
            go_to(PAGE_LANDING)

# Working Memory page
elif st.session_state.page == PAGE_WORKING_MEMORY:
    with right_col:
        st.header(PAGE_WORKING_MEMORY)
        st.write("Placeholder page for Working Memory content.")
        st.write("Add span tasks, explanations, or demos here.")
        st.divider()
        if st.button("← Back to landing", key="back_from_working"):
            go_to(PAGE_LANDING)

    with left_col:
        st.markdown("### Navigation")
        if st.button("Home", key="home_from_working"):
            go_to(PAGE_LANDING)

# Safety fallback (shouldn't trigger)
else:
    st.error("Unknown page. Returning to home.")
    go_to(PAGE_LANDING)
