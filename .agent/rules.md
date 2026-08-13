# Agent Rules & Execution Guidelines

## 1. Mật khẩu & Bảo mật Server
- Tuyệt đối KHÔNG tự ý đổi mật khẩu login hoặc database của ThingsBoard.
- Khi nghi vấn hoặc không nhớ credential, hỏi trực tiếp người dùng.

## 2. Nâng số Phiên bản (Versioning Rule)
- Mỗi khi sửa code ảnh hưởng tính năng hoặc ra bản phát hành mới, **BẮT BUỘC nâng số phiên bản** (`v1.0.0` -> `v1.0.1` -> `v1.1.0`).
- Sản phẩm đóng gói được đưa vào thư mục `product/widgets/<widget_alias>_v<version>.json`.

## 3. Kiến trúc Widget ThingsBoard 4.x
- Luôn kiểm tra `dataKeys` có `"settings": {"hideDataByDefault": false}`.
- Không nổ lỗi scope `self` (tất cả helper function nằm trong closure `self.onInit`).
- Cấu hình `defaultConfig` đầy đủ `function` datasources để ô Preview trong Widget Editor luôn có Live Demo.
- Scope jQuery selector `$('#id', self.ctx.$container)`.
- Đặt `"settingsDirective": ""` khi khai báo `settingsForm` để ThingsBoard 4.x hiển thị tab Cài đặt tùy chỉnh trên UI.
