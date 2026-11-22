# MISSING ASSETS REPORT

Laporan status aset yang diharapkan vs aset yang ada di disk per spesifikasi `AGENTS.md`.

## Tahap 1 — Boot
| Aset | Nama file yang diharapkan | Tahap | Prioritas | Dampak | Keadaan sekarang |
|---|---|---|---|---|---|
| Logo Developer | `boot_logo_dev.png` | 1 | P0 | Logo tampil saat Boot | Ada di disk (`ASSETS/BOOT/LOGO/boot_logo_dev.png`), 2213×496 (RGBA). Ditampilkan terskala 512×115 via GDevelop. |

## Tahap 2 — Loading
| Aset | Nama file yang diharapkan | Tahap | Prioritas | Dampak | Keadaan sekarang |
|---|---|---|---|---|---|
| Dummy Background | `boot_loading_bg_dummy.png` | 2 | P0 | Latar belakang scene loading | Ada di disk (`ASSETS/BOOT/LOADING/boot_loading_bg_dummy.png`), 1672×941 (RGB). Tampil di layer Base. |
| Loading Indicator | `boot_loading_indicator_0.png` s.d. `_7.png` | 2 | P0 | Animasi indikator loading memutar | 8 frame 16×16 aktif berputar loop di `Spr_LoadingIndicator` (0.08s/frame). |
| Loading Bar Frame | `boot_loading_bar_frame.png` | 2 | P0 | Bingkai loading bar | Ada di disk (`ASSETS/BOOT/LOADING/boot_loading_bar_frame.png`), proporsi proporsional 640×24 px. |
| Loading Bar Fill | `boot_loading_bar_fill.png` | 2 | P0 | Isi loading bar progres | Ada di disk (`ASSETS/BOOT/LOADING/boot_loading_bar_fill.png`), aktif bertambah via aksi `SetWidth` (maks 565 px). |
| Font VCR | `vcr.ttf` | 2 | P0 | Tipografi retro resmi | Ada di disk (`ASSETS/UI/vcr.ttf`). Dipakai untuk semua teks loading (putih polos, tanpa stroke). |

## Tahap 3 — Lobby
| Aset | Nama file yang diharapkan | Tahap | Prioritas | Dampak | Keadaan sekarang |
|---|---|---|---|---|---|
| Background Lobby | `bg_lobby.png` | 3 | P0 | Latar scene lobby | Ada di disk (`ASSETS/LOBBY/bg_lobby.png`), 1920×1080. |
| Tombol UI Lobby | `ui_btn_*` | 3 | P0 | Navigasi menu Lobby | Belum ada di disk. |
