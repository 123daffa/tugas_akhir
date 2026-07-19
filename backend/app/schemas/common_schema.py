from dataclasses import dataclass, asdict

@dataclass
class ErrorResponse:
    detail: str

    def to_dict(self):
        return asdict(self)

@dataclass  
class HealthCheckResponse:
    status: str

    def to_dict(self):
        return asdict(self)