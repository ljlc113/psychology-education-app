# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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
    st.session_state.psych_tab = "Introduction"

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
        st.session_state.psych_tab = "Introduction"
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
        # radio acts as the internal tabs under the Home button (three tabs)
        options = ["Introduction", "Default Example", "Simulator"]
        # compute default index from current session state
        current = st.session_state.get("psych_tab", "Introduction")
        default_index = options.index(current) if current in options else 0
        psych_choice = st.radio("", options, index=default_index, key="psych_radio")
        # store selected subtab in session state so we can persist between reruns
        st.session_state.psych_tab = psych_choice

    # Right column: render content for the selected psychometrics subtab
    with right_col:
        st.header(PAGE_PSYCHOMETRICS)

        if st.session_state.psych_tab == "Introduction":
            st.subheader("Psychometrics")
            st.write("Psychometrics examines the relationship between stimulus properties and behavioral responses, using curves and statistical models to quantify perception and decision thresholds.")
            st.divider()

        elif st.session_state.psych_tab == "Default Example":
            st.subheader("See a psychometric function interpreted in the context of a study")
            st.markdown("**Study:** Perimetric sensitivity and response variability in glaucoma (Miranda & Henson, 2008)")

            st.write(
                "This study looked at how reliably people with glaucoma detected brief flashes of light of different brightness. It compared two testing methods to see which gave more consistent and sensitive results across parts of the visual field."
            )

            st.markdown(
                "**Method.** A flash of light of variable intensity was presented repeatedly at a fixed location in the visual field of a subject who reported whether the flash was visible. There were 3–20 trials at each stimulus level."
            )

            # Display embedded study figure from repo assets
            st.image("assets/miranda_henson.png", caption="Examples of psychometric data from Miranda & Henson (2008)")

            st.write(
                "These plots show how the probability of seeing a flash changes with its brightness for four example locations. In some cases the two testing methods agree closely, while in others one method shows lower sensitivity or more variability."
            )

            st.markdown("---")

            st.markdown("""
| **Feature**        | **Interpretation (max 2 sentences)** |
|-------------------|----------------------------------------|
| **Threshold (α)** | The threshold marks the stimulus intensity where the observer begins to reliably detect the flash. In glaucoma, higher thresholds reflect reduced sensitivity at that location. |
| **Slope (β)**     | The slope indicates how quickly detection improves as intensity increases. Steeper slopes mean responses are more consistent and less variable. |
| **Guess rate (γ)**| The guess rate reflects the baseline probability of reporting a flash when it is too dim to see. It is usually low in this task and relates to response bias. |
| **Lapse rate (λ)**| The lapse rate captures occasional misses even at bright intensities. These lapses can reflect momentary inattention or blinking and reduce the maximum performance. |
""")

            st.divider()

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

            # Interactive Plot using Plotly with hover tooltips for simulated points
            import plotly.graph_objects as go

            stim = np.array(st.session_state.psych_sim_data["stim"]) if st.session_state.psych_sim_data is not None else stim_levels
            succ = np.array(st.session_state.psych_sim_data["successes"]) if st.session_state.psych_sim_data is not None else (psychometric_fn(stim, alpha, beta, gamma, lambd) * ntrials).astype(int)
            trials = np.array(st.session_state.psych_sim_data["trials"]) if st.session_state.psych_sim_data is not None else np.full_like(succ, ntrials)
            prop_obs = succ / trials

            fig = go.Figure()
            # psychometric curve
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Psychometric curve'))
            # simulated data points with hovertemplate
            hover_tmpl = "This is a trial where stimulus intensity is %{x:.2f} and proportion correct is %{y:.2f}<extra></extra>"
            fig.add_trace(go.Scatter(x=stim, y=prop_obs, mode='markers', name='Simulated data', marker=dict(color='orange', size=10), hovertemplate=hover_tmpl))

            fig.update_layout(xaxis_title='Stimulus', yaxis_title='Proportion correct', yaxis=dict(range=[-0.05, 1.05]), title=f"Psychometric function — α={alpha:.2f}, β={beta:.2f}, γ={gamma:.2f}, λ={lambd:.3f}")

            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # --- Sliders BELOW the graph (they update session_state) ---
            col1, col2 = st.columns([1, 1])
            with col1:
                alpha_new = st.slider("Threshold (α)", -2.5, 2.5, float(alpha), step=0.01, key="psych_alpha_slider")
                st.caption("Sliding left lowers the threshold, shifting the curve leftward and making the stimulus easier to detect; sliding right raises the threshold, shifting the curve rightward and indicating reduced sensitivity.")
                st.caption("In the Default Example, higher α reflected reduced sensitivity at affected visual-field locations.")
                beta_new = st.slider("Slope (β)", 0.1, 10.0, float(beta), step=0.1, key="psych_beta_slider")
                st.caption("Sliding left makes the curve shallower, increasing variability in responses; sliding right steepens the curve, making performance rise more abruptly.")
                st.caption("In the Default Example, steeper β meant more consistent detection and reduced variability.")
            with col2:
                gamma_new = st.slider("Guess rate (γ)", 0.0, 0.5, float(gamma), step=0.01, key="psych_gamma_slider")
                st.caption("Sliding left lowers the baseline probability of responding ‘seen’ when the flash is very dim; sliding right raises this baseline, mimicking more guessing or bias.")
                st.caption("In the Default Example, γ was low because observers rarely guessed when the flash was undetectable.")
                lambda_new = st.slider("Lapse rate (λ)", 0.0, 0.2, float(lambd), step=0.005, key="psych_lambda_slider")
                st.caption("Sliding left reduces lapses, allowing the curve to reach closer to 1.0 at high intensities; sliding right increases lapses, lowering the top of the curve.")
                st.caption("In the Default Example, non-zero λ reflected occasional misses even for bright stimuli.")

            ntrials_new = st.slider("Trials per stimulus", 1, 500, int(ntrials), step=1, key="psych_ntrials_slider")
            st.caption("Sliding left reduces the number of trials and increases noise in the observed proportions; sliding right provides more trials and smoother estimates.")

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
                st.success("Simulated new dataset.")

            st.divider()


