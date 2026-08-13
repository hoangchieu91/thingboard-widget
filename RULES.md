# ThingsBoard 4.x Widget Agent Rules & Anti-Patterns

Bộ quy tắc này được đúc kết từ thực chiến trên phiên bản **ThingsBoard 4.2.0** nhằm đảm bảo mọi Widget tạo ra đều **hoạt động 100%, có Live Preview trong Editor, không bị đơ trình duyệt và không bị chặn khi kéo thả vào Dashboard**.

---

## 🚫 ANTI-PATTERNS (CÁC BẪY KỸ THUẬT BẮT BUỘC TRÁNH)

### ❌ Anti-Pattern 1: Khai báo DataKey thiếu thuộc tính `settings`
- **Tác hại**: Khi ThingsBoard thực thi hàm `entityDataToDatasourceData` trong `chunk-FR5XBJAK.js`, nó gọi `g.settings.hideDataByDefault`. Nếu `g.settings` bị `undefined`, trình duyệt lập tức nổ ngoại lệ `TypeError: Cannot read properties of undefined (reading 'hideDataByDefault')` làm đóng băng giao diện.
- **Quy tắc**: Mọi đối tượng `dataKey` trong mảng `dataKeys` (kể cả trong `defaultConfig` hay Dashboard Config) MUST chứa:
  ```json
  "settings": { "hideDataByDefault": false }
  ```

---

### ❌ Anti-Pattern 2: Khai báo hàm helper outside `self.onInit`
- **Tác hại**: Trong Widget Controller Script của ThingsBoard, `self` là biến cục bộ chỉ tồn tại bên trong `self.onInit` và `self.onDataUpdated`. Nếu viết `function updateHtml() { ... self.ctx ... }` ở cấp ngoài cùng (top-level), khi hàm chạy sẽ nổ `ReferenceError: self is not defined` làm ô Preview xoay vòng màu cam vĩnh viễn.
- **Quy tắc**: Mọi hàm hỗ trợ (`updateHtml`, `hashCode`, `padValue`, `processHtmlPattern`) MUST nằm trọn bên trong closure `self.onInit = function() { ... }`.

---

### ❌ Anti-Pattern 3: Dùng ngoặc chéo ES6 (Template Literals `` ` ``) chèn mã HTML trực tiếp trong JS Tab
- **Tác hại**: Trình biên dịch Widget Editor của ThingsBoard 4.2.0 đánh dấu lỗi cú pháp (chấm đỏ) khi parse chuỗi ngoặc chéo nhiều dòng trong JS tab, làm Widget không biên dịch được.
- **Quy tắc**: 
  - Đưa HTML vào `defaultConfig.settings.cardHtml` dưới dạng JSON String được escape chuẩn.
  - Hoặc đưa HTML vào tab **HTML** (`templateHtml`).

---

### ❌ Anti-Pattern 4: Selector jQuery không có ngữ cảnh `self.ctx.$container`
- **Tác hại**: Sử dụng `$('#inv-title')` thay vì `$('#inv-title', self.ctx.$container)`. Khi kéo 10 Widget cùng loại vào 1 Dashboard, thao tác bấm nút hoặc đổi số liệu ở Widget này sẽ đè chéo sang Widget khác.
- **Quy tắc**: Luôn sử dụng **Scoped Selector**:
  ```javascript
  $('#element-id', self.ctx.$container)
  ```

---

### ❌ Anti-Pattern 5: Gán chuỗi Version Semantic ("1.0.0") vào thuộc tính `version` top-level của JSON
- **Tác hại**: Trong Java Backend của ThingsBoard, thuộc tính `version` thuộc kiểu `java.lang.Long` (dùng cho JPA Optimistic Locking). Nếu truyền chuỗi string `"1.0.0"`, khi Import Widget qua ThingsBoard UI sẽ nổ ngay lỗi `JSON parse error: Cannot deserialize value of type java.lang.Long from String "1.0.0"`.
- **Quy tắc**: Không đặt trường `"version": "1.0.0"` ở top-level của JSON payload. Quản lý số phiên bản ở tên file (`_v1.0.0.json`) hoặc trường `name`.

---

### ❌ Anti-Pattern 6: Bỏ trống `templateHtml` và `templateCss` trong `descriptor`
- **Tác hại**: Khi mở Widget Editor, tab **HTML** và **CSS** bị trắng tinh (dòng 1 rỗng). Container `$container` không được ThingsBoard render khung HTML trước khi gọi `self.onInit`, dẫn đến ô Preview bị trắng trơn không hiển thị gì.
- **Quy tắc**: 
  - Đưa trực tiếp mã HTML/CSS vào `descriptor.templateHtml` và `descriptor.templateCss`.
  - Trong `self.onInit`, luôn có lệnh kiểm tra fallback: nếu `$container` chưa có con (`children().length === 0`), tự động inject `cardHtml` & `cardCss` vào DOM.

---

## ✅ MUST-HAVE PATTERNS (CÁC QUY TẮC BẮT BUỘC KHAI BÁO)

### 1. Cấu hình `typeParameters`
Luôn khai báo trong Widget Descriptor:
```json
"typeParameters": {
    "maxDatasources": 1,
    "singleEntity": true,
    "dataKeysOptional": true,
    "hideDataByDefault": false,
    "hasDataPageSize": false,
    "previewWidth": "360px",
    "previewHeight": "600px"
}
```

### 2. Khai báo `defaultConfig` giả lập (Function Datasources)
Để cửa sổ Preview góc dưới bên phải nhảy số realtime sống động ngay trong Widget Editor:
```json
"defaultConfig": JSON.stringify({
    "datasources": [{
        "type": "function",
        "name": "function",
        "dataKeys": [
            { "name": "active_power", "type": "function", "label": "active_power", "settings": {"hideDataByDefault": false}, "funcBody": "return 50 + Math.random()*20;" }
        ]
    }],
    "settingsDirective": "tb-html-card-widget-settings",
    "settings": {
        "cardHtml": "<div class=\"my-widget\">${active_power} kW</div>",
        "cardCss": ".my-widget { color: green; font-size: 20px; }"
    }
})
```

### 3. Action chuyển State (Popup Detail)
Khi bấm nút chuyển State trong Widget, luôn định dạng tham số `entityId` là Object:
```javascript
var entityId = {
    id: datasource.entityId,
    entityType: datasource.entityType || 'DEVICE'
};
self.ctx.actionsApi.handleWidgetAction(event, descriptor, entityId, entityName, {}, entityLabel);
```

### 4. Cấu hình Settings Form động (`settingsForm` & `settingsDirective: ""`)
Để ThingsBoard 4.x tự động render giao diện Form cài đặt tùy chỉnh cho người dùng (ví dụ: nhập Dòng điện tối đa `maxCurrent`, tên tùy chỉnh `widgetTitle`), **BẮT BUỘC**:
1. Đặt `"settingsDirective": ""` (chuỗi rỗng) trong `descriptor` (KHÔNG dùng `"tb-html-card-widget-settings"` vì nó sẽ chặn hiển thị `settingsForm`).
2. Khai báo mảng `settingsForm` chuẩn Schema:
```json
"settingsDirective": "",
"settingsForm": [
    {
        "id": "maxCurrent",
        "name": "Dòng điện tối đa (Max Current - A)",
        "type": "number",
        "default": 75,
        "required": false,
        "fieldClass": "flex"
    }
]
```
