# KiCad Mega Library

**Thư viện KiCad tổng hợp của Trần Đăng Khoa** — gom góp và cập nhật tự động từ nhiều nguồn thư viện chính thức của các nhà sản xuất linh kiện.

> © 2026 **Trần Đăng Khoa**. Mọi nội dung trong hệ thống thư viện này thuộc về tác giả.

---

## 📦 Thư viện có trong hệ thống

Hệ thống gồm **4 nguồn thư viện** đã được clone về máy cục bộ và nối thẳng vào KiCad:

| Nguồn | Nhà sản xuất | Nội dung |
|---|---|---|
| `Mega_Espressif` | Espressif | Chip ESP32, module WiFi/BLE |
| `Mega_SparkFun` | SparkFun | Linh kiện, sensor, module phổ biến |
| `Mega_DigiKey` | DigiKey | Hàng nghìn linh kiện từ nhà phân phối |
| `Mega_JLCPCB` | JLCPCB (CDFER) | Linh kiện basic/preferred của JLCPCB |

**Tổng số:** khoảng **8.900 symbol**, **1.400 footprint**, **750 model 3D**.

---

## 🚀 Cách dùng

Thư viện **đã được đăng ký sẵn trong KiCad**. Chỉ cần mở KiCad:

1. Mở **Symbol Editor** / **Footprint Editor**
2. Tìm các thư viện tên bắt đầu bằng **`Mega_`**
3. Chọn linh kiện — model 3D sẽ hiển thị khi xem footprint

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
├── symbols/          ← Thư viện symbol (KiCad trỏ tới)
├── footprints/       ← Thư viện footprint .pretty (KiCad trỏ tới)
├── 3dmodels/         ← Model 3D (KiCad trỏ tới)
├── Archived-Symbols-Footprints/  ← Dữ liệu lưu trữ cũ
├── Backup/           ← Bản sao lưu đề phòng
├── logs/             ← Nhật ký + báo cáo
└── resources/        ← Script hỗ trợ (chạy bởi file bat)
```

---

## 🔧 Thêm thư viện thủ công

### Thêm symbol (file `.kicad_sym`)
1. Sao chép file vào `D:\KICAD_MEGA_LIBRARY\symbols\`
2. Mở KiCad → **Preferences → Manage Symbol Libraries**
3. Bấm **+** → điền **Nickname** (vd `Mega_Custom`), **Path** = `D:\KICAD_MEGA_LIBRARY\symbols\<file>.kicad_sym`

### Thêm footprint (thư mục `.pretty`)
1. Tạo thư mục `D:\KICAD_MEGA_LIBRARY\footprints\Custom.pretty`, bỏ `.kicad_mod` vào
2. Mở KiCad → **Preferences → Manage Footprint Libraries**
3. Bấm **+** → điền **Nickname** (vd `Mega_Custom`), **Path** = `D:\KICAD_MEGA_LIBRARY\footprints\Custom.pretty`

### Thêm model 3D
1. Bỏ file `.step`/`.wrl` vào `D:\KICAD_MEGA_LIBRARY\3dmodels\`
2. Trong **Footprint Editor** → chọn footprint → **3D Models tab → Add**

---

## ⚖️ Nguồn gốc & giấy phép

| Nguồn | Giấy phép |
|---|---|
| KiCad Official | CC-BY-SA-4.0 |
| Espressif | CC-BY-SA-4.0 |
| SparkFun | CC-BY-SA-4.0 |
| DigiKey | MIT |
| JLCPCB-CDFER | MIT (cộng đồng) |

Hệ thống tổng hợp: **© Trần Đăng Khoa**
