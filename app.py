import html
import json
import re
import time
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image
from sentinel_img import download_sentinel_image
from streamlit_option_menu import option_menu


CACHE_DIR = Path("cache")
REPORTS_DIR = Path("reports")
LOGO_PATH = Path(__file__).with_name("git.png")
MAX_ANIMATION_DAYS = 14

RISK_COLORS = {
    "Safe": "#10b981",
    "Medium": "#f59e0b",
    "High": "#ef4444",
}


icon_img = Image.open(LOGO_PATH)
st.set_page_config(
    page_title="Fachverein Physik der UZH",
    page_icon=icon_img,
    layout="wide",
)


def risk_level(score):
    if score >= 0.66:
        return "High"
    if score >= 0.33:
        return "Medium"
    return "Safe"


def load_village_risk_data():
    """Fixed demonstration data until the prediction model is connected."""
    data = [
        {
            "village": "Blatten (Loetschen)",
            "lat": 46.417,
            "lon": 7.822,
            "risk_score": 0.82,
            "signal": "Steep terrain and nearby glacier/rockfall exposure",
        },
        {
            "village": "Zermatt",
            "lat": 46.020,
            "lon": 7.749,
            "risk_score": 0.58,
            "signal": "Glacier proximity and narrow valley corridors",
        },
        {
            "village": "Saas-Fee",
            "lat": 46.108,
            "lon": 7.928,
            "risk_score": 0.61,
            "signal": "High alpine slopes and debris-flow pathways",
        },
        {
            "village": "Grindelwald",
            "lat": 46.624,
            "lon": 8.036,
            "risk_score": 0.70,
            "signal": "Known unstable slopes and rapid meltwater channels",
        },
        {
            "village": "Andermatt",
            "lat": 46.639,
            "lon": 8.594,
            "risk_score": 0.34,
            "signal": "Moderate slope exposure around transport corridors",
        },
        {
            "village": "Pontresina",
            "lat": 46.491,
            "lon": 9.905,
            "risk_score": 0.43,
            "signal": "Avalanche paths and glacial catchments nearby",
        },
        {
            "village": "Arosa",
            "lat": 46.779,
            "lon": 9.680,
            "risk_score": 0.28,
            "signal": "Lower current demo score for mapped settlement area",
        },
        {
            "village": "Leukerbad",
            "lat": 46.379,
            "lon": 7.628,
            "risk_score": 0.52,
            "signal": "Rock-wall exposure and steep approach valleys",
        },
        {
            "village": "Wengen",
            "lat": 46.605,
            "lon": 7.921,
            "risk_score": 0.40,
            "signal": "Slope exposure above transport routes",
        },
        {
            "village": "Lauterbrunnen",
            "lat": 46.593,
            "lon": 7.907,
            "risk_score": 0.67,
            "signal": "Narrow valley floor beneath steep rock walls",
        },
    ]
    df = pd.DataFrame(data)
    df["risk_level"] = df["risk_score"].apply(risk_level)
    df["marker_color"] = df["risk_level"].map(RISK_COLORS)
    df["marker_size"] = (100 + df["risk_score"] * 180).round()
    return df


def clear_cache(folder_path=CACHE_DIR):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    folder = Path(folder_path)
    if not folder.exists():
        return 0

    deleted = 0
    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            file_path.unlink()
            deleted += 1
    return deleted


def animate_sentinel_images(image_paths, duration):
    valid_images = [Path(path) for path in image_paths if Path(path).exists()]
    if not valid_images:
        st.warning("No valid image files found.")
        return

    img_placeholder = st.empty()
    progress = st.progress(0)
    status_text = st.empty()

    total = len(valid_images)
    for idx, path in enumerate(valid_images):
        img_placeholder.image(
            str(path),
            use_container_width=True,
            caption=f"Frame {idx + 1} of {total}",
        )
        status_text.text(f"Showing image {idx + 1}/{total}")
        progress.progress((idx + 1) / total)
        time.sleep(duration)

    progress.empty()
    status_text.empty()
    st.success("Animation finished.")


