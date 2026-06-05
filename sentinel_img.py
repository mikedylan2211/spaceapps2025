from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

from TOKEN import make_token


PROCESS_URL = "https://services.sentinel-hub.com/api/v1/process"
BIRCHGLETSCHER_BBOX = [7.78, 46.38, 7.88, 46.45]
IMAGE_SIZE = 1024
REQUEST_TIMEOUT_SECONDS = 30


def is_image_dark(image_bytes, threshold=10):
    """Return True when Sentinel Hub returns a mostly black image."""
    try:
        img = Image.open(BytesIO(image_bytes))
        grayscale = img.convert("L")
        avg = sum(grayscale.getdata()) / (grayscale.width * grayscale.height)
        return avg < threshold
    except Exception:
        return True


def _candidate_dates(date_obj, max_delta_days):
    seen = set()
    for delta in range(max_delta_days + 1):
        offsets = [0] if delta == 0 else [delta, -delta]
        for offset in offsets:
            candidate = date_obj + timedelta(days=offset)
            date_str = candidate.strftime("%Y-%m-%d")
            if date_str not in seen:
                seen.add(date_str)
                yield date_str


def _payload_for_date(date_str, bbox):
    return {
        "input": {
            "bounds": {"bbox": bbox},
            "data": [
                {
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": f"{date_str}T00:00:00Z",
                            "to": f"{date_str}T23:59:59Z",
                        },
                        "maxCloudCoverage": 20,
                    },
                }
            ],
        },
        "output": {
            "width": IMAGE_SIZE,
            "height": IMAGE_SIZE,
            "responses": [
                {
                    "identifier": "default",
                    "format": {"type": "image/png"},
                }
            ],
        },
        "evalscript": """
//VERSION=3
function setup() {
    return {input: ["B02", "B03", "B04"], output: {bands: 3}};
}
function evaluatePixel(sample) {
    return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
}
""",
    }


def download_sentinel_image(
    date,
    save_folder="cache",
    bbox=None,
    max_delta_days=5,
):
    save_path = Path(save_folder)
    save_path.mkdir(parents=True, exist_ok=True)
    bbox = bbox or BIRCHGLETSCHER_BBOX

    try:
        date_obj = datetime.strptime(str(date), "%Y-%m-%d")
    except ValueError:
        return {
            "date": str(date),
            "file_path": None,
            "error": "Date must use YYYY-MM-DD format.",
        }

    try:
        token = make_token()
    except Exception as exc:
        return {"date": str(date), "file_path": None, "error": str(exc)}

    last_error = None
    for check_date in _candidate_dates(date_obj, max_delta_days):
        file_path = save_path / f"sentinel_image_{check_date}.png"
        if file_path.exists():
            return {
                "date": check_date,
                "file_path": str(file_path),
                "cached": True,
            }

        try:
            response = requests.post(
                PROCESS_URL,
                headers={"Authorization": f"Bearer {token}"},
                json=_payload_for_date(check_date, bbox),
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException as exc:
            last_error = f"Request failed for {check_date}: {exc}"
            continue

        if response.status_code != 200:
            last_error = (
                f"Sentinel Hub returned HTTP {response.status_code} for {check_date}."
            )
            continue

        if is_image_dark(response.content):
            last_error = f"Image for {check_date} was empty or mostly dark."
            continue

        file_path.write_bytes(response.content)
        return {"date": check_date, "file_path": str(file_path), "cached": False}

    return {
        "date": str(date),
        "file_path": None,
        "error": last_error or "No suitable image found within +/- 5 days.",
    }
