# Hướng dẫn Công cụ Deploy & Live Debug

Thư mục này chứa các công cụ giao tiếp trực tiếp với máy chủ ThingsBoard qua REST API và Chrome Headless.

## 1. Deploy Widget tự động (`deploy_widget.py`)
```bash
python3 deploy/deploy_widget.py --file product/widgets/solar_inverter_detail_v1.0.0.json --server "http://10.25.7.152:8080" --bundle "amitech_widgets"
```

## 2. Live Debug ngầm qua Chrome Headless (`live_debug.js`)
```bash
node deploy/live_debug.js <WIDGET_ID>
```
