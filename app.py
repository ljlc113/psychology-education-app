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
if "psych_alpha" not in st.session_state:
    st.session_state.psych_alpha = 0.0
if "psych_beta" not in st.session_state:
    st.session_state.psych_beta = 3.0
if "psych_gamma" not in st.session_state:
    st.session_state.psych_gamma = 0.0
if "psych_lambda" not in st.session_state:
    st.session_state.psych_lambda = 0.02
if "psych_amp" not in st.session_state:
    st.session_state.psych_amp = 1.0
if "psych_ntrials" not in st.session_state:
    st.session_state.psych_ntrials = 40

# storage for simulated dataset
if "psych_sim_data" not in st.session_state:
    st.session_state.psych_sim_data = None


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
            st.subheader("Simulator: Psychometric function & simulated data")
            st.write("Interactive simulator showing a psychometric function (cumulative Gaussian) with simulated binary response data. Use the sliders below the graph to change parameters and press 'Simulate data' to draw a new dataset.")

            # --- Plot using current stored parameters (so sliders can appear below the plot) ---
            import numpy as np
            import matplotlib.pyplot as plt
            from math import erf

            # read parameters from session state (these will be updated by sliders below)
            alpha = st.session_state.get("psych_alpha", 0.0)  # threshold
            beta = st.session_state.get("psych_beta", 3.0)    # slope
            gamma = st.session_state.get("psych_gamma", 0.0)  # guess rate
            lambd = st.session_state.get("psych_lambda", 0.02) # lapse rate
            ntrials = int(st.session_state.get("psych_ntrials", 40))

            # Stimulus levels (can be adjusted later)
            stim_levels = np.linspace(-3, 3, 9)

            # psychometric function: cumulative normal with slope beta
            def Phi(z):
                # standard normal CDF using math.erf but applied elementwise.
                # math.erf doesn't accept numpy arrays, so compute elementwise and return an array.
                from math import erf as _erf
                z_arr = np.asarray(z)
                erf_vals = np.array([_erf(float(zi) / np.sqrt(2)) for zi in z_arr])
                return 0.5 * (1 + erf_vals)

            def psychometric_fn(x, alpha, beta, gamma=0.0, lambd=0.02):
                # common parameterization: p = gamma + (1 - gamma - lambda) * Phi((x - alpha) * beta)
                z = (x - alpha) * beta
                return gamma + (1 - gamma - lambd) * Phi(z)

            # range for plotting continuous curve
            x = np.linspace(stim_levels[0] - 1.0, stim_levels[-1] + 1.0, 400)
            y = psychometric_fn(x, alpha, beta, gamma, lambd)

            # If simulated data exists in session state, use it; else create an initial deterministic dataset
            sim_data = st.session_state.get("psych_sim_data", None)

            if sim_data is None:
                # generate expected proportions (no noise) so user sees points aligned to curve initially
                prop = psychometric_fn(stim_levels, alpha, beta, gamma, lambd)
                counts = (prop * ntrials).astype(int)
                sim_data = {"stim": stim_levels, "successes": counts, "trials": np.full_like(counts, ntrials)}
                st.session_state.psych_sim_data = sim_data

            # Plot
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x, y, lw=2, label="Psychometric curve")

            # plot simulated data points (proportion correct) with error bars
            stim = np.array(st.session_state.psych_sim_data["stim"])
            succ = np.array(st.session_state.psych_sim_data["successes"])
            trials = np.array(st.session_state.psych_sim_data["trials"])
            prop_obs = succ / trials
            ax.plot(stim, prop_obs, 'o', label="Simulated data")

            ax.set_xlabel("Stimulus")
            ax.set_ylabel("Proportion correct")
            ax.set_ylim(-0.05, 1.05)
            ax.set_title(f"Psychometric function — α={alpha:.2f}, β={beta:.2f}, γ={gamma:.2f}, λ={lambd:.3f}")
            ax.grid(alpha=0.2)
            ax.legend()

            st.pyplot(fig)

            st.markdown("---")

            # --- Sliders BELOW the graph (they update session_state) ---
            col1, col2 = st.columns([1, 1])
            with col1:
                alpha_new = st.slider("Threshold (α)", -2.5, 2.5, float(alpha), step=0.01, key="psych_alpha_slider")
                beta_new = st.slider("Slope (β)", 0.1, 10.0, float(beta), step=0.1, key="psych_beta_slider")
            with col2:
                gamma_new = st.slider("Guess rate (γ)", 0.0, 0.5, float(gamma), step=0.01, key="psych_gamma_slider")
                lambda_new = st.slider("Lapse rate (λ)", 0.0, 0.2, float(lambd), step=0.005, key="psych_lambda_slider")

            ntrials_new = st.slider("Trials per stimulus", 1, 500, int(ntrials), step=1, key="psych_ntrials_slider")

            # Persist new values so the plot uses them on the next rerun
            st.session_state.psych_alpha = alpha_new
            st.session_state.psych_beta = beta_new
            st.session_state.psych_gamma = gamma_new
            st.session_state.psych_lambda = lambda_new
            st.session_state.psych_ntrials = int(ntrials_new)

            # Simulate data button to draw binomial noisy data given the current parameters
            if st.button("Simulate data", key="psych_simulate_button"):
                rng = np.random.default_rng()
                p_true = psychometric_fn(stim_levels, alpha_new, beta_new, gamma_new, lambda_new)
                successes = rng.binomial(ntrials_new, p_true)
                st.session_state.psych_sim_data = {"stim": stim_levels, "successes": successes, "trials": np.full_like(successes, ntrials_new)}
                st.experimental_rerun()

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
