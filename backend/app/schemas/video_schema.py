from dataclasses import dataclass, asdict, field
from typing import List, Optional

@dataclass
class VideoCheckResponse:
    jumlah_frame: int
    jumlah_artikel: int
    score_tavily: float
    klasifikasi: str
    confidence: float
    video_relevance_score: float
    penjelasan_teks: str
    penjelasan_video: str
    artikel_video_paling_relevan: Optional[str] = None
    stance_breakdown: dict = field(default_factory=dict)
    alasan_per_artikel: List[dict] = field(default_factory=list)
    detail_video_per_artikel: List[dict] = field(default_factory=list)
    articles: List[dict] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)