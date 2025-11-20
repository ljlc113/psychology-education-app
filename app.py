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

# Ensure psychometrics tab state exists
if "psych_tab" not in st.session_state:
    st.session_state.psych_tab = "Default Example"

# persistent simulator parameters (used so sliders can appear below the plot)
if "psych_mu" not in st.session_state:
    st.session_state.psych_mu = 0.0
if "psych_sigma" not in st.session_state:
    st.session_state.psych_sigma = 1.0
if "psych_amp" not in st.session_state:
    st.session_state.psych_amp = 1.0


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
        # when entering the Psychometrics section from landing, default to Default Example
        st.session_state.psych_tab = "Default Example"
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
        st.markdown("<h1 style='margin-bottom:8px;'>Computational Models of Perception, Choice, and Memory</h1>", unsafe_allow_html=True)
        st.write("This app provides an interactive introduction to how humans perceive information, evaluate uncertain outcomes, and maintain short-term memories. Across the modules, you will explore how stimulus–response relationships are modeled in psychometrics, how economics describes rational and real-world decisions under uncertainty, how the brain normalizes value based on context, and how working memory can be stored silently through synaptic mechanisms. Use the sidebar to move through each section, adjust parameters, and observe how models and neural theories behave.")
        st.divider()

# Psychometrics page - replaced filler with two internal tabs and a simulator
elif st.session_state.page == PAGE_PSYCHOMETRICS:
    # Left column: Home + psychometrics internal tabs
    with left_col:
        st.markdown("### Navigation")
        if st.button("Home", key="home_from_psych"):
            go_to(PAGE_LANDING)

        st.markdown("---")
        st.markdown("### Psychometrics")
        # radio acts as the two internal tabs under the Home button
        # default index depends on current session state
        options = ["Default Example", "Simulator"]
        default_index = 0 if st.session_state.get("psych_tab", "Default Example") == "Default Example" else 1
        psych_choice = st.radio("", options, index=default_index, key="psych_radio")
        # store selected subtab in session state so we can persist between reruns
        st.session_state.psych_tab = psych_choice

    # Right column: render content for the selected psychometrics subtab
    with right_col:
        st.header(PAGE_PSYCHOMETRICS)

        if st.session_state.psych_tab == "Default Example":
            st.subheader("Default Example")
            st.write("This is a placeholder for the Default Example. Add explanatory text, examples, or starter visuals here.")
            st.divider()
            if st.button("← Back to landing", key="back_from_psych_default"):
                go_to(PAGE_LANDING)

        else:
            st.subheader("Simulator: Cumulative Gaussian")
            st.write("Interactive simulator showing a cumulative Gaussian (CDF). Use the sliders below the graph to change parameters.")

            # --- Plot using current stored parameters (so sliders can appear below the plot) ---
            import numpy as np
            import matplotlib.pyplot as plt

            # read parameters from session state (these will be updated by sliders below)
            mu_val = st.session_state.get("psych_mu", 0.0)
            sigma_val = st.session_state.get("psych_sigma", 1.0)
            amp_val = st.session_state.get("psych_amp", 1.0)

            x = np.linspace(-6, 6, 400)

            def cum_gauss(x, mu, sigma):
                # CDF of normal distribution using the error function.
                # Some numpy builds don't expose np.erf; use math.erf applied elementwise
                from math import erf
                # If `x` is an array-like, compute erf elementwise with a list comprehension
                arr = np.array([erf((float(xi) - mu) / (sigma * np.sqrt(2))) for xi in x])
                return 0.5 * (1 + arr)

            y = amp_val * cum_gauss(x, mu_val, sigma_val)

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(x, y, lw=2)
            ax.set_xlabel("x")
            ax.set_ylabel("Cumulative probability")
            ax.set_ylim(-0.05, 1.05 * max(1.0, amp_val))
            ax.set_title(f"Cumulative Gaussian — μ={mu_val:.2f}, σ={sigma_val:.2f}")
            ax.grid(alpha=0.2)

            st.pyplot(fig)

            st.markdown("---")
            # --- Sliders BELOW the graph (they update session_state) ---
            mu_new = st.slider("Mean (μ)", -3.0, 3.0, mu_val, step=0.05, key="psych_mu_slider")
            sigma_new = st.slider("Std dev (σ)", 0.05, 3.0, sigma_val, step=0.05, key="psych_sigma_slider")
            amp_new = st.slider("Amplitude", 0.1, 3.0, amp_val, step=0.05, key="psych_amp_slider")

            # Persist new values so the plot uses them on the next rerun
            st.session_state.psych_mu = mu_new
            st.session_state.psych_sigma = sigma_new
            st.session_state.psych_amp = amp_new

            st.divider()
            if st.button("← Back to landing", key="back_from_psych_sim"):
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
