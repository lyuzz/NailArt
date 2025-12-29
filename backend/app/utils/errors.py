class NailArtError(Exception):
    code = "PROCESSING_ERROR"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class HandNotDetectedError(NailArtError):
    code = "HAND_NOT_DETECTED"


class ImageReadError(NailArtError):
    code = "IMAGE_READ_FAILED"


class AssetNotFoundError(NailArtError):
    code = "ASSET_NOT_FOUND"
