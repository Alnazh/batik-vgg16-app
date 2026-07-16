# Script untuk membuat ulang model/metrics.json versi LENGKAP
# (termasuk laporan_per_kelas & confusion_matrix) TANPA training ulang.
# Cukup evaluasi model yang sudah ada terhadap dataset/test.
#
# Jalankan: python regenerate_metrics.py
# Syarat: folder dataset/test/<Motif>/... harus ada di komputer kamu,
# dan model/batik_vgg16_model.h5 sudah ada.

import json
import os

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import config


def main():
    if not os.path.isdir(config.TEST_DIR) or len(os.listdir(config.TEST_DIR)) == 0:
        raise FileNotFoundError(
            f"Folder '{config.TEST_DIR}' kosong/tidak ada. Jalankan split_dataset.py dulu."
        )
    if not os.path.exists(config.MODEL_PATH):
        raise FileNotFoundError(f"Model tidak ditemukan di '{config.MODEL_PATH}'.")

    import tensorflow as tf
    print("[INFO] Memuat model...")
    model = tf.keras.models.load_model(config.MODEL_PATH)

    test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    test_generator = test_datagen.flow_from_directory(
        config.TEST_DIR, target_size=config.IMG_SIZE, batch_size=config.BATCH_SIZE,
        class_mode="categorical", shuffle=False,
    )
    nama_kelas = list(test_generator.class_indices.keys())

    print("[INFO] Mengevaluasi model pada data uji...")
    test_loss, test_acc = model.evaluate(test_generator)

    y_pred_prob = model.predict(test_generator)
    y_pred = np.argmax(y_pred_prob, axis=1)
    y_true = test_generator.classes

    laporan_per_kelas = classification_report(y_true, y_pred, target_names=nama_kelas, output_dict=True)
    cm = confusion_matrix(y_true, y_pred).tolist()

    # Hitung ulang jumlah data per split juga (train/val butuh folder itu ada)
    def hitung_split(folder_dir):
        if not os.path.isdir(folder_dir):
            return 0
        total = 0
        for kelas in os.listdir(folder_dir):
            path_kelas = os.path.join(folder_dir, kelas)
            if os.path.isdir(path_kelas):
                total += len([f for f in os.listdir(path_kelas) if f.lower().endswith((".jpg", ".jpeg", ".png"))])
        return total

    ringkasan = {
        "jumlah_kelas": len(nama_kelas),
        "nama_kelas": nama_kelas,
        "jumlah_data_train": hitung_split(config.TRAIN_DIR),
        "jumlah_data_val": hitung_split(config.VAL_DIR),
        "jumlah_data_test": test_generator.samples,
        "akurasi_test": round(float(test_acc) * 100, 2),
        "loss_test": round(float(test_loss), 4),
        "batch_size": config.BATCH_SIZE,
        "epoch_feature_extraction": config.EPOCHS_FEATURE_EXTRACTION,
        "epoch_fine_tuning": config.EPOCHS_FINE_TUNING,
        "laporan_per_kelas": laporan_per_kelas,
        "confusion_matrix": cm,
    }

    os.makedirs(config.MODEL_DIR, exist_ok=True)
    with open(config.METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(ringkasan, f, indent=2, ensure_ascii=False)

    print(f"\n[SELESAI] metrics.json lengkap disimpan di: {config.METRICS_PATH}")
    print(f"[INFO] Akurasi: {ringkasan['akurasi_test']}% | Loss: {ringkasan['loss_test']}")


if __name__ == "__main__":
    main()
