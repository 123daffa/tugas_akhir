# ===== Threshold untuk Klasifikasi =====
SIMILARITY_THRESHOLD_HIGH = 0.5
SIMILARITY_THRESHOLD_LOW = 0.2

KREDIBILITAS_THRESHOLD_HIGH = 0.6
KREDIBILITAS_THRESHOLD_LOW = 0.3
KREDIBILITAS_THRESHOLD_VERY_LOW = 0.1

# ===== Label Klasifikasi =====
LABEL_FAKTA = "FAKTA"
LABEL_MISLEADING = "MISLEADING"
LABEL_FABRICATED = "FABRICATED"
LABEL_FALSE = "FALSE"

# ===== Konfigurasi Tavily Search =====
TAVILY_MAX_RESULTS = 10
TAVILY_SEARCH_DEPTH = "advanced"
TAVILY_TOPIC = "news"
INCLUDE_DOMAINS = ["detik.com", "kompas.com", "cnnindonesia.com", "tribunnews.com", "liputan6.com"]

# ===== Konfigurasi Video Pipeline =====
MAX_FRAMES_TO_EXTRACT = 5          # jumlah frame yang diambil dari video
FRAME_EXTRACTION_INTERVAL_SEC = 2  # ambil 1 frame tiap berapa detik

# ===== Konfigurasi Model =====
# MAX_TEXT_LENGTH = 512        # batas panjang teks untuk tokenizer
# GROQ_MODEL_NAME = "llama-3.3-70b-versatile"

# ===== Limitasi File Upload =====
MAX_IMAGE_SIZE_MB = 10
MAX_VIDEO_SIZE_MB = 50
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi"}