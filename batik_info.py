# Kamus informasi edukatif (asal daerah, makna, ciri visual) untuk tiap motif batik
BATIK_INFO = {
    "Kawung": {
        "asal": "Yogyakarta & Surakarta",
        "filosofi": "Kesucian dan keadilan",
        "ciri": ["Bentuk bulat lonjong", "Pola simetris", "Empat lingkaran mengelilingi titik pusat"],
        "deskripsi": (
            "Motif berbentuk bulatan lonjong menyerupai buah kolang-kaling (kawung) "
            "yang disusun secara geometris. Pada masa kerajaan, motif ini khusus "
            "dikenakan oleh raja dan keluarga kerajaan sebagai simbol kesucian."
        ),
    },
    "Mega_Mendung": {
        "asal": "Cirebon",
        "filosofi": "Kesabaran dan pengendalian diri",
        "ciri": ["Garis lengkung menyerupai awan", "Gradasi warna", "Bentuk memanjang bertumpuk"],
        "deskripsi": (
            "Motif berbentuk awan bergradasi warna yang terinspirasi dari budaya "
            "Tiongkok. Melambangkan kesabaran dan pengendalian diri, karena awan "
            "pembawa hujan tidak datang tergesa-gesa."
        ),
    },
    "Parang": {
        "asal": "Yogyakarta & Surakarta",
        "filosofi": "Semangat pantang menyerah",
        "ciri": ["Garis diagonal menyerupai huruf S", "Pola berulang tanpa putus", "Kesan dinamis"],
        "deskripsi": (
            "Motif diagonal menyerupai huruf S yang saling berkaitan tanpa "
            "putus, terinspirasi dari ombak laut selatan. Melambangkan semangat "
            "pantang menyerah dan kekuatan yang tidak pernah terputus."
        ),
    },
    "Truntum": {
        "asal": "Surakarta (Solo)",
        "filosofi": "Cinta yang tumbuh kembali",
        "ciri": ["Titik kecil menyerupai bintang", "Tersebar merata", "Latar polos gelap"],
        "deskripsi": (
            "Motif bunga kecil menyerupai taburan bintang, diciptakan oleh "
            "Kanjeng Ratu Kencana. Melambangkan cinta yang bersemi/tumbuh "
            "kembali, sering dikenakan orang tua pengantin."
        ),
    },
}

# Deskripsi default jika nama kelas tidak ditemukan pada BATIK_INFO
DEFAULT_INFO = {
    "asal": "Tidak diketahui",
    "filosofi": "Tidak diketahui",
    "ciri": [],
    "deskripsi": (
        "Deskripsi motif ini belum tersedia. Silakan tambahkan informasinya "
        "pada file batik_info.py."
    ),
}


def get_batik_info(class_name: str) -> dict:
    # Ambil info asal daerah, filosofi, ciri visual, dan deskripsi berdasarkan nama kelas hasil prediksi
    return BATIK_INFO.get(class_name, DEFAULT_INFO)
