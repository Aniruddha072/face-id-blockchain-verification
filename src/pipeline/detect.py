from dataclasses import dataclass

from deepface import DeepFace

from .exceptions import NoFaceDetectedError

DETECTOR_BACKEND = "retinaface"
MODEL_NAME = "ArcFace"


@dataclass
class FaceEncoding:
    bbox: dict[str, int]
    confidence: float


def detect_and_encode(image_path: str) -> FaceEncoding:
    """Detect the most prominent face in an image.

    Picks the largest detected face by bounding-box area (ties broken by
    confidence) when more than one face is present. verify_candidates()
    re-runs detection itself per candidate, so only the bbox and confidence
    are needed here, not the embedding DeepFace.represent() also computes.
    """
    try:
        results = DeepFace.represent(
            img_path=image_path,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR_BACKEND,
        )
    except ValueError as exc:
        raise NoFaceDetectedError(f"no face detected in {image_path}") from exc

    if not results:
        raise NoFaceDetectedError(f"no face detected in {image_path}")

    best = max(results, key=_face_rank)
    region = best["facial_area"]
    bbox = {"x": region["x"], "y": region["y"], "w": region["w"], "h": region["h"]}

    return FaceEncoding(bbox=bbox, confidence=best["face_confidence"])


def _face_rank(entry: dict) -> tuple[int, float]:
    region = entry["facial_area"]
    area = region["w"] * region["h"]
    return (area, entry["face_confidence"])