# Economic Choices + Utility Curves page
elif st.session_state.page == PAGE_ECONOMIC:
    # ---------------------------------------
    # Helper utilities
    # ---------------------------------------
    def _two_cols():
        return st.columns(2)


    def _show_eq(title: str, latex: str):
        st.markdown(f"### {title}")
        st.latex(latex)


    def _plot_simple(x, y, xlabel, ylabel, title):
        import matplotlib.pyplot as plt   # <-- REQUIRED
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        st.pyplot(fig, clear_figure=True)


    def _plot_multi(x, ys, labels, xlabel, ylabel, title):
        fig, ax = plt.subplots()
        for y, lab in zip(ys, labels):
            ax.plot(x, y, label=lab)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        st.pyplot(fig, clear_figure=True)

    # Left column: econ navigation tabs
    with left_col:
        st.markdown("### Navigation")
        if st.button("Home", key="home_from_econ"):
            go_to(PAGE_LANDING)

        st.markdown("---")
        st.markdown("### Economic Choices + Utility Curves")
        econ_tabs = ["Introduction", "Expected Value (EV)", "Expected Utility (EU)", 
                     "Prospect Theory (PT)", "Normalization"]

        if "econ_tab" not in st.session_state:
            st.session_state.econ_tab = "Introduction"

        current_econ = st.session_state.econ_tab
        default_econ_idx = econ_tabs.index(current_econ) if current_econ in econ_tabs else 0

        econ_choice = st.radio("", econ_tabs, index=default_econ_idx, key="econ_radio")
        st.session_state.econ_tab = econ_choice

    # Right column: content for selected econ tab
    with right_col:
        st.header("Economic Choices + Utility Curves")

        if st.session_state.econ_tab == "Introduction":
            st.subheader("How do we make economic decisions?")
            st.markdown(
    """
- **Normative models** explain how people *should* decide if they're rational.
  - *Example:* Expected Value (EV) theory says that when faced with uncertain outcomes, choose the option with the highest expected value.
- **But people often violate EV predictions** and choose options that are not normatively optimal.
- We are **risk-averse**, **loss-averse**, and **sensitive to framing**.
- **Descriptive models** explain how people *actually* behave, often deviating from EV because of psychological biases.
    """
)

            st.markdown("---")

            # Insert the exact Overview text provided by the user
            st.subheader("Decision Models")
            st.markdown(
            """
            - **Expected Value (EV):** linear utility, linear probability.
            - **Expected Utility (EU):** nonlinear utility over outcomes.
            - **Prospect Theory (PT):** reference-dependent value and nonlinear probability weighting.

            **Normalization techniques (applied in a choosing restaurants example):**

            - **Range normalization** → linear scaling, sensitive to min and max.
            - **Divisive normalization** → relative to the mean, not bounded.
            - **Recurrent divisive normalization** → bounded, compresses large values.
            - **Adaptive gain / logistic value** → nonlinear, highlights contrasts around the mean.
            """
            )

        elif st.session_state.econ_tab == "Expected Value (EV)":
                st.subheader("Expected Value (EV)")
                st.markdown("Expected value theory: when faced with uncertain outcomes, you should choose the option with the highest expected value. ")
                st.markdown("EV assumes **linear utility** and **linear probability weighting**. It is computed by multiplying the value of an outcome by its probability.")

                _show_eq("EV of two-outcome lottery, where v1 = probability p and v2 = probability 1-p", r"EV = p \times v_1 + (1 - p) \times v_2")

                st.divider()
                st.subheader("Worked examples")
                # Example 1: Lottery ticket .01% chance to win 100,000
                p1 = 0.0001
                v1_1, v2_1 = 100_000.0, 0.0
                ev1 = p1 * v1_1 + (1 - p1) * v2_1

                # Example 2: 50% chance +55, 50% chance -50
                p2 = 0.5
                v1_2, v2_2 = 55.0, -50.0
                ev2 = p2 * v1_2 + (1 - p2) * v2_2

                colA, colB = st.columns(2)
                with colA:
                    st.markdown("**Lottery ticket:** 0.01% chance to win 100,000; otherwise 0")
                    st.latex(r"\\mathrm{EV} = 0.0001 \times 100{,}000 + 0.9999 \times 0 = 10")
                    st.metric("EV", f"{ev1:.2f}")
                    st.markdown("**What does this mean?** You should pursue this gamble, if the ticket costs less than 10 dollars.")
                with colB:
                    st.markdown("**50–50 gamble:** +55 with 50%, −50 with 50%")
                    st.latex(r"\\mathrm{EV} = 0.5 \times 55 + 0.5 \times (-50) = 2.5")
                    st.metric("EV", f"{ev2:.2f}")
                    st.markdown("**What does this mean?** You should pursue this gamble, because expected value is positive.")

                st.divider()
                st.subheader("Graphics of EV utility and probability weighting functions:")
            # Utility and probability equations with their graphs side by side
                col1, col2 = _two_cols()
                with col1:
                    st.latex(r"u(x) = x")
                    xr = np.linspace(-100, 100, 400)
                    _plot_simple(xr, xr, "Outcome x", "Utility u(x)", "Linear utility: u(x)=x")

                with col2:
                    st.latex(r"w(p) = p")
                    pr = np.linspace(0, 1, 200)
                    _plot_simple(pr, pr, "Probability p", "Weight w(p)", "Identity weighting: w(p)=p")

        elif st.session_state.econ_tab == "Expected Utility (EU)":
            st.subheader("Expected Utility (EU)")
            st.markdown("""
            **Expected utility theory:** rational agents should evaluate choices by multiplying the utility of outcomes by their probabilities and picking the highest total.
            - People assign each possible outcomes a utility (a subjective measure of value)
            - They treat probabilities objectively
            - They choose the option that maximizes expected utility
            - It assumes stable, consistent, and context-independent preferences
                    """
            )
            st.markdown(
                "EU allows **nonlinear utility**, which EV does not consider. However, note that **linear probability weighting** remains an assumption. "
                "We use a sign–power (CRRA-style) function that raises value to the power of α, "
                "capturing diminishing sensitivity for gains and losses."
            )
            st.latex(r"EU(v) = \operatorname{sign}(v)\,|v|^{\alpha}")

            # -----------------------------
            # 4. Slider for curvature
            # -----------------------------
            alpha = st.slider("Curvature α", 0.2, 2.0, 0.8, 0.05)

            st.caption(
                "Sliding left (lower α) makes the utility curve more pronouncedly curved, meaning outcomes grow in subjective value more slowly; "
                "sliding right (higher α) straightens the curve so large outcomes grow in utility more quickly."
            )
            st.caption(
                "When curvature exceeds 1, the function becomes convex for positive outcomes—this means the decision-maker becomes risk-seeking in the gain domain, "
                "valuing large gains disproportionately more than small ones."
            )


            st.divider()

            # -----------------------------
            # 5. Graphics
            # -----------------------------
            st.subheader("Graphics of EU utility and probability weighting:")

            col_eq1, col_eq2 = st.columns(2)

            with col_eq1:
                st.latex(r"u(v) = (1 \text{ if } v\ge0 \text{ else } -1)\cdot |v|^{\alpha}")
                xr = np.linspace(-100, 100, 400)
                u_vals = np.array([(1 if v >= 0 else -1) * (abs(v) ** alpha) for v in xr], dtype=float)
                _plot_simple(xr, u_vals, "Outcome v", "Utility u(v)", f"Nonlinear utility (α={alpha:.2f})")

            with col_eq2:
                st.latex(r"w(p) = p")
                pr = np.linspace(0, 1, 200)
                _plot_simple(pr, pr, "Probability p", "Weight w(p)", "Identity weighting: w(p)=p")

            st.divider()

            # -----------------------------
            # 6. Worked Examples
            # -----------------------------
            st.subheader("Worked examples (EU)")

            # utility function
            def u_func(v, alpha):
                return (1 if v >= 0 else -1) * (abs(v) ** alpha)

            # expected utility of two-outcome gamble
            def EU_value(p, x1, x2):
                return p * u_func(x1, alpha) + (1 - p) * u_func(x2, alpha)

            # Example 1
            p1 = 0.0001
            EU1 = EU_value(p1, 100_000.0, 0.0)

            # Example 2
            p2 = 0.5
            EU2 = EU_value(p2, 55.0, -50.0)

            colA, colB = st.columns(2)

            with colA:
                st.markdown("**Lottery ticket:** 0.01% chance to win 100,000; otherwise 0")
                st.latex(r"EU = p\,u(100{,}000) + (1-p)\,u(0)")
                st.metric("EU (lottery)", f"{EU1:.2f}")

            with colB:
                st.markdown("**50–50 gamble:** +55 with 50%, −50 with 50%")
                st.latex(r"EU = 0.5\,u(55) + 0.5\,u(-50)")
                st.metric("EU (gamble)", f"{EU2:.2f}")


        elif st.session_state.econ_tab == "Prospect Theory (PT)":
            st.subheader("Prospect Theory (PT)")
            st.markdown("""
            **Prospect theory:** models real human behavior stemming from the idea that we have both internal subjective estimates of value AND probability.
            - PT uses a **reference-dependent value function** and **nonlinear probability weighting**. It has distinct domains with different functions for behaviors if they are considered a LOSS or GAIN.
            - **Loss aversion:** losses loom larger than gains, in that a loss of a given size feels more painful than an equivalent gain feels good
            - **Risk-averse for gains:** when faced with a choice between a sure gain and a gamble with a potentially larger gain, people tend to prefer the sure thing
            - **Risk-seeking for losses:** when faced with a choice between a sure loss and a gamble with a potentially larger loss, people are more likely to take the risk to avoid the certain loss
            - **Framing effect:** human judgements differ when we frame things as 'wins' or 'losses', so there are different shapes for the two domains
            - People **distort probabilities,** overweighting small probabilities (e.g., buying lottery tickets) and underweighting large ones (e.g., insurance choices)
            """)

            _show_eq("Value (reference-dependent)", r"v(x) = \begin{cases}(x-r)^{\alpha}, & x \ge r \\ -\lambda\, (r-x)^{\beta}, & x < r\end{cases}")

            st.subheader("Parameters")
            colA, colB = st.columns(2)
            with colA:
                alpha = st.slider("Curvature for gains (α)", 0.2, 1.5, 0.88, 0.02)
                st.caption(
                "Sliding α left increases curvature, flattening the value function for positive outcomes so gains feel less sensitive; sliding α right makes the curve steeper so equal increments in gains feel more impactful. "
                "In practice, lower α means stronger diminishing sensitivity (more risk aversion for gains), while higher α means gains feel more linear and risk attitudes become less strongly averse."
                )
                gamma = st.slider("Weighting (gains) γ", 0.2, 1.5, 0.61, 0.01)
                st.caption(
                "Sliding γ left makes the probability weighting curve more curved, exaggerating small probabilities and down-weighting moderate ones; sliding right straightens the curve so weighting becomes closer to the actual objective probabilities. "
                "In practice, lower γ means people overweight rare gains (e.g., lottery tickets), while higher γ means they behave more like expected-value decision makers for gains."
                )
                ref = st.slider("Reference point r", -50.0, 50.0, 0.0, 1.0)
                st.caption(
                "Sliding r left or right shifts the entire value function horizontally, changing which outcomes are categorized as gains versus losses. "
                "In practice, changing r captures framing: different baselines cause the same outcome to feel like a gain or loss, strongly influencing risk preference."
                )

            with colB:
                beta = st.slider("Curvature for losses (β)", 0.2, 1.5, 0.88, 0.02)
                st.caption(
                "Sliding β left increases curvature so losses become steeper and more sensitive at small magnitudes; sliding β right flattens the loss function so sensitivity grows less rapidly. "
                "In practice, lower β means people react more sharply to small losses, while higher β reduces the disproportionate impact of small losses on decision making."
                )
                delta = st.slider("Weighting (losses) δ", 0.2, 1.5, 0.69, 0.01)
                st.caption(
                "Sliding δ left increases curvature in the weighting function for losses, causing overweighting of small-probability losses; sliding δ right makes weighting more linear with fewer distortions. "
                "In practice, lower δ makes people fear unlikely losses more intensely, while higher δ means they judge loss probabilities more objectively."
                )
                lam = st.slider("Loss aversion λ", 0.5, 4.0, 2.25, 0.05)
                st.caption(
                "Sliding λ left reduces the steepness of the loss side of the value function, while sliding right steepens it dramatically to amplify the psychological weight of losses. "
                "In practice, higher λ means losses feel much more painful than equivalent gains, producing strong avoidance of sure losses and greater willingness to gamble to escape them."
                )

            # Visuals
            col1, col2 = _two_cols()
            with col1:
                x = np.linspace(-100, 100, 500)
                v = np.where(x >= ref, (x - ref) ** alpha, -lam * (ref - x) ** beta)
                _plot_simple(x, v, "Outcome x", "Value v(x)", "Prospect Theory value function")

            with col2:
                p = np.linspace(0.001, 0.999, 400)
                w_plus = p ** gamma / ( (p ** gamma + (1 - p) ** gamma) ** (1/gamma) )
                w_minus = p ** delta / ( (p ** delta + (1 - p) ** delta) ** (1/delta) )
                _plot_multi(p, [w_plus, w_minus], ["w₊(p) (gains)", "w₋(p) (losses)"], "Probability p", "Weight", "Probability weighting (TK-1992)")

            st.divider()
            st.subheader("Worked examples (PT)")

            def v_fn(x):
                x = np.asarray(x, dtype=float)
                return np.where(x >= ref, (x - ref) ** alpha, -lam * (ref - x) ** beta)

            def w_plus_fn(p):
                p = np.asarray(p, dtype=float)
                return p ** gamma / ((p ** gamma + (1 - p) ** gamma) ** (1 / gamma))

            def w_minus_fn(p):
                p = np.asarray(p, dtype=float)
                return p ** delta / ((p ** delta + (1 - p) ** delta) ** (1 / delta))

            # Example 1: 0.01% to win 100,000; else 0
            p1 = 0.0001
            PT1 = w_plus_fn(p1) * v_fn(100_000.0) + w_minus_fn(1 - p1) * v_fn(0.0)

            # Example 2: 50% +55, 50% -50
            p2 = 0.5
            PT2 = w_plus_fn(p2) * v_fn(55.0) + w_minus_fn(1 - p2) * v_fn(-50.0)

            colA, colB = st.columns(2)
            with colA:
                st.markdown("**Lottery ticket:** 0.01% chance to win 100,000")
                st.latex(r"\\mathrm{PT} = w_+(0.0001)\,v(100{,}000) + w_-(0.9999)\,v(0)")
                st.metric("PT value (utils)", f"{PT1:.3g}")
            with colB:
                st.markdown("**50–50 gamble:** +55 / −50")
                st.latex(r"\\mathrm{PT} = w_+(0.5)\,v(55) + w_-(0.5)\,v(-50)")
                st.metric("PT value (utils)", f"{PT2:.3g}")


        elif st.session_state.econ_tab == "Normalization":
            st.subheader("Normalization Models")
            st.markdown("""
                **Normalization** in economic decision-making refers to the process by which the brain **adjusts the subjective value of an option based on the context of other available options.** Instead of evaluating an option in absolute terms, the brain scales or normalizes its value relative to the values around it.
                - **Range Normalization:** the subjective value of an option is scaled relative to the **range** (min-max) of values in the current choice set
                  - When the range of available values is large, differences between options shrink in subjective space
                  - When the range is small, the same objective difference is perceived as larger
                - **Divisive normalization:** the subjective value of an option is **reduced by the overall value of the other options** in the choice set (an option looks less valuable when it is surrounded by higher-value alternatives)
                - **Recurrent divisive normalization:** a form of divisive normalization in which the influence of each option is adjusted through **repeated feedback processes**, often giving more weight to options that receive more attention
                - **Adaptive gain:** the brain **adjusts its sensitivity** to differences in value depending on which values are most relevant in the moment
            """)
            import pandas as pd
            data = {
                "Normalization Model": [
                    "Range Normalization",
                    "Divisive Normalization",
                    "Recurrent Divisive Normalization",
                    "Adaptive Gain / Logistic Model"
                ],
                "Equation (as implemented)": [
                    r"$f(v) = \dfrac{v}{\max(v) - \min(v)}$",
                    r"$f(v) = \dfrac{v}{\text{mean}(v)}$",
                    r"$f(v) = \dfrac{v}{v + \text{mean}(v)}$",
                    r"$f(v) = \dfrac{1}{1 + \exp\big(-(v - \text{mean}(v)) \cdot \text{slope}\big)}$"
                ],
                "When to Use": [
                    "Scales values by the observed range. Useful when absolute min/max bounds of options matter.",
                    "Normalizes relative to the average. Good when choices are judged against the context mean.",
                    "Adds recurrent suppression (self + mean). Captures competitive dynamics between options.",
                    "Produces sigmoidal sensitivity around the context mean, with adjustable slope. Useful for adaptive gain and psychophysical modeling."
                ]
            }

            df_norm = pd.DataFrame(data).set_index("Normalization Model")

            # Display the table in Streamlit
            st.table(df_norm)
            # -----------------------------
            # Helper: parse arrays from text
            # -----------------------------
            def parse_array(s: str) -> np.ndarray:
                toks = [t for t in s.replace(",", " ").split() if t]
                try:
                    return np.array([float(t) for t in toks], dtype=float)
                except Exception:
                    return np.array([], dtype=float)
                
            # -----------------------------
            # On-page inputs
            # -----------------------------
            st.header("Example: Restaurant prices")
            st.caption("Imagine you're choosing between a set of restaurants, each with different average prices. You can compare what happens when your restaurant group has a larger range, when the average prices overall tend to be cheaper vs. expensive, and how that scales with each normalization method.")

            def_v1 = "1 2 5 10"
            def_v2 = "1 5 9 10"

            st.info("Tip: paste different arrays (e.g., low-biased vs high-biased) to see how context shifts each normalization.")

            col_in1, col_in2 = st.columns(2)
            with col_in1:
                v1_str = st.text_input("Restaurant Group 1 (comma/space separated)", value=def_v1)
            with col_in2:
                v2_str = st.text_input("Restaurant Group 1 (comma/space separated)", value=def_v2)

            col_in3, col_in4 = st.columns([1,1])
            with col_in3:
                slope = st.slider("Adaptive gain slope k", 0.05, 2.0, 0.7, 0.05)
                st.caption(
                    "Moving k left (smaller) makes the adaptive-gain sigmoid shallower so outputs change more gradually with value (less contrast around the mean); moving k right (larger) steepens the sigmoid so a small change around the group mean produces a large jump in the normalized output. "
                    )
            with col_in4:
                st.markdown("""
                    Contextually, a larger k means choices become highly sensitive to small differences near the contextual average (amplifying contrast between similar options), while a smaller k makes the decision-maker less context-sensitive and treats value differences more smoothly (reducing contrast effects).              
                """)

            v1 = parse_array(v1_str)
            v2 = parse_array(v2_str)

            # Guardrail
            if v1.size == 0 or v2.size == 0:
                st.error("Please provide valid numeric arrays for Restaurant Group 1 and Restaurant Group 2.")
                st.stop()
                
            # Inline summary right under inputs
            col_sum = st.columns(4)
            col_sum[0].metric("Mean G1", f"{np.mean(v1):.2f}")
            col_sum[1].metric("Range G1", f"{(np.max(v1) - np.min(v1)):.2f}")
            col_sum[2].metric("Mean G2", f"{np.mean(v2):.2f}")
            col_sum[3].metric("Range G2", f"{(np.max(v2) - np.min(v2)):.2f}")

            # -----------------------------
            # Normalization functions
            # -----------------------------
            def range_normalization(v: np.ndarray) -> np.ndarray:
                v = np.asarray(v, dtype=float)
                if v.size == 0:
                    return v
                denom = v.max() - v.min()
                if denom == 0:
                    return np.ones_like(v)
                return v / denom


            def divisive_normalization(v: np.ndarray) -> np.ndarray:
                v = np.asarray(v, dtype=float)
                if v.size == 0:
                    return v
                mu = v.mean()
                if mu == 0:
                    return np.zeros_like(v)
                return v / mu


            def recurrent_normalization(v: np.ndarray) -> np.ndarray:
                v = np.asarray(v, dtype=float)
                if v.size == 0:
                    return v
                mu = v.mean()
                return v / (v + mu)


            def adaptive_gain(v: np.ndarray, k: float = 0.7) -> np.ndarray:
                v = np.asarray(v, dtype=float)
                if v.size == 0:
                    return v
                mu = v.mean()
                return 1.0 / (1.0 + np.exp(-(v - mu) * k))

            # -----------------------------
            # Compute
            # -----------------------------
            v1_rn  = range_normalization(v1)
            v1_dn  = divisive_normalization(v1)
            v1_rdn = recurrent_normalization(v1)
            v1_ag  = adaptive_gain(v1, slope)

            v2_rn  = range_normalization(v2)
            v2_dn  = divisive_normalization(v2)
            v2_rdn = recurrent_normalization(v2)
            v2_ag  = adaptive_gain(v2, slope)

            # -----------------------------
            # Plots (two panels like your Colab)
            # -----------------------------
            st.markdown("### Plots")
            fig, ax = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

            # Colors matching your Colab example
            c_rn = "#F8766D"
            c_dn = "#7CAE00"
            c_rdn = "#00BFC4"
            c_ag = "#C77CFF"

            ax[0].plot(v1, v1_rn,  color=c_rn,  marker='o')
            ax[0].plot(v1, v1_dn,  color=c_dn,  marker='o')
            ax[0].plot(v1, v1_rdn, color=c_rdn, marker='o')
            ax[0].plot(v1, v1_ag,  color=c_ag,  marker='o')
            ax[0].legend(['range normalization','divisive normalization','recurrent divisive norm','adaptive gain/logistic'])
            ax[0].set_xlabel('Value')
            ax[0].set_ylabel('Normalization model output')
            ax[0].set_title('Normalization models (Restaurant Group 1)')

            ax[1].plot(v2, v2_rn,  color=c_rn,  marker='o')
            ax[1].plot(v2, v2_dn,  color=c_dn,  marker='o')
            ax[1].plot(v2, v2_rdn, color=c_rdn, marker='o')
            ax[1].plot(v2, v2_ag,  color=c_ag,  marker='o')
            ax[1].tick_params(labelleft=True)
            ax[1].legend(['range normalization','divisive normalization','recurrent divisive norm','adaptive gain/logistic'])
            ax[1].set_xlabel('Value')
            ax[1].set_ylabel('Normalization model output')
            ax[1].set_title('Normalization models (Restaurant Group 2)')

            st.pyplot(fig, clear_figure=True)

# Working Memory page
elif st.session_state.page == PAGE_WORKING_MEMORY:
    with right_col:
        st.header(PAGE_WORKING_MEMORY)
        st.write("Placeholder page for Working Memory content.")
        st.write("Add span tasks, explanations, or demos here.")
        st.divider()

    with left_col:
        st.markdown("### Navigation")
        if st.button("Home", key="home_from_working"):
            go_to(PAGE_LANDING)

# Safety fallback (shouldn't trigger)
else:
    st.error("Unknown page. Returning to home.")
    go_to(PAGE_LANDING)