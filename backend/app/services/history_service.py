from app.repositories.detection_repository import DetectionRepository
from app.repositories.user_repository import UserRepository
from app.utils.errors import NotFoundError, ForbiddenError


class HistoryService:
    @staticmethod
    def list_for_user(user_id, category, search_term, page, per_page):
        pagination = DetectionRepository.search(
            user_id=user_id, category=category,
            search_term=search_term, page=page, per_page=per_page
        )
        return {
            'items': [i.to_list_dict() for i in pagination.items],
            'totalPages': pagination.pages,
            'currentPage': pagination.page,
            'totalItems': pagination.total
        }

    @staticmethod
    def get_detail(user_id, history_id):
        record = DetectionRepository.find_by_id(history_id)
        if not record:
            raise NotFoundError('Riwayat tidak ditemukan.')

        current_user = UserRepository.find_by_id(user_id)
        is_owner = str(record.user_id) == str(user_id)
        is_admin = current_user and current_user.is_admin
        if not is_owner and not is_admin:
            raise ForbiddenError('Anda tidak memiliki akses ke riwayat ini.')

        return record.to_detail_dict()

    @staticmethod
    def save_check_result(user_id, mode, result, input_text=None, caption=None, image_path=None):
        """Simpan hasil pipeline cek teks/gambar/video ke detection_history.
        Dipanggil dari text_routes.py / image_routes.py / video_routes.py
        SETELAH pipeline berhasil. Kalau user_id kosong (tidak login), tidak
        disimpan — cukup return None, jangan sampai gagal/nge-crash request
        utama yang sudah berhasil dapat hasil cek kontennya."""
        if not user_id:
            return None

        articles = result.get('articles') or []
        first_article = articles[0] if articles else {}

        # Judul riwayat: dari teks asli (mode text) atau caption (mode image/video)
        raw_title = input_text if mode == 'text' else caption
        title = (raw_title or '').strip()[:100] or f'Cek {mode}'

        # kredibilitas_score dari pipeline biasanya 0.0 - 1.0, kolom `accuracy`
        # di model berupa Integer (persentase 0-100)
        kredibilitas = result.get('kredibilitas_score', 0) or 0
        accuracy = round(kredibilitas * 100) if kredibilitas <= 1 else round(kredibilitas)

        return DetectionRepository.create(
            user_id=user_id,
            mode=mode,
            title=title,
            category=result.get('klasifikasi', 'Tidak diketahui'),
            accuracy=accuracy,
            conclusion=result.get('penjelasan', ''),
            input_text=input_text if mode == 'text' else None,
            image_path=image_path,
            source_title=first_article.get('title'),
            source_url=first_article.get('url'),
            metrics={
                'articles': articles,
                'jumlah_artikel': result.get('jumlah_artikel'),
                'similarity_score': result.get('similarity_score'),
                'caption_translated': result.get('caption_translated'),
            }
        )