# Save Blatten & Beyond

Rapid response prototype for visualizing mountain hazard signals in Switzerland.

This Streamlit app was developed for the NASA Space Apps Challenge 2025 in Zurich
by physics students at the University of Zurich. It combines a demo village risk
map with Sentinel-2 image lookup for the Blatten/Birchgletscher area.

## Features

- Interactive Swiss village map with fixed demonstration risk levels
- Color-coded village markers and risk summaries
- Sentinel-2 image lookup by date with local image caching
- Side-by-side Sentinel image comparison
- Short date-range animation with replay support
- Local contact/report capture with optional attachments
- Placeholder page for future AI prediction work

## Project Structure

| Path | Purpose |
| --- | --- |
| `app.py` | Streamlit interface and app workflow |
| `sentinel_img.py` | Sentinel Hub process API image downloader |
| `TOKEN.py` | Sentinel Hub OAuth token helper |
| `pyproject.toml` | uv/Python project metadata |
| `requirements.txt` | pip-compatible dependency list |
| `.streamlit/secrets.toml.example` | Sentinel credential template |

Generated runtime data is intentionally ignored by git:

- `cache/` stores downloaded Sentinel images
- `reports/` stores submitted local reports
- `.streamlit/secrets.toml` stores local credentials

## Setup

Prerequisites:

- Python 3.10+
- uv
- Sentinel Hub client credentials for image lookup

Install dependencies:

```bash
uv sync
```

Configure Sentinel Hub credentials with either environment variables:

```bash
export SENTINEL_CLIENT_ID="your-client-id"
export SENTINEL_CLIENT_SECRET="your-client-secret"
```

Or copy the example Streamlit secrets file:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Then edit `.streamlit/secrets.toml` with your real credentials.

## Run

```bash
uv run streamlit run app.py
```

The installer script does the same setup/run sequence:

```bash
./installer.sh
```

## Notes

The risk values in the main map are fixed demonstration data. They are not live
predictions and should not be used for operational safety decisions.

The contact form stores reports locally in `reports/`; it does not send email or
upload reports to an external service.