def show_sentinel_result(info, requested_date, label="Birchgletscher"):
    if info and info.get("file_path"):
        source = "cached" if info.get("cached") else "downloaded"
        st.caption(f"{label} on {info['date']} ({source})")
        st.image(info["file_path"], use_container_width=True)
        return

    error = info.get("error") if info else "No response from Sentinel image loader."
    st.warning(f"No image found for {requested_date}. {error}")


def is_valid_email(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email or "") is not None


def safe_attachment_name(uploaded_file, index):
    original = Path(uploaded_file.name)
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", original.stem).strip("._")
    suffix = original.suffix.lower()
    return f"{index:02d}_{stem or 'attachment'}{suffix}"


def save_report(name, email, message, uploaded_files):
    created_at = datetime.now(timezone.utc)
    report_id = f"{created_at:%Y%m%dT%H%M%SZ}_{uuid.uuid4().hex[:8]}"
    report_dir = REPORTS_DIR / report_id
    report_dir.mkdir(parents=True, exist_ok=False)

    saved_files = []
    for index, uploaded_file in enumerate(uploaded_files or [], start=1):
        file_name = safe_attachment_name(uploaded_file, index)
        file_data = uploaded_file.getbuffer()
        (report_dir / file_name).write_bytes(file_data)
        saved_files.append(
            {
                "original_name": uploaded_file.name,
                "stored_name": file_name,
                "content_type": uploaded_file.type,
                "size_bytes": len(file_data),
            }
        )

    payload = {
        "id": report_id,
        "created_at_utc": created_at.isoformat(),
        "name": name.strip(),
        "email": email.strip(),
        "message": message.strip(),
        "attachments": saved_files,
    }
    (report_dir / "report.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    return report_id, report_dir


def render_risk_pill(level):
    css_class = {
        "High": "pill-high",
        "Medium": "pill-med",
        "Safe": "pill-safe",
    }[level]
    return f"<span class='pill {css_class}'>{level}</span>"


def selected_dates(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


st.markdown(
    """
<style>
.block-container { padding-top: .6rem; }
hr { margin: .6rem 0 1rem 0; }
.centered {
    display: flex;
    align-items: center;
    justify-content: center;
}
.hero { padding:.6rem 0 1rem 0; text-align:center; }
.hero h1 { margin:0; font-size:2.0rem; }
.hero p  { margin:.2rem 0 0 0; color:#4b5563; font-size:1.05rem; }
.pill {
    display:inline-block;
    padding:.2rem .55rem;
    border-radius:999px;
    font-weight:600;
    font-size:.82rem;
    margin-right:.35rem;
}
.pill-safe {
    background:rgba(16,185,129,.12);
    color:#0f766e;
    border:1px solid rgba(16,185,129,.35);
}
.pill-med {
    background:rgba(245,158,11,.12);
    color:#92400e;
    border:1px solid rgba(245,158,11,.35);
}
.pill-high {
    background:rgba(239,68,68,.13);
    color:#991b1b;
    border:1px solid rgba(239,68,68,.35);
}
.soft-card {
    border:1px solid #e5e7eb;
    border-radius:8px;
    padding:14px;
    background:#fff;
    margin-bottom:.7rem;
}
.muted { color:#6b7280; font-size:.9rem; }
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
""",
    unsafe_allow_html=True,
)

c1, c2 = st.columns([1, 6], gap="small")
with c1:
    st.image(icon_img, width=120)
with c2:
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.markdown("## Fachverein Physik der UZH")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

selected = option_menu(
    None,
    ["Main Site", "Find Previous Data", "AI Prediction"],
    icons=["house", "calendar3", "cpu"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "nav": {"justify-content": "center"},
        "nav-link": {"text-align": "center", "margin": "0px"},
        "nav-link-selected": {
            "color": "#0055a4",
            "border-bottom": "3px solid #0055a4",
        },
    },
)

st.divider()

if selected == "Main Site":
    st.markdown(
        """
    <div class="hero">
      <h1>Swiss Mountain Risk Monitoring Platform</h1>
      <p>Developed by the <b>Fachverein Physik der UZH</b> using physics,
      satellite imagery, and AI to identify dangerous zones and protect
      mountain communities across Switzerland.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.caption("Risk values shown here are fixed demonstration data, not live predictions.")
    st.divider()

    village_data = load_village_risk_data()
    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        st.subheader("Explore Villages and Risk Levels")
        q = st.text_input(
            "Search for a Swiss village",
            placeholder="Type a name, e.g. Blatten, Zermatt, Saas-Fee...",
        )

        st.caption(
            "Legend: "
            f"{render_risk_pill('High')} "
            f"{render_risk_pill('Medium')} "
            f"{render_risk_pill('Safe')}",
            unsafe_allow_html=True,
        )

        df_show = (
            village_data[
                village_data["village"].str.contains(q, case=False, na=False)
            ]
            if q
            else village_data
        )

        if df_show.empty:
            st.info("No village matches that search.")
        else:
            st.map(
                df_show,
                latitude="lat",
                longitude="lon",
                color="marker_color",
                size="marker_size",
                zoom=8 if len(df_show) < 3 else 7,
                height=460,
            )

        st.markdown("#### Villages and Risk Levels")
        for _, row in df_show.iterrows():
            level = str(row["risk_level"])
            st.markdown(
                f"""
                <div class="soft-card">
                  <div style="display:flex;justify-content:space-between;gap:1rem;align-items:center;">
                    <div>
                      <b>{html.escape(row['village'])}</b><br>
                      <span class="muted">lat {row['lat']:.3f}, lon {row['lon']:.3f}</span>
                    </div>
                    <div>{render_risk_pill(level)}</div>
                  </div>
                  <div class="muted" style="margin-top:.4rem;">
                    Risk score (0-1): {row['risk_score']:.2f}<br>
                    Signal: {html.escape(row['signal'])}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_right:
        st.subheader("Contact Form")
        st.caption("Submitted reports are saved locally under reports/.")

        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            message = st.text_area(
                "Describe the issue or observation",
                placeholder="Rockfall, landslide, map issue, blocked path...",
            )
            files = st.file_uploader(
                "Attach photos or documents (optional)",
                type=["jpg", "jpeg", "png", "pdf"],
                accept_multiple_files=True,
            )
            submitted = st.form_submit_button("Send Report")

            if submitted:
                if not name.strip() or not email.strip() or not message.strip():
                    st.warning("Please fill in all required fields.")
                elif not is_valid_email(email.strip()):
                    st.warning("Please enter a valid email address.")
                else:
                    report_id, _report_dir = save_report(name, email, message, files)
                    st.success(f"Report saved. Reference: {report_id}")
                    st.toast("Report saved successfully")

        st.markdown("---")
        st.subheader("Today's Summary")
        safe = int((village_data["risk_level"] == "Safe").sum())
        med = int((village_data["risk_level"] == "Medium").sum())
        high = int((village_data["risk_level"] == "High").sum())
        st.write(
            f"<span class='pill pill-safe'>Safe: {safe}</span> "
            f"<span class='pill pill-med'>Medium: {med}</span> "
            f"<span class='pill pill-high'>High: {high}</span>",
            unsafe_allow_html=True,
        )

elif selected == "Find Previous Data":
    pad_left, main, pad_right = st.columns([1, 8, 1])
    with main:
        with st.expander("Image cache"):
            st.caption("Downloaded Sentinel images are reused until the cache is cleared.")
            if st.button("Clear image cache"):
                deleted = clear_cache()
                st.success(f"Cleared {deleted} cached image(s).")

        col_mode, _col_date = st.columns([3, 2], gap="large")
        with col_mode:
            option_prev = st.radio(
                "Visualization mode",
                ("Photo by date", "Photo comparison", "Animation"),
                horizontal=True,
                label_visibility="collapsed",
            )

        if option_prev == "Photo by date":
            tdate = st.date_input(
                "Analysis date",
                value=None,
                format="YYYY-MM-DD",
                key="analysis_date",
            )

            if tdate:
                if st.button("Show image"):
                    with st.spinner("Looking up Sentinel imagery..."):
                        data = download_sentinel_image(str(tdate))
                    show_sentinel_result(data, str(tdate))
            else:
                st.info("Please select a date to display the image.")

        elif option_prev == "Photo comparison":
            left_col, right_col = st.columns(2)

            with left_col:
                date_left = st.date_input("Select date 1", value=None, key="date_left")
            with right_col:
                date_right = st.date_input("Select date 2", value=None, key="date_right")

            if date_left and date_right:
                if st.button("Show images"):
                    with st.spinner("Looking up Sentinel imagery..."):
                        info_left = download_sentinel_image(str(date_left))
                        info_right = download_sentinel_image(str(date_right))

                    with left_col:
                        show_sentinel_result(info_left, str(date_left))
                    with right_col:
                        show_sentinel_result(info_right, str(date_right))
            else:
                st.info("Please select both dates to display images.")

        else:
            st.caption("Simple animation preview by date range")

            start = st.date_input(
                "Start date",
                date(2025, 5, 15),
                key="animation_start",
            )
            end = st.date_input(
                "End date",
                date(2025, 5, 22),
                key="animation_end",
            )
            duration = st.slider("Display time per image (s)", 0.5, 5.0, 1.5, 0.5)

            st.session_state.setdefault("animation_images", [])
            st.session_state.setdefault("animation_duration", duration)

            if end < start:
                st.warning("End date must be on or after start date.")
            else:
                dates = list(selected_dates(start, end))
                if len(dates) > MAX_ANIMATION_DAYS:
                    st.warning(
                        f"Please select {MAX_ANIMATION_DAYS} days or fewer "
                        "to avoid excessive Sentinel API calls."
                    )
                elif st.button("Start Animation"):
                    unique_images = []
                    seen_dates = set()
                    progress = st.progress(0)
                    status_text = st.empty()

                    st.info("Downloading available Sentinel images...")
                    for index, current_date in enumerate(dates, start=1):
                        date_str = str(current_date)
                        info = download_sentinel_image(date_str)

                        if info and info.get("file_path") and info["date"] not in seen_dates:
                            unique_images.append(info["file_path"])
                            seen_dates.add(info["date"])

                        progress.progress(index / len(dates))
                        status_text.text(f"Processed date: {date_str}")

                    progress.empty()
                    status_text.empty()
                    st.session_state["animation_images"] = unique_images
                    st.session_state["animation_duration"] = duration

                    if not unique_images:
                        st.warning("No unique images found in the selected date range.")
                    else:
                        st.success(
                            f"Found {len(unique_images)} unique images. Starting animation..."
                        )
                        animate_sentinel_images(unique_images, duration)

            if st.session_state.get("animation_images"):
                if st.button("Replay Animation"):
                    animate_sentinel_images(
                        st.session_state["animation_images"],
                        st.session_state["animation_duration"],
                    )

elif selected == "AI Prediction":
    st.header("AI Prediction")
    st.write(
        "This section will later display automatic model predictions for landslide "
        "and rockfall risks, based on data patterns detected in previous observations."
    )
    st.info("The AI prediction model is under development.")

st.markdown(
    """
---
<div style='text-align:center;color:gray;font-size:.9rem;margin-top:2em;'>
  Developed by <b>Yuliia Melnychuk</b>, <b>Mike Dylan Poppelaars</b>, <b>Borys Tereschenko</b><br>
  Substantially improved by <b>Mike Dylan Poppelaars</b><br>
  &copy; 2026 Fachverein Physik der UZH - All rights reserved
</div>
""",
    unsafe_allow_html=True,
)
