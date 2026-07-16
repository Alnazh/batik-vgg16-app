# Script untuk menyimpan hasil hitungan jumlah gambar per motif (train/val/test)
# ke file kecil model/dataset_stats.json, supaya bisa ikut di-commit ke GitHub
# TANPA perlu upload folder dataset yang isinya ribuan foto.
#
# Jalankan sekali di komputer kamu (dataset/train, val, test harus ada di sini):
#   python generate_dataset_stats.py

import json
import os

import config

EKSTENSI_VALID = (".jpg", ".jpeg", ".png")
OUTPUT_PATH = os.path.join(config.MODEL_DIR, "dataset_stats.json")


def main():
    if not os.path.isdir(config.TRAIN_DIR):
        raise FileNotFoundError(
            f"Folder '{config.TRAIN_DIR}' tidak ditemukan. Pastikan dataset sudah di-split."
        )

    nama_kelas_di_disk = sorted(
        d for d in os.listdir(config.TRAIN_DIR) if os.path.isdir(os.path.join(config.TRAIN_DIR, d))
    )
    if not nama_kelas_di_disk:
        raise FileNotFoundError(f"Tidak ada folder kelas di dalam '{config.TRAIN_DIR}'.")

    statistik = []
    for nama_kelas in nama_kelas_di_disk:
        jumlah = {}
        for split_name, split_dir in [("train", config.TRAIN_DIR), ("val", config.VAL_DIR), ("test", config.TEST_DIR)]:
            folder_kelas = os.path.join(split_dir, nama_kelas)
            if os.path.isdir(folder_kelas):
                jumlah[split_name] = len(
                    [f for f in os.listdir(folder_kelas) if f.lower().endswith(EKSTENSI_VALID)]
                )
            else:
                jumlah[split_name] = 0
        statistik.append({
            "nama": nama_kelas,
            "train": jumlah["train"],
            "val": jumlah["val"],
            "test": jumlah["test"],
            "total": jumlah["train"] + jumlah["val"] + jumlah["test"],
        })

    os.makedirs(config.MODEL_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(statistik, f, indent=2, ensure_ascii=False)

    total_semua = sum(item["total"] for item in statistik)
    print(f"[SELESAI] Statistik {len(statistik)} motif ({total_semua} total gambar) disimpan di: {OUTPUT_PATH}")
    for item in statistik:
        print(f"  - {item['nama']}: train={item['train']}, val={item['val']}, test={item['test']}, total={item['total']}")


if __name__ == "__main__":
    main()
