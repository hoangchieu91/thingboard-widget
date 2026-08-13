# ThingsBoard Widget Agent Framework
## AMItech Industrial Commercial Ready Widget Toolkit

Chuyên gia tự động hóa phát triển, kiểm định, đóng gói và triển khai **Custom Widget cho ThingsBoard 4.x** phục vụ sản xuất và kỹ sư hiện trường AMItech.

---

## 📁 Cấu trúc Thư mục Quy hoạch chuẩn

```text
thingsboard-widget-agent/
├── .agent/                    # Thư mục quy tắc & quy trình hoạt động của AI Agent
│   ├── rules.md               # Bộ quy tắc bảo mật, versioning, dọn dẹp & đóng gói
│   └── workflow.md            # Quy trình 4 bước hoạt động cho Agent
├── deploy/                    # Công cụ triển khai & Live Debug trên máy chủ ThingsBoard
│   ├── README.md              # Hướng dẫn công cụ deploy/debug
│   ├── deploy_widget.py       # Script deploy Widget tự động qua REST API
│   └── live_debug.js          # Tool soi lỗi Console & chụp hình qua Chrome Headless
├── product/                   # Sản phẩm Widget thương mại cho AMItech & Kỹ sư hiện trường
│   ├── README.md              # Sổ tay hướng dẫn kỹ sư hiện trường import Widget
│   └── widgets/               # Các bản phát hành Widget chính thức (.json) theo số phiên bản
├── templates/                 # Các mã nguồn mẫu khởi tạo Widget
│   └── html_value_card.py     # Template khởi tạo HTML Value Card có sẵn Live Preview
├── scripts/                   # Công cụ quản lý hệ thống
│   ├── cleanup.py             # Script tự động quét & dọn dẹp file rác, file tạm
│   └── package_product.py     # Script đóng gói Widget sản phẩm chuẩn số phiên bản
├── sandbox/                   # Môi trường Workbench phát triển & test Widget cục bộ
│   ├── runner.py
│   └── index.html
├── README.md                  # Hướng dẫn tổng quan dự án (File này)
└── RULES.md                   # Bộ Quy tắc Vàng ThingsBoard 4.x (Gold Rules & Anti-Patterns)
```

---

## ⚡ Các Quy tắc Vàng (Core Rules Summary)

1. **Bảo mật & Credentials**: Tuyệt đối không tự ý đổi mật khẩu login/database. Hỏi trực tiếp người dùng khi nghi vấn.
2. **Nâng số Phiên bản (Versioning)**: Sửa code ảnh hưởng tính năng -> **Bắt buộc nâng số phiên bản** (`v1.0.0` -> `v1.0.1` -> `v1.1.0`).
3. **DataKeys luôn chứa `settings: {}`**: Mọi DataKey trong `defaultConfig` và `datasources` phải chứa `"settings": {"hideDataByDefault": false}` để tránh nổ lỗi Core `g.settings.hideDataByDefault`.
4. **Không nổ lỗi Scope `self`**: Toàn bộ hàm helper (`updateHtml`, `hashCode`, `padValue`) phải nằm trọn trong closure `self.onInit = function() { ... }`.
5. **Luôn có Live Preview**: Thuộc tính `defaultConfig` phải chứa mảng `datasources` loại `"type": "function"` phát số ngẫu nhiên để kỹ sư mở Editor hay kéo vào Dashboard là thấy số nhảy ngay.
6. **jQuery Scoped Selector**: Luôn dùng `$('#id', self.ctx.$container)` để không đè DOM giữa các Widget.

---

## 🚀 Quy trình Sử dụng Nhanh

### 1. Tạo Widget Mới từ Template:
```bash
python3 templates/html_value_card.py --name "Smart Energy Meter" --alias "smart_energy_meter"
```

### 2. Đóng gói Sản phẩm cho Kỹ sư Hiện trường:
```bash
python3 scripts/package_product.py --file smart_energy_meter.json --version "1.0.0"
```
*File đóng gói sẽ nằm tại `product/widgets/smart_energy_meter_v1.0.0.json`.*

### 3. Deploy lên Server ThingsBoard:
```bash
python3 deploy/deploy_widget.py --file product/widgets/smart_energy_meter_v1.0.0.json --server "http://10.25.7.152:8080" --bundle "amitech_widgets"
```

### 4. Live Debug qua Chrome Headless:
```bash
node deploy/live_debug.js <WIDGET_ID>
```

### 5. Dọn dẹp File Rác sau khi Phát triển:
```bash
python3 scripts/cleanup.py
```
