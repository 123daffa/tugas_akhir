from app.core.constants import (
    SIMILARITY_THRESHOLD_HIGH,
    SIMILARITY_THRESHOLD_LOW,
    KREDIBILITAS_THRESHOLD_HIGH,
    KREDIBILITAS_THRESHOLD_LOW,
    LABEL_FAKTA,
    LABEL_MISLEADING,
    LABEL_FABRICATED,
    LABEL_FALSE
)

def classify_text_only ( kredibilitas_score: float) -> str:
    if kredibilitas_score >= KREDIBILITAS_THRESHOLD_HIGH:
        return LABEL_FAKTA
    else:
        return LABEL_FALSE

def classify_content(similarity_score: float, kredibilitas_score: float) -> str:
    if similarity_score >= SIMILARITY_THRESHOLD_HIGH and kredibilitas_score >= KREDIBILITAS_THRESHOLD_HIGH:
        return LABEL_FAKTA
    elif similarity_score < SIMILARITY_THRESHOLD_HIGH and kredibilitas_score >= KREDIBILITAS_THRESHOLD_HIGH:
        return LABEL_MISLEADING
    elif similarity_score >= SIMILARITY_THRESHOLD_HIGH and kredibilitas_score < KREDIBILITAS_THRESHOLD_LOW:
        return LABEL_FABRICATED
    else:
        return LABEL_FALSE