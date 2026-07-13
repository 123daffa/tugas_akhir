# test_image_pipeline.py (di folder backend/)
import sys
import os
import requests
from io import BytesIO
from PIL import Image

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.pipelines.image_pipeline import run_image_pipeline

# def download_image_as_bytes(url: str) -> bytes:
#     """Download gambar dari URL dan kembalikan sebagai bytes."""
#     response = requests.get(url, timeout=10)
#     return response.content

# def pil_to_bytes(pil_image: Image.Image) -> bytes:
#     """Konversi PIL Image ke bytes."""
#     buffer = BytesIO()
#     pil_image.save(buffer, format="JPEG")
#     return buffer.getvalue()

def test_image_pipeline():
    print("=" * 60)
    print("SIMULASI IMAGE PIPELINE")
    print("=" * 60)

    # ================================================
    # Contoh 1: Gambar dan caption tidak sesuai
    # ================================================
    # print("\n[TEST 1] Gambar dan caption berbeda sumber berasal dari mafindo")
    # print("-" * 40)

    # gambar_lokal = "frame_3.jpg"

    # if os.path.exists(gambar_lokal):
    #     with open(gambar_lokal, "rb") as f:
    #         image_bytes_1 = f.read()

    #     caption_1 = "Laporan menyebutkan serangan udara Rusia menargetkan lokasi aman di Ukraina, yang diduga membunuh Presiden Volodymyr Zelenskyy. Media Ukraina dilaporkan sedang meliput insiden tersebut, meskipun konfirmasi resmi masih menunggu.Jika benar, serangan ini bisa menandai eskalasi besar dalam perang, memicu kepanikan dan ketidakpastian di seluruh wilayah."

    #     print(f"Input caption  : {caption_1}")
    #     print(f"File gambar    : {gambar_lokal}")
    #     print("\nMemproses...")

    #     result_1 = run_image_pipeline(image_bytes_1, caption_1)

    #     print("\n[HASIL TEST 1]")
    #     print(f"  Similarity score   : {result_1['similarity_score']}")
    #     print(f"  Caption translated : {result_1['caption_translated']}")
    #     print(f"  Jumlah artikel     : {result_1['jumlah_artikel']}")
    #     print(f"  Rata-rata score    : {result_1['rata_rata_score']}")
    #     print(f"  Kredibilitas score : {result_1['kredibilitas_score']}")
    #     # print(f"  Penjelasan         : {result_1['penjelasan']}")
    #     print(f"  Klasifikasi        : {result_1['klasifikasi']}")
    # else:
    #     print("Taruh file gambar dengan nama 'contoh_gambar.jpg' di folder backend/ untuk test ini")

    # print("\n[TEST 2] Gambar dan caption sama berasal dari detik.com (kemungkinan FAKTA)")
    # print("-" * 40)

    # gambar_lokal = "penjagaan_tni.jpeg"

    # if os.path.exists(gambar_lokal):
    #     with open(gambar_lokal, "rb") as f:
    #         image_bytes_2 = f.read()

    #     caption_2 = "Prajurit TNI dikabarkan menjaga ketat rumah Jampidsus Kejaksaan Agung (Kejagung), Febrie Adriansyah yang berlokasi di Kramat Pela, Jakarta Selatan (Jaksel). Pusat Penerangan (Puspen) TNI menjelaskan alasan penjagaan ketat tersebut."


    #     print(f"Input caption  : {caption_2}")
    #     print(f"File gambar    : {gambar_lokal}")
    #     print("\nMemproses...")

    #     result_2 = run_image_pipeline(image_bytes_2, caption_2)

    #     print("\n[HASIL TEST 2]")
    #     print(f"  Similarity score   : {result_2['similarity_score']}")
    #     print(f"  Caption translated : {result_2['caption_translated']}")
    #     print(f"  Jumlah artikel     : {result_2['jumlah_artikel']}")
    #     print(f"  Rata-rata score    : {result_2['rata_rata_score']}")
    #     print(f"  Kredibilitas score : {result_2['kredibilitas_score']}")
    #     # print(f"  Penjelasan         : {result_2['penjelasan']}")
    #     print(f"  Klasifikasi        : {result_2['klasifikasi']}")
    # else:
    #     print("Taruh file gambar dengan nama 'contoh_gambar.jpg' di folder backend/ untuk test ini")

    print("\n[TEST 3] Gambar dan caption tidak sama berasal dari mafindo (fabricated content)")
    print("-" * 40)

    gambar_lokal = "pertamina.jpg"

    if os.path.exists(gambar_lokal):
        with open(gambar_lokal, "rb") as f:
            image_bytes_3 = f.read()

        caption_3 = "Pertalite Mau Dihapus?Wacana ini kembali mencuat dan bikin masyarakat bertanya-tanya.Pemerintah kembali menyoroti keberadaan Pertalite dalam upaya memperbaiki penyaluran subsidi BBM agar lebih tepat sasaran. Selama ini, Pertalite yang seharusnya dinikmati masyarakat yang berhak masih banyak digunakan oleh kalangan mampu, sehingga beban subsidi dan kompensasi energi negara terus meningkat."


        print(f"Input caption  : {caption_3}")
        print(f"File gambar    : {gambar_lokal}")
        print("\nMemproses...")

        result_3 = run_image_pipeline(image_bytes_3, caption_3)

        print("\n[HASIL TEST 3]")
        print(f"  Similarity score   : {result_3['similarity_score']}")
        print(f"  Caption translated : {result_3['caption_translated']}")
        print(f"  Jumlah artikel     : {result_3['jumlah_artikel']}")
        print(f"  Rata-rata score    : {result_3['rata_rata_score']}")
        print(f"  Kredibilitas score : {result_3['kredibilitas_score']}")
        # print(f"  Penjelasan         : {result_3['penjelasan']}")
        print(f"  Klasifikasi        : {result_3['klasifikasi']}")
    else:
        print("Taruh file gambar dengan nama 'contoh_gambar.jpg' di folder backend/ untuk test ini")


if __name__ == "__main__":
    test_image_pipeline()