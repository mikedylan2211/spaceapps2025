# Save Blatten & Beyond  
*Rapid Response to Natural and Man-Made Disasters*  

An interactive web app to show and predict dangerous locations in the mountains, developed by physics students at UZH for the NASA Hackathon 2025 in Zurich.

---

## Table of Contents

1. [About](#about)  
2. [Motivation & Goals](#motivation--goals)  
3. [Features](#features)  
4. [Architecture & Technology Stack](#architecture--technology-stack)  
5. [Installation & Setup](#installation--setup)  

---

## About

“Save Blatten & Beyond” is a web app that helps visualize and predict hazardous areas in mountainous terrain (e.g. avalanche risk zones, landslides) via an interactive map.  
The app combines Sentinel-1 and Sentinel-2 radar and imagery data to highlight high-risk zones and inform rescue planning or precautionary measures.

We created this as our project for the *NASA Hackathon 2025* in Zurich. We are physics students at the *University of Zurich (UZH)*, bringing together skills in data analysis, geospatial modeling, and web development.

---

## Motivation & Goals

- Mountainous terrain poses significant risks (avalanches, rockfalls, landslides).  
- Early identification of dangerous areas helps in disaster prevention, planning, and rescue operations.  
- We aim to build a tool for *rapid response*: enabling rescue teams, local authorities, or hikers to visualize risk in real time.  
- The app should be intuitive, interactive, and extensible for future enhancements (e.g. adding more sensors, real-time updates).

---

## Features

- Interactive map interface with zoom / pan  
- Overlay of predicted risk zones (color-coded)  
- Ability to click / hover to see risk level, contributing data  
- Data ingestion / preprocessing from satellite / remote sensing  
- Backend logic to compute predictions  
- (Optional / future) Alerts, time series, forecasts  

---

## Architecture & Technology Stack

Here’s a rough breakdown of the components and technologies used:

| Component              | Technology / Library         |
|------------------------|-------------------------------|
| Backend / API          | Python (Streamlit, ...) |
| Predictive model logic | Python, Torch (in development) |
| Satellite / remote data | Sentinel-2, Sentinel-1 |
| Frontend / UI          | Streamlit (Python)
| Deployment / scripts   | installer.sh, environment setup, etc. |
| Dependencies           | listed in requirements.txt |

---

## Installation & Setup

Below is a general guide. 

### Prerequisites

- Python 3.8+  
- (Optionally) virtual environment tool (venv, conda)  
- Git  

### Steps

1. *Clone the repository*  
  <pre> ```bash
   git clone https://github.com/borystereschenko/Hackthon.git
   cd Hackthon
  </pre>
   
2. *Make Installer executable and (optional) give everyone on the system privilege to execute*
  <pre>```bash
  chmod +x installer.sh && chmod 755 installer.sh
  </pre>
     
3. *Get API keys*
   Get your own api key at sentinel-hub.com

4. *Run the installer*
   <pre>```bash
   ./installer.sh
   </pre>
