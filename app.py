import streamlit as st

# Set page config
st.set_page_config(page_title="Cognition Educational App", layout="wide")

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "landing"

# Page labels
PAGES = {
    "Psychometrics": "Psychometrics",
    "Economic Choices + Utility Curves": "Economic Choices + Utility Curves",
    "Working Memory": "Working Memory",
}

# Helper to render the landing page
def show_landing():
    left_col, right_col = st.columns([1, 3])

    with left_col:
        st.markdown("### Sections")
        # Buttons that set the current page in session state
        if st.button("Psychometrics", key="btn_psycho"):
            st.session_state.page = "Psychometrics"
        if st.button("Economic Choices + Utility Curves", key="btn_econ"):
            st.session_state.page = "Economic Choices + Utility Curves"
        if st.button("Working Memory", key="btn_wm"):
            st.session_state.page = "Working Memory"

    with right_col:
        st.title("Cognition Educational App")
        st.write("Welcome — choose a section from the left to explore the topic.")


# Helper to render a content page with a back-arrow button
def show_content(page_label: str):
    left_col, right_col = st.columns([1, 3])

    with left_col:
        # Keep a small navigation area on the left for consistency
        st.markdown("### Navigation")
        # Optional: show a disabled listing of other pages
        for k in PAGES:
            if k == page_label:
                st.markdown(f"- **{k}**")
            else:
                st.markdown(f"- {k}")

    with right_col:
        st.header(page_label)
        st.write(f"This page will contain content about **{page_label}**.")
        if st.button("← Back to landing", key=f"back_{page_label}"):
            st.session_state.page = "landing"


# Router - decide which view to show
if st.session_state.page == "landing":
    show_landing()
elif st.session_state.page in PAGES:
    show_content(st.session_state.page)
else:
    # Fallback to landing if something unexpected appears in session state
    st.session_state.page = "landing"
    show_landing()


# Footer small note
st.sidebar.write("\n\nMade for the psychology-education-app repository")
