from dataclasses import dataclass, asdict, field
from typing import List

@dataclass
class ArticleItem:
    title: str
    url: str
    score: float

    def to_dict(self):
        return asdict(self)

@dataclass
class VideoCheckResponse:
    similarity_score: float
    similarity_per_frame: List[float]
    jumlah_frame_dianalisis: int
    caption_translated: str
    jumlah_artikel: int
    rata_rata_score: float
    kredibilitas_score: float
    penjelasan: str
    klasifikasi: str
    articles: List[dict] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)