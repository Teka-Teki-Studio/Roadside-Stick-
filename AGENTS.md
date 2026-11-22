# PROJECT: ROADSIDE STICK — AI WORKING GUIDE

> Versi 1.0. File ini diletakkan di folder utama project, sejajar dengan `game.json`.
> Setiap AI atau agen yang bekerja di project ini WAJIB membaca SELURUH file ini sebelum menyentuh apa pun.
> Bahasa dokumen: Indonesia. Istilah teknis GDevelop memakai nama aslinya.

---

## 0. CARA MEMAKAI FILE INI

### 0.1 Urutan wajib di awal setiap sesi

1. Baca seluruh `AGENTS.md` ini.
2. Baca `AI_NOTES/PROGRESS.md` bila ada (status tahap, keputusan, asumsi yang sudah disetujui).
3. Baca `AI_NOTES/MISSING_ASSETS.md` bila ada.
4. Daftar semua tool MCP yang tersedia (terutama GDevelop 5 MCP). Catat apa yang bisa dan tidak bisa dilakukan tiap tool. Jangan berasumsi nama tool.
5. Periksa `game.json` dan struktur folder project secara langsung.
6. Baru kerjakan perintah pengguna, dan hanya perintah itu.

### 0.2 Prioritas instruksi

1. Pesan terbaru dari pengguna, selama tidak melanggar Bab 1.
2. Bab 1 (Aturan Mutlak) di file ini.
3. Bab lain di file ini.
4. Default dan saran di file ini.

Bila dua instruksi bertentangan, atau perintah pengguna melanggar Bab 1: BERHENTI, jelaskan konfliknya dalam 2–3 kalimat, tanyakan pilihan. Jangan menebak.

### 0.3 Tentang perintah "Jalankan Tahap N"

Pengguna akan memberi perintah seperti: "Jalankan Tahap 1 — Boot ..." dan menempelkan tabel aset tahap itu. Artinya:

- Kerjakan SELURUH implementasi tahap N sesuai Bab 11 file ini (scene, object, event, variabel, interaksi), bukan hanya memeriksa aset.
- Tabel aset di pesan pengguna adalah daftar aset yang HARUS dicek keberadaannya di folder. Cocokkan dengan folder; laporkan selisihnya.
- Jangan mengerjakan tahap lain, kecuali stub minimum yang dibutuhkan agar tahap ini bisa tersambung (lihat 6.4).
- Nomor tahap sama dengan nomor di dokumen "Daftar Aset & Flow Produksi" (Tahap 1 = Boot, dst.).

---

## 1. ATURAN MUTLAK

### A. Aset

1. Seluruh visual game adalah PNG yang dibuat dan disediakan tim. AI TIDAK boleh membuat, menggambar, mengedit, mengubah warna, mengubah ukuran, memotong, menggeser pixel, menggabungkan, atau menyalin-lalu-memodifikasi aset visual.
2. DILARANG membuat visual pengganti: kotak, lingkaran, garis, gradien, shape, emoji, atau teks sebagai ganti gambar. DILARANG mengunduh aset dari internet. DILARANG membuat audio atau font.
3. Satu-satunya pengecualian visual non-aset adalah efek engine berwarna solid satu layar penuh (fade putih atau fade hitam) memakai Shape Painter atau efek layer bawaan GDevelop. Itu bukan seni, dan tidak boleh dipakai untuk hal lain.
4. Teks dinamis memakai Text object GDevelop (uang, timer, jarak, nama stick, harga, kapasitas, deskripsi difficulty, teks About, nomor level). Jangan dibuat sebagai PNG.
4b. **Gaya Teks & Tipografi (Wajib):** Seluruh teks wajib menggunakan font `vcr.ttf` (VCR OSD Mono). Warna default adalah putih polos (`255;255;255`). DILARANG menambahkan outline / stroke / shadow pada teks apa pun tanpa instruksi eksplisit dari pengguna (outline otomatis membuat visual terlihat generik/AI).
5. Bila aset belum ada: tulis ke Missing Asset Report (Bab 15) dan TETAP bangun logikanya. Buat object dengan struktur animasi bernama benar tetapi tanpa gambar, supaya tim bisa memasukkan PNG lewat editor GDevelop nanti tanpa menyentuh event. JANGAN mereferensikan file resource yang tidak ada di disk.
6. Jangan mengganti nama, memindahkan, atau menghapus file aset sumber tanpa persetujuan tertulis pengguna. Jangan "merapikan" aset yang dianggap tidak terpakai.
7. Mengiris sprite sheet menjadi file frame terpisah, atau operasi lain yang menghasilkan file gambar baru, hanya boleh setelah bertanya dan mendapat izin. Cek dulu apakah GDevelop/MCP bisa memakai sprite sheet langsung. Bila ya, pakai cara itu.
8. Jangan mengubah desain asli PNG dengan cara apa pun, termasuk "memperbaiki" transparansi atau padding.

### B. Layout milik tim

9. Layout akhir Lobby (posisi, ukuran, komposisi, urutan layer visual) dirancang tim di editor GDevelop. AI hanya menyiapkan object, state, event interaksi, dan modal. Lihat 9.3.

### C. Integritas project

10. Sebelum mengubah apa pun: salin `game.json` (dan file project lain yang akan diubah) ke `AI_NOTES/backup/` dengan nama `game_YYYYMMDD_HHMM_sebelum-tahapN.json`.
11. Setiap perubahan harus menghasilkan JSON yang valid dan project yang tetap bisa dibuka di GDevelop 5. Validasi setelah setiap penulisan.
12. JANGAN menebak skema `game.json`. Pelajari dari file yang sudah ada dan dari output tool MCP. Tiru pola object, event, dan resource yang dibuat editor. Bila tidak yakin tentang struktur, kerjakan satu elemen kecil, validasi, baru lanjutkan.
13. Gunakan tool MCP GDevelop untuk semua operasi yang didukung. Edit langsung `game.json` hanya untuk yang tidak didukung MCP, dengan langkah kecil dan validasi.
14. Jangan menimpa pekerjaan tim. Tim bisa saja mengatur layout, mengganti PNG, atau mengubah event di editor di antara sesi. Selalu baca keadaan terbaru project sebelum mengubah. Jangan menulis ulang scene secara total; ubah bagian yang diminta saja.
15. Ingatkan pengguna: project TIDAK boleh sedang terbuka di editor GDevelop saat AI mengubah file. Bila editor menyimpan setelahnya, perubahan AI bisa tertimpa. Setelah AI selesai, pengguna membuka ulang project.

### D. Kejujuran dan scope

16. Jangan menyatakan sesuatu "sudah berjalan" atau "sudah dites" tanpa bukti. Bila AI tidak bisa menjalankan preview GDevelop, katakan terus terang dan beri langkah tes manual (6.3).
17. Kerjakan hanya tahap yang diminta. Jangan menambah fitur di luar brief.
18. Bila ambigu dan taruhannya kecil: pilih default di file ini, tandai sebagai ASUMSI di laporan. Bila ambigu dan mahal diulang (menyentuh banyak scene, merombak struktur data): tanya dulu.
19. Jangan menulis pesan panjang. Laporan mengikuti format Bab 15.
20. **Sinkronisasi README.md (Wajib):** Setiap kali AI melakukan commit & push ke Git (khususnya branch `danans-version`), AI WAJIB memperbarui file `README.md` di root project. Update mencakup: nomor versi terkini, tanggal update, ringkasan changelog/fitur baru, dan status checklist aset/tahap produksi terkini agar dokumentasi repository selalu sinkron dengan state kode.

