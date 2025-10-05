import requests
import os
from TOKEN import make_token
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO

TOKEN = make_token()


def is_image_dark(image_bytes, threshold=10):
    """ Check if the image is mostly black. """
    try:
        img = Image.open(BytesIO(image_bytes))
        grayscale = img.convert("L")  # convert to grayscale
        avg = sum(grayscale.getdata()) / (grayscale.width * grayscale.height)
        return avg < threshold
    except:
        return True


def download_sentinel_image(date: str, save_folder: str = "cache"):
    os.makedirs(save_folder, exist_ok=True)

    url = "https://services.sentinel-hub.com/api/v1/process"
    date_obj = datetime.strptime(date, "%Y-%m-%d")

    # ±5 Days
    for delta in range(0, 6):
        for sign in [1, -1]:
            check_date = (date_obj + timedelta(days=delta * sign)).strftime("%Y-%m-%d")

            payload = {
                "input": {
                    "bounds": {"bbox": [7.78, 46.38, 7.88, 46.45]},
                    "data": [
                        {
                            "type": "sentinel-2-l2a",
                            "dataFilter": {
                                "timeRange": {
                                    "from": f"{check_date}T00:00:00Z",
                                    "to": f"{check_date}T23:59:59Z",
                                },
                                "maxCloudCoverage": 20,
                            },
                        }
                    ],
                },
                "output": {
                    "width": 1024,
                    "height": 1024,
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

            response = requests.post(
                url, headers={"Authorization": f"Bearer {TOKEN}"}, json=payload
            )

            if response.status_code == 200 and not is_image_dark(response.content):
                file_path = os.path.join(save_folder, f"sentinel_image_{check_date}.png")
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Image saved as {file_path} for date {check_date}")
                return {"date": check_date, "file_path": file_path}

    print("No suitable image found within ±5 days")
    return {"date": date, "file_path": None, "error": "No suitable image found"}
