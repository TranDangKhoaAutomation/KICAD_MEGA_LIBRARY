# KICAD Mega Library

Kho lưu trữ tổng hợp thư viện dành cho **KiCad**, giúp bạn quản lý linh kiện, footprint và symbol ở một nơi thống nhất để tái sử dụng cho nhiều dự án mạch in.

## Mục tiêu

- Tập trung thư viện KiCad vào một repo duy nhất, dễ theo dõi và mở rộng.
- Tái sử dụng linh kiện giữa các dự án, giảm thời gian dựng schematic/PCB.
- Chuẩn hóa dữ liệu thư viện để làm việc nhóm nhất quán hơn.

## Nội dung thư viện (định hướng)

Repo này hướng tới việc lưu trữ:

- **Symbols** (`.kicad_sym`)
- **Footprints** (`.pretty/`)
- **3D Models** (`.step`, `.wrl`)
- **Template và tài nguyên hỗ trợ** cho quy trình thiết kế với KiCad

## Cách sử dụng với KiCad

1. Clone repo về máy.
2. Mở **KiCad** → **Preferences** → **Manage Symbol Libraries** và **Manage Footprint Libraries**.
3. Thêm đường dẫn thư viện trong repo vào Global hoặc Project libraries.
4. Đồng bộ thư viện khi có cập nhật mới.

## Định hướng phát triển

- Bổ sung thư viện theo nhóm linh kiện (MCU, nguồn, RF, connector, sensor, ...).
- Chuẩn hóa naming convention cho symbol/footprint.
- Bổ sung kiểm tra chất lượng thư viện trước khi merge.

## Đóng góp

Rất hoan nghênh đóng góp từ cộng đồng:

- Thêm linh kiện mới
- Cải thiện footprint/symbol hiện có
- Báo lỗi hoặc đề xuất cấu trúc thư viện tốt hơn

---

**English summary:** A centralized mega-library repository for KiCad symbols, footprints, and related assets to improve reuse, consistency, and collaboration across electronics projects.