from extensions import db
from app.models import DetectionHistory


def make_title(text, max_len=80):
    text = (text or '').strip()
    return text[:max_len] + ('...' if len(text) > max_len else '')


def save_detection_result(user_id, mode, text, result, image_path=None, video_path=None):
    record = DetectionHistory(
        user_id=user_id, mode=mode, title=make_title(text) or f'Deteksi {mode}',
        input_text=text, image_path=image_path, video_path=video_path,
        category=result['category'], accuracy=result['accuracy'], conclusion=result['conclusion'],
        source_title=result.get('source_title'), source_url=result.get('source_url'),
        metrics=result.get('metrics')
    )
    db.session.add(record)
    db.session.commit()
    return record