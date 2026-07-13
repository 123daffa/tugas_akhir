# test_text_pipeline.py (di folder backend/)
import sys
import os

# Pastikan Python bisa menemukan folder app/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.pipelines.text_pipeline import run_text_pipeline

def test_text_pipeline():
    print("=" * 60)
    print("SIMULASI TEXT PIPELINE")
    print("=" * 60)

    # ================================================
    # Contoh 1: Teks yang kemungkinan FAKTA
    # ================================================
    print("\n[TEST 1] Teks kemungkinan FAKTA")
    print("-" * 40)

    teks_1 = """
    Badan Meteorologi, Klimatologi, dan Geofisika (BMKG) 
    mengeluarkan peringatan dini cuaca ekstrem di wilayah 
    Jabodetabek pada Senin 8 Juli 2026. Hujan lebat disertai 
    angin kencang diprediksi terjadi mulai sore hingga malam hari.
    """

    print(f"Input teks: {teks_1.strip()}")
    print("\nMemproses...")

    result_1 = run_text_pipeline(teks_1.strip())

    print("\n[HASIL TEST 1]")
    # print(f"  Query digunakan    : {result_1['query_used']}")
    print(f"  Jumlah artikel     : {result_1['jumlah_artikel']}")
    print(f"  Rata-rata score    : {result_1['rata_rata_score']}")
    print(f"  Kredibilitas score : {result_1['kredibilitas_score']}")
    # print(f"  Penjelasan         : {result_1['penjelasan']}")
    print(f"  Klasifikasi        : {result_1['klasifikasi']}")

    # ================================================
    # Contoh 2: Teks yang kemungkinan FALSE
    # ================================================
    print("\n" + "=" * 60)
    print("[TEST 2] Teks kemungkinan FALSE")
    print("-" * 40)

    teks_2 = """
    Pemerintah Indonesia resmi mengumumkan lockdown total 
    seluruh wilayah Indonesia mulai besok pagi. Semua 
    aktivitas masyarakat dihentikan selama 30 hari penuh.
    """

    print(f"Input teks: {teks_2.strip()}")
    print("\nMemproses...")

    result_2 = run_text_pipeline(teks_2.strip())

    print("\n[HASIL TEST 2]")
    # print(f"  Query digunakan    : {result_2['query_used']}")
    print(f"  Jumlah artikel     : {result_2['jumlah_artikel']}")
    print(f"  Rata-rata score    : {result_2['rata_rata_score']}")
    print(f"  Kredibilitas score : {result_2['kredibilitas_score']}")
    # print(f"  Penjelasan         : {result_2['penjelasan']}")
    print(f"  Klasifikasi        : {result_2['klasifikasi']}")


if __name__ == "__main__":
    test_text_pipeline()