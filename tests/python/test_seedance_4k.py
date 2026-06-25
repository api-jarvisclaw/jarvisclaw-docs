"""
Test: bytedance/seedance-2.0 with resolution=4K

Environment Variables:
  JARVISCLAW_API_KEY  - Your API key (sk-...)

Usage:
  export JARVISCLAW_API_KEY=sk-your-api-key
  python test_seedance_4k.py
"""

import os
import sys
import json
import time
import logging
import requests
from datetime import datetime
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────
API_KEY = os.environ.get("JARVISCLAW_API_KEY", "")
BASE_URL = os.environ.get("JARVISCLAW_BASE_URL", "https://api.jarvisclaw.ai/v1")

if not API_KEY:
    print("ERROR: JARVISCLAW_API_KEY environment variable is required")
    sys.exit(1)

# ─── Logging ─────────────────────────────────────────────────────────────────
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"test_seedance_4k_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

output_dir = Path(__file__).parent / "output" / f"seedance_4k_{timestamp}"
output_dir.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def main():
    logger.info("Test: bytedance/seedance-2.0 with resolution=4K")
    logger.info(f"Base URL: {BASE_URL}")
    logger.info(f"API Key: {API_KEY[:8]}...{API_KEY[-4:]}")
    logger.info(f"Log: {log_file}")
    logger.info(f"Output: {output_dir}")
    logger.info("")

    url = f"{BASE_URL}/videos/generations"
    payload = {
        "model": "bytedance/seedance-2.0",
        "prompt": "",
        "duration_seconds": 5,
        "resolution": "4K",
    }

    logger.info(f"POST {url}")
    logger.info(f"Request: {json.dumps(payload, indent=2)}")

    # Submit
    resp = requests.post(url, headers=HEADERS, json=payload, timeout=60)
    logger.info(f"Status: {resp.status_code}")
    data = resp.json()
    logger.info(f"Response: {json.dumps(data, indent=2)}")

    if resp.status_code != 200:
        logger.error(f"Submission failed: {resp.status_code}")
        return

    job_id = data.get("id", "")
    poll_path = data.get("poll_url", "")
    if not poll_path and job_id:
        poll_path = f"/v1/videos/generations/{requests.utils.quote(job_id, safe='')}"

    if not poll_path:
        logger.error("No poll_url or id in response")
        return

    base_host = BASE_URL.split("/v1")[0]
    poll_url = base_host + poll_path
    logger.info(f"Polling: {poll_url}")

    # Poll
    max_wait = 600  # 10 minutes
    interval = 10
    elapsed = 0

    while elapsed < max_wait:
        time.sleep(interval)
        elapsed += interval

        poll_resp = requests.get(poll_url, headers=HEADERS, timeout=30)
        poll_data = poll_resp.json()
        status = poll_data.get("status", "unknown")
        progress = poll_data.get("progress", "?")
        logger.info(f"Poll [{elapsed}s]: status={status}, progress={progress}%")

        if status == "completed":
            logger.info(f"Result: {json.dumps(poll_data, indent=2)}")
            video_items = poll_data.get("data", [])
            if video_items:
                video_url = video_items[0].get("url", "")
                if video_url:
                    logger.info(f"Downloading: {video_url}")
                    dl = requests.get(video_url, timeout=(10, 300), stream=True)
                    video_path = output_dir / "seedance_4k.mp4"
                    total = 0
                    with open(video_path, "wb") as f:
                        for chunk in dl.iter_content(65536):
                            f.write(chunk)
                            total += len(chunk)
                    logger.info(f"Downloaded: {video_path.name} ({total} bytes)")
            logger.info("✓ PASSED")
            return

        elif status == "failed":
            logger.error(f"Generation failed: {json.dumps(poll_data, indent=2)}")
            return

    logger.warning(f"⚠ TIMEOUT after {max_wait}s (job: {job_id})")
    logger.warning("Job is NOT lost — retrieve within 48h")


if __name__ == "__main__":
    main()
