Hãy viết mã nguồn hoàn chỉnh cho một ThingsBoard Custom Widget (loại HTML/JS widget) dùng để giám sát đồng hồ đo điện 3 pha công nghiệp. Widget này cần được tối ưu hiển thị theo cả 2 giao diện: **Dark Mode** và **Light Mode** (tự động chuyển theo theme của ThingsBoard Dashboard hoặc có tùy chọn chuyển đổi).

Dưới đây là các yêu cầu chi tiết về giao diện và tính năng:

1. **Bố cục & Tính năng cốt lõi (UI/UX):**
   - **Nút chuyển đổi chế độ xem (View Switcher):** Cho phép người dùng bấm chuyển đổi qua lại giữa 2 Tab:
     - **Tab 1: Thông số & Điện năng (Gauge/Progress & Energy Analytics)**
     - **Tab 2: Biểu đồ thời gian thực (Live Time-series Chart)**

2. **Chi tiết Tab 1 (Thông số & Điện năng):**
   - **Thẻ Chỉ số Điện năng Tổng (Lifetime Energy):** Hiển thị nổi bật ở trên cùng để nhân viên vận hành đối chiếu trực tiếp với mặt đồng hồ thực tế tại tủ điện (số tăng tích lũy dạng kWh).
   - **Lưới 3 Pha (Pha A, Pha B, Pha C):** - Mỗi pha hiển thị song song **Dòng điện ($A$)** và **Điện áp tương ứng ($V$)**.
     - Có thanh tiến trình (Progress Bar) thể hiện % tải hiện tại so với dòng định mức (Max Current = 75A), tự động đổi màu cảnh báo (vàng/đỏ) khi tải vượt ngưỡng 70% hoặc 85%.
   - **Panel Tiến độ Tiêu thụ Điện năng (Energy Progress):**
     - **Hôm nay:** Hiển thị số kWh đã dùng từ 0h00 đến hiện tại, kèm thanh Progress Bar thể hiện tỷ lệ đạt được (%) so với tổng số kWh của cả ngày hôm qua, kèm số liệu tổng ngày hôm qua để đối chiếu.
     - **Tuần này:** Hiển thị số kWh từ đầu tuần đến hiện tại, kèm Progress Bar thể hiện % đạt được so với tổng số kWh của cả tuần trước.

3. **Chi tiết Tab 2 (Biểu đồ thời gian thực):**
   - Sử dụng Chart.js để vẽ biểu đồ đường (Line chart) thể hiện diễn biến dòng điện 3 pha ($I_A, I_B, I_C$) theo thời gian.

4. **Yêu cầu kỹ thuật ThingsBoard & Responsive:**
   - Sử dụng cơ chế `self.ctx` để binding dữ liệu telemetry từ thiết bị ThingsBoard (các key: `currentA`, `currentB`, `currentC`, `voltageA`, `voltageB`, `voltageC`, `powerTotal`, `energyTotal`, v.v.).
   - Thiết kế chuẩn Responsive, co giãn linh hoạt trên mọi kích thước màn hình Dashboard.
   - **Đặc biệt:** Cung cấp sẵn cơ chế CSS Variables (`:root`) hoặc class toggle để widget có thể hiển thị hoàn hảo ở cả **Dark Theme** và **Light Theme**.

Hãy cung cấp đầy đủ các phần: HTML Template, CSS Styles (tích hợp cả 2 mode), và JavaScript Controller (xử lý sự kiện, cập nhật dữ liệu real-time).

mã nguồn tham khảo: /home/nxchieu/projects/thingsboard/Ami-agent/thingsboard-widget-agent/prompt/electric_3phase_demo.html