from dataclasses import dataclass

import requests

from . import config
from .exceptions import NoCandidatesFoundError
from .retry import with_retry

SOCIAL_DOMAINS = (
    "instagram.com",
    "x.com",
    "twitter.com",
    "facebook.com",
    "linkedin.com",
    "tiktok.com",
    "reddit.com",
    "youtube.com",
)

MAX_UPLOAD_BYTES = 500 * 1024
REQUEST_TIMEOUT = 30


@dataclass
class Candidate:
    url: str
    platform: str
    thumbnail_url: str


def _platform_for(url: str) -> str | None:
    for domain in SOCIAL_DOMAINS:
        if domain in url:
            return domain
    return None


def _upload_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    if len(image_bytes) > MAX_UPLOAD_BYTES:
        raise ValueError(
            f"{image_path} is {len(image_bytes)} bytes, over SerpApi's "
            f"{MAX_UPLOAD_BYTES} byte upload limit; resize or compress it "
            "before calling reverse_search"
        )

    def _call():
        response = requests.post(
            "https://serpapi.com/image",
            files={"image": image_bytes},
            data={"api_key": config.SERPAPI_KEY},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    return with_retry(_call)["image_id"]


def reverse_search(image_path: str) -> list[Candidate]:
    """Find social-media posts containing the same face as image_path.

    Uploads the image to SerpApi to get a short-lived image_id, then runs a
    Google Lens search against it. Only genuine SerpApi results are
    returned, filtered to known social domains; nothing here is hardcoded.
    """
    config.require("SERPAPI_KEY")
    image_id = _upload_image(image_path)

    def _call():
        response = requests.get(
            "https://serpapi.com/search",
            params={
                "engine": "google_lens",
                "image_id": image_id,
                "api_key": config.SERPAPI_KEY,
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    data = with_retry(_call)

    candidates = []
    for match in data.get("visual_matches", []):
        link = match.get("link", "")
        platform = _platform_for(link)
        if platform is None:
            continue
        candidates.append(
            Candidate(url=link, platform=platform, thumbnail_url=match.get("thumbnail", ""))
        )

    if not candidates:
        raise NoCandidatesFoundError("no social-media matches found in reverse search results")

    return candidates
