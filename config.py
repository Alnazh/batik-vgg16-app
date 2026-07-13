# Konfigurasi terpusat: path folder, ukuran gambar, dan parameter training

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder dataset
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "val")
TEST_DIR = os.path.join(DATASET_DIR, "test")

# Lokasi file model dan hasil evaluasi
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "batik_vgg16_model.h5")
CLASS_INDEX_PATH = os.path.join(MODEL_DIR, "class_indices.json")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

# Grafik evaluasi disimpan di static/evaluasi supaya bisa ditampilkan langsung di halaman web
EVAL_STATIC_DIR = os.path.join(BASE_DIR, "static", "evaluasi")
HISTORY_PLOT_PATH = os.path.join(EVAL_STATIC_DIR, "training_history.png")
CONFUSION_MATRIX_PATH = os.path.join(EVAL_STATIC_DIR, "confusion_matrix.png")

# VGG16 membutuhkan input 224x224 piksel, 3 channel RGB
IMG_SIZE = (224, 224)
IMG_SHAPE = (224, 224, 3)

# Parameter training
BATCH_SIZE = 32
EPOCHS_FEATURE_EXTRACTION = 15
EPOCHS_FINE_TUNING = 10
LEARNING_RATE = 1e-4
FINE_TUNE_LEARNING_RATE = 1e-5
FINE_TUNE_AT_LAYER = 15

# Konfigurasi upload gambar
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_CONTENT_LENGTH_MB = 5
MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH_MB * 1024 * 1024

# Informasi sumber dataset untuk halaman Dataset
DATASET_SOURCE_NAME = "Dataset Batik Keraton"
DATASET_SOURCE_URL = "https://www.kaggle.com/datasets/stefaron/dataset-batik-keraton"

# Dipakai sebagai fallback sebelum model/class_indices.json tersedia
DEFAULT_CLASS_NAMES = [
    "Kawung",
    "Mega_Mendung",
    "Parang",
    "Truntum",
]
