from dataclasses import dataclass
from typing import List

@dataclass
class Tag:
    label: str
    confidence: str

@dataclass
class Recommendation:
    title: str
    video_id: str
    summary: str
    tags: List[Tag]