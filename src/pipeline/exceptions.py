class PipelineError(Exception):
    """Base class for every error the pipeline stages raise on purpose."""


class NoFaceDetectedError(PipelineError):
    """Raised when no face could be detected in the input image."""


class NoCandidatesFoundError(PipelineError):
    """Raised when reverse search returns no social-media candidates."""


class NoVerifiedMatchError(PipelineError):
    """Raised when no candidate passes face verification against the source."""


class ChainError(PipelineError):
    """Raised when a blockchain read or write fails after retries are exhausted."""


class ConfigError(PipelineError):
    """Raised when a required .env setting is missing."""
