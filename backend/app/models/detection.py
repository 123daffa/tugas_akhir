from datetime import datetime, timezone
from extensions import db


class DetectionHistory(db.Model):
    __tablename__ = 'detection_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    mode = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    input_text = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(500), nullable=True)
    video_path = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    accuracy = db.Column(db.Integer, nullable=False)
    conclusion = db.Column(db.Text, nullable=False)
    source_title = db.Column(db.String(255), nullable=True)
    source_url = db.Column(db.String(500), nullable=True)
    metrics = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def to_list_dict(self):
        return {
            'id': self.id, 'image': self.image_path or '', 'category': self.category,
            'date': self.created_at.strftime('%d %b %Y'),
            'type': {'text': 'Teks', 'image': 'Gambar', 'video': 'Video'}.get(self.mode, self.mode),
            'title': self.title, 'verified': True
        }

    def to_detail_dict(self):
        data = self.to_list_dict()
        metrics = self.metrics or {}

        data.update({
            'mode': self.mode,  # mode mentah ('text'/'image'/'video'), untuk kondisi tampilan
            'accuracy': self.accuracy,
            'conclusion': self.conclusion,
            'source': {'title': self.source_title or '', 'url': self.source_url or '#'},
            'articles': metrics.get('articles', []),
            'jumlah_artikel': metrics.get('jumlah_artikel'),
            'confidence': metrics.get('confidence'),
            'stance_breakdown': metrics.get('stance_breakdown', {}),
            'alasan_per_artikel': metrics.get('alasan_per_artikel', []),
            'penjelasan_gambar': metrics.get('penjelasan_gambar'),
            'image_relevance_score': metrics.get('image_relevance_score'),
            'artikel_gambar_paling_relevan': metrics.get('artikel_gambar_paling_relevan'),
            'detail_gambar_per_artikel': metrics.get('detail_gambar_per_artikel', []),
            'jumlah_frame': metrics.get('jumlah_frame'),
            'penjelasan_video': metrics.get('penjelasan_video'),
            'video_relevance_score': metrics.get('video_relevance_score'),
            'artikel_video_paling_relevan': metrics.get('artikel_video_paling_relevan'),
            'detail_video_per_artikel': metrics.get('detail_video_per_artikel', []),
        })
        return data