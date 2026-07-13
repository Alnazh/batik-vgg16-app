# Script training model klasifikasi motif batik dengan transfer learning VGG16
# Jalankan: python train_model.py (dataset harus sudah ada di dataset/train, val, test)

import os
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import config


def siapkan_data_generator():
    # Data train diberi augmentasi supaya model tahan variasi foto, data val/test hanya dinormalisasi
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=25,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest",
    )
    val_test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

    train_generator = train_datagen.flow_from_directory(
        config.TRAIN_DIR, target_size=config.IMG_SIZE, batch_size=config.BATCH_SIZE,
        class_mode="categorical", shuffle=True,
    )
    val_generator = val_test_datagen.flow_from_directory(
        config.VAL_DIR, target_size=config.IMG_SIZE, batch_size=config.BATCH_SIZE,
        class_mode="categorical", shuffle=False,
    )
    test_generator = val_test_datagen.flow_from_directory(
        config.TEST_DIR, target_size=config.IMG_SIZE, batch_size=config.BATCH_SIZE,
        class_mode="categorical", shuffle=False,
    )
    return train_generator, val_generator, test_generator


def bangun_model(jumlah_kelas: int):
    # VGG16 dipakai sebagai ekstraktor fitur, ditambah classifier head baru untuk motif batik
    base_model = VGG16(weights="imagenet", include_top=False, input_shape=config.IMG_SHAPE)
    base_model.trainable = False

    model = Sequential([
        base_model,
        Flatten(),
        Dense(256, activation="relu"),
        Dropout(0.5),
        Dense(jumlah_kelas, activation="softmax"),
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=config.LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model, base_model


def siapkan_callbacks():
    # Simpan model terbaik, hentikan lebih awal jika stagnan, turunkan learning rate saat plateau
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    checkpoint = ModelCheckpoint(config.MODEL_PATH, monitor="val_accuracy", save_best_only=True, verbose=1)
    early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, min_lr=1e-7, verbose=1)
    return [checkpoint, early_stop, reduce_lr]


def gabungkan_riwayat(history_1, history_2):
    # Gabungkan history feature extraction dan fine-tuning menjadi satu kurva utuh
    gabungan = {}
    for key in history_1.history:
        gabungan[key] = history_1.history[key] + history_2.history.get(key, [])
    return gabungan


def simpan_grafik_riwayat(history_dict: dict):
    # Simpan grafik akurasi dan loss selama training ke file PNG
    os.makedirs(config.EVAL_STATIC_DIR, exist_ok=True)
    epochs_range = range(1, len(history_dict["accuracy"]) + 1)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, history_dict["accuracy"], label="Akurasi Training")
    plt.plot(epochs_range, history_dict["val_accuracy"], label="Akurasi Validasi")
    plt.title("Tingkat Akurasi Model")
    plt.xlabel("Epoch")
    plt.ylabel("Akurasi")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, history_dict["loss"], label="Loss Training")
    plt.plot(epochs_range, history_dict["val_loss"], label="Loss Validasi")
    plt.title("Proses Pelatihan (Loss)")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()

    plt.tight_layout()
    plt.savefig(config.HISTORY_PLOT_PATH)
    plt.close()
    print(f"[INFO] Grafik training disimpan di: {config.HISTORY_PLOT_PATH}")


