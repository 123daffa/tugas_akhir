from sqlalchemy import func
from extensions import db
from app.models import DetectionHistory


class DetectionRepository:
    """Semua query ke tabel detection_history ada di sini."""

    @staticmethod
    def find_by_id(detection_id):
        return DetectionHistory.query.get(detection_id)

    @staticmethod
    def search(user_id=None, category=None, search_term='', page=1, per_page=10):
        query = DetectionHistory.query
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        if category and category != 'Semua':
            query = query.filter_by(category=category)
        if search_term:
            query = query.filter(DetectionHistory.title.ilike(f'%{search_term}%'))
        return query.order_by(DetectionHistory.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def count():
        return DetectionHistory.query.count()

    @staticmethod
    def category_breakdown():
        return dict(
            db.session.query(DetectionHistory.category, func.count(DetectionHistory.id))
            .group_by(DetectionHistory.category).all()
        )

    @staticmethod
    def mode_breakdown():
        return dict(
            db.session.query(DetectionHistory.mode, func.count(DetectionHistory.id))
            .group_by(DetectionHistory.mode).all()
        )
    @staticmethod
    def create(user_id, mode, title, category, accuracy, conclusion,
               input_text=None, image_path=None, video_path=None,
               source_title=None, source_url=None, metrics=None):
        item = DetectionHistory(
            user_id=user_id,
            mode=mode,
            title=title,
            input_text=input_text,
            image_path=image_path,
            video_path=video_path,
            category=category,
            accuracy=accuracy,
            conclusion=conclusion,
            source_title=source_title,
            source_url=source_url,
            metrics=metrics
        )
        db.session.add(item)
        db.session.commit()
        return item
    
    @staticmethod
    def delete(item):
        db.session.delete(item)
        db.session.commit()