---

## 2. RINGKASAN GAME

**Nama:** PROJECT: ROADSIDE STICK. **Tema kompetisi:** PULANG.
**Genre:** 2D side-scrolling exploration / collection / time pressure, retro pixel art 16-bit.
**Platform:** HTML5 dari GDevelop 5, dimainkan di itch.io.

Seorang anak SD berjalan pulang sekolah ke arah kanan. Di sepanjang jalan ada ranting dan kayu (stick) unik, sebagian umum, sebagian sangat langka. Pemain harus sampai rumah sebelum timer habis (orang tua menjemput naik motor). Kapasitas tas awalnya 1 stick, jadi pemain harus memutuskan stick mana yang layak dibawa. Stick yang berhasil dibawa pulang masuk koleksi permanen (Stick Index). Uang dipakai membeli kosmetik (baju, celana) dan upgrade (tas lebih besar, Speed Drink). Setelah sukses, level berikutnya terbuka dan siklus berulang.

**Tagline:** "Every road leads home, but not every stick makes it there."

### 2.1 Pilar desain

1. The Journey: perjalanan pulang dan timer.
2. The Collection: menemukan, mengambil, menukar, mengoleksi stick.
3. The Decision: tas terbatas, pilih stick mana yang layak.
4. The Progression: level, koleksi, uang, kosmetik, upgrade.

### 2.2 BUKAN fokus game (jangan dibuat)

Combat, musuh, platforming/lompat, puzzle kompleks, cerita panjang, sistem quest, skill tree.

---

## 3. TARGET TEKNIS DAN KOMPATIBILITAS

### 3.1 Wajib

- Engine: GDevelop 5. Project harus bisa dibuka, dimainkan (Preview), dan diedit visual di editor GDevelop 5 oleh orang non-programmer.
- Ekspor: HTML5 (Web) dari GDevelop, diunggah ke itch.io sebagai game HTML5.
- Input: keyboard + mouse. Layar sentuh adalah pengembangan lanjutan; jangan menutup kemungkinannya (pakai kondisi yang juga mendukung touch bila mudah).
- Tidak ada backend, login, atau multiplayer. Penyimpanan memakai Storage bawaan GDevelop (localStorage di web).

### 3.2 Pengaturan project (diterapkan di Tahap 0)

Verifikasi nama properti sebenarnya di `game.json` / MCP, jangan menebak.

| Pengaturan | Nilai |
|---|---|
| Nama game | Roadside Stick |
| Resolusi game | 1024 × 576 (ASUMSI, 16:9; berubah hanya atas persetujuan) |
| Orientasi | Landscape |
| Skala | Mode nearest (pixel art), pixel rounding aktif bila tersedia |
| Adapt game resolution at runtime | Aktif |
| Smoothing gambar | Nonaktif untuk semua resource gambar |
| FPS maksimum | 60 |
| Scene pertama | Boot |

Pengaturan loading screen bawaan GDevelop/watermark di properti project jangan diubah tanpa diminta.

### 3.3 Aturan khusus web / itch.io

- Nama file dan path di web bersifat case-sensitive. Gunakan huruf kecil persis seperti penamaan di Bab 10. Folder `ASSETS/` ditulis persis seperti itu. Jangan campur huruf besar-kecil di referensi resource. Tidak ada spasi di nama file.
- Browser memblokir audio sebelum ada interaksi pengguna. Musik latar baru dimulai setelah klik pertama pemain (misalnya klik pertama di Lobby), bukan saat Boot.
- Jangan memakai fitur yang hanya jalan di desktop (akses file sistem, dsb.).
- Hindari extension komunitas yang harus dipasang. Prioritaskan fitur dan behavior bawaan GDevelop (Tween, Tiled Sprite, Storage, Text object, Shape Painter). Bila sebuah extension benar-benar perlu, tanya dulu.
- Hindari JavaScript event kecuali tidak ada cara visual. Tujuannya: tim bisa mengedit semuanya di editor visual.
- Perhatikan ukuran: jangan memuat ulang aset besar berulang kali; gunakan preload di scene Loading bila fitur tersedia di versi yang terpasang.

---

## 4. CARA BEKERJA DENGAN FILE PROJECT

1. `game.json` adalah file project GDevelop. Bila project memakai format multi-file (ada file/folder tambahan hasil "save as multiple files"), hormati struktur yang sudah ada; jangan menggabungkan atau memecah sendiri.
2. Cek apakah MCP GDevelop menyediakan operasi: membuat scene, object, animasi, layer, event, variabel, resource, validasi, preview/ekspor. Catat hasilnya di `AI_NOTES/PROGRESS.md` bagian "Kapabilitas tool".
3. Sebelum menulis: backup (Aturan 10). Setelah menulis: validasi JSON dan, bila ada, validasi MCP. Bila validasi gagal: pulihkan dari backup, jangan biarkan project rusak.
4. Perubahan dikerjakan bertahap per fitur kecil dan divalidasi tiap langkah.
5. Resource gambar dirujuk dengan path relatif ke folder project, sesuai lokasi aslinya di `ASSETS/...`. Jangan menyalin ulang aset ke folder lain.
6. Catat setiap file yang diubah dan alasannya di laporan.

---

## 5. KONVENSI PENAMAAN DAN STRUKTUR GDEVELOP

Tujuannya agar tim non-programmer mudah mencari dan mengedit di editor.

### 5.1 Scene

`Boot`, `Loading`, `Lobby`, `Gameplay`, `Success`, `FailureCutscene`, `GameOver`.
Settings, About, Shop, Upgrade, Stick Index, Difficulty adalah modal di Lobby (bukan scene). Inventory, Swap, Pause adalah modal di Gameplay.

### 5.2 Prefix object

| Prefix | Jenis | Contoh |
|---|---|---|
| `Spr_` | Sprite biasa | `Spr_Player`, `Spr_StickWorld` |
| `Btn_` | Tombol (Sprite dengan animasi state) | `Btn_Play`, `Btn_Close` |
| `Pnl_` | Panel / window / kartu | `Pnl_Settings`, `Pnl_ShopCard` |
| `Tld_` | Tiled Sprite | `Tld_Sky`, `Tld_Mountain` |
| `Txt_` | Text object | `Txt_Money`, `Txt_Timer` |
| `Ico_` | Ikon | `Ico_Money`, `Ico_Bag` |
| `Fx_` | Efek engine | `Fx_FadeOverlay` |

### 5.3 Tombol

Setiap tombol adalah Sprite dengan animasi bernama persis: `Normal`, `Hover`, `Pressed` (dan `Disabled` bila ada). Dimensi canvas semua state identik. Semua tombol dikumpulkan dalam Object Group `Grp_Buttons` sehingga satu event umum menangani hover dan pressed:

- Kursor di atas tombol → animasi `Hover`.
- Tombol mouse ditekan di atas tombol → animasi `Pressed`.
- Selain itu → `Normal`.
- Klik sah = tombol mouse dilepas saat kursor masih di atas tombol DAN tombol sedang aktif (modal-nya terbuka / state memperbolehkan).

Tim harus bisa mengganti PNG sebuah tombol di editor (di tab animasi object) tanpa menyentuh event.

### 5.4 Layer

