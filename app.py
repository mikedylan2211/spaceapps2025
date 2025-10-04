import streamlit as st
from datetime import datetime

# --- Title and description ---
st.title("Save Blatten & Beyond: Rapid Response to Disasters")
st.markdown("""
On **May 29, 2025**, the Alpine village of **Blatten (Switzerland)** was devastated 
by one of the largest glacier-related landslides ever recorded.  
We are building a tool to **visualize and predict such disasters** 
using satellite SAR data for early warning and crisis response.
""")

# --- Selection bar ---
option = st.radio(
    "Choose visualization type:",
    ("Photo by date", "Photo comparison", "Animation")
)

st.write(f"🔹 Selected option: {option}")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🛰 Detect Change"):
        st.session_state['status'] = "Running change detection..."
        # TODO: call your model here
        st.success("✅ Change detection done!")

with col2:
    if st.button("📊 Risk Forecast"):
        st.session_state['status'] = "Predicting risk..."
        # TODO: call risk model
        st.info("Risk map ready!")

with col3:
    if st.button("💾 Export Results"):
        st.session_state['status'] = "Exporting..."
        # TODO: export file
        st.success("Files exported!")

# --- Image ---
if option == "Photo by date":
    image_url = "https://github.com/user-attachments/assets/9627614a-7dc7-40f7-a9bf-347d07a9c7a9"
    st.image(image_url)
elif option == "Photo comparison":
    image_url_1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/The_Blue_Marble%2C_AS17-148-22727.jpg/1200px-The_Blue_Marble%2C_AS17-148-22727.jpg"
    image_url_2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/330px-FullMoon2010.jpg"
    st.image(image_url_1, width = 300)
    st.image(image_url_2, width = 300)

else:
    image_url = "https://via.placeholder.com/600x400?text=Option+3"
    st.image(image_url)

# --- Calendar ---
date = st.date_input(
    "Select a date for data analysis:",
    datetime.today()
)

st.write(f"📅 Selected date: {date}")
