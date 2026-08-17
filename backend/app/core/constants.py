# ===== Threshold untuk Klasifikasi =====
MINIMAL_SCORES_TAVILY = 0.8
CLIP_SIMILARITY_FLOOR = 0.45
CLIP_SIMILARITY_CEILING = 0.85

# ===== Label Klasifikasi =====
KATEGORI_VALID = {"Fakta", "False Content", "Misleading Content", "Fabricated Content"}

# ===== Konfigurasi Tavily Search =====
TAVILY_MAX_RESULTS = 10
TAVILY_SEARCH_DEPTH = "advanced"
TAVILY_TOPIC = "news"
TAVILY_EXCLUDE_DOMAINS = ["https://www.instagram.com/", "https://www.facebook.com/", "https://twitter.com/", "https://www.tiktok.com/", "https://www.youtube.com/"]
TAVILY_MAX_RETRIES = 3
TAVILY_RETRY_BASE_DELAY = 2

# ===== Konfigurasi Video Pipeline =====
MAX_FRAMES_TO_EXTRACT = 5          # jumlah frame yang diambil dari video
FRAME_EXTRACTION_INTERVAL_SEC = 2  # ambil 1 frame tiap berapa detik
MAX_VIDEO_DURATION_SECONDS = 60
MIN_IMAGE_DIMENSION = 32

# ===== Konfigurasi Model =====
# MAX_TEXT_LENGTH = 512        # batas panjang teks untuk tokenizer
GROQ_MODEL_NAME = "openai/gpt-oss-20b" 

# ===== Limitasi File Upload =====
MAX_IMAGE_SIZE_MB = 10
MAX_VIDEO_SIZE_MB = 50
MAX_DIMENSION = 512  # resize gambar biar hemat ukuran, cukup untuk perbandingan CLIP
JPEG_QUALITY = 70
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi"}