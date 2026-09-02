import os
import tempfile
from dataclasses import dataclass

import requests
from deepface import DeepFace

from .detect import MODEL_NAME
from .exceptions import NoVerifiedMatchError
from .retry import with_retry
from .search import Candidate

REQUEST_TIMEOUT = 30


@dataclass
class Match:
    candidate: Candidate
    similarity_score: float
    model: str


def _download_to_temp(url: str) -> str:
    def _call():
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.content

    content = with_retry(_call)
    fd, path = tempfile.mkstemp(suffix=".jpg")
    with os.fdopen(fd, "wb") as f:
        f.write(content)
    return path


def verify_candidates(image_path: str, candidates: list[Candidate]) -> Match:
    """Confirm which candidates are genuinely the same face as image_path.

    Downloads each candidate's thumbnail and runs DeepFace.verify() against
    the source image, keeping the best-scoring genuine match. A candidate
    whose thumbnail can't be downloaded or decoded is skipped, not fatal.
    """
    best: Match | None = None

    for candidate in candidates:
        try:
            thumb_path = _download_to_temp(candidate.thumbnail_url)
        except Exception:
            continue

        try:
            result = DeepFace.verify(
                img1_path=image_path, img2_path=thumb_path, model_name=MODEL_NAME
            )
        except Exception:
            continue
        finally:
            os.remove(thumb_path)

        if not result["verified"]:
            continue
        if best is None or result["distance"] < best.similarity_score:
            best = Match(candidate=candidate, similarity_score=result["distance"], model=MODEL_NAME)

    if best is None:
        raise NoVerifiedMatchError("no candidate verified as a genuine match")

    return best
