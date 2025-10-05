import os
from datetime import datetime, timedelta
import time
from PIL import Image
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from sentinel_img import download_sentinel_image

def clear_cache(folder_path="cache"):
    """
    Deletes all image files from the cache folder.

    Arguments:
    folder_path (str): path to the cache folder
    """
    # File extensions considered as images
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")

    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            file_path = os.path.join(folder_path, filename)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

def animate_sentinel_images(image_paths, duration):
    """
    Displays a sequence of Sentinel images as an animation.

    Args:
        image_paths (list[str]): List of image file paths to display.
        duration (float): Duration (seconds) to show each image.
    """
    if not image_paths:
        st.warning("No images to animate.")
        return

    # Filter out missing files (in case some were deleted or moved)
    valid_images = [p for p in image_paths if os.path.exists(p)]
    if not valid_images:
        st.warning("No valid image files found.")
        return

    # Image placeholder (updated dynamically)
    img_placeholder = st.empty()
    progress = st.progress(0)
    status_text = st.empty()

    total = len(valid_images)
    for idx, path in enumerate(valid_images):
        img_placeholder.image(path, use_container_width=True, caption=f"Frame {idx + 1} of {total}")
        status_text.text(f"Showing image {idx + 1}/{total}")
        progress.progress((idx + 1) / total)
        time.sleep(duration)

    progress.empty()
    status_text.empty()
    st.success("🎬 Animation finished!")

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
    ["Main Site", "Find Previous Data", "AI Prediction"],
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
    # ==========================================================
    # --- PAGE INTRO & STYLE ---
    # ==========================================================
    st.markdown("""
    <style>
    .hero { padding:.6rem 0 1rem 0; text-align:center; }
    .hero h1 { margin:0; font-size:2.0rem; }
    .hero p  { margin:.2rem 0 0 0; color:#4b5563; font-size:1.05rem; }

    .section { margin-top:1.5rem; }
    .pill { display:inline-block; padding:.2rem .55rem; border-radius:999px;
            font-weight:600; font-size:.82rem; margin-right:.35rem; }
    .pill-safe   { background:rgba(16,185,129,.12); color:#0f766e; border:1px solid rgba(16,185,129,.35); }
    .pill-med    { background:rgba(245,158,11,.12); color:#92400e; border:1px solid rgba(245,158,11,.35); }
    .pill-high   { background:rgba(239,68,68,.13); color:#991b1b; border:1px solid rgba(239,68,68,.35); }
    .soft-card { border:1px solid #e5e7eb; border-radius:14px; padding:14px; background:#fff; }
    .muted { color:#6b7280; font-size:.9rem; }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================================
    # --- HERO INTRO TEXT ---
    # ==========================================================
    st.markdown("""
    <div class="hero">
      <h1>Swiss Mountain Risk Monitoring Platform</h1>
      <p>Developed by the <b>Fachverein Physik der UZH</b> — using physics, satellite imagery, and AI to identify
      dangerous zones and protect mountain communities across Switzerland.</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ==========================================================
    # --- MAIN CONTENT: VILLAGE MAP + CONTACT FORM ---
    # ==========================================================
    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        st.subheader("Explore Villages and Risk Levels")
        q = st.text_input("Search for a Swiss village", placeholder="Type a name (e.g., Blatten, Zermatt, Saas-Fee)...")

        st.caption(
            "Legend: "
            "<span class='pill pill-high'>High</span> "
            "<span class='pill pill-med'>Medium</span> "
            "<span class='pill pill-safe'>Safe</span>",
            unsafe_allow_html=True
        )

        import pandas as pd, numpy as np
        np.random.seed(13)
        demo = pd.DataFrame({
            "village": ["Blatten (Lötschen)", "Zermatt", "Saas-Fee", "Grindelwald", "Andermatt",
                        "Pontresina", "Arosa", "Leukerbad", "Wengen", "Lauterbrunnen"],
            "lat": [46.417, 46.020, 46.108, 46.624, 46.639, 46.491, 46.779, 46.379, 46.605, 46.593],
            "lon": [7.822, 7.749, 7.928, 8.036, 8.594, 9.905, 9.680, 7.628, 7.921, 7.907],
        })
        demo["risk_score"] = np.clip(np.random.normal(0.35, 0.22, len(demo)), 0, 1)
        demo["risk_level"] = pd.cut(demo["risk_score"], [-0.01, .33, .66, 1.01], labels=["Safe","Medium","High"])

        df_show = demo[demo["village"].str.contains(q, case=False, na=False)] if q else demo

        st.map(df_show[["lat","lon"]], zoom=8 if len(df_show)<3 else 7)

        st.markdown("#### Villages and Risk Levels")
        for _, r in df_show.iterrows():
            pill = "pill-high" if r["risk_level"]=="High" else "pill-med" if r["risk_level"]=="Medium" else "pill-safe"
            st.markdown(
                f"""
                <div class="soft-card">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div><b>{r['village']}</b><br><span class="muted">lat {r['lat']:.3f}, lon {r['lon']:.3f}</span></div>
                    <div><span class="pill {pill}">{r['risk_level']}</span></div>
                  </div>
                  <div class="muted" style="margin-top:.4rem;">Risk score (0–1): {r['risk_score']:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ==========================================================
# --- RIGHT COLUMN: CONTACT FORM ---
# ==========================================================

    with col_right:
        st.subheader("Contact Form")

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

        st.markdown("---")
        st.subheader("Today's Summary")
        safe = int((demo["risk_level"]=="Safe").sum())
        med  = int((demo["risk_level"]=="Medium").sum())
        high = int((demo["risk_level"]=="High").sum())
        st.write(
            f"<span class='pill pill-safe'>Safe: {safe}</span> "
            f"<span class='pill pill-med'>Medium: {med}</span> "
            f"<span class='pill pill-high'>High: {high}</span>",
            unsafe_allow_html=True
        )

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
            clear_cache()

            # --- Date selection ---
            tdate = st.date_input("Analysis date", value=None, format="YYYY-MM-DD", key="analysis_date")

            if tdate:
                if st.button("Show image"):
                    tdate_str = str(tdate)
                    data = download_sentinel_image(tdate_str)

                    if data and data.get("file_path"):
                        tdate_name = str(data["date"])
                        st.write(f"Birchgletscher at day {tdate_name}")
                        st.image(data["file_path"], use_container_width=True)
                    else:
                        st.warning(f"No image found for {tdate_str}")
            else:
                st.info("Please select a date to display the image.")


        elif option_prev == "Photo comparison":
            left_col, right_col = st.columns(2)
            clear_cache()

            # --- Date selection ---
            with left_col:
                date_left = st.date_input("Select date 1", value=None, key="date_left")
            with right_col:
                date_right = st.date_input("Select date 2", value=None, key="date_right")

            if date_left and date_right:
                if st.button("Show images"):
                    # Convert to string
                    date_left_str = str(date_left)
                    date_right_str = str(date_right)

                    # Download images
                    info_left = download_sentinel_image(date_left_str)
                    info_right = download_sentinel_image(date_right_str)

                    # --- Display ---
                    with left_col:
                        if info_left and info_left.get("file_path"):
                            st.image(info_left["file_path"], caption=f"Birchgletscher at {info_left['date']}", use_container_width=True)
                        else:
                            st.warning(f"No image found for {date_left_str}")

                    with right_col:
                        if info_right and info_right.get("file_path"):
                            st.image(info_right["file_path"], caption=f"Birchgletscher at {info_right['date']}", use_container_width=True)
                        else:
                            st.warning(f"No image found for {date_right_str}")
            else:
                st.info("Please select both dates to display images.")

        else:
            st.caption("Simple animation preview by date range")

            clear_cache()

            # --- Date range selection ---
            start = st.date_input("Start date", datetime(2025, 5, 1))
            end = st.date_input("End date", datetime(2025, 6, 1))

            # --- Animation speed control ---
            duration = st.slider("Display time per image (s)", 0.5, 5.0, 1.5, 0.5)

            # --- Start animation ---
            if st.button("Start Animation"):
                from datetime import timedelta

                # Generate list of dates in the range
                total_days = (end - start).days + 1
                current_date = start

                unique_images = []
                seen_files = set()
                processed_dates = set()

                progress = st.progress(0)
                status_text = st.empty()

                st.info("Downloading available Sentinel images...")

                for i in range(total_days):
                    date_str = str(current_date)

                    # Skip already processed dates
                    if date_str in processed_dates:
                        current_date += timedelta(days=1)
                        progress.progress((i + 1) / total_days)
                        continue
                    
                    processed_dates.add(date_str)

                    # Download the image (with your ±5 day logic)
                    info = download_sentinel_image(date_str)

                    # Add only unique file paths
                    if info and info.get("file_path"):
                        file_path = info["file_path"]
                        if file_path not in seen_files:
                            unique_images.append(file_path)
                            seen_files.add(file_path)

                    progress.progress((i + 1) / total_days)
                    status_text.text(f"Processed date: {date_str}")

                    current_date += timedelta(days=1)

                progress.empty()
                status_text.empty()

                if not unique_images:
                    st.warning("No unique images found in the selected date range.")
                else:
                    st.success(f"✅ Found {len(unique_images)} unique images. Starting animation...")
                    animate_sentinel_images(unique_images, duration)

                    # --- Repeat animation section ---
                    if st.button("Replay Animation"):
                        st.info("Replaying animation...")
                        animate_sentinel_images(unique_images, duration)


# ---- AI PREDICTION ----
elif selected == "AI Prediction":
    st.header("🤖 AI Prediction")
    st.write(
        "This section will later display automatic model predictions for landslide and rockfall risks, "
        "based on data patterns detected in previous observations."
    )
    st.info("🧠 The AI prediction model is under development.")


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
