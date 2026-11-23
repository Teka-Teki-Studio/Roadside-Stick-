# PROGRESS PROJECT: ROADSIDE STICK

## 1. Status Tahap
- [x] **Tahap 0 — Foundation**: Selesai. Pengaturan resolusi 1024×576, firstLayout: Boot, variabel global (Save, Config, Data, Run), 7 layout stub, backup dibuat.
- [x] **Tahap 1 — Boot**: Selesai. Scene `Boot` berlatar putih (#FFFFFF), object `Spr_BootLogo` (512×115) di tengah layar, urutan fade-in (0.5-1.1s), tahan (1.1-2.3s), fade-out (2.3-2.9s), dan transisi ke `Loading` pada 3.0s.
- [x] **Tahap 2 — Loading (Revisi Sempurna)**: Selesai. 
  - Proporsi bar diperbaiki menjadi 640×24 px (ramping retro, melebar proporsional di viewport 1024).
  - Fill loading bar aktif menggunakan aksi standar GDevelop 5.6 `SetWidth` (0 s.d. 565 px).
  - Animasi spinner 8-frame aktif berputar loop di sebelah teks loading.
  - Teks menggunakan font `vcr.ttf` (VCR OSD Mono), warna putih murni (#FFFFFF), outline & stroke dinonaktifkan total.
  - Durasi loading diperpanjang menjadi 4.0 detik agar transisi mulus dan dapat dinikmati.
- [x] **Tahap 3 — Lobby (Interactive Mockup & Living VFX)**: Selesai. Robi portrait idle 10-frame (128x128 loop), 4 tombol 3D pixel-art responsif (Hover & Pressed), VFX breathing & pulsing, BGM loading & menu terintegrasi.
- [ ] **Tahap 4 — Settings & About**: Belum dimulai.
- [x] **Tahap 5 — Difficulty**: Selesai (Mockup Fungsional). 5 level (Peaceful, Easy, Normal, Hard, Super Hard), deskripsi dinamis, tombol Confirm menuju Gameplay, Back kembali ke Lobby.
- [ ] **Tahap 6 — Stick Index**: Belum dimulai.
- [ ] **Tahap 7 — Shop**: Belum dimulai.
- [ ] **Tahap 8 — Upgrade**: Belum dimulai.
- [x] **Tahap 9 — Gameplay: Environment**: Selesai (Versi Dasar). Layer BG_Sky (Langit_Pagi), BG_Village (Rumah dan Pohon), deretan terrain Rumput1..3 berselang-seling di Y=448, kamera mengikuti pemain.
- [x] **Tahap 10 — Karakter & Kostum**: Selesai (Versi Dasar). Robi gameplay memiliki 10 frame Idle dan 10 frame Walk dari robi_sd.png, kontrol A/D, flip horizontal otomatis, batas kiri start.
- [ ] **Tahap 11 — Stick (Koleksi)**: Belum dimulai.
- [ ] **Tahap 12 — HUD, Inventory, Swap, Pause**: Belum dimulai.
- [ ] **Tahap 13 — Success & Result**: Belum dimulai.
- [ ] **Tahap 14 — Failure, Cutscene, GameOver**: Belum dimulai.
- [ ] **Tahap 15 — Loop & Integrasi**: Belum dimulai.

## 2. Aturan Khusus Terkini (Bab 1.A.4b AGENTS.md)
- Seluruh teks wajib menggunakan font `vcr.ttf` warna putih murni (`255;255;255`).
- Dilarang menambahkan stroke/outline/shadow pada teks tanpa instruksi eksplisit dari pengguna.

### Update 2026-11-23 02:45 — Tahap 2: Loading Bar Ramping & Spinner Kanan
- **Loading Bar:** Instance disesuaikan ramping (tinggi 12px, lebar 920px) dengan file frame & fill terkini.
- **Bar Fill:** Memperbaiki instruction menjadi ChangeWidth (menggantikan SetWidth yang sebelumnya di-skip engine libGD). Bar fill kini valid dan lebarnya bertambah mulus dari 1px hingga 920px.
- **Spinner / Indicator:** Dipindahkan ke sisi kanan loading bar (X: 968, Y: 514, W: 24, H: 24) sejajar vertikal dengan bar di dalam layar 1024x576.
- **Tipografi:** Menggunakan font cr.ttf, warna putih murni 255;255;255, outline nonaktif (isOutlineEnabled: false).
- **Validasi:** Kompilasi libGD 5.6.287 sukses untuk seluruh 7 scene dengan 0 error/diagnostics.

### Update 2026-11-23 14:00 — Tahap 5 & Tahap 9-10: Modal Difficulty & Gameplay Playable Dasar
- **Modal Difficulty (Tahap 5):**
  - Klik tombol `Btn_Play` di Lobby membuka layer `Modals` dengan dim background.
  - 5 tingkat kesulitan dengan selector panah `<` dan `>`: Peaceful (3.0x), Easy (2.2x), Normal (1.7x), Hard (1.35x), Super Hard (1.15x).
  - Tombol Confirm menyimpan `Run.difficulty` dan beralih ke scene `Gameplay` via `PushScene`.
  - Tombol Back menutup modal kembali ke Lobby.
- **Scene Gameplay (Tahap 9 & 10):**
  - **Environment:** Layer `BG_Sky` dengan `Langit_Pagi.png`, layer `BG_Village` dengan `Rumah dan Pohon.png` di Y=192, dan deretan 16 tile terrain `Rumput1..3.png` berselang-seling di garis tanah Y=448 membentang sepanjang lintasan jalan.
  - **Karakter Robi:** Memotong 10 frame berjalan Robi (`robi_walk_00..09.png`) dari row 2 `robi_sd.png`. Player memiliki animasi Idle dan Walk.
  - **Kontrol:** Input keyboard <kbd>A</kbd>/<kbd>D</kbd> atau panah kiri/kanan menggerakkan Robi dengan kecepatan 160 px/detik, auto flip horizontal, dan transisi ke Idle saat tombol dilepas. Batas start kiri dibatasi di X=50.
  - **Kamera & HUD:** Kamera horizontal dinamis berpusat mengikuti posisi Robi. HUD menampilkan countdown timer dan panduan kontrol. Tombol <kbd>Esc</kbd> kembali ke Lobby.
- **Validasi:** Kompilasi libGD 5.6.287 sukses untuk seluruh 7 scene dengan 0 diagnostics.

### Update 2026-11-23 13:42 — Penggantian Loading BG ke Tes64.png
- **Loading Background Baru:** Mengganti background `Spr_LoadingBg` menjadi `Tes64.png` (114×64 RGBA). Visual menampilkan ilustrasi naratif pixel-art Robi berlari membawa ranting kayu dikejar motor orang tua.
- **Render Settings:** Resource didaftarkan dengan `smoothed: false` sehingga saat di-scale ke 1024×576 di GDevelop, pixel art-nya tampil tajam dan presisi rasio 16:9.
- **Validasi:** Kompilasi libGD 5.6.287 sukses untuk seluruh 7 layout dengan 0 diagnostics.

### Update 2026-11-23 12:30 — Revisi Detail: Boot Logo Compact, Loading Pixel-Art BG & Logo, Clean Robi Idle Frame, & Lobby Waist-Up Zoom
- **Boot Logo Dikecilkan:** Logo developer dikecilkan menjadi 480×108 px (centered) agar proporsional dan tidak mendominasi layar.
- **Loading Screen Tajam:** Background diperbarui ke `BGLoadingPX.png` (256×144) hasil export LibreSprite, menghasilkan tampilan pixel-art tajam tanpa blur. Ditambahkan logo game `Logo Gam.png` di kiri atas (X: 36, Y: 28) dengan margin aman.
- **Pembersihan Frame 0 Idle Robi:** Menghapus 24 piksel label teks "IDLE" yang menempel di frame 0. Seluruh 10 frame idle kini bersih total 100%.
- **Lobby Waist-Up Zoom:** Menyesuaikan ukuran tampilan Robi di Lobby menjadi waist-up portrait yang besar dan gagah di sisi kiri, serta menonaktifkan efek osilasi gerak nafas (posisi tetap stabil).
- **Validasi:** Kompilasi libGD 5.6.287 sukses untuk seluruh 7 scene dengan 0 diagnostics.

### Update 2026-11-23 12:15 — Polish Visual: HD Logo, Loading BG, 10-Frame Robi, BGM, & VFX
- **Boot Logo HD & Camera Shake:** Resolusi tampilan logo disesuaikan menjadi 884×198 px (skala proporsional 40% dari 2213×496) centered di layar 1024×576. Ditambahkan efek camera shake halus (amplitudo 4px) saat logo muncul pada 1.05s s.d. 1.25s.
- **Loading Screen BG:** Mengintegrasikan visual background baru `DraftLoadingPXFix.png` (1280×720 RGBA) menggantikan dummy.
- **Robi Idle 10 Frames:** Memotong 10 frame idle dari row 1 `robi_sd.png` (128×128 tiap frame) ke folder `ASSETS/CHARACTER/PLAYER/idle_frames/`. Ditampilkan dalam format portrait kepala-pinggang besar (384×384 px) di sisi kiri Lobby dengan loop mulus (0.12s per frame).
- **Audio & BGM:** Mengintegrasikan `bgm_loading.mp3` pada Loading scene dan `bgm_menu.mp3` pada Lobby scene di channel 1 independen.
- **Living VFX:** Ditambahkan dynamic float/breathe subtle oscillation pada Robi (`sin(TimeFromStart())`) dan denyut glow/pulse pada tombol Play di Lobby.
- **Validasi:** Kompilasi libGD 5.6.287 sukses untuk seluruh 7 scene dengan 0 diagnostics.

- **Karakter Idle (Robi):** Dicrop dari sprite sheet acuan (
obi_sd.png), ditampilkan di sisi kiri Lobby dengan portrait waist-up besar (kepala-pinggang) tajam pixel-art.
- **4 Tombol Interaktif 3D:**
  1. Tombol Atas: Btn_Play (Mainkan) — Kuning 3D (420×64 px)
  2. Tombol Kiri Bawah: Btn_Shop (Toko) — Kuning 3D (200×56 px)
  3. Tombol Kanan Bawah: Btn_Index (Koleksi) — Ungu 3D (200×56 px)
  4. Tombol Bawah: Btn_Upgrade (Upgrade) — Kuning 3D (420×64 px, sama besar dengan Mainkan)
- **Interaksi Hover & Click:** Setiap tombol memiliki 3 state animasi (Normal, Hover, Pressed). Kursor di atas tombol otomatis berganti state Hover, dan saat klik mouse kiri ditekan otomatis berganti state Pressed (efek tombol tertekan 3D).
- **Tipografi:** Teks tombol menggunakan font cr.ttf warna putih murni tanpa stroke.
- **Git:** Perubahan di-commit dan di-push ke branch Danans-Version di remote origin.
