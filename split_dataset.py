# Membagi dataset mentah (folder per kelas) menjadi struktur dataset/train, val, test
# Cara pakai: python split_dataset.py --source "path/ke/folder/hasil_ekstrak_kaggle"

import argparse
import os
import random
import shutil

import config

VALID_EXT = {".jpg", ".jpeg", ".png"}


def ambil_daftar_gambar(folder_kelas: str):
    # Ambil semua nama file gambar valid di dalam satu folder kelas
    return [f for f in os.listdir(folder_kelas) if os.path.splitext(f)[1].lower() in VALID_EXT]


def split_dataset(source_dir: str, train_ratio: float, val_ratio: float, seed: int = 42):
    # Bagi dataset mentah per kelas menjadi train/val/test, lalu salin ke folder dataset/
    random.seed(seed)

    nama_kelas_list = [
        d for d in sorted(os.listdir(source_dir))
        if os.path.isdir(os.path.join(source_dir, d))
    ]

    if not nama_kelas_list:
        raise ValueError(
            f"Tidak ditemukan sub-folder kelas di dalam '{source_dir}'. "
            "Pastikan --source menunjuk ke folder yang berisi satu folder per motif batik."
        )

    print(f"[INFO] Ditemukan {len(nama_kelas_list)} kelas: {nama_kelas_list}")

    for nama_kelas in nama_kelas_list:
        folder_kelas = os.path.join(source_dir, nama_kelas)
        daftar_gambar = ambil_daftar_gambar(folder_kelas)
        random.shuffle(daftar_gambar)

        n_total = len(daftar_gambar)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)

        pembagian = {
            "train": daftar_gambar[:n_train],
            "val": daftar_gambar[n_train:n_train + n_val],
            "test": daftar_gambar[n_train + n_val:],
        }

        for split_name, files in pembagian.items():
            target_dir = os.path.join(config.DATASET_DIR, split_name, nama_kelas)
            os.makedirs(target_dir, exist_ok=True)
            for filename in files:
                shutil.copy2(
                    os.path.join(folder_kelas, filename),
                    os.path.join(target_dir, filename),
                )

        print(
            f"[INFO] {nama_kelas}: total={n_total} -> "
            f"train={len(pembagian['train'])}, val={len(pembagian['val'])}, test={len(pembagian['test'])}"
        )

    print("\n[SELESAI] Dataset berhasil dibagi ke folder dataset/train, dataset/val, dataset/test")
    print("[INFO] Jangan lupa cek/edit 'batik_info.py' & 'config.py' agar nama kelas sesuai.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Membagi dataset batik mentah menjadi train/val/test.")
    parser.add_argument("--source", required=True, help="Path ke folder hasil ekstraksi dataset (berisi satu folder per motif).")
    parser.add_argument("--train_ratio", type=float, default=0.7, help="Proporsi data training (default 0.7)")
    parser.add_argument("--val_ratio", type=float, default=0.15, help="Proporsi data validasi (default 0.15)")
    args = parser.parse_args()

    split_dataset(args.source, args.train_ratio, args.val_ratio)
