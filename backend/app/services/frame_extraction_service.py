import cv2
import os
import tempfile
from PIL import Image
from app.core.constants import MAX_FRAMES_TO_EXTRACT


def extract_keyframes(video_bytes: bytes, max_frames: int = MAX_FRAMES_TO_EXTRACT) -> list:
    """
    Ekstrak frame-frame penting dari video secara merata
    dari awal sampai akhir durasi video.

    Parameter:
        video_bytes : isi file video dalam bentuk bytes
        max_frames  : jumlah maksimum frame yang diekstrak

    Return:
        list of PIL.Image — siap dipakai oleh CLIP
    """

    # ================================================
    # Step 1: Tulis bytes ke file temporary di disk
    # OpenCV tidak bisa baca dari bytes langsung,
    # butuh path file fisik
    # ================================================
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
        tmp_file.write(video_bytes)
        tmp_path = tmp_file.name

    frames = []

    try:
        # ================================================
        # Step 2: Buka video dengan OpenCV
        # ================================================
        cap = cv2.VideoCapture(tmp_path)

        if not cap.isOpened():
            raise ValueError(
                "Video tidak bisa dibuka — "
                "pastikan format video didukung (mp4, avi, mov)"
            )

        # ================================================
        # Step 3: Ambil metadata video
        # ================================================
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        durasi_detik = total_frames / fps if fps > 0 else 0

        print(f"[INFO] Video: {total_frames} frames | "
              f"{fps:.1f} FPS | "
              f"durasi {durasi_detik:.1f} detik")

        # ================================================
        # Step 4: Tentukan posisi frame yang diambil
        # Strategi: interval merata sepanjang video
        # ================================================
        if total_frames == 0:
            raise ValueError("Video tidak memiliki frame yang bisa diekstrak")

        if total_frames <= max_frames:
            # Video sangat pendek — ambil semua frame yang ada
            frame_positions = list(range(total_frames))
        else:
            # Bagi video menjadi max_frames bagian yang sama panjang
            # Ambil 1 frame dari tiap bagian
            interval = total_frames / max_frames
            frame_positions = [int(i * interval) for i in range(max_frames)]

        print(f"[INFO] Posisi frame yang akan diambil: {frame_positions}")

        # ================================================
        # Step 5: Ekstrak frame satu per satu
        # ================================================
        for pos in frame_positions:
            # Pindahkan "kursor" video ke posisi frame yang diinginkan
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos)

            # Baca frame di posisi tersebut
            ret, frame = cap.read()

            if not ret:
                # Gagal baca frame — lewati, lanjut ke posisi berikutnya
                print(f"[WARNING] Gagal baca frame di posisi {pos}, dilewati")
                continue

            # ================================================
            # Step 6: Konversi BGR → RGB
            # OpenCV menyimpan gambar dalam format BGR (urutan channel terbalik)
            # PIL dan CLIP butuh format RGB
            # Kalau tidak dikonversi: warna merah jadi biru, biru jadi merah
            # ================================================
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # ================================================
            # Step 7: Konversi numpy array → PIL Image
            # CLIP butuh input dalam format PIL Image
            # ================================================
            pil_image = Image.fromarray(frame_rgb)
            frames.append(pil_image)

        cap.release()

    finally:
        # ================================================
        # Step 8: Hapus file temporary
        # Wajib dilakukan di blok finally supaya
        # file selalu terhapus meski terjadi error
        # ================================================
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
            print(f"[INFO] File temporary dihapus: {tmp_path}")

    # ================================================
    # Step 9: Validasi hasil
    # ================================================
    if len(frames) == 0:
        raise ValueError(
            "Tidak ada frame yang berhasil diekstrak. "
            "Pastikan file video tidak rusak."
        )

    print(f"[INFO] Berhasil mengekstrak {len(frames)} frame dari video")
    return frames