from enum import Enum

class ProductPreviewStatus(str, Enum):
    PREVIEW = "preview"
    APPROVED = "approved"
    REJECTED = "rejected"
    MOVED = "moved"