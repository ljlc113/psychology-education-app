def render_landing_left():
    st.markdown("""
    <style>
    /* Target Streamlit buttons inside our container */
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

    # Each button is inside a div with class "big-button" so CSS targets only these
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
