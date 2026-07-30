from app.repositories.user_repository import UserRepository
from app.repositories.detection_repository import DetectionRepository
from app.utils.errors import NotFoundError, ConflictError, ServiceError

CATEGORY_LABELS = ['Fakta', 'False Content', 'Misleading Content', 'Fabricated Content']


class AdminService:
    # ---- Users ----
    @staticmethod
    def list_users(search_term, page, per_page):
        pagination = UserRepository.search(search_term, page, per_page)
        return {
            'items': [u.to_dict() for u in pagination.items],
            'totalPages': pagination.pages,
            'currentPage': pagination.page,
            'totalItems': pagination.total
        }

    @staticmethod
    def create_user(data):
        full_name = (data.get('fullName') or '').strip()
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''
        role = data.get('role') if data.get('role') in ('user', 'admin') else 'user'

        if not full_name or not email or not password:
            raise ServiceError('Nama, email, dan password wajib diisi.')
        if len(password) < 6:
            raise ServiceError('Password minimal 6 karakter.')
        if UserRepository.email_taken(email):
            raise ConflictError('Email sudah digunakan akun lain.')

        user = UserRepository.create(full_name, email, password, role)
        return user.to_dict()

    @staticmethod
    def get_user_detail(user_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFoundError('User tidak ditemukan.')
        return user.to_dict()

    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFoundError('User tidak ditemukan.')

        if 'fullName' in data:
            user.full_name = data['fullName'].strip()
        if 'email' in data:
            new_email = data['email'].strip().lower()
            if UserRepository.email_taken(new_email, exclude_id=user.id):
                raise ConflictError('Email sudah digunakan akun lain.')
            user.email = new_email
        if 'role' in data and data['role'] in ('user', 'admin'):
            user.role = data['role']

        UserRepository.save(user)
        return user.to_dict()

    @staticmethod
    def delete_user(requesting_user_id, target_user_id):
        if str(target_user_id) == str(requesting_user_id):
            raise ServiceError('Tidak bisa menghapus akun sendiri.')
        user = UserRepository.find_by_id(target_user_id)
        if not user:
            raise NotFoundError('User tidak ditemukan.')
        UserRepository.delete(user)

    # ---- Content ----
    @staticmethod
    def list_content(category, search_term, page, per_page):
        pagination = DetectionRepository.search(
            category=category, search_term=search_term, page=page, per_page=per_page
        )
        items = []
        for item in pagination.items:
            d = item.to_list_dict()
            d['ownerName'] = item.user.full_name if item.user else '(user dihapus)'
            d['ownerEmail'] = item.user.email if item.user else '-'
            items.append(d)
        return {
            'items': items,
            'totalPages': pagination.pages,
            'currentPage': pagination.page,
            'totalItems': pagination.total
        }

    @staticmethod
    def get_content_detail(content_id):
        item = DetectionRepository.find_by_id(content_id)
        if not item:
            raise NotFoundError('Konten tidak ditemukan.')
        data = item.to_detail_dict()
        data['ownerName'] = item.user.full_name if item.user else '(user dihapus)'
        data['ownerEmail'] = item.user.email if item.user else '-'
        return data

    @staticmethod
    def delete_content(content_id):
        item = DetectionRepository.find_by_id(content_id)
        if not item:
            raise NotFoundError('Konten tidak ditemukan.')
        DetectionRepository.delete(item)

    # ---- Stats ----
    @staticmethod
    def get_stats():
        category_breakdown = DetectionRepository.category_breakdown()
        for cat in CATEGORY_LABELS:
            category_breakdown.setdefault(cat, 0)
        return {
            'totalUsers': UserRepository.count(),
            'totalDetections': DetectionRepository.count(),
            'categoryBreakdown': category_breakdown,
            'modeBreakdown': DetectionRepository.mode_breakdown()
        }