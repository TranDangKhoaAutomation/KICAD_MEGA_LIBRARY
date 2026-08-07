# KiCad Mega Library

**Thư viện KiCad tổng hợp của Trần Đăng Khoa** — gom góp và cập nhật tự động từ nhiều nguồn thư viện chính thức của các nhà sản xuất linh kiện.

> © 2026 **Trần Đăng Khoa**. Mọi nội dung trong hệ thống thư viện này thuộc về tác giả.

---

## 📦 Thư viện có trong hệ thống

| Nguồn | Nhà sản xuất | Nội dung |
|---|---|---|
| `Mega_Espressif` | Espressif | Chip ESP32, module WiFi/BLE |
| `Mega_SparkFun` | SparkFun | Linh kiện, sensor, module phổ biến |
| `Mega_DigiKey` | DigiKey | Hàng nghìn linh kiện từ nhà phân phối |
| `Mega_JLCPCB` | JLCPCB (CDFER) | Linh kiện basic/preferred của JLCPCB |
| `Mega_MCU_ST_STM32F0/F1/F3/F4/F7/H7/L4/L4+` | STMicroelectronics | Symbol MCU STM32 chính thức (~835 MCU) |
| `Mega_STM32_Board` | STM32 dev boards | Footprint + symbol board dev STM32 (40 boards) |
| `Mega_Espressif` | ESP32 dev boards | Footprint + symbol board dev ESP32 (14 boards) |

### 📊 Tổng số linh kiện

| Loại | Số lượng |
|---|---|
| **Symbol** (linh kiện) | **3.818** symbol chính trong 74 file |
| **Footprint** (chân linh kiện) | **1.442** footprint trong 25 thư viện |
| **Model 3D** (`.step`/`.wrl`) | **751** model |
| **Board dev STM32** | **40** boards |
| **Board dev ESP32** | **14** boards |
| **MCU STM32** | **835** chip (trong 8 thư viện `MCU_ST_STM32*`) |

---

### 🧩 Board dev STM32 (trong `Mega_STM32_Board`)

- **Pill boards**: Blue Pill (F103C8/CB), Black Pill (F401/F411, WeAct)
- **Core boards**: F407VET6/ZGT6/VGT6, F405RGT6, H743VIT6, H750VBT6
- **Discovery**: F0, F3, F4, F407G-DISC1, F401C, F411E, F429I, F469I, F746G, F769I, H747I, L476G, U5G9J
- **Nucleo**: NUCLEO-32/64/144, F030R8, F103RB, F401RE, F411RE, F446RE/ZF, F767ZI, G431RB, G474RE, H743ZI, H753ZI, L432KC, L476RG
- **Khác**: STM32F103C8T6 Mini, Maple Mini STM32F103

### 🧩 Board dev ESP32 (trong `Mega_Espressif`)

- **Espressif chính thức**: DevKitC (classic/S2/S3/C3/C5/C6), DevKitM-1, Saola-1
- **Cộng đồng**: ESP32-DevKit-V1-DOIT, NodeMCU-32S, NodeMCU-ESP8266, ESP32-S3-DevKitC-1

---

## 🚀 Cách dùng

Thư viện **đã được đăng ký sẵn trong KiCad** (nếu đã chạy cài đặt trên máy này). Chỉ cần mở KiCad:

1. Mở **Symbol Editor** / **Footprint Editor**
2. Tìm các thư viện tên bắt đầu bằng **`Mega_`**
3. Chọn linh kiện — model 3D sẽ hiển thị khi xem footprint

> 💡 Mẹo: Trong **Eeschema**, bấm **A** (Add Symbol) rồi gõ `Mega_` để lọc nhanh tất cả linh kiện của hệ thống.

---

## 🔧 Hướng dẫn thêm toàn bộ thư viện vào KiCad

Có **2 cách**: tự động (nhanh, khuyên dùng) hoặc thủ công (khi cần kiểm soát).

