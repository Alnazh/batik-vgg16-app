// Menangani interaksi halaman upload (preview, drag & drop) dan inisialisasi grafik Chart.js

document.addEventListener("DOMContentLoaded", function () {
  inisialisasiGrafikDistribusiDataset();
  inisialisasiGrafikTop3();
  inisialisasiGrafikSplitDataset();
  inisialisasiProgressBar();

  const dropzone = document.getElementById("dropzone");
  const inputFile = document.getElementById("file-input");
  const previewImage = document.getElementById("preview-image");
  const placeholderText = document.getElementById("dropzone-placeholder");
  const uploadForm = document.getElementById("upload-form");
  const submitButton = document.getElementById("submit-button");
  const loadingOverlay = document.getElementById("loading-overlay");

  if (!dropzone || !inputFile) {
    return; // Bukan halaman upload, tidak perlu lanjut.
  }

  const UKURAN_MAKS_MB = 5;
  const TIPE_DIIZINKAN = ["image/jpeg", "image/png", "image/jpg"];

  // Fungsi menampilkan preview gambar yang dipilih user
  function tampilkanPreview(file) {
    if (!file) return;

    // Validasi tipe file
    if (!TIPE_DIIZINKAN.includes(file.type)) {
      alert("Format file tidak didukung. Gunakan JPG, JPEG, atau PNG.");
      inputFile.value = "";
      return;
    }

    // Validasi ukuran file
    const ukuranMB = file.size / (1024 * 1024);
    if (ukuranMB > UKURAN_MAKS_MB) {
      alert(`Ukuran file terlalu besar (maksimal ${UKURAN_MAKS_MB} MB).`);
      inputFile.value = "";
      return;
    }

    const pembaca = new FileReader();
    pembaca.onload = function (e) {
      previewImage.src = e.target.result;
      previewImage.style.display = "block";
      if (placeholderText) placeholderText.style.display = "none";
    };
    pembaca.readAsDataURL(file);
  }

  // Event: user memilih file lewat dialog klik
  dropzone.addEventListener("click", function () {
    inputFile.click();
  });

  inputFile.addEventListener("change", function () {
    tampilkanPreview(inputFile.files[0]);
  });

  // Event: drag & drop file gambar ke area dropzone
  ["dragenter", "dragover"].forEach((eventName) => {
    dropzone.addEventListener(eventName, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropzone.addEventListener(eventName, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove("dragover");
    });
  });

  dropzone.addEventListener("drop", function (e) {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      inputFile.files = files; // Menyalin file hasil drop ke input asli
      tampilkanPreview(files[0]);
    }
  });

  // Event: tampilkan overlay loading saat form dikirim untuk prediksi
  if (uploadForm) {
    uploadForm.addEventListener("submit", function (e) {
      if (!inputFile.files || inputFile.files.length === 0) {
        e.preventDefault();
        alert("Silakan pilih gambar motif batik terlebih dahulu.");
        return;
      }
      if (loadingOverlay) loadingOverlay.style.display = "flex";
      if (submitButton) submitButton.setAttribute("disabled", "disabled");
    });
  }
});

// Fungsi pembuat grafik Chart.js, tiap fungsi berhenti diam-diam jika elemen canvas-nya tidak ada di halaman

// Mengisi lebar progress bar hasil klasifikasi berdasarkan data-confidence
function inisialisasiProgressBar() {
  document.querySelectorAll(".progress-bar[data-confidence]").forEach(function (bar) {
    bar.style.width = bar.dataset.confidence + "%";
  });
}

// Palet warna konsisten dengan tema visual aplikasi (lihat variabel CSS di style.css)
const WARNA_GRAFIK = {
  sogan: "#a15c2b",
  sogan_muda: "#c98a4f",
  indigo: "#1f2d50",
  gold: "#c9a227",
};

// Grafik batang jumlah gambar per motif pada halaman Dashboard
function inisialisasiGrafikDistribusiDataset() {
  const canvas = document.getElementById("chart-distribusi-motif");
  if (!canvas || typeof Chart === "undefined") return;

  const labels = JSON.parse(canvas.dataset.labels || "[]");
  const totals = JSON.parse(canvas.dataset.totals || "[]");

  new Chart(canvas, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Jumlah Gambar",
          data: totals,
          backgroundColor: WARNA_GRAFIK.sogan,
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0 } },
      },
    },
  });
}

// Grafik batang berkelompok (train/val/test) pada halaman Dataset
function inisialisasiGrafikSplitDataset() {
  const canvas = document.getElementById("chart-split-dataset");
  if (!canvas || typeof Chart === "undefined") return;

  const labels = JSON.parse(canvas.dataset.labels || "[]");
  const train = JSON.parse(canvas.dataset.train || "[]");
  const val = JSON.parse(canvas.dataset.val || "[]");
  const test = JSON.parse(canvas.dataset.test || "[]");

  new Chart(canvas, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        { label: "Train", data: train, backgroundColor: WARNA_GRAFIK.indigo, borderRadius: 4 },
        { label: "Validasi", data: val, backgroundColor: WARNA_GRAFIK.sogan_muda, borderRadius: 4 },
        { label: "Test", data: test, backgroundColor: WARNA_GRAFIK.gold, borderRadius: 4 },
      ],
    },
    options: {
      responsive: true,
      plugins: { legend: { position: "bottom" } },
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0 } },
      },
    },
  });
}

// Grafik donat top-3 kemungkinan motif pada halaman hasil klasifikasi
function inisialisasiGrafikTop3() {
  const canvas = document.getElementById("chart-top3");
  if (!canvas || typeof Chart === "undefined") return;

  const labels = JSON.parse(canvas.dataset.labels || "[]");
  const nilai = JSON.parse(canvas.dataset.values || "[]");

  new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          data: nilai,
          backgroundColor: [WARNA_GRAFIK.gold, WARNA_GRAFIK.sogan, WARNA_GRAFIK.indigo],
          borderColor: "#fff",
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: { legend: { position: "bottom" } },
    },
  });
}
