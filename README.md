# Roadside Stick (Stick Scavenger)

Petualangan eksplorasi 2D pixel-art santai (cozy platformer) yang dikembangkan menggunakan **GDevelop 5**.

Pemain menjelajah keluar dari rumah hangat, menelusuri tepian hutan hingga batas hutan gelap untuk mengumpulkan berbagai varian ranting unik, lalu membawanya pulang untuk melengkapi album koleksi dan memajangnya di teras rumah.

---

## Fitur Utama

- **8 Varian Ranting Unik**:
  1. *Ranting Kering* (5 skor) - Ranting rapuh di Tepi Hutan
  2. *Ranting Bercabang* (12 skor) - Ranting cabang Y di Tepi Hutan
  3. *Ranting Berlumut* (20 skor) - Meliuk hijau di perbatasan Rimba
  4. *Ranting Pinus* (35 skor) - Harum damar di dahan pohon Hutan Rimba
  5. *Ranting Kayu Besi* (55 skor) - Batang pejal kelabu di pedalaman Rimba
  6. *Ranting Kristal* (80 skor) - Tetesan getah beku di Hutan Gelap
  7. *Ranting Kuno* (120 skor) - Guratan spiral ungu di dahan Hutan Gelap
  8. *Ranting Rembulan* (200 skor) - Cahaya perak di puncak ujung dunia
- **3 Biome Eksplorasi Terpadat (0 - 4.800 px)**:
  - **Rumah** (X: 0 - 220): Titik aman untuk menyetor ranting dan melihat rak pajangan
  - **Tepi Hutan** (X: 221 - 1.650): Wilayah terang dengan ranting umum
  - **Hutan Rimba** (X: 1.651 - 3.250): Wilayah rimbun dengan platform dahan alami
  - **Hutan Gelap** (X: 3.251 - 4.720): Wilayah mistik dengan ranting bercahaya
- **Visible World Progression (Rak Pajangan Rumah)**:
  Setiap varian ranting yang berhasil dibawa pulang akan terpajang secara fisik dan permanen di teras rumah.
- **Album Koleksi Lengkap [C] / [Tab]**:
  Buku catatan koleksi di dalam game dengan siluet dan petunjuk wilayah untuk varian yang belum ditemukan.
- **Gentle Speed Progression**:
  Setiap varian ranting unik yang masuk koleksi memberikan bonus kecepatan jalan permanen (+4 px/s, dari 230 hingga 262 px/s).
- **Audio Chiptune & Warm Marimba**:
  Efek suara langkah kaki renyah, lentera hangat berdenyut, akor marimba lembut saat menyetor ranting, dan denting kristal saat menemukan varian baru.

---

## Kontrol Permainan

| Tombol | Aksi |
| :--- | :--- |
| **[A] / [D]** atau **Panah Kiri/Kanan** | Berjalan ke kiri / kanan |
| **[Space]** atau **[W]** / **Panah Atas** | Melompat |
| **[E]** | Mengambil atau menukar ranting di tanah |
| **[Q]** | Melepaskan ranting yang sedang dipegang |
| **[C]** atau **[Tab]** | Membuka / menutup Album Koleksi Ranting |
| **[ESC]** | Menu Pause (Lanjut, [R] Ulang, [M] Menu) |

---

## Struktur Folder Proyek

```
Roadside-Stick/
├── assets/                  # Seluruh aset visual pixel art dan audio WAV
│   ├── audio/               # SFX prosedural (marimba, step, pickup, pause, discover)
│   ├── sprites/             # Sprite platform ledge, lentera, panel album
│   ├── sticks_v2/           # Sprite pixel art 8 varian ranting dan ikon UI (24x24 px)
│   └── sprint*/             # Aset latar, parallax, debu partikel, dan font
├── data/                    # Konfigurasi data balance permainan
│   └── game_balance.json    # Nilai skor, biome, kecepatan, dan deskripsi ranting
├── tools/                   # Alat pengujian dan validasi integritas engine
│   ├── healthcheck_gd5.py   # Linter AST statis GDevelop 5
│   ├── run_libgd_validator.js # Validator AST engine native libGD 5.6.287
│   ├── test_compile_all.js  # Kompilasi nyata JavaScript via gd.LayoutCodeGenerator
│   └── verify_cozy_pivot.py # Test suite runtime readiness (12/12 checks)
├── scripts/                 # Skrip pembantu dan arsip riwayat sprint
│   └── legacy_sprints/      # Skrip generasi dan migrasi sprint terdahulu
├── game.json                # File proyek standar GDevelop 5
├── StickScavenger.json      # File proyek utama GDevelop 5
└── README.md                # Dokumentasi proyek
```

---

## Cara Membuka & Menjalankan Game

1. Buka aplikasi **GDevelop 5** (versi 5.6 atau lebih baru).
2. Pilih menu **Open a project**.
3. Arahkan ke folder ini dan pilih **`game.json`** atau **`StickScavenger.json`**.
4. Klik tombol **Preview / Play** (ikon segitiga di pojok kanan atas) untuk mulai bermain.

---

## Verifikasi & Integritas Teknis

Seluruh event sheet, layout, dan struktur data telah melalui audit otomatis:
- **libGD AST Engine Validator**: 0 errors
- **Layout Code Generator (Real JS Compiler)**: 0 errors
- **Static Linter**: 0 violations
- **Runtime Verification**: 12/12 checks passed
