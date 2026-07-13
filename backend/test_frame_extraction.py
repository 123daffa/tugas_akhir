# test_frame_extraction.py (di folder backend/)
from app.services.frame_extraction_service import extract_keyframes

# Baca file video
with open("Zelensky_dead.mp4", "rb") as f:
    video_bytes = f.read()

# Ekstrak frame
frames = extract_keyframes(video_bytes, max_frames=5)

print(f"Jumlah frame: {len(frames)}")
print(f"Ukuran frame pertama (width x height): {frames[0].size}")

# Simpan frame ke file untuk dicek secara visual
for i, frame in enumerate(frames, 1):
    frame.save(f"frame_{i}.jpg")
    print(f"Frame {i} disimpan → frame_{i}.jpg")