Scene gameplay: `BG_Sky`, `BG_Mountain`, `BG_Treeline`, `BG_Village`, `BG_Road`, `World`, `Foreground`, `HUD`, `Modals`.
Scene menu: `Base`, `UI`, `Modals`.
Layer `HUD` dan `Modals` tidak ikut bergerak dengan kamera.

### 5.5 Variabel

- Variabel global (level project): `Save` (data permanen), `Config` (angka yang bisa dituning), `Data` (tabel konten: stick, shop, difficulty), `Run` (data perjalanan yang sedang berlangsung/baru selesai). Skema di Bab 8.
- Variabel scene: PascalCase, contoh `GameState`, `TimeRemaining`, `ModalOpen`.
- Jangan menaruh angka ajaib di event. Angka yang bisa berubah masuk `Config`. Konten (stick, produk shop, teks difficulty) masuk `Data`.

### 5.6 Event

- Kelompokkan dengan Group event berjudul `[T3] Lobby — Tombol` (T + nomor tahap + fitur). Beri komentar singkat untuk logika non-trivial.
- Jangan membuat satu event sheet raksasa. Logika bersama (Save/Load, tombol umum, transisi, audio) boleh dipisah ke External Events dan di-link dari scene. Pastikan setiap scene yang me-link external events memang memiliki object dan group yang dirujuk.
- Object yang dipakai di lebih dari satu scene (Btn_Close, Btn_ReturnToLobby, Ico_Money, ikon rarity, ikon stick) dijadikan Global Object, supaya mengganti PNG sekali berlaku di semua scene.

### 5.7 Data-driven

- Stick: satu Sprite `Spr_StickWorld`, satu `Spr_StickIcon`, satu `Spr_StickIndexIcon`, masing-masing punya satu animasi per stick dengan nama animasi = ID stick (`stick_001` … `stick_012`). Ganti gambar dengan mengganti animasi lewat nama.
- Kostum: lapisan terpisah `Spr_PlayerBody`, `Spr_PlayerShirt`, `Spr_PlayerPants`, `Spr_PlayerBag`. Animasi lapisan baju dan celana bernama `<itemId>_<state>`, contoh `shirt_00_walk`, `pants_01_idle`. Setiap frame, lapisan disinkronkan dengan animasi dan frame tubuh.
- Ikon produk shop: animasi bernama ID produk.

---

## 6. PROTOKOL KERJA PER PERINTAH TAHAP

### 6.1 Langkah

1. Konfirmasi singkat (1 kalimat) tahap apa yang akan dikerjakan.
2. Baca PROGRESS.md. Bila Tahap 0 (Foundation) belum tercatat selesai, jalankan dulu (6.2).
3. Cek prasyarat tahap (Bab 11). Prasyarat yang belum ada: pakai stub minimum (6.4) dan catat.
4. Backup project.
5. Scan folder aset; cocokkan dengan tabel aset di pesan pengguna dan Bab 10; perbarui `AI_NOTES/ASSET_MANIFEST.md` (nama, path, dimensi px, ada alpha atau tidak, jumlah frame bila sprite sheet); perbarui `AI_NOTES/MISSING_ASSETS.md`.
6. Implementasikan bertahap, validasi tiap langkah.
7. Uji sejauh yang bisa dibuktikan (6.3).
8. Perbarui `AI_NOTES/PROGRESS.md` (status, keputusan, asumsi, hal belum selesai).
8b. Perbarui `README.md` (versi, changelog terkini, checklist tahap dan aset) sebelum melakukan commit dan push.
9. Kirim laporan (Bab 15).

### 6.2 Tahap 0 — Foundation (otomatis, sekali saja, idempotent)

Dijalankan otomatis sebelum Tahap 1 bila belum tercatat selesai. Isinya:

- Buat `AI_NOTES/` dengan `PROGRESS.md`, `ASSET_MANIFEST.md`, `MISSING_ASSETS.md`, dan folder `backup/`.
- Terapkan pengaturan project (3.2).
- Buat scene kosong (stub) untuk semua scene di 5.1 yang belum ada. Stub hanya scene tanpa logika, diberi komentar event "STUB — diisi pada Tahap N".
- Buat variabel global `Save`, `Config`, `Data`, `Run` sesuai Bab 8 dengan nilai default.
- Periksa struktur folder `ASSETS/` (Bab 10). Jangan memindahkan atau membuat aset. Folder kosong boleh dibuat bila belum ada.
- Catat versi GDevelop (`gdVersion`) dan kapabilitas MCP.

### 6.3 Pengujian

- Bila MCP atau lingkungan bisa menjalankan preview/ekspor: jalankan dan laporkan hasil apa adanya.
- Bila tidak bisa: katakan "tidak bisa menjalankan preview di sini" dan berikan Langkah Tes Manual numerik (klik apa, harapan apa) yang bisa dicoba pengguna di GDevelop. Jangan menulis "sudah dites".
- Selalu lakukan yang bisa dilakukan: validasi JSON, cek semua referensi resource ada di disk, cek nama object/animasi/layer konsisten dengan Bab 5, cek tidak ada event yang merujuk object yang tidak ada.

### 6.4 Stub minimum

Bila tahap ini memerlukan sesuatu dari tahap yang belum dikerjakan (contoh: tombol Confirm di Difficulty perlu pindah ke scene `Gameplay`): cukup pastikan scene tujuan ada (stub) dan tautan transisinya benar. Jangan membangun fitur tahap itu. Catat di "Belum selesai".

---

## 7. ALUR GAME LENGKAP

```
BOOT:    White Screen -> Developer Logo -> Fade Out -> Loading -> Lobby

LOBBY:   Play -> Difficulty -> Confirm -> Gameplay
         Settings | About | Stick Index | Shop | Upgrade (modal, tutup kembali ke Lobby)

GAMEPLAY: Timer mulai -> jalan -> kamera mengikuti -> temukan stick -> E ambil
          tas ada slot  -> masuk inventory -> lanjut
          tas penuh     -> jendela Swap (timer berhenti) -> Keep / Replace / Cancel
          sampai rumah sebelum timer habis? YA -> Success   TIDAK -> Failure

SUCCESS: berhenti -> stick masuk Stick Index -> uang -> level naik -> Result -> Lobby

FAILURE: timer habis -> layar gelap -> orang tua jemput naik motor
         -> stick di tas dibuang -> Game Over -> Retry atau Return to Lobby
```

---

## 8. SPESIFIKASI SISTEM

Nilai di bawah adalah DEFAULT awal dan semuanya disimpan di `Config` / `Data` supaya mudah dituning. Tanda [TUNE] = perlu diuji dan akan berubah.

### 8.1 Kontrol (desktop)

| Input | Fungsi |
|---|---|
| A / Panah Kiri | Gerak kiri |
| D / Panah Kanan | Gerak kanan |
| E | Ambil stick |
| I | Buka / tutup Inventory |
| Q | Pakai Speed Drink |
| Esc | Pause; juga menutup modal teratas |

Tidak ada lompat. Tidak ada tombol Run terpisah (ASUMSI): animasi Run dipakai ketika Speed Boost aktif.

### 8.2 Pergerakan dan kamera

- Dunia horizontal. Pemain berjalan di garis tanah tetap (`GroundY`), tanpa physics dan tanpa behavior platformer.
- Kecepatan jalan `Config.walkSpeed` = 160 px/detik [TUNE]. Dengan Speed Boost × `Config.boostMultiplier` = 1.6 selama `Config.boostDuration` = 10 detik [TUNE].
- Kamera mengikuti pemain secara horizontal, pemain ditahan sekitar 1/3 lebar layar dari kiri, dibatasi di batas kiri start dan batas kanan rumah. Posisi kamera dibulatkan ke integer agar pixel art tidak bergetar.
- Pemain menghadap kanan secara default; menghadap kiri memakai flip horizontal (aset hanya digambar menghadap kanan).

### 8.3 Parallax

Cara utama: setiap layer background (`BG_*`, `Foreground`) memakai Tiled Sprite yang cukup lebar (membentang minimal sepanjang level dikali faktornya, ditambah selebar layar), dan kamera tiap layer digerakkan dengan `kameraUtamaX × faktor`.

| Layer | Faktor awal |
|---|---:|
| Sky | 0.10 |
| Mountain | 0.22 |
| Treeline | 0.35 |
| Village | 0.50 |
| Road / Distant Ground | 0.75 |
| Main Terrain (`World`) | 1.00 |
| Foreground | 1.15 |

Faktor disimpan di `Config.parallax.*`. Alternatif sah bila cara di atas bermasalah: offset gambar Tiled Sprite per frame. Pilih satu cara, catat di PROGRESS.

### 8.4 Susunan visual (belakang ke depan) dan Y awal

Sky, Mountain, Treeline, Village, Road, Main Grassland (terrain), dekorasi, stick, pemain, foreground grass, HUD.

Titik awal untuk diuji (viewport 576 tinggi), semua [TUNE] dan harus dicatat bila diubah:

| Elemen | Y atas (px) | Catatan |
|---|---:|---|
| Sky (256 tinggi) | 0 | Menutup bagian atas |
| Mountain | 96 | Tepi bawah di y 352 |
| Treeline | 144 | Tepi bawah di y 400 |
| Village | 168 | Tepi bawah di y 424 |
| Road strip (96 tinggi) | 392 | Sebagian tertutup terrain |
| Terrain (tile 128 tinggi) | `GroundY` = 448 | Permukaan rumput di atas, tepi bawah tepat di 576 |
| Foreground grass (96 tinggi) | 480 | Layer paling depan, hanya di bawah layar |

Rumah tujuan (256 × 192) berdiri di ujung level di atas permukaan terrain. Pintu (32 × 48) menjadi titik masuk.

### 8.5 Terrain, dekorasi, foreground

- Terrain: 8 tile (`terrain_A` … `terrain_H`, 256 × 128). Dibangun lewat event saat scene mulai: tile berurutan sepanjang level, pemilihan acak per posisi dengan seed tetap per level (agar konsisten saat Retry), boleh mirror horizontal. Hindari tile yang sama berurutan lebih dari 2 kali.
- Dekorasi (bush, rock, stone, flower; sprite individual): disebar acak dengan seed per level di atas terrain, tanpa menutupi stick dan tanpa menghalangi pemain. Bush dan rock besar tidak berdekatan.
- Foreground grass: 4 strip, loop horizontal, hanya di bawah layar.

### 8.6 Panjang level, timer, difficulty

- Panjang level `LevelLength = 9600 + 1600 × (level − 1)` px, maksimum 30000 [TUNE].
- Waktu dasar = `LevelLength / walkSpeed` detik (waktu jalan murni tanpa berhenti).
- Batas waktu = waktu dasar × pengali difficulty. Pengali awal [TUNE]:

| Index | Difficulty | Pengali waktu | Teks singkat |
|---:|---|---:|---|
| 0 | Peaceful | 3.00 | Waktu sangat longgar |
| 1 | Easy | 2.20 | Waktu cukup longgar |
| 2 | Normal | 1.70 | Tantangan seimbang |
| 3 | Hard | 1.35 | Waktu lebih terbatas |
| 4 | Super Hard | 1.15 | Waktu sangat terbatas |

- Difficulty HANYA memengaruhi batas waktu. Tidak mengubah peluang rarity stick.
- Timer berjalan hanya saat `GameState = Playing`. Timer berhenti ketika Inventory, Swap, atau Pause terbuka.

### 8.7 Spawn stick

- Jumlah titik spawn = `8 + 2 × (level − 1)`, maksimum 30 [TUNE]. Jarak minimum antar titik 300 px; tidak di zona start (300 px pertama) dan tidak di zona rumah (400 px terakhir).
- Posisi titik dibangkitkan dengan seed tetap per level (posisi terkontrol dan konsisten antar percobaan). Stick yang muncul di tiap titik dipilih acak setiap percobaan menurut bobot rarity.
- Bobot rarity awal [TUNE]: Common 70, Uncommon 20, Rare 8, Very Rare 2. Dalam satu rarity, jenis stick dipilih rata.
- Stick diletakkan di tanah, bisa dijangkau, tidak tertutup dekorasi.
- Opsional di masa depan: titik spawn manual lewat object marker yang ditempatkan tim. Bila tim ingin, ganti pembangkit otomatis tanpa mengubah sistem lain.

### 8.8 Pengambilan, inventory, swap

- Jarak interaksi horizontal ≤ 40 px dari stick terdekat. Muncul `Spr_PickupPrompt` ("E") di atas stick itu.
- Tekan E: bila `jumlah dibawa < kapasitas` → stick masuk inventory, hilang dari dunia, animasi Pickup.
- Kapasitas = `1 + Save.bagTier` (tier 0..3 → 1..4).
- Bila penuh → modal Swap, timer berhenti. Modal menampilkan stick baru dan stick yang dibawa (slot). Bila tas > 1 slot, pemain memilih (Selected Slot) stick yang akan diganti.
  - Replace with New Stick: stick terpilih dilepas, diletakkan di tanah pada titik stick baru (ASUMSI, bisa diambil lagi); stick baru masuk inventory.
  - Keep Current Stick: tutup modal, stick baru tetap di dunia.
  - Cancel: tutup modal, tidak ada perubahan.
- Inventory hanya berisi stick perjalanan ini. Tidak ada hubungan dengan Stick Index sampai sukses.

### 8.9 Stick Index vs Inventory

| Inventory | Stick Index |
|---|---|
| Penyimpanan saat perjalanan | Katalog permanen |
| Kapasitas terbatas | Tanpa batas |
| Berubah saat swap | Tidak berubah karena swap |
| Hilang saat gagal | Tetap tersimpan |
| Dipindah ke Index setelah sukses | Mencatat penemuan dan jumlah duplikat |

Kartu Index: belum ditemukan = Locked (siluet / status terkunci), sudah = Unlocked + nama + rarity + jumlah kepemilikan (`x3`).

### 8.10 Sukses

Pemain memasuki zona rumah (di depan pintu) sebelum timer nol:

1. Input dikunci, gerak berhenti, timer berhenti, animasi Arrive Home.
2. Hitung stick di inventory; tambahkan ke `Save.sticks[id]`.
3. Reward uang = `Config.rewardBase + Config.rewardPerLevel × level` + bonus `floor(TimeRemaining) × Config.timeBonusPerSecond` [TUNE: 100, 20, 2]. Tambahkan ke `Save.money`.
4. `Save.level += 1`. Simpan.
5. Isi `Run.result` (level selesai, daftar stick, ringkasan rarity, sisa waktu, uang didapat) lalu pindah ke scene `Success`.
6. Result: tombol Continue (membuka Lobby dengan panel Difficulty terbuka untuk level berikutnya; ASUMSI) dan Return to Lobby.

### 8.11 Gagal

Timer mencapai 0 sebelum sampai rumah:

1. Input dikunci, timer berhenti.
2. Layar menggelap perlahan (fade hitam efek engine).
3. Pindah ke scene `FailureCutscene`: orang tua datang naik motor, anak naik, motor pergi. Tanpa interaksi.
4. Seluruh stick di inventory dibuang (tidak masuk Index). Catat `Run.lostCount`.
5. Scene `GameOver`: judul, level yang gagal, jumlah stick hilang, Retry, Return to Lobby.
6. Level tidak bertambah. Retry memulai level yang sama dengan difficulty yang sama. Koleksi lama tidak terhapus. Tidak ada reward penyelesaian.

### 8.12 Speed Drink

- Dimiliki dalam jumlah `Save.drinkQty`. Tekan Q atau tombol Use Drink: bila qty > 0 dan boost belum aktif → qty − 1, boost aktif `boostDuration` detik, animasi Speed Boost.
- HUD menampilkan jumlah minuman; tombol disabled saat qty = 0.

### 8.13 Shop dan Upgrade

- Shop: tab Shirt dan Pants; setiap produk punya gambar, nama, harga, status Owned / Not Owned, tombol Buy dan Equip. Beli bila uang cukup (kurangi uang, tandai owned, simpan). Equip mengubah `Save.equipped.*` dan tampilan karakter. Pakaian hanya kosmetik, tanpa efek statistik. Pakaian sekolah default dimiliki sejak awal.
- Upgrade: Bag Upgrade 3 tier (kapasitas 2, 3, 4), harga naik per tier; tampilkan "MAX" bila tier penuh. Speed Drink: beli satuan.
- Harga awal [TUNE]: shirt 150 / 250 / 400, pants 120 / 200 / 350, bag tier 200 / 500 / 1000, drink 60.

### 8.14 Audio

- Sound ON/OFF memengaruhi seluruh suara (volume global 0 / 100) dan disimpan di `Save.soundOn`.
- Audio belum tentu tersedia. Jangan merujuk file audio yang tidak ada di disk. Siapkan fungsi/event pemanggil hanya untuk file yang sudah ada; sisanya dicatat di Missing Asset Report.

### 8.15 Skema data

**`Save`** (global, structure; disimpan sebagai JSON di Storage dengan key `roadsidestick_save_v1`):

| Kunci | Tipe | Default |
|---|---|---|
| `version` | number | 1 |
| `level` | number | 1 |
| `money` | number | 0 |
| `soundOn` | number (1/0) | 1 |
| `bagTier` | number (0–3) | 0 |
| `drinkQty` | number | 0 |
| `equipped.shirt` | string | `shirt_00` |
| `equipped.pants` | string | `pants_00` |
| `ownedShirts` | structure id → 1 | `shirt_00` |
| `ownedPants` | structure id → 1 | `pants_00` |
| `sticks` | structure id → jumlah | kosong (jumlah > 0 = ditemukan) |

Simpan setiap ada perubahan penting (beli, equip, sukses, setting). Muat di scene `Loading`. Bila data rusak, tidak ada, atau versi berbeda: buat default tanpa crash, jangan menghapus data lama diam-diam.

**`Config`** (global): `walkSpeed`, `boostMultiplier`, `boostDuration`, `levelBaseLength`, `levelLengthPerLevel`, `levelMaxLength`, `spawnBase`, `spawnPerLevel`, `spawnMax`, `spawnMinGap`, `rarityWeights` (common/uncommon/rare/veryRare), `difficultyMultipliers` (5 nilai), `rewardBase`, `rewardPerLevel`, `timeBonusPerSecond`, `parallax.*`, `groundY`, `pickupRange`, `devMode` (0).

**`Data`** (global): 
- `Data.sticks`: array 12 entri `{id, name, rarity}`. Default: `stick_001`–`005` Common, `006`–`009` Uncommon, `010`–`011` Rare, `012` Very Rare. Nama sementara "Stick 001" dst.; tim akan mengganti.
- `Data.shop.shirts` / `Data.shop.pants`: array `{id, name, price}`. Default minimum prototype: `shirt_00`–`03`, `pants_00`–`03`; `_00` harga 0 (default sekolah).
- `Data.difficulty`: array 5 entri `{index, name, description, timeMultiplier}`.

**`Run`** (global, tidak disimpan): `difficulty` (0–4), `level`, `carried` (array id stick), `timeLimit`, `lastResult`, `lostCount`.

---

## 9. SPESIFIKASI SCENE

### 9.1 Boot

Latar putih polos (properti warna latar scene = putih; efek engine). Logo developer di tengah, fade-in, tahan, fade-out, lalu pindah ke `Loading`. Waktu awal [TUNE]: putih 0,5 dtk; fade-in 0,6; tahan 1,2; fade-out 0,6. Gunakan behavior Tween atau aksi opacity bawaan. Tidak ada tombol, tidak ada audio.

### 9.2 Loading

Background dummy (`boot_loading_bg_dummy.png`), indikator loading (animasi frame), bar frame + bar fill, teks "Loading..." dan persen (Text object, opsional). Progres: gunakan preload resource dan ekspresi progres loading scene bawaan GDevelop bila ada di versi terpasang; bila tidak ada, pakai progres berbasis waktu minimum 1,5 dtk dan catat di PROGRESS. Bar fill: sebaiknya Tiled Sprite yang lebarnya mengikuti progres (bulat, tanpa peregangan) agar pixel tidak terdistorsi; bila art bar fill punya ujung khusus, tanyakan ke tim. Di scene ini juga: muat `Save` (atau buat default). Selesai → `Lobby`.

### 9.3 Lobby

Pusat aktivitas. AI menyiapkan:

- Object background (`bg_lobby.png`) dan karakter idle (`Spr_Player` dengan kostum yang sedang dipakai).
- Enam tombol: Play, Settings, About, Stick Index, Shop, Upgrade (3 state masing-masing).
- Currency display kanan atas (frame + ikon + `Txt_Money`) dan level indicator (`Txt_Level` dengan format "CURRENT JOURNEY: LEVEL 01", dua digit).
- Modal: Difficulty, Settings, About, Stick Index, Shop, Upgrade, masing-masing di layer `Modals` dan disembunyikan secara default, dengan `Spr_ModalDim` di belakangnya.
- Event interaksi dan state `ModalOpen`: saat modal terbuka, tombol Lobby tidak merespons klik; Esc / Close menutup modal teratas.

AI TIDAK menentukan komposisi final. Tempatkan instance di area yang rapi dan tidak saling menimpa agar mudah digeser (misalnya deretan di tepi), beri komentar event "LAYOUT DIATUR TIM". Posisi tersebut sementara. Saat tim sudah menyusun layout, JANGAN memindahkannya lagi.

### 9.4 Gameplay

Layer 5.4. Dunia dibangun saat scene mulai dari `Run.level` dan `Run.difficulty`. Menyertakan: environment (8.4–8.5), pemain (T10), stick (T11), HUD dan modal (T12), logika sukses/gagal (T13–T14).

### 9.5 Success

Panel Level Complete, ringkasan stick (ikon stick + ikon rarity + badge NEW untuk penemuan pertama bila aset ada), sisa waktu, uang didapat, tombol Continue dan Return to Lobby.

### 9.6 FailureCutscene

Pemandangan memakai ulang layer environment (sky sunset bila tersedia, mountain, treeline, village, road, terrain, foreground). Orang tua + motor masuk dari kanan, anak naik, motor pergi. Tanpa interaksi. Berakhir ke `GameOver`.

### 9.7 GameOver

Panel Game Over, level gagal, jumlah stick hilang, Retry, Return to Lobby.

---

## 10. KATALOG ASET, PENAMAAN, FOLDER

### 10.1 Standar aset

PNG; alpha asli untuk sprite; pixel edge tajam; tanpa blur; tanpa anti-aliasing; ukuran frame sprite sheet konsisten; nama file jelas. Pemeriksaan yang BOLEH dilakukan AI: baca dimensi, cek ada kanal alpha, cek apakah dimensi sesuai tabel, deteksi sprite sheet dari rasio. Pemeriksaan hanya dilaporkan, tidak diperbaiki.

### 10.2 Struktur folder

```
ASSETS/
  ENVIRONMENT/ SKY, MOUNTAINS, TREELINE, VILLAGE, ROAD, TERRAIN, DECORATIONS, FOREGROUND
  CHARACTER/   PLAYER, PARENTS, MOTORCYCLE, COSTUMES
  STICKS/      WORLD, ICONS, INDEX
  UI/          BUTTONS, PANELS, ICONS, HUD, INVENTORY, SHOP, UPGRADE, RESULTS
  BOOT/        LOGO, LOADING
  AUDIO/
```

Bila aset ada di lokasi lain, pakai lokasi sebenarnya dan catat; jangan memindahkannya.

### 10.3 Katalog per tahap

Prefix nama: `boot_`, `bg_`, `terrain_`, `deco_`, `fg_`, `env_`, `char_`, `costume_`, `stick_`, `ui_`, `fx_`, `audio_`. Ukuran UI di bawah adalah saran; ukuran lingkungan mengikuti brief. Tanda `*` = state `normal`, `hover`, `pressed` (tombol tertentu juga `disabled`). Prioritas P0 wajib untuk game bisa dimainkan.

**Tahap 1 — Boot:** `boot_logo_dev.png` (bebas, lebar ≤ 512) P0.

**Tahap 2 — Loading:** `boot_loading_bg_dummy.png` (sesuai viewport, disediakan developer), `boot_loading_indicator.png` (48×48 per frame, 4 frame), `boot_loading_bar_frame.png` (400×32), `boot_loading_bar_fill.png` (392×24). Semua P0.

**Tahap 3 — Lobby:** `bg_lobby.png`; karakter idle = `char_player_idle.png` (Tahap 10); `ui_btn_play_*` (192×64), `ui_btn_settings_*` (64×64), `ui_btn_about_*` (64×64), `ui_btn_index_*` (160×64), `ui_btn_shop_*` (160×64), `ui_btn_upgrade_*` (160×64); `ui_hud_money_frame.png` (160×40), `ui_icon_money.png` (32×32), `ui_lobby_level_frame.png` (320×40, P1), `ui_modal_dim.png` (sesuai viewport).

**Tahap 4 — Settings dan About:** `ui_panel_settings.png` (480×320), `ui_btn_sound_on_*`, `ui_btn_sound_off_*` (96×48), `ui_btn_close_*` (40×40), `ui_panel_about.png` (640×400).

**Tahap 5 — Difficulty:** `ui_panel_difficulty.png` (640×360), `ui_slider_track.png` (480×16, 5 penanda), `ui_slider_knob_normal/hover/active.png` (32×32), `ui_btn_help_*` (32×32), `ui_panel_tooltip.png` (320×160), `ui_btn_confirm_*` (160×48), `ui_btn_back_*` (160×48).

**Tahap 6 — Stick Index:** `ui_panel_index.png` (800×480), `ui_index_card.png`, `ui_index_card_locked.png`, `ui_index_card_unlocked.png`, `ui_index_card_selected.png` (160×128), `ui_rarity_common/uncommon/rare/veryrare.png` (32×32), `ui_index_locked_icon.png` (32×32, P1). Gambar stick di kartu = `stick_NNN_index.png`.

**Tahap 7 — Shop:** `ui_panel_shop.png` (800×480), `ui_shop_tab_shirt_on/off.png`, `ui_shop_tab_pants_on/off.png` (128×40), `ui_shop_card.png` (160×200), `ui_shop_preview.png` (192×256), `ui_btn_buy_*` (+disabled, 128×40), `ui_btn_equip_*` (128×40), `ui_btn_selected.png` (128×40), `ui_shop_owned.png`, `ui_shop_nomoney.png` (64×24), `ui_shop_icon_shirt_NN.png`, `ui_shop_icon_pants_NN.png` (64×64).

**Tahap 8 — Upgrade:** `ui_panel_upgrade.png` (640×400), `ui_upgrade_card_bag.png`, `ui_upgrade_card_drink.png` (280×240), `ui_icon_bag.png`, `ui_icon_drink.png` (48×48), `ui_upgrade_slot_full.png`, `ui_upgrade_slot_empty.png` (24×24), `ui_upgrade_max.png` (64×24, P1).

**Tahap 9 — Environment:**
- Sky: `bg_sky_day.png`, `bg_sky_sunset.png` (1024×256).
- `bg_mountain_loop.png`, `bg_treeline_loop.png`, `bg_village_loop.png` (1536×256).
- `bg_road_loop.png` (1536×96), `terrain_curb.png` (256×32).
- Terrain: `terrain_A.png` … `terrain_H.png` (256×128; permukaan rumput di atas; tinggi permukaan identik; tepi kiri-kanan menyambung; bisa di-mirror).
- Dekorasi (alpha): `deco_bush_large_01–05` (96×80), `deco_bush_small_01–06` (64×48), `deco_rock_large_01–05` (64×48), `deco_stone_small_01–06` (48×32), `deco_flower_white_01–06` (32×32), `deco_flower_color_01–08` (32×32).
- Foreground: `fg_grass_01–04.png` (512×96, transparan, lebih gelap dari terrain).
- Tujuan: `env_house_main.png` (256×192), `env_house_door.png` (32×48), `env_sign_road.png` (64×64, P2), `env_start_marker.png` (96×128, P2).

**Tahap 10 — Karakter dan kostum:** frame disarankan 48×64 (atau 32×48; ukuran harus sama di semua animasi dan lapisan). Animasi tubuh: `char_player_idle` (4 frame), `_walk` (6), `_run` (6), `_pickup` (4), `_swap` (4), `_boost` (4), `_arrive` (4), `_gameover` (1–2). Kostum sejajar piksel dengan frame tubuh: `costume_shirt_00_school_*`, `costume_pants_00_school_*`, `costume_bag_*`, `costume_shirt_01–03_*`, `costume_pants_01–03_*` (satu sheet gabungan per item atau satu file per animasi; ikuti yang ada). Cutscene: `char_parent.png`, `char_motorcycle.png`, `char_motorcycle_riding.png` (P1).

**Tahap 11 — Stick:** per stick (12 jenis, `001`–`012`): `stick_NNN_world.png` (32×16 atau 48×16), `stick_NNN_icon.png` (32×32), `stick_NNN_index.png` (32×32), `stick_NNN_held.png` (opsional, 32×16). Opsional: `fx_stick_glint.png` (4 frame, 32×32, P2).

**Tahap 12 — HUD, Inventory, Swap, Pause:** `ui_hud_timer_frame.png` (160×48), `ui_icon_timer.png`, `ui_hud_distance_bar.png` (480×24), `ui_hud_marker_start/home/player.png` (24×24), `ui_hud_inventory_counter.png` (96×40), `ui_icon_inventory.png`, `ui_icon_pause.png` (32×32), `ui_prompt_pickup.png` (32×32); tombol `ui_btn_inventory_*`, `ui_btn_pause_*` (56×56), `ui_btn_drink_*` (+disabled, 72×72), `ui_btn_swap_*` (128×40, P1), `ui_btn_pickup_*` (P2); `ui_panel_inventory.png` (480×240), `ui_slot_empty/occupied/selected.png` (64×64); `ui_panel_swap.png` (560×320), `ui_btn_keep_*`, `ui_btn_replace_*`, `ui_btn_cancel_*` (176×48); `ui_panel_pause.png` (400×280), `ui_btn_resume_*` (192×56).

**Tahap 13 — Success:** `ui_panel_levelcomplete.png` (640×440), `ui_panel_reward.png` (320×160), `ui_result_stick_new.png` (64×24, P1), `ui_btn_continue_*`, `ui_btn_lobby_*` (192×56).

**Tahap 14 — Game Over:** `ui_panel_gameover.png` (640×440), `ui_result_stick_lost.png` (64×24, P1), `ui_btn_retry_*` (192×56). Return to Lobby memakai `ui_btn_lobby_*`.

**Tahap 15 — Loop:** tidak ada aset baru.

**Audio (folder `ASSETS/AUDIO/`):** `audio_bgm_lobby`, `audio_bgm_gameplay`, `audio_sfx_click`, `_hover`, `_step`, `_pickup`, `_swap`, `_rare`, `_buy`, `_denied`, `_equip`, `_drink`, `_timer_warn`, `audio_jingle_success`, `audio_jingle_gameover`, `audio_sfx_motor`. Format MP3 paling aman untuk browser.

### 10.4 Aset yang belum ada di brief awal tetapi dibutuhkan

Overlay modal (`ui_modal_dim`), pause panel dan Resume, ikon produk shop, motor + penumpang, penanda start, frame level lobby, ikon terkunci, indikator MAX, badge NEW/Lost, efek kilau, dan audio. Bila belum ada, masuk Missing Asset Report.

---

## 11. PETA TAHAP → IMPLEMENTASI

Format: Scope, Prasyarat, Selesai bila.

### Tahap 1 — Boot (Scene: Boot)
- Scope: scene Boot sesuai 9.1; set scene pertama; object `Spr_BootLogo` di tengah layar; urutan putih → logo fade-in → tahan → fade-out → `Loading`.
- Prasyarat: Tahap 0.
- Selesai bila: Boot adalah scene pertama; alur berjalan tanpa error di event; transisi ke Loading (stub bila belum dibangun); bila logo belum ada, Boot tetap berjalan (putih lalu pindah) dan logo dilaporkan hilang.

### Tahap 2 — Loading (Scene: Loading)
- Scope: 9.2; muat/inisialisasi `Save`; progres; pindah ke Lobby.
- Prasyarat: Tahap 1.
- Selesai bila: `Save` termuat atau dibuat default; bar bergerak sampai penuh; masuk Lobby.

### Tahap 3 — Lobby (Scene: Lobby)
- Scope: 9.3 selengkapnya (object, tombol 3 state via `Grp_Buttons`, uang, level, modal manager, Esc/Close, character idle).
- Prasyarat: Tahap 2.
- Selesai bila: semua tombol berganti state benar; Play/Settings/About/Index/Shop/Upgrade membuka modal masing-masing (isi modal bisa stub); uang dan level tampil dari `Save`; layout tidak dikunci.

### Tahap 4 — Settings dan About
- Scope: modal Settings (toggle Sound ON/OFF dengan tampilan berbeda, simpan ke `Save.soundOn`, terapkan volume global) dan About (teks panjang di `Txt_About` yang mudah diedit); tombol Close.
- Selesai bila: toggle tersimpan dan terbaca ulang; teks About bisa diedit tanpa mengganti panel.

### Tahap 5 — Difficulty
- Scope: modal Difficulty dengan slider 5 titik (knob bisa digeser dan snap ke titik terdekat; hover/active), teks nama + deskripsi dari `Data.difficulty`, tombol `?` memunculkan tooltip, Confirm menyimpan `Run.difficulty` dan `Run.level = Save.level` lalu pindah ke `Gameplay`, Back menutup.
- Selesai bila: 5 posisi jelas dan bernama; Confirm memulai Gameplay (stub bila Gameplay belum dibangun).

### Tahap 6 — Stick Index
- Scope: modal Index berbasis `Data.sticks` dan `Save.sticks`; kartu Locked/Unlocked/Selected; nama, rarity, jumlah; pilih kartu menampilkan detail; paginasi bila perlu.
- Selesai bila: stick belum ditemukan tampil Locked; yang sudah ada tampil benar dan sesuai jumlahnya (uji dengan mengubah `Save` manual).

### Tahap 7 — Shop
- Scope: tab Shirt/Pants; kartu produk dari `Data.shop`; Buy (cek uang, kurangi, simpan); Equip; status Owned; indikator uang kurang; preview karakter dengan kostum.
- Prasyarat: Tahap 10 (kostum) untuk preview penuh; sebelum itu pakai stub.
- Selesai bila: beli dan equip tersimpan; produk dimiliki bisa dipakai berulang.

### Tahap 8 — Upgrade
- Scope: Bag Upgrade 3 tier (kapasitas, harga, MAX), Speed Drink (beli satuan, jumlah tampil), cek uang, simpan.
- Selesai bila: `bagTier` dan `drinkQty` bertambah dan tersimpan; kapasitas efektif = `1 + bagTier`.

### Tahap 9 — Gameplay: Environment
- Scope: scene Gameplay, layer, parallax, terrain, dekorasi, foreground, jalan, rumah di ujung; pembangkit level dari seed; kamera mengikuti; pergerakan dasar pemain kiri/kanan (tanpa sistem animasi lengkap).
- Prasyarat: Tahap 5 (Confirm masuk ke sini).
- Selesai bila: level terbangun tanpa celah visual, parallax halus, kamera terkunci di batas, rumah tercapai; seed tetap menghasilkan level sama saat Retry.

### Tahap 10 — Karakter dan kostum
- Scope: state machine animasi (Idle, Walk, Run saat boost, Pickup, Hold Stick, Swap, Speed Boost, Arrive Home, Game Over); lapisan kostum tersinkron; flip kiri/kanan; kostum dari `Save.equipped`; held stick bila aset ada; objek cutscene (orang tua, motor).
- Selesai bila: pergantian baju/celana tidak butuh kombinasi sprite baru; semua state memainkan animasi yang benar.

### Tahap 11 — Stick (sistem koleksi)
- Scope: pembangkit spawn (8.7), bobot rarity, world sprite, prompt E, pengambilan ke `Run.carried` bila ada slot, pemicu modal Swap bila penuh.
- Selesai bila: stick muncul di tempat terjangkau; distribusi rarity mengikuti bobot (uji dengan banyak sampel dan laporkan angka); duplikat bisa muncul.

