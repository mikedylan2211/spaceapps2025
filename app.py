import os
from datetime import datetime
from PIL import Image
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# ==========================================================
# --- PAGE CONFIGURATION ---
# ==========================================================
st.write("""
    #############################################
    """)
LOGO_PATH = os.path.expanduser("git.png")   # <-- your logo file in the same folder
icon_img = Image.open(LOGO_PATH)
       # PIL image object (best for favicon)

st.set_page_config(
    page_title="Fachverein Physik der UZH",
    page_icon=icon_img,     # favicon in browser tab
    layout="wide",
)

# Optional: small CSS to tighten spacing + subtle divider
st.markdown("""
<style>
.block-container { padding-top: .6rem; }
hr { margin: .6rem 0 1rem 0; }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER ROW 1: Logo (col1) + Title (col2)
# =========================
st.markdown("""
<style>
.centered {
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1, 6], gap="small")

with c1:
    #st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.image(icon_img, width=120)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.markdown("## Fachverein Physik der UZH")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==========================================================
# --- GLOBAL STYLE ---
# ==========================================================
st.markdown("""
<style>
/* general spacing */
.block-container { padding-top: .6rem; }

/* header (logo + title centered) */
.header {
  text-align: center;
  margin-bottom: 0.5rem;
}
.header img {
  height: 80px;
  margin-bottom: 0.2rem;
}
.header h1 {
  font-size: 1.8rem;
  margin: 0;
  color: #002f6c;
}
.header p {
  margin: 0;
  color: #555;
  font-size: 0.95rem;
}

/* navigation bar */
.navbar {
  position: sticky;
  top: 0;
  z-index: 999;
  background: rgba(255,255,255,0.97);
  border-bottom: 1px solid #e5e7eb;
  padding: 0.3rem 0;
}
ul.streamlit-option-menu.navbar > li > a {
  font-weight: 600;
  font-size: 15px;
  color: #333;
  padding: 8px 16px;
}
ul.streamlit-option-menu.navbar > li.active > a {
  border-bottom: 3px solid #0055a4;
  color: #0055a4;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# --- HEADER: LOGO + TITLE ---
# ==========================================================

# ==========================================================
# --- NAVIGATION BAR (TABS) ---
# ==========================================================
selected = option_menu(
    None,
    ["Main Site", "Find Previous Data", "AI Prediction", "Dangerous Mountains Now"],
    icons=["house", "calendar3", "cpu", "map"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "nav": {"justify-content": "center"},
        "nav-link": {"text-align": "center", "margin": "0px"},
        "nav-link-selected": {"color": "#0055a4", "border-bottom": "3px solid #0055a4"},
    },
)

st.divider()

# ==========================================================
# --- TAB CONTENT ---
# ==========================================================

# ---- MAIN SITE ----
if selected == "Main Site":
    st.header("Welcome ")
    st.write(
        "This platform monitors Swiss mountain regions for rockfall, landslides, and related risks using AI analysis. "
        "You can explore past data, run AI predictions, and report new incidents directly."
    )

    # --- Split into two columns ---
    col_left, col_right = st.columns([2, 1], gap="large")

    # --- Left: info text or image ---
    with col_left:
        st.markdown("### About the Project")
        st.write(
            "The Fachverein Physik der UZH aims to combine physics, data science, and environmental monitoring "
            "to help detect and predict geological risks. "
            "This app allows you to view AI results, compare satellite data, and report new events."
        )

        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/f/fb/Swiss_Alps_view_from_Swissair_Airbus_A330-223_HB-IQH.jpg",
            caption="Swiss Alps region under observation",
            use_container_width=True,
        )

    # --- Right: Contact / Report Form ---
    with col_right:
        st.subheader(" Contact Form")

        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            message = st.text_area(
                "Describe the issue or observation (e.g., rockfall, landslide, or map error)"
            )
            files = st.file_uploader(
                "Attach photos or documents (optional)",
                type=["jpg", "jpeg", "png", "pdf"],
                accept_multiple_files=True,
            )
            submitted = st.form_submit_button("Send Report")

            if submitted:
                if not name or not email or not message:
                    st.warning("⚠️ Please fill in all required fields.")
                else:
                    st.success("✅ Thank you for your report! We’ll review it shortly.")
                    st.toast("📨 Report sent successfully", icon="✉️")


# ---- FIND PREVIOUS DATA ----
elif selected == "Find Previous Data":

    # Center the content
    padL, main, padR = st.columns([1, 8, 1])
    with main:
        # --- Controls on top ---
        col_mode, col_date = st.columns([3, 2], gap="large")
        with col_mode:
            option_prev = st.radio(
                "Visualization mode",
                ("Photo by date", "Photo comparison", "Animation"),
                horizontal=True,
                label_visibility="collapsed"
            )

        if option_prev == "Photo by date":
            tdate = st.date_input("Analysis date", datetime.today(), format="YYYY-MM-DD")
            st.image(
                "https://github.com/user-attachments/assets/9627614a-7dc7-40f7-a9bf-347d07a9c7a9",
                use_container_width=True,
            )

        elif option_prev == "Photo comparison":
            left_col, right_col = st.columns(2)

            with left_col:
                date_left = st.date_input("Select date (t0)", value=None, key="date_left")
                if date_left:
                    #TODO
                    # тут можна підставити завантаження зображення за датою
                    img1 = f"https://via.placeholder.com/512x512.png?text=Image+{date_left}"
                    st.image(img1, use_container_width=True, caption=f"t0: {date_left}")
                else:
                    st.info("Please select a date for t0")

            with right_col:
                date_right = st.date_input("Select date (t1)", value=None, key="date_right")
                if date_right:
                    #TODO
                    # тут можна підставити завантаження зображення за датою
                    img2 = f"https://via.placeholder.com/512x512.png?text=Image+{date_right}"
                    st.image(img2, use_container_width=True, caption=f"t1: {date_right}")
                else:
                    st.info("Please select a date for t1")

        else:
            st.caption("Simple animation preview by date range")
            import datetime

            # Select start and end dates
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start date", datetime.date(2024, 1, 1))
            with col2:
                end_date = st.date_input("End date", datetime.date(2024, 12, 31))

            # Date slider between chosen dates
            selected_date = st.slider(
                "Select Date",
                min_value=start_date,
                max_value=end_date,
                value=start_date,
                format="YYYY-MM-DD"
            )

            st.image(
                f"https://via.placeholder.com/900x520?text=Date+{selected_date}",
                use_container_width=True
            )


            st.image(
                f"https://via.placeholder.com/900x520?text=Date+{selected_date}",
                use_container_width=True
            )


        st.divider()

# ---- AI PREDICTION ----
elif selected == "AI Prediction":
    st.header("🤖 AI Prediction")
    st.write(
        "This section will later display automatic model predictions for landslide and rockfall risks, "
        "based on data patterns detected in previous observations."
    )
    st.info("🧠 The AI prediction model is under development.")


# ---- DANGEROUS MOUNTAINS ----
elif selected == "Dangerous Mountains Now":
    st.header("Dangerous Mountains in Switzerland")
    st.write("Color-coded markers: red = high risk, orange = medium, green = safe (demo data).")

    np.random.seed(7)
    df = pd.DataFrame({
        "lat": np.random.uniform(46.0, 47.5, 30),
        "lon": np.random.uniform(7.0, 9.5, 30),
        "risk": np.random.choice(["🟢 Safe", "🟠 Medium", "🔴 High"], 30),
        "name": [f"Peak {i+1}" for i in range(30)],
    })

    st.map(df[["lat","lon"]])
    st.dataframe(df, use_container_width=True, hide_index=True)

# ==========================================================
# --- FOOTER ---
# ==========================================================
st.markdown("""
---
<div style='text-align:center;color:gray;font-size:.9rem;margin-top:2em;'>
  Developed by <b>Yuliia Melnychuk</b>, <b>Mike Poppelaars</b>, <b>Borys Tereschenko</b><br>
  &copy; 2025 Fachverein Physik der UZH - All rights reserved
</div>
""", unsafe_allow_html=True)
