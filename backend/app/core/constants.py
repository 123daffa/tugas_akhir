# ===== Threshold untuk Klasifikasi =====
MINIMAL_SCORES_TAVILY = 0.8

# ===== Label Klasifikasi =====
LABEL_FAKTA = "Fakta"
LABEL_MISLEADING = "Misleading Content"
LABEL_FABRICATED = "Fabricated Content"
LABEL_FALSE = "False Content"

# ===== Konfigurasi Tavily Search =====
TAVILY_MAX_RESULTS = 10
TAVILY_SEARCH_DEPTH = "advanced"
TAVILY_TOPIC = "news"

# ===== Konfigurasi Video Pipeline =====
MAX_FRAMES_TO_EXTRACT = 5          # jumlah frame yang diambil dari video
FRAME_EXTRACTION_INTERVAL_SEC = 2  # ambil 1 frame tiap berapa detik

# ===== Konfigurasi Model =====
# MAX_TEXT_LENGTH = 512        # batas panjang teks untuk tokenizer
GROQ_MODEL_NAME = "llama-3.1-8b-instant" 

# ===== Limitasi File Upload =====
MAX_IMAGE_SIZE_MB = 5
MAX_VIDEO_SIZE_MB = 10
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi"}