### Cách 1 — Tự động (khuyên dùng)

Nếu có file `Update-KiCadMegaLibrary.bat` ở gốc thư viện:

```
Update-KiCadMegaLibrary.bat
```

File này sẽ tự động:
1. **Pull** mã mới nhất từ các repo nhà sản xuất vào `Sources/`
2. **Đồng bộ** file thư viện mới vào `symbols/`, `footprints/`, `3dmodels/`
3. **Sửa** model paths 3D bị hỏng
4. **Đăng ký lại** toàn bộ bảng thư viện trong KiCad (tự ghi `sym-lib-table` + `fp-lib-table`)

> ⚠️ **Lưu ý:** Đóng KiCad trước khi chạy file bat.

### Cách 2 — Thủ công (đăng ký từng thư viện)

> 💡 **Bước 0 (quan trọng):** Đảm bảo biến môi trường `MEGA_KICAD_LIB` trỏ đúng đường dẫn:
> ```
> MEGA_KICAD_LIB = D:\KICAD_MEGA_LIBRARY
> ```
> (Kiểm tra: `System Properties → Environment Variables → User variables`)
> Nếu không có, các đường dẫn `${MEGA_KICAD_LIB}` sẽ không hoạt động.

#### A. Thêm Symbol Libraries (file `.kicad_sym`)