def simpan_metrik(test_acc, test_loss, nama_kelas, train_gen, val_gen, test_gen, laporan_per_kelas, cm):
    # Simpan ringkasan hasil evaluasi ke JSON agar bisa ditampilkan di halaman Evaluasi Model
    ringkasan = {
        "jumlah_kelas": len(nama_kelas),
        "nama_kelas": nama_kelas,
        "jumlah_data_train": train_gen.samples,
        "jumlah_data_val": val_gen.samples,
        "jumlah_data_test": test_gen.samples,
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
    print(f"[INFO] Ringkasan metrik disimpan di: {config.METRICS_PATH}")


def evaluasi_model(model, test_generator, nama_kelas):
    # Evaluasi model pada data uji, cetak classification report, simpan confusion matrix
    os.makedirs(config.EVAL_STATIC_DIR, exist_ok=True)
    test_loss, test_acc = model.evaluate(test_generator)
    print(f"\n[HASIL EVALUASI] Akurasi pada data uji: {test_acc:.2%}")
    print(f"[HASIL EVALUASI] Loss pada data uji     : {test_loss:.4f}")

    y_pred_prob = model.predict(test_generator)
    y_pred = np.argmax(y_pred_prob, axis=1)
    y_true = test_generator.classes
    print("\n[CLASSIFICATION REPORT]")
    laporan_teks = classification_report(y_true, y_pred, target_names=nama_kelas)
    print(laporan_teks)
    laporan_per_kelas = classification_report(y_true, y_pred, target_names=nama_kelas, output_dict=True)

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation="nearest", cmap="Blues")
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(nama_kelas))
    plt.xticks(tick_marks, nama_kelas, rotation=90)
    plt.yticks(tick_marks, nama_kelas)
    plt.xlabel("Prediksi")
    plt.ylabel("Label Sebenarnya")
    plt.tight_layout()
    plt.savefig(config.CONFUSION_MATRIX_PATH)
    plt.close()
    print(f"[INFO] Confusion matrix disimpan di: {config.CONFUSION_MATRIX_PATH}")

    return test_loss, test_acc, laporan_per_kelas, cm.tolist()


def simpan_mapping_kelas(class_indices: dict):
    # Balik mapping {nama_kelas: index} dari Keras menjadi {index: nama_kelas} untuk dipakai app.py
    index_to_class = {str(v): k for k, v in class_indices.items()}
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    with open(config.CLASS_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index_to_class, f, indent=2, ensure_ascii=False)
    print(f"[INFO] Mapping kelas disimpan di: {config.CLASS_INDEX_PATH}")


def main():
    print("=" * 60)
    print("TRAINING MODEL KLASIFIKASI MOTIF BATIK - TRANSFER LEARNING VGG16")
    print("=" * 60)

    # Pastikan dataset sudah tersedia sebelum training dimulai
    for path in [config.TRAIN_DIR, config.VAL_DIR, config.TEST_DIR]:
        if not os.path.isdir(path) or len(os.listdir(path)) == 0:
            raise FileNotFoundError(
                f"Folder dataset '{path}' belum berisi data. Lihat dataset/README.md."
            )

    train_gen, val_gen, test_gen = siapkan_data_generator()
    nama_kelas = list(train_gen.class_indices.keys())
    print(f"[INFO] Ditemukan {len(nama_kelas)} kelas motif batik: {nama_kelas}")

    model, base_model = bangun_model(jumlah_kelas=len(nama_kelas))
    model.summary()
    callbacks = siapkan_callbacks()

    # Tahap 1: feature extraction, seluruh layer VGG16 dibekukan
    print("\n[TAHAP 1] Feature Extraction (VGG16 dibekukan)...")
    history_1 = model.fit(train_gen, validation_data=val_gen, epochs=config.EPOCHS_FEATURE_EXTRACTION, callbacks=callbacks)

    # Tahap 2: fine-tuning, buka sebagian layer akhir VGG16 dengan learning rate lebih kecil
    print("\n[TAHAP 2] Fine-Tuning (membuka sebagian layer akhir VGG16)...")
    base_model.trainable = True
    for layer in base_model.layers[: config.FINE_TUNE_AT_LAYER]:
        layer.trainable = False
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=config.FINE_TUNE_LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    history_2 = model.fit(train_gen, validation_data=val_gen, epochs=config.EPOCHS_FINE_TUNING, callbacks=callbacks)

    model.save(config.MODEL_PATH)
    print(f"[INFO] Model final disimpan di: {config.MODEL_PATH}")

    simpan_mapping_kelas(train_gen.class_indices)
    riwayat_gabungan = gabungkan_riwayat(history_1, history_2)
    simpan_grafik_riwayat(riwayat_gabungan)

    test_loss, test_acc, laporan_per_kelas, cm = evaluasi_model(model, test_gen, nama_kelas)
    simpan_metrik(test_acc, test_loss, nama_kelas, train_gen, val_gen, test_gen, laporan_per_kelas, cm)

    print("\n[SELESAI] Training model klasifikasi motif batik selesai!")


if __name__ == "__main__":
    main()
