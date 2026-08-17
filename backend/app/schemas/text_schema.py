from dataclasses import dataclass, asdict, field
from typing import List, Dict

# Pengecekan field dari dict jadi dataclass 
@dataclass
class TextCheckRequest:
    text: str

@dataclass
class TextCheckResponse:
    jumlah_artikel: int
    score_tavily: float
    klasifikasi: str
    confidence: float
    penjelasan: str
    alasan_per_artikel: List[dict] = field(default_factory=list)
    stance_breakdown: Dict[str, float] = field(default_factory=dict)
    articles: List[dict] = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)