from dataclasses import dataclass, asdict, field
from typing import List, Optional

@dataclass
class ImageCheckResponse:
    jumlah_artikel: int
    kredibilitas_score: float
    klasifikasi: str
    confidence: float
    image_relevance_score: float
    penjelasan_teks: str
    penjelasan_gambar: str
    artikel_gambar_paling_relevan: Optional[str] = None
    stance_breakdown: dict = field(default_factory=dict)
    alasan_per_artikel: List[dict] = field(default_factory=list)
    detail_gambar_per_artikel: List[dict] = field(default_factory=list)
    articles: List[dict] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)