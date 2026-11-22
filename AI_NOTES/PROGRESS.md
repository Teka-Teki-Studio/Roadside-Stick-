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
- [ ] **Tahap 3 — Lobby**: Belum dimulai.
- [ ] **Tahap 4 — Settings & About**: Belum dimulai.
- [ ] **Tahap 5 — Difficulty**: Belum dimulai.
- [ ] **Tahap 6 — Stick Index**: Belum dimulai.
- [ ] **Tahap 7 — Shop**: Belum dimulai.
- [ ] **Tahap 8 — Upgrade**: Belum dimulai.
- [ ] **Tahap 9 — Gameplay: Environment**: Belum dimulai.
- [ ] **Tahap 10 — Karakter & Kostum**: Belum dimulai.
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
