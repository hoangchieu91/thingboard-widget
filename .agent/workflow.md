# AI Agent 5-Step Widget Development Workflow

## Bước 1: Khởi tạo (Generate)
Dùng `templates/html_value_card.py` để dựng khung Widget JSON mẫu có sẵn Live Preview.

## Bước 2: Đóng gói Sản phẩm (Package)
Dùng `scripts/package_product.py` để kiểm tra chuẩn quy tắc Vàng và gắn nhãn số phiên bản (`v1.0.0`) vào `product/widgets/`.

## Bước 3: Kiểm thử Offline Tự động (Offline AI Self-Test)
Dùng `scripts/ai_test_offline.py` để kiểm tra Widget JSON trên Sandbox ngầm trước khi đẩy lên server:
```bash
python3 scripts/ai_test_offline.py --file product/widgets/<widget_file>.json
```

## Bước 4: Triển khai (Deploy)
Dùng `deploy/deploy_widget.py` để đẩy Widget JSON lên server ThingsBoard và gán vào Widget Bundle.

## Bước 5: Soi lỗi & Chụp hình trên Server (Live Debug)
Dùng `deploy/live_debug.js` chạy Chrome Headless trên server thật để kiểm tra console log và xác nhận không có lỗi runtime.