### Tahap 12 — HUD, Inventory, Swap, Pause
- Scope: timer, distance bar (Start / Player / Home + angka jarak tempuh dan sisa bila memungkinkan), penghitung `n / kapasitas`, tombol Inventory dan Pause, indikator + tombol Speed Drink (Q), modal Inventory (slot kosong/terisi/terpilih), modal Swap (Keep/Replace/Cancel), modal Pause (Resume), aturan timer (8.6), `GameState`.
- Selesai bila: timer berhenti saat modal terbuka dan lanjut saat ditutup; Q, I, E, Esc berfungsi; swap sesuai 8.8.

### Tahap 13 — Success dan Result
- Scope: deteksi rumah, urutan sukses (8.10), simpan, scene Success dengan ringkasan, Continue dan Return to Lobby.
- Selesai bila: stick pindah ke `Save.sticks`, uang dan level bertambah, tersimpan, Lobby menampilkan level baru.

### Tahap 14 — Failure, Cutscene, Game Over
- Scope: timer nol → fade gelap → FailureCutscene → GameOver; stick dibuang; Retry dan Return to Lobby.
- Selesai bila: level tidak naik, stick perjalanan tidak masuk Index, koleksi lama utuh, Retry memulai level sama.

### Tahap 15 — Loop dan integrasi
- Scope: uji end-to-end Boot → Lobby → Play → sukses/gagal → Lobby → level berikutnya; ketahanan Save (kosong/rusak/versi lama); penyetelan awal `Config` bila diminta; mode dev opsional (`Config.devMode = 1` mengaktifkan debug: tambah uang, lompat level, tampilkan seed; default 0 dan tidak muncul di rilis); pemeriksaan performa dan referensi resource; daftar periksa ekspor.
- Selesai bila: tidak ada referensi rusak, tidak ada event yatim, semua alur Bab 7 berjalan.

---

## 12. DAFTAR PERIKSA UJI MINIMUM

Untuk dilaporkan sebagai "tidak bisa dijalankan di sini + langkah tes manual" bila preview tidak tersedia:

1. Buka project di GDevelop 5 tanpa pesan kesalahan.
2. Preview dari scene Boot: putih → logo → fade → Loading → Lobby.
3. Lobby: hover dan klik tiap tombol; buka dan tutup tiap modal (Esc / Close).
4. Settings: toggle suara, tutup game, buka lagi, status tetap.
5. Play → geser difficulty ke 5 posisi → Confirm → Gameplay.
6. Gameplay: A/D bergerak, kamera dan parallax halus, E ambil stick, tas penuh memunculkan Swap, I buka inventory, Q minum, Esc pause; timer berhenti saat modal.
7. Sampai rumah: Result, stick di Index, uang dan level naik.
8. Biarkan timer habis: gelap → cutscene → Game Over; stick hilang; Retry; level sama.
9. Shop dan Upgrade: beli, equip, kapasitas tas bertambah.
10. Muat ulang halaman/game: semua data tetap.

---

## 13. DAFTAR PERIKSA EKSPOR ITCH.IO (untuk pengguna)

1. Pastikan nama file/folder aset konsisten huruf kecil sesuai Bab 10.
2. Ekspor HTML5 dari GDevelop ("Web (HTML5)") dan hasilkan zip dengan `index.html` di root zip.
3. Di itch.io: tipe "HTML", centang "This file will be played in the browser", atur ukuran embed sesuai resolusi game (default 1024 × 576), uji dengan "Fullscreen button" bila perlu.
4. Uji di Chrome dan satu browser lain, termasuk suara setelah klik pertama.
5. Penyimpanan memakai localStorage browser: data tersimpan per browser dan per domain.

---

## 14. ASUMSI DAN KEPUTUSAN TERBUKA

Item ini tidak diubah diam-diam. Bila pengguna menjawab, catat di PROGRESS.md.

1. Resolusi 1024 × 576 (asumsi dari ukuran aset lingkungan).
2. Ukuran frame karakter: 32×48 atau 48×64 (saran 48×64).
3. Kostum: satu sheet per item atau satu file per animasi.
4. Stick belum ditemukan: siluet PNG per stick atau digelapkan engine saat runtime.
5. Jumlah produk Shop (default 4 shirt + 4 pants).
6. Pause punya tombol Return to Lobby atau tidak.
7. Cara stick dipegang: held sprite + titik tangan, atau pose karakter khusus.
8. Run hanya saat Speed Boost (asumsi).
9. Replace menaruh stick lama di tanah (asumsi).
10. Continue di Success membuka Difficulty level berikutnya (asumsi).
11. Font pixel khusus: belum ada, pakai font bawaan sementara.
12. Mengiris sprite sheet menjadi file frame: butuh izin (Aturan 7).

---

## 15. FORMAT LAPORAN

Setiap tahap diakhiri laporan singkat, tanpa mengulang langkah. Isi, dalam urutan ini:

1. **Hasil** (1–3 kalimat): apa yang sekarang bisa dilakukan.
2. **Yang diubah:** scene, object, layer, variabel, event group, file project yang disentuh. Backup ada di mana.
3. **Cara mencoba di GDevelop:** langkah numerik, maks. 8 langkah.
4. **Terbukti vs belum terbukti:** apa yang benar-benar divalidasi/dijalankan, apa yang tidak bisa dijalankan.
5. **Missing Asset Report.**
6. **Asumsi dan pertanyaan** (maksimal 5, yang menghalangi saja).
7. **Berikutnya:** tahap yang disarankan.

### Template Missing Asset Report

| Aset | Nama file yang diharapkan | Tahap | Prioritas | Dampak | Keadaan sekarang |
|---|---|---|---|---|---|
| Logo developer | `boot_logo_dev.png` | 1 | P0 | Logo tidak tampil | Object `Spr_BootLogo` sudah ada tanpa gambar |

Tulis juga aset yang ditemukan tetapi tidak sesuai standar (dimensi tidak cocok, tidak ada alpha, sheet frame tidak rata), tanpa memperbaikinya.

### Isi `AI_NOTES/PROGRESS.md`

Status per tahap (Belum / Sebagian / Selesai), kapabilitas tool MCP, keputusan dan asumsi yang disetujui, daftar stub, daftar hal belum selesai, catatan teknis (cara parallax dipilih, cara preload, dsb.). Perbarui di akhir setiap tahap. File ini adalah ingatan untuk sesi AI berikutnya; tulis agar bisa dipahami tanpa riwayat chat.

---

## 16. RINGKASAN ATURAN DALAM 12 BARIS

1. Baca file ini dulu, setiap sesi.
2. Jangan membuat, mengubah, atau mengganti aset visual, audio, atau font.
3. Tidak ada placeholder geometris. Pengecualian hanya fade layar penuh.
4. Aset hilang → laporkan, bangun logikanya, jangan merujuk file yang tidak ada.
5. Jangan rename, pindah, hapus aset sumber.
6. Layout Lobby milik tim.
7. Backup sebelum mengubah, validasi setelahnya.
8. Jangan menebak skema `game.json`; tiru pola editor dan MCP.
9. Semua bisa diedit visual di GDevelop 5 dan jalan di HTML5/itch.io.
10. Angka di `Config`, konten di `Data`, penyimpanan di `Save`.
11. Hanya kerjakan tahap yang diminta; jangan klaim sudah dites tanpa bukti.
12. Akhiri dengan laporan format Bab 15.