Các file symbol nằm trong: **`D:\KICAD_MEGA_LIBRARY\symbols\`**

1. Mở KiCad → **Preferences → Manage Symbol Libraries** (hoặc **Symbol Editor → Preferences → Manage Symbol Libraries**)
2. Bấm **+** để thêm từng thư viện, điền:
   - **Nickname**: tên hiển thị (vd `Mega_DigiKey_1`)
   - **Path**: `${MEGA_KICAD_LIB}/symbols/<tên file>.kicad_sym`
   - **Plugin Type**: `KiCad`
3. Bấm **OK**

**Các thư viện symbol nên thêm** (74 file trong `symbols/`):

| Nhóm | File | Nickname gợi ý |
|---|---|---|
| DigiKey | `DigiKey_1.kicad_sym` → `DigiKey_12.kicad_sym` | `Mega_DigiKey_1` → `Mega_DigiKey_12` |
| JLCPCB | `JLCPCB-*.kicad_sym` (18 file) | `Mega_JLCPCB_<Tên>` |
| SparkFun | `SparkFun-*.kicad_sym` (28 file) | `Mega_SparkFun-<Tên>` |
| Espressif | `Espressif.kicad_sym` | `Mega_Espressif` |
| MCU STM32 | `MCU_ST_STM32F0/F1/F3/F4/F7/H7/L4/L4+.kicad_sym` | `Mega_MCU_ST_STM32F0`… |
| Board STM32 | `STM32_Board.kicad_sym` | `Mega_STM32_Board` |

#### B. Thêm Footprint Libraries (thư mục `.pretty`)

Các thư mục footprint nằm trong: **`D:\KICAD_MEGA_LIBRARY\footprints\`**

1. Mở KiCad → **Preferences → Manage Footprint Libraries** (hoặc **Footprint Editor → Preferences → Manage Footprint Libraries**)
2. Bấm **+** để thêm từng thư mục, điền:
   - **Nickname**: tên hiển thị (vd `Mega_Espressif`)
   - **Path**: `${MEGA_KICAD_LIB}/footprints/<tên thư mục>.pretty`
   - **Plugin Type**: `KiCad`
3. Bấm **OK**

**Các thư viện footprint nên thêm** (25 thư mục trong `footprints/`):

| Thư mục | Nickname gợi ý |
|---|---|
| `digikey-footprints.pretty` | `Mega_DigiKey` |
| `JLCPCB.pretty` | `Mega_JLCPCB` |
| `Espressif.pretty` | `Mega_Espressif` |
| `STM32_Board.pretty` | `Mega_STM32_Board` |
| `SparkFun-*.pretty` (21 thư mục) | `Mega_SparkFun-<Tên>` |

#### C. Thêm Model 3D

Model 3D được tham chiếu tự động qua footprint (trong tab **3D Models** của từng footprint). Nếu cần thêm thủ công:

1. Bỏ file `.step`/`.wrl` vào **`D:\KICAD_MEGA_LIBRARY\3dmodels\`** (đúng thư mục theo nhà sản xuất)
2. Trong **Footprint Editor** → chọn footprint → **3D Models tab → Add**
3. Chọn đường dẫn tới file model 3D

#### D. Kiểm tra sau khi đăng ký

1. Mở **Symbol Editor** → danh sách thư viện bên trái phải hiện các `Mega_*`
2. Chọn 1 symbol bất kỳ (vd `Mega_Espressif:ESP32-DevKitC`) → phải hiển thị pinout
3. Mở **Footprint Editor** → chọn `Mega_Espressif:ESP32-DevKitC` → phải hiện footprint + model 3D

---

### 🔧 Thêm thư viện mới tự tạo (Custom)

Nếu tự tạo thư viện riêng:

**Symbol (`.kicad_sym`):**
1. Sao chép file vào `D:\KICAD_MEGA_LIBRARY\symbols\`
2. Đăng ký như mục **A** ở trên (Nickname `Mega_Custom`, Path `${MEGA_KICAD_LIB}/symbols/Custom.kicad_sym`)

**Footprint (`.pretty`):**
1. Tạo thư mục `D:\KICAD_MEGA_LIBRARY\footprints\Custom.pretty`, bỏ `.kicad_mod` vào
2. Đăng ký như mục **B** ở trên (Nickname `Mega_Custom`, Path `${MEGA_KICAD_LIB}/footprints/Custom.pretty`)

---

## 🔄 Cập nhật thư viện (Pull mới từ nhà sản xuất)

Khi nhà sản xuất phát hành linh kiện mới, chạy file:

```
Update-KiCadMegaLibrary.bat
```

File này sẽ tự động:
1. **Pull** mã mới nhất từ 4 repo nhà sản xuất vào `Sources/`
2. **Đồng bộ** file thư viện mới vào `symbols/`, `footprints/`, `3dmodels/`
3. **Sửa** model paths 3D
4. **Đăng ký lại** bảng thư viện trong KiCad

> ⚠️ **Lưu ý:** Đóng KiCad trước khi chạy file bat. File bat sẽ tự kiểm tra.

---

## 📁 Cấu trúc thư mục

```
D:\KICAD_MEGA_LIBRARY
├── Sources/          ← Các repo Git nguồn (Espressif, SparkFun, DigiKey, JLCPCB-CDFER)
├── symbols/          ← Thư viện symbol .kicad_sym (74 file, 3818 symbol)
├── footprints/       ← Thư viện footprint .pretty (25 thư mục, 1442 footprint)
├── 3dmodels/         ← Model 3D .step/.wrl (751 model)
├── Archived-Symbols-Footprints/  ← Dữ liệu lưu trữ cũ
├── Backup/           ← Bản sao lưu đề phòng
├── logs/             ← Nhật ký + báo cáo
└── resources/        ← Script hỗ trợ (chạy bởi file bat)
```

---

## ⚖️ Nguồn gốc & giấy phép

| Nguồn | Giấy phép |
|---|---|
| KiCad Official | CC-BY-SA-4.0 |
| Espressif | CC-BY-SA-4.0 |
| SparkFun | CC-BY-SA-4.0 |
| DigiKey | MIT |
| JLCPCB-CDFER | MIT (cộng đồng) |
| STM32 (MCU_ST_STM32*) | CC-BY-SA-4.0 (KiCad official) |

Hệ thống tổng hợp: **© Trần Đăng Khoa**
