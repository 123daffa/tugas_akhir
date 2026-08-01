import cv2
import os
import tempfile
from PIL import Image
from app.core.constants import MAX_FRAMES_TO_EXTRACT, MAX_VIDEO_DURATION_SECONDS


def extract_keyframes(video_bytes: bytes, max_frames: int = MAX_FRAMES_TO_EXTRACT) -> list:
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
        tmp_file.write(video_bytes)
        tmp_path = tmp_file.name

    frames = []

    try:
        cap = cv2.VideoCapture(tmp_path)

        if not cap.isOpened():
            raise ValueError(
                "Video tidak bisa dibuka — "
                "pastikan format video didukung (mp4, avi, mov)"
            )

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        durasi_detik = total_frames / fps if fps > 0 else 0

        print(f"[INFO] Video: {total_frames} frames | "
              f"{fps:.1f} FPS | "
              f"durasi {durasi_detik:.1f} detik")

        # VALIDASI BARU: tolak video terlalu panjang SEBELUM ekstraksi frame,
        # supaya tidak buang waktu proses & representasi frame tetap rapat
        if durasi_detik > MAX_VIDEO_DURATION_SECONDS:
            raise ValueError(
                f"Video terlalu panjang ({durasi_detik:.0f} detik). "
                f"Maksimal durasi yang didukung: {MAX_VIDEO_DURATION_SECONDS} detik."
            )

        if total_frames == 0:
            raise ValueError("Video tidak memiliki frame yang bisa diekstrak")

        if total_frames <= max_frames:
            frame_positions = list(range(total_frames))
        else:
            interval = total_frames / max_frames
            frame_positions = [int(i * interval) for i in range(max_frames)]

        print(f"[INFO] Posisi frame yang akan diambil: {frame_positions}")

        for pos in frame_positions:
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
            ret, frame = cap.read()

            if not ret:
                print(f"[WARNING] Gagal baca frame di posisi {pos}, dilewati")
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            frames.append(pil_image)

        cap.release()

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
            print(f"[INFO] File temporary dihapus: {tmp_path}")

    if len(frames) == 0:
        raise ValueError(
            "Tidak ada frame yang berhasil diekstrak. "
            "Pastikan file video tidak rusak."
        )

    print(f"[INFO] Berhasil mengekstrak {len(frames)} frame dari video")
    return frames