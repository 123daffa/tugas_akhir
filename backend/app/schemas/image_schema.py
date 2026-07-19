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
class ImageCheckResponse:
    similarity_score: float
    jumlah_artikel: int
    caption_translated: str
    kredibilitas_score: float
    penjelasan: str
    klasifikasi: str
    articles: List[dict] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)