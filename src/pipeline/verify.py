import os
import tempfile
from dataclasses import dataclass

import requests
from deepface import DeepFace

from .detect import DETECTOR_BACKEND, MODEL_NAME
from .exceptions import NoVerifiedMatchError
from .retry import with_retry
from .search import Candidate

REQUEST_TIMEOUT = 30


@dataclass
class Match:
    candidate: Candidate
    similarity_score: float
    model: str
    models_agreed: int
    models_total: int


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


TOP_N_MATCHES = 3
ENSEMBLE_MODELS = (MODEL_NAME, "Facenet512", "VGG-Face")
AGREEMENT_NEEDED = 2  # of len(ENSEMBLE_MODELS), a majority


def verify_candidates(image_path: str, candidates: list[Candidate]) -> list[Match]:
    """Confirm which candidates are genuinely the same face as image_path.

    Downloads each candidate's thumbnail and runs it past an ensemble of
    face-verification models. A single model can confidently match the
    wrong person, so a candidate only counts as genuinely verified if a
    majority of ENSEMBLE_MODELS agree. Ranking still uses the primary
    model's (ArcFace) distance, the agreement count travels alongside it
    for transparency and gets anchored on-chain. A candidate whose
    thumbnail can't be downloaded or decoded is skipped, not fatal.
    """
    verified: list[Match] = []

    for candidate in candidates:
        try:
            thumb_path = _download_to_temp(candidate.thumbnail_url)
        except Exception:
            continue

        try:
            agreed = 0
            primary_distance = None
            for model_name in ENSEMBLE_MODELS:
                result = DeepFace.verify(
                    img1_path=image_path,
                    img2_path=thumb_path,
                    model_name=model_name,
                    detector_backend=DETECTOR_BACKEND,
                )
                if model_name == MODEL_NAME:
                    primary_distance = result["distance"]
                if result["verified"]:
                    agreed += 1
        except Exception:
            continue
        finally:
            os.remove(thumb_path)

        if agreed < AGREEMENT_NEEDED:
            continue
        verified.append(
            Match(
                candidate=candidate,
                similarity_score=primary_distance,
                model=MODEL_NAME,
                models_agreed=agreed,
                models_total=len(ENSEMBLE_MODELS),
            )
        )

    if not verified:
        raise NoVerifiedMatchError("no candidate verified as a genuine match")

    verified.sort(key=lambda m: m.similarity_score)
    return verified[:TOP_N_MATCHES]
