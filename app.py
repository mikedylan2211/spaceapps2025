import os
from datetime import datetime
from PIL import Image
import streamlit as st

# =========================
# Page config FIRST (no UI calls before this)
# =========================
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


# =========================
# HEADER ROW 2: Visualization selector + Date + Buttons
# =========================
row2_col_mode, row2_col_date, row2_col_actions = st.columns([4, 2, 3], gap="large")

with row2_col_mode:
    option = st.radio(
        "Choose visualization",     # (label text stays internally, but is hidden)
        ("Photo by date", "Photo comparison", "Animation"),
        horizontal=True,
        label_visibility="collapsed",   # 👈 hides the label completely
    )


with row2_col_date:
    tdate = st.date_input("Analysis date", datetime.today(), format="YYYY-MM-DD")

with row2_col_actions:
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("Detect", use_container_width=True):
            with st.spinner("Running change detection..."):
                st.session_state["status"] = "Change detection done ✅"
                st.toast("Change detection complete", icon="🛰")
    with b2:
        if st.button("Risk", use_container_width=True):
            with st.spinner("Predicting risk..."):
                st.session_state["status"] = "Risk map ready 📊"
                st.toast("Risk map generated", icon="📈")
    with b3:
        if st.button("Export", use_container_width=True):
            with st.spinner("Exporting..."):
                st.session_state["status"] = "Exported 💾"
                st.toast("Export ready", icon="📦")

st.divider()

# =========================
# MAIN CONTENT
# =========================
left, right = st.columns([2, 1], gap="large")

with left:
    st.subheader("Visualization")
    if option == "Photo by date":
        st.caption(f"Selected date: {tdate}")
        st.image(
            "https://github.com/user-attachments/assets/9627614a-7dc7-40f7-a9bf-347d07a9c7a9",
            use_container_width=True,
        )
    elif option == "Photo comparison":
        try:
            from streamlit_image_comparison import image_comparison
            img1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/The_Blue_Marble%2C_AS17-148-22727.jpg/1200px-The_Blue_Marble%2C_AS17-148-22727.jpg"
            img2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/330px-FullMoon2010.jpg"
            image_comparison(img1=img1, img2=img2, label1="t0", label2="t1", width=700)
        except Exception:
            cA, cB = st.columns(2)
            with cA: st.image(img1, use_container_width=True, caption="t0")
            with cB: st.image(img2, use_container_width=True, caption="t1")
    else:
        st.caption("Simple animation preview")
        frame = st.slider("Frame", 0, 10, 0)
        st.image(f"https://via.placeholder.com/900x520?text=Frame+{frame}", use_container_width=True)

with right:
    st.subheader("Controls")
    thresh = st.slider("Change threshold", 0.30, 0.95, 0.60, 0.01)
    smooth = st.slider("Post-filter (px)", 0, 7, 2, 1)
    st.toggle("Show risk overlay", value=False)
    st.file_uploader(
        "Upload t0/t1 images (optional)",
        type=["png", "jpg", "jpeg", "tif"],
        accept_multiple_files=True,
    )

    # ==========================================================
    # --- Contact Form (instead of logs) ---
    # ==========================================================
    st.subheader("Contact Form")

    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area(
            "Describe the issue or observation (e.g., rockfall, landslide, or map error)"
        )
        uploaded_files = st.file_uploader(
            "Attach photos or documents (optional)",
            type=["jpg", "png", "jpeg", "pdf"],
            accept_multiple_files=True,
        )
        submitted = st.form_submit_button("Send Report")

        if submitted:
            if not name or not email or not message:
                st.warning("⚠️ Please fill in all required fields (Name, Email, Message).")
            else:
                # ✅ You could add email or database logic here later
                st.success("✅ Thank you for your report! We’ll review it shortly.")
                st.toast("📨 Report sent successfully", icon="✉️")

# ==========================================================
# --- Footer (bottom of the page) ---
# ==========================================================
st.markdown("""
---
<div style='text-align: center; color: gray; font-size: 0.9rem; margin-top: 2em;'>
  Developed by <b>Yuliia Melnychuk</b>, <b>Mike Poppelaars</b>, <b>Borys Tereschenko </b><br>
  &copy; 2025 Fachverein Physik der UZH - All rights reserved
</div>
""", unsafe_allow_html=True)
