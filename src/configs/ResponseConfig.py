from enum import Enum


class ResponseConfig(Enum):
    ASSET_UNSUPPORTED_TYPE: str = "asset type is not supported"
    ASSET_EXCEEDED_MAX_SIZE: str = "asset exceeded maximum allowed size"
    ASSET_UPLOAD_FAILED: str = "asset upload failed"
    ASSET_UPLOAD_SUCCEEDED: str = "asset upload succeeded"
