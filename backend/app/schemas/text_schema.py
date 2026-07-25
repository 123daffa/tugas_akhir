from dataclasses import dataclass, asdict, field
from typing import List

@dataclass
class TextCheckRequest:
    text: str

@dataclass
class TextCheckResponse:
    jumlah_artikel: int
    kredibilitas_score: float
    penjelasan: str
    klasifikasi: str
    articles: List[dict] = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)