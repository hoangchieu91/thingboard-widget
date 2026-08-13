import json
import argparse
import os

def generate_electric_3phase_widget(theme_mode="dual"):
    """
    theme_mode: 'dual', 'light', 'dark'
    """
    is_light_only = (theme_mode == "light")
    is_dark_only = (theme_mode == "dark")

    # Set alias and widget name based on theme_mode
    if is_light_only:
        alias = "electric_3phase_meter_light"
        name = "Electric 3-Phase Meter (Light Theme)"
        root_class = "tb-electric-3phase-widget light-theme"
        theme_toggle_btn_html = ""
    elif is_dark_only:
        alias = "electric_3phase_meter_dark"
        name = "Electric 3-Phase Meter (Dark Theme)"
        root_class = "tb-electric-3phase-widget dark-theme"
        theme_toggle_btn_html = ""
    else:
        alias = "electric_3phase_meter"
        name = "Electric 3-Phase Meter"
        root_class = "tb-electric-3phase-widget dark-theme"
        theme_toggle_btn_html = """<button class="btn-theme-toggle" id="btn-theme-toggle" title="Chuyển đổi Chế độ Sáng / Tối">
                    <span class="theme-icon">🌙</span> <span class="theme-label">Tối</span>
                </button>"""

    card_html = f"""<div class="{root_class}">
    <div class="widget-container">
        <div class="widget-header">
            <h3 class="widget-title">
                <span class="icon-bolt">⚡</span>
                <span class="title-text">Đồng hồ đo điện 3 Pha & Năng lượng</span>
            </h3>
            <div class="header-actions">
                {theme_toggle_btn_html}
                <div class="view-switcher">
                    <button class="btn-switch active" id="btn-tab-gauge">Thông số & Điện năng</button>
                    <button class="btn-switch" id="btn-tab-chart">Biểu đồ thời gian</button>
                </div>
            </div>
        </div>

        <!-- Thẻ hiển thị số điện tổng tích lũy đối chiếu thực tế -->
        <div class="total-meter-box">
            <div class="total-meter-label">
                <span class="lbl-main">⚡ CHỈ SỐ ĐIỆN NĂNG TỔNG (LIFETIME)</span>
                <span class="lbl-sub">Dùng để đối chiếu trực tiếp với đồng hồ cơ/điện tử tại tủ điện</span>
            </div>
            <div class="total-meter-value" id="val-total-energy">0.0 kWh</div>
        </div>

        <!-- Chế độ 1: Dòng điện, Điện áp và Điện năng tiêu thụ so sánh dạng thanh tiến trình -->
        <div id="view-gauge" class="view-content active">
            <!-- 3 Pha: Dòng điện & Điện áp tương ứng -->
            <div class="grid-3">
                <!-- Pha A -->
                <div class="phase-card phase-a">
                    <div class="phase-title"><span>PHA A</span> <span class="phase-tag-a">L1</span></div>
                    <div class="metric-row">
                        <span>Dòng điện:</span>
                        <strong class="gauge-value" id="val-ia">0.0 A</strong>
                    </div>
                    <div class="metric-row">
                        <span>Điện áp (U<sub>an</sub>):</span>
                        <strong class="voltage-val" id="val-va">0.0 V</strong>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar bar-a" id="bar-ia" style="width: 0%;"></div>
                    </div>
                    <div class="percentage-text">
                        <span class="lbl-max-current">Tải (Max 75A)</span>
                        <span id="pct-ia">0.0%</span>
                    </div>
                </div>

                <!-- Pha B -->
                <div class="phase-card phase-b">
                    <div class="phase-title"><span>PHA B</span> <span class="phase-tag-b">L2</span></div>
                    <div class="metric-row">
                        <span>Dòng điện:</span>
                        <strong class="gauge-value" id="val-ib">0.0 A</strong>
                    </div>
                    <div class="metric-row">
                        <span>Điện áp (U<sub>bn</sub>):</span>
                        <strong class="voltage-val" id="val-vb">0.0 V</strong>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar bar-b" id="bar-ib" style="width: 0%;"></div>
                    </div>
                    <div class="percentage-text">
                        <span class="lbl-max-current">Tải (Max 75A)</span>
                        <span id="pct-ib">0.0%</span>
                    </div>
                </div>

                <!-- Pha C -->
                <div class="phase-card phase-c">
                    <div class="phase-title"><span>PHA C</span> <span class="phase-tag-c">L3</span></div>
                    <div class="metric-row">
                        <span>Dòng điện:</span>
                        <strong class="gauge-value" id="val-ic">0.0 A</strong>
                    </div>
                    <div class="metric-row">
                        <span>Điện áp (U<sub>cn</sub>):</span>
                        <strong class="voltage-val" id="val-vc">0.0 V</strong>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar bar-c" id="bar-ic" style="width: 0%;"></div>
                    </div>
                    <div class="percentage-text">
                        <span class="lbl-max-current">Tải (Max 75A)</span>
                        <span id="pct-ic">0.0%</span>
                    </div>
                </div>
            </div>

            <!-- Panel Quản lý Điện năng tiêu thụ -->
            <div class="energy-panel">
                <div class="energy-title">
                    <span>📊 Tiến độ Tiêu thụ Điện năng</span>
                    <span class="power-summary">Công suất hiện tại: <strong id="val-power">0.0 kW</strong></span>
                </div>

                <div class="energy-grid">
                    <!-- Thẻ Hôm Nay -->
                    <div class="energy-card">
                        <div class="energy-header-row">
                            <span class="energy-label">Hôm nay (0h00 đến hiện tại)</span>
                            <span class="energy-val" id="val-energy-today">0.0 kWh</span>
                        </div>
                        <div class="energy-progress-container">
                            <div class="energy-progress-bar" id="bar-energy-today" style="width: 0%;"></div>
                        </div>
                        <div class="energy-comparison-info">
                            <span>Đã đạt <strong id="pct-energy-today">0.0%</strong> so với tổng cả ngày hôm qua</span>
                            <span>Tổng qua: <strong id="val-energy-yesterday">0.0 kWh</strong></span>
                        </div>
                    </div>

                    <!-- Thẻ Tuần Nay -->
                    <div class="energy-card">
                        <div class="energy-header-row">
                            <span class="energy-label">Tuần này (Đến hiện tại)</span>
                            <span class="energy-val" id="val-energy-week">0.0 kWh</span>
                        </div>
                        <div class="energy-progress-container">
                            <div class="energy-progress-bar" id="bar-energy-week" style="width: 0%;"></div>
                        </div>
                        <div class="energy-comparison-info">
                            <span>Đã đạt <strong id="pct-energy-week">0.0%</strong> so với tổng cả tuần trước</span>
                            <span>Tổng tuần trước: <strong id="val-energy-lastweek">0.0 kWh</strong></span>
                        </div>
                    </div>
                </div>
            </div>

            <div id="alarm-box" style="display: none;" class="alarm-badge">
                <span>⚠️</span> Cảnh báo: Lệch pha dòng điện hoặc điện áp vượt ngưỡng cho phép!
            </div>
        </div>

        <!-- Chế độ 2: Biểu đồ thời gian thực -->
        <div id="view-chart" class="view-content">
            <div class="chart-container">
                <canvas id="currentChart"></canvas>
            </div>
        </div>
    </div>
</div>"""

    if is_light_only:
        card_css = """.tb-electric-3phase-widget {
    --bg-color: #f8fafc;
    --card-bg: #ffffff;
    --card-sub-bg: #f1f5f9;
    --text-primary: #0f172a;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    --accent-blue: #0284c7;
    --phase-a: #dc2626;
    --phase-b: #d97706;
    --phase-c: #2563eb;
    --danger: #dc2626;
    --warning: #d97706;
    --success: #16a34a;
    --progress-bg: #e2e8f0;

    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    overflow-y: auto;
    background-color: var(--bg-color);
    color: var(--text-primary);
    padding: 12px;
}

.widget-container {
    width: 100%;
    background-color: var(--card-bg);
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
    padding: 16px;
    box-sizing: border-box;
    border: 1px solid var(--border-color);
}

.widget-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 10px;
    flex-wrap: wrap;
    gap: 8px;
}

.widget-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--accent-blue);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 10px;
}

.view-switcher {
    display: flex;
    background: var(--card-sub-bg);
    border-radius: 8px;
    padding: 3px;
    border: 1px solid var(--border-color);
}

.btn-switch {
    background: transparent;
    border: none;
    color: var(--text-secondary);
    padding: 5px 12px;
    font-size: 12px;
    cursor: pointer;
    border-radius: 6px;
    transition: all 0.3s ease;
    font-weight: 500;
}

.btn-switch.active {
    background: var(--accent-blue);
    color: #ffffff;
    font-weight: 700;
}

.view-content {
    display: none;
}

.view-content.active {
    display: block;
}

/* Lifetime Energy Card */
.total-meter-box {
    background: linear-gradient(135deg, #ffffff, #f1f5f9);
    border: 1px solid var(--accent-blue);
    border-radius: 10px;
    padding: 10px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    flex-wrap: wrap;
    gap: 8px;
}

.total-meter-label {
    display: flex;
    flex-direction: column;
}

.total-meter-label .lbl-main {
    font-size: 12px;
    color: var(--text-primary);
    font-weight: 700;
    letter-spacing: 0.5px;
}

.total-meter-label .lbl-sub {
    color: var(--accent-blue);
    font-size: 11px;
}

.total-meter-value {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: 1px;
    font-family: 'Courier New', Courier, monospace;
}

/* 3-Phase Grid */
.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 14px;
}

@media (max-width: 600px) {
    .grid-3 {
        grid-template-columns: 1fr;
    }
}

.phase-card {
    background: var(--card-sub-bg);
    padding: 12px;
    border-radius: 10px;
    border: 1px solid var(--border-color);
    position: relative;
    overflow: hidden;
}

.phase-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
}

.phase-card.phase-a::before { background-color: var(--phase-a); }
.phase-card.phase-b::before { background-color: var(--phase-b); }
.phase-card.phase-c::before { background-color: var(--phase-c); }

.phase-title {
    font-size: 12px;
    color: var(--text-secondary);
    margin-bottom: 8px;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
}

.phase-tag-a { color: var(--phase-a); }
.phase-tag-b { color: var(--phase-b); }
.phase-tag-c { color: var(--phase-c); }

.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
    font-size: 12px;
}

.metric-row span:first-child {
    color: var(--text-secondary);
}

.gauge-value {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
}

.voltage-val {
    color: var(--text-primary);
    font-weight: 600;
}

.progress-container {
    background: var(--progress-bg);
    border-radius: 4px;
    height: 6px;
    width: 100%;
    margin: 8px 0 6px 0;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    width: 0%;
    transition: width 0.4s ease, background-color 0.4s ease;
    border-radius: 4px;
}

.progress-bar.bar-a { background-color: var(--phase-a); }
.progress-bar.bar-b { background-color: var(--phase-b); }
.progress-bar.bar-c { background-color: var(--phase-c); }

.percentage-text {
    font-size: 10px;
    color: var(--text-secondary);
    display: flex;
    justify-content: space-between;
}

/* Energy Panel */
.energy-panel {
    background: var(--card-sub-bg);
    border-radius: 10px;
    padding: 14px;
    border: 1px solid var(--border-color);
    margin-bottom: 12px;
}

.energy-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--accent-blue);
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 6px;
}

.power-summary {
    font-size: 11px;
    color: var(--text-secondary);
    font-weight: 500;
}

.power-summary strong {
    color: var(--text-primary);
}

.energy-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 12px;
}

.energy-card {
    background: var(--card-bg);
    padding: 12px 14px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

.energy-header-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
}

.energy-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-primary);
}

.energy-val {
    font-size: 17px;
    font-weight: 700;
    color: var(--accent-blue);
}

.energy-progress-container {
    background: var(--progress-bg);
    border-radius: 6px;
    height: 8px;
    width: 100%;
    margin: 8px 0 6px 0;
    overflow: hidden;
}

.energy-progress-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, var(--accent-blue), #818cf8);
    border-radius: 6px;
    transition: width 0.4s ease;
}

.energy-comparison-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: var(--text-secondary);
}

.energy-comparison-info strong {
    color: var(--text-primary);
}

.chart-container {
    position: relative;
    height: 250px;
    width: 100%;
}

.alarm-badge {
    background: rgba(220, 38, 38, 0.1);
    color: var(--danger);
    border: 1px solid var(--danger);
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}"""
    elif is_dark_only:
        card_css = """.tb-electric-3phase-widget {
    --bg-color: #0f172a;
    --card-bg: #1e293b;
    --card-sub-bg: #0f172a;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --border-color: #334155;
    --accent-blue: #38bdf8;
    --phase-a: #ef4444;
    --phase-b: #eab308;
    --phase-c: #3b82f6;
    --danger: #ef4444;
    --warning: #f59e0b;
    --success: #10b981;
    --progress-bg: #334155;

    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    overflow-y: auto;
    background-color: var(--bg-color);
    color: var(--text-primary);
    padding: 12px;
}

.widget-container {
    width: 100%;
    background-color: var(--card-bg);
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    padding: 16px;
    box-sizing: border-box;
    border: 1px solid var(--border-color);
}

.widget-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 10px;
    flex-wrap: wrap;
    gap: 8px;
}

.widget-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--accent-blue);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 10px;
}

.view-switcher {
    display: flex;
    background: var(--card-sub-bg);
    border-radius: 8px;
    padding: 3px;
    border: 1px solid var(--border-color);
}

.btn-switch {
    background: transparent;
    border: none;
    color: var(--text-secondary);
    padding: 5px 12px;
    font-size: 12px;
    cursor: pointer;
    border-radius: 6px;
    transition: all 0.3s ease;
    font-weight: 500;
}

.btn-switch.active {
    background: var(--accent-blue);
    color: #ffffff;
    font-weight: 700;
}

.view-content {
    display: none;
}

.view-content.active {
    display: block;
}

/* Lifetime Energy Card */
.total-meter-box {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid var(--accent-blue);
    border-radius: 10px;
    padding: 10px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    flex-wrap: wrap;
    gap: 8px;
}

.total-meter-label {
    display: flex;
    flex-direction: column;
}

.total-meter-label .lbl-main {
    font-size: 12px;
    color: var(--text-primary);
    font-weight: 700;
    letter-spacing: 0.5px;
}

.total-meter-label .lbl-sub {
    color: var(--accent-blue);
    font-size: 11px;
}

.total-meter-value {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: 1px;
    font-family: 'Courier New', Courier, monospace;
}

/* 3-Phase Grid */
.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 14px;
}

@media (max-width: 600px) {
    .grid-3 {
        grid-template-columns: 1fr;
    }
}

.phase-card {
    background: var(--card-sub-bg);
    padding: 12px;
    border-radius: 10px;
    border: 1px solid var(--border-color);
    position: relative;
    overflow: hidden;
}

.phase-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
}

.phase-card.phase-a::before { background-color: var(--phase-a); }
.phase-card.phase-b::before { background-color: var(--phase-b); }
.phase-card.phase-c::before { background-color: var(--phase-c); }

.phase-title {
    font-size: 12px;
    color: var(--text-secondary);
    margin-bottom: 8px;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
}

.phase-tag-a { color: var(--phase-a); }
.phase-tag-b { color: var(--phase-b); }
.phase-tag-c { color: var(--phase-c); }

.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
    font-size: 12px;
}

.metric-row span:first-child {
    color: var(--text-secondary);
}

.gauge-value {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
}

.voltage-val {
    color: var(--text-primary);
    font-weight: 600;
}

.progress-container {
    background: var(--progress-bg);
    border-radius: 4px;
    height: 6px;
    width: 100%;
    margin: 8px 0 6px 0;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    width: 0%;
    transition: width 0.4s ease, background-color 0.4s ease;
    border-radius: 4px;
}

.progress-bar.bar-a { background-color: var(--phase-a); }
.progress-bar.bar-b { background-color: var(--phase-b); }
.progress-bar.bar-c { background-color: var(--phase-c); }

.percentage-text {
    font-size: 10px;
    color: var(--text-secondary);
    display: flex;
    justify-content: space-between;
}

/* Energy Panel */
.energy-panel {
    background: var(--card-sub-bg);
    border-radius: 10px;
    padding: 14px;
    border: 1px solid var(--border-color);
    margin-bottom: 12px;
}

.energy-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--accent-blue);
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 6px;
}

.power-summary {
    font-size: 11px;
    color: var(--text-secondary);
    font-weight: 500;
}

.power-summary strong {
    color: var(--text-primary);
}

.energy-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 12px;
}

.energy-card {
    background: var(--card-bg);
    padding: 12px 14px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

.energy-header-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
}

.energy-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-primary);
}

.energy-val {
    font-size: 17px;
    font-weight: 700;
    color: var(--accent-blue);
}

.energy-progress-container {
    background: var(--progress-bg);
    border-radius: 6px;
    height: 8px;
    width: 100%;
    margin: 8px 0 6px 0;
    overflow: hidden;
}

.energy-progress-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, var(--accent-blue), #818cf8);
    border-radius: 6px;
    transition: width 0.4s ease;
}

.energy-comparison-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: var(--text-secondary);
}

.energy-comparison-info strong {
    color: var(--text-primary);
}

.chart-container {
    position: relative;
    height: 250px;
    width: 100%;
}

.alarm-badge {
    background: rgba(239, 68, 68, 0.15);
    color: var(--danger);
    border: 1px solid var(--danger);
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}"""
    else:
        # Dual Theme CSS
        card_css = """.tb-electric-3phase-widget {
    --bg-color: #0f172a;
    --card-bg: #1e293b;
    --card-sub-bg: #0f172a;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --border-color: #334155;
    --accent-blue: #38bdf8;
    --phase-a: #ef4444;
    --phase-b: #eab308;
    --phase-c: #3b82f6;
    --danger: #ef4444;
    --warning: #f59e0b;
    --success: #10b981;
    --progress-bg: #334155;

    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    overflow-y: auto;
    background-color: var(--bg-color);
    color: var(--text-primary);
    padding: 12px;
}

.tb-electric-3phase-widget.light-theme {
    --bg-color: #f8fafc;
    --card-bg: #ffffff;
    --card-sub-bg: #f1f5f9;
    --text-primary: #0f172a;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    --accent-blue: #0284c7;
    --phase-a: #dc2626;
    --phase-b: #d97706;
    --phase-c: #2563eb;
    --danger: #dc2626;
    --warning: #d97706;
    --success: #16a34a;
    --progress-bg: #e2e8f0;
}

.widget-container {
    width: 100%;
    background-color: var(--card-bg);
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    padding: 16px;
    box-sizing: border-box;
    border: 1px solid var(--border-color);
    transition: background-color 0.3s ease, border-color 0.3s ease;
}

.widget-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 10px;
    flex-wrap: wrap;
    gap: 8px;
}

.widget-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--accent-blue);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 10px;
}

.btn-theme-toggle {
    background: var(--card-sub-bg);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 5px 10px;
    font-size: 12px;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.btn-theme-toggle:hover {
    border-color: var(--accent-blue);
}

.view-switcher {
    display: flex;
    background: var(--card-sub-bg);
    border-radius: 8px;
    padding: 3px;
    border: 1px solid var(--border-color);
}

.btn-switch {
    background: transparent;
    border: none;
    color: var(--text-secondary);
    padding: 5px 12px;
    font-size: 12px;
    cursor: pointer;
    border-radius: 6px;
    transition: all 0.3s ease;
    font-weight: 500;
}

.btn-switch.active {
    background: var(--accent-blue);
    color: #ffffff;
    font-weight: 700;
}

.view-content {
    display: none;
}

.view-content.active {
    display: block;
}

/* Lifetime Energy Card */
.total-meter-box {
    background: linear-gradient(135deg, var(--card-bg), var(--card-sub-bg));
    border: 1px solid var(--accent-blue);
    border-radius: 10px;
    padding: 10px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    flex-wrap: wrap;
    gap: 8px;
}

.total-meter-label {
    display: flex;
    flex-direction: column;
}

.total-meter-label .lbl-main {
    font-size: 12px;
    color: var(--text-primary);
    font-weight: 700;
    letter-spacing: 0.5px;
}

.total-meter-label .lbl-sub {
    color: var(--accent-blue);
    font-size: 11px;
}

.total-meter-value {
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: 1px;
    font-family: 'Courier New', Courier, monospace;
}

/* 3-Phase Grid */
.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 14px;
}

@media (max-width: 600px) {
    .grid-3 {
        grid-template-columns: 1fr;
    }
}

.phase-card {
    background: var(--card-sub-bg);
    padding: 12px;
    border-radius: 10px;
    border: 1px solid var(--border-color);
    position: relative;
    overflow: hidden;
}

.phase-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
}

.phase-card.phase-a::before { background-color: var(--phase-a); }
.phase-card.phase-b::before { background-color: var(--phase-b); }
.phase-card.phase-c::before { background-color: var(--phase-c); }

.phase-title {
    font-size: 12px;
    color: var(--text-secondary);
    margin-bottom: 8px;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
}

.phase-tag-a { color: var(--phase-a); }
.phase-tag-b { color: var(--phase-b); }
.phase-tag-c { color: var(--phase-c); }

.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
    font-size: 12px;
}

.metric-row span:first-child {
    color: var(--text-secondary);
}

.gauge-value {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
}

.voltage-val {
    color: var(--text-primary);
    font-weight: 600;
}

.progress-container {
    background: var(--progress-bg);
    border-radius: 4px;
    height: 6px;
    width: 100%;
    margin: 8px 0 6px 0;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    width: 0%;
    transition: width 0.4s ease, background-color 0.4s ease;
    border-radius: 4px;
}

.progress-bar.bar-a { background-color: var(--phase-a); }
.progress-bar.bar-b { background-color: var(--phase-b); }
.progress-bar.bar-c { background-color: var(--phase-c); }

.percentage-text {
    font-size: 10px;
    color: var(--text-secondary);
    display: flex;
    justify-content: space-between;
}

/* Energy Panel */
.energy-panel {
    background: var(--card-sub-bg);
    border-radius: 10px;
    padding: 14px;
    border: 1px solid var(--border-color);
    margin-bottom: 12px;
}

.energy-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--accent-blue);
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 6px;
}

.power-summary {
    font-size: 11px;
    color: var(--text-secondary);
    font-weight: 500;
}

.power-summary strong {
    color: var(--text-primary);
}

.energy-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 12px;
}

.energy-card {
    background: var(--card-bg);
    padding: 12px 14px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

.energy-header-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
}

.energy-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-primary);
}

.energy-val {
    font-size: 17px;
    font-weight: 700;
    color: var(--accent-blue);
}

.energy-progress-container {
    background: var(--progress-bg);
    border-radius: 6px;
    height: 8px;
    width: 100%;
    margin: 8px 0 6px 0;
    overflow: hidden;
}

.energy-progress-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, var(--accent-blue), #818cf8);
    border-radius: 6px;
    transition: width 0.4s ease;
}

.energy-comparison-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: var(--text-secondary);
}

.energy-comparison-info strong {
    color: var(--text-primary);
}

.chart-container {
    position: relative;
    height: 250px;
    width: 100%;
}

.alarm-badge {
    background: rgba(239, 68, 68, 0.15);
    color: var(--danger);
    border: 1px solid var(--danger);
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}"""

    is_dark_flag_init = "false" if is_light_only else "true"
    style_id = f"tb-{alias}-style"

    controller_js = f"""self.onInit = function() {{
    var $container = self.ctx.$container;

    // Populate HTML & CSS into container if not rendered automatically by ThingsBoard
    var htmlContent = (self.ctx.settings && self.ctx.settings.cardHtml) || self.ctx.templateHtml || '';
    var cssContent = (self.ctx.settings && self.ctx.settings.cardCss) || self.ctx.templateCss || '';

    if ($container.children().length === 0 && htmlContent) {{
        $container.html(htmlContent);
    }}
    if (cssContent && $('#{style_id}', $container).length === 0) {{
        $container.append('<style id="{style_id}">' + cssContent + '</style>');
    }}

    var currentChart = null;
    var isDarkTheme = {is_dark_flag_init};
    var chartHistoryData = {{
        labels: [],
        ia: [],
        ib: [],
        ic: []
    }};

    function formatNumber(num, decimals) {{
        return num.toFixed(decimals);
    }}

    function normalizeKey(k) {{
        if (!k) return '';
        return String(k).toLowerCase().replace(/[^a-z0-9]/g, '');
    }}

    function updateWidgetTitle() {{
        var title = '';
        if (self.ctx.defaultSubscription && self.ctx.defaultSubscription.datasources.length > 0) {{
            var ds = self.ctx.defaultSubscription.datasources[0];
            if (ds.type !== 'function') {{
                title = ds.entityLabel || ds.entityName || '';
            }}
        }}
        if (!title && self.ctx.settings && self.ctx.settings.widgetTitle) {{
            title = self.ctx.settings.widgetTitle;
        }}
        if (!title) {{
            title = 'Đồng hồ đo điện 3 Pha & Năng lượng';
        }}
        $('.title-text', $container).text(title);
    }}

    function toggleTheme() {{
        isDarkTheme = !isDarkTheme;
        var widgetEl = $('.tb-electric-3phase-widget', $container);
        var toggleBtn = $('#btn-theme-toggle', $container);
        
        if (isDarkTheme) {{
            widgetEl.removeClass('light-theme').addClass('dark-theme');
            toggleBtn.html('<span class="theme-icon">🌙</span> <span class="theme-label">Tối</span>');
        }} else {{
            widgetEl.removeClass('dark-theme').addClass('light-theme');
            toggleBtn.html('<span class="theme-icon">☀️</span> <span class="theme-label">Sáng</span>');
        }}

        if (currentChart) {{
            updateChartTheme();
        }}
    }}

    function switchView(type) {{
        $('.btn-switch', $container).removeClass('active');
        $('.view-content', $container).removeClass('active');

        if (type === 'gauge') {{
            $('#view-gauge', $container).addClass('active');
            $('#btn-tab-gauge', $container).addClass('active');
        }} else {{
            $('#view-chart', $container).addClass('active');
            $('#btn-tab-chart', $container).addClass('active');
            if (!currentChart) {{
                initChart();
            }} else {{
                currentChart.update();
            }}
        }}
    }}

    function updatePhaseCard(phaseId, value, maxCurrent, defaultColor) {{
        var valEl = $('#val-' + phaseId, $container);
        var barEl = $('#bar-' + phaseId, $container);
        var pctEl = $('#pct-' + phaseId, $container);

        if (value === null || value === undefined || isNaN(value)) {{
            valEl.text('N/A');
            barEl.css('width', '0%');
            pctEl.text('N/A');
            return;
        }}

        valEl.text(formatNumber(value, 1) + ' A');
        var percent = (value / maxCurrent) * 100;
        var displayPercent = Math.min(percent, 100).toFixed(1);

        barEl.css('width', displayPercent + '%');
        pctEl.text(displayPercent + '%');

        if (percent > 85) {{
            barEl.css('background-color', 'var(--danger)');
        }} else if (percent > 70) {{
            barEl.css('background-color', 'var(--warning)');
        }} else {{
            barEl.css('background-color', defaultColor);
        }}
    }}

    function updateTelemetryData() {{
        updateWidgetTitle();

        var isFunctionPreview = false;
        if (self.ctx.defaultSubscription && self.ctx.defaultSubscription.datasources.length > 0) {{
            if (self.ctx.defaultSubscription.datasources[0].type === 'function') {{
                isFunctionPreview = true;
            }}
        }}

        var dataMap = {{}};
        if (self.ctx.data && self.ctx.data.length > 0) {{
            for (var i = 0; i < self.ctx.data.length; i++) {{
                var ds = self.ctx.data[i];
                if (ds && ds.dataKey && ds.data && ds.data.length > 0) {{
                    var latestVal = ds.data[ds.data.length - 1][1];
                    if (ds.dataKey.name) dataMap[normalizeKey(ds.dataKey.name)] = latestVal;
                    if (ds.dataKey.label) dataMap[normalizeKey(ds.dataKey.label)] = latestVal;
                }}
            }}
        }}

        function renderTelemetryMap() {{
            function getVal(aliasList, defaultPreviewVal) {{
                for (var i = 0; i < aliasList.length; i++) {{
                    var norm = normalizeKey(aliasList[i]);
                    if (dataMap.hasOwnProperty(norm) && dataMap[norm] !== undefined && dataMap[norm] !== null && dataMap[norm] !== '') {{
                        var num = parseFloat(dataMap[norm]);
                        return isNaN(num) ? dataMap[norm] : num;
                    }}
                }}
                if (!isFunctionPreview) {{
                    return null;
                }}
                return defaultPreviewVal;
            }}

            // Dynamic Max Current resolution: Telemetry -> Attribute -> Widget Settings -> Auto Scale -> Default (75.0A)
            var maxCurrentConfig = (self.ctx.settings && self.ctx.settings.maxCurrent) ? parseFloat(self.ctx.settings.maxCurrent) : 75.0;
            var maxCurrentVal = getVal(['maxCurrent', 'ratedCurrent', 'max_current', 'rated_current', 'imax', 'i_max'], maxCurrentConfig);
            var maxCurrent = (maxCurrentVal !== null && maxCurrentVal > 0) ? maxCurrentVal : maxCurrentConfig;

            var ia = getVal(['currentA', 'current_a', 'ia', 'i_a', 'i_phase_a', 'l1_current', 'current_l1', 'currentl1', 'i1', 'phase_a_current', 'a_current'], 45.2);
            var ib = getVal(['currentB', 'current_b', 'ib', 'i_b', 'i_phase_b', 'l2_current', 'current_l2', 'currentl2', 'i2', 'phase_b_current', 'b_current'], 44.8);
            var ic = getVal(['currentC', 'current_c', 'ic', 'i_c', 'i_phase_c', 'l3_current', 'current_l3', 'currentl3', 'i3', 'phase_c_current', 'c_current'], 46.1);

            // Auto-scale maxCurrent if measured current exceeds configured max
            var maxI = Math.max(ia || 0, ib || 0, ic || 0);
            if (maxI > maxCurrent) {{
                maxCurrent = Math.ceil(maxI * 1.2);
            }}

            $('.lbl-max-current', $container).text('Tải (Max ' + formatNumber(maxCurrent, 0) + 'A)');

            var va = getVal(['voltageA', 'voltage_a', 'va', 'v_a', 'uan', 'u_an', 'l1_voltage', 'voltage_l1', 'voltagel1', 'v1', 'phase_a_voltage', 'ua'], 220.1);
            var vb = getVal(['voltageB', 'voltage_b', 'vb', 'v_b', 'ubn', 'u_bn', 'l2_voltage', 'voltage_l2', 'voltagel2', 'v2', 'phase_b_voltage', 'ub'], 220.5);
            var vc = getVal(['voltageC', 'voltage_c', 'vc', 'v_c', 'ucn', 'u_cn', 'l3_voltage', 'voltage_l3', 'voltagel3', 'v3', 'phase_c_voltage', 'uc'], 220.8);

            var powerTotal = getVal(['powerTotal', 'power_total', 'activePower', 'active_power', 'Power_Active_Total', 'power_active_total', 'poweractivetotal', 'active_power_total', 'activepowertotal', 'ptotal', 'p_total', 'kw', 'power', 'p', 'w', 'total_power', 'totalpower', 'activepower', 'total_active_power'], null);
            
            // Auto-calculate 3-Phase active power (kW) if not explicitly provided by device telemetry
            if (powerTotal === null && va !== null && vb !== null && vc !== null && ia !== null && ib !== null && ic !== null) {{
                powerTotal = parseFloat((((va * ia + vb * ib + vc * ic) * 0.92) / 1000).toFixed(1));
            }} else if (powerTotal === null && ia !== null && ib !== null && ic !== null) {{
                powerTotal = parseFloat((((220 * (ia + ib + ic)) * 0.92) / 1000).toFixed(1));
            }}

            var energyTotal = getVal(['energyTotal', 'energy_total', 'totalEnergy', 'total_energy', 'total_kwh', 'totalkwh', 'kwh', 'energy', 'active_energy', 'etotal', 'e_total', 'energy_lifetime'], null);

            // Backend-Driven Energy Progress: Rely strictly on Backend Calculated Fields / Rule Engine telemetry
            var energyToday = getVal(['energyToday', 'energy_today', 'todayEnergy', 'today_energy', 'dailyEnergy', 'daily_energy', 'today_kwh', 'todaykwh', 'e_today', 'etoday', 'kwh_today', 'daily_kwh'], null);
            var energyYesterday = getVal(['energyYesterday', 'energy_yesterday', 'yesterdayEnergy', 'yesterday_energy', 'yesterday_kwh', 'yesterdaykwh', 'e_yesterday', 'eyesterday', 'kwh_yesterday'], null);
            var energyWeek = getVal(['energyWeek', 'energy_week', 'weekEnergy', 'week_energy', 'weekly_energy', 'weeklyenergy', 'week_kwh', 'e_week', 'eweek'], null);
            var energyLastWeek = getVal(['energyLastWeek', 'energy_lastweek', 'lastweekEnergy', 'lastweek_energy', 'last_week_energy', 'lastweek_kwh', 'e_lastweek'], null);

            // Render Values
            $('#val-total-energy', $container).text(energyTotal !== null ? formatNumber(energyTotal, 1) + ' kWh' : 'N/A');

            updatePhaseCard('ia', ia, maxCurrent, 'var(--phase-a)');
            updatePhaseCard('ib', ib, maxCurrent, 'var(--phase-b)');
            updatePhaseCard('ic', ic, maxCurrent, 'var(--phase-c)');

            $('#val-va', $container).text(va !== null ? formatNumber(va, 1) + ' V' : 'N/A');
            $('#val-vb', $container).text(vb !== null ? formatNumber(vb, 1) + ' V' : 'N/A');
            $('#val-vc', $container).text(vc !== null ? formatNumber(vc, 1) + ' V' : 'N/A');

            $('#val-power', $container).text(powerTotal !== null ? formatNumber(powerTotal, 1) + ' kW' : 'N/A');

            // Energy Today
            $('#val-energy-today', $container).text(energyToday !== null ? formatNumber(energyToday, 1) + ' kWh' : 'N/A');
            $('#val-energy-yesterday', $container).text(energyYesterday !== null ? formatNumber(energyYesterday, 1) + ' kWh' : 'N/A');
            var pctToday = (energyToday !== null && energyYesterday !== null && energyYesterday > 0) ? ((energyToday / energyYesterday) * 100).toFixed(1) : '0.0';
            $('#bar-energy-today', $container).css('width', (pctToday !== '0.0' ? Math.min(parseFloat(pctToday), 100) : 0) + '%');
            $('#pct-energy-today', $container).text(energyToday !== null && energyYesterday !== null ? pctToday + '%' : 'N/A');

            // Energy Week
            $('#val-energy-week', $container).text(energyWeek !== null ? formatNumber(energyWeek, 1) + ' kWh' : 'N/A');
            $('#val-energy-lastweek', $container).text(energyLastWeek !== null ? formatNumber(energyLastWeek, 1) + ' kWh' : 'N/A');
            var pctWeek = (energyWeek !== null && energyLastWeek !== null && energyLastWeek > 0) ? ((energyWeek / energyLastWeek) * 100).toFixed(1) : '0.0';
            $('#bar-energy-week', $container).css('width', (pctWeek !== '0.0' ? Math.min(parseFloat(pctWeek), 100) : 0) + '%');
            $('#pct-energy-week', $container).text(energyWeek !== null && energyLastWeek !== null ? pctWeek + '%' : 'N/A');

            // Backend-Driven Alarm Resolution: Only display alarm box when Backend Rule Engine / Gateway sends an explicit alarm tag
            var alarmMsg = getVal(['alarm_message', 'alarmMessage', 'alarm_text', 'alarmText', 'warning_message', 'warningMessage', 'alarm_status', 'alarmStatus', 'alarm', 'warning', 'has_alarm'], null);
            var isAlarmActive = false;
            var alarmDisplayText = '';

            if (alarmMsg !== null && alarmMsg !== false && alarmMsg !== 0 && alarmMsg !== '0' && alarmMsg !== 'OK' && alarmMsg !== 'NORMAL' && alarmMsg !== 'false') {{
                isAlarmActive = true;
                alarmDisplayText = (typeof alarmMsg === 'string' && alarmMsg.length > 1) ? alarmMsg : 'Cảnh báo hệ thống từ Backend!';
            }}

            if (isAlarmActive) {{
                $('.alarm-text', $container).text('⚠️ ' + alarmDisplayText);
                $('#alarm-box', $container).css('display', 'flex');
            }} else {{
                $('#alarm-box', $container).css('display', 'none');
            }}

            // Add to Chart Data buffer
            if (ia !== null || ib !== null || ic !== null) {{
                var timeLabel = new Date().toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit', second: '2-digit' }});
                chartHistoryData.labels.push(timeLabel);
                chartHistoryData.ia.push(ia !== null ? ia : 0);
                chartHistoryData.ib.push(ib !== null ? ib : 0);
                chartHistoryData.ic.push(ic !== null ? ic : 0);

                if (chartHistoryData.labels.length > 15) {{
                    chartHistoryData.labels.shift();
                    chartHistoryData.ia.shift();
                    chartHistoryData.ib.shift();
                    chartHistoryData.ic.shift();
                }}

                if (currentChart) {{
                    currentChart.options.scales.y.suggestedMax = maxCurrent;
                    currentChart.data.labels = chartHistoryData.labels;
                    currentChart.data.datasets[0].data = chartHistoryData.ia;
                    currentChart.data.datasets[1].data = chartHistoryData.ib;
                    currentChart.data.datasets[2].data = chartHistoryData.ic;
                    currentChart.update('none');
                }}
            }}
        }}

        renderTelemetryMap();

        // REST API Fallback: Automatically query ALL latest telemetry keys directly from ThingsBoard server
        if (!isFunctionPreview && self.ctx.defaultSubscription && self.ctx.defaultSubscription.datasources.length > 0) {{
            var ds0 = self.ctx.defaultSubscription.datasources[0];
            if (ds0.entityId && ds0.entityType) {{
                var http = self.ctx.http || (self.ctx.$scope && self.ctx.$scope.$injector ? self.ctx.$scope.$injector.get('$http') : null);
                if (http && !self.ctx._fetchedLatestApi) {{
                    self.ctx._fetchedLatestApi = true;
                    var apiUrl = '/api/plugins/telemetry/' + ds0.entityType + '/' + ds0.entityId + '/values/timeseries';
                    function handleLatestData(latestObj) {{
                        if (latestObj) {{
                            for (var key in latestObj) {{
                                if (latestObj.hasOwnProperty(key)) {{
                                    var arr = latestObj[key];
                                    if (arr && arr.length > 0) {{
                                        var val = arr[arr.length - 1].value;
                                        dataMap[normalizeKey(key)] = val;
                                    }}
                                }}
                            }}
                            renderTelemetryMap();
                        }}
                    }}

                    var httpOpts = {{ headers: {{ ignoreErrors: 'true' }} }};
                    var req = http.get(apiUrl, httpOpts);
                    if (req && typeof req.subscribe === 'function') {{
                        req.subscribe(function(res) {{
                            handleLatestData(res && res.data ? res.data : res);
                        }}, function(e) {{}});
                    }} else if (req && typeof req.then === 'function') {{
                        req.then(function(res) {{
                            handleLatestData(res && res.data ? res.data : res);
                        }}).catch(function(e) {{}});
                    }}
                }}
            }}
        }}
    }}

    function initChart() {{
        var canvas = $('#currentChart', $container)[0];
        if (!canvas) return;

        if (typeof Chart === 'undefined') {{
            // Load Chart.js dynamically if not present
            var script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
            script.onload = function() {{
                createChartInstance(canvas);
            }};
            document.head.appendChild(script);
        }} else {{
            createChartInstance(canvas);
        }}
    }}

    function createChartInstance(canvas) {{
        var ctx = canvas.getContext('2d');
        var gridColor = isDarkTheme ? '#334155' : '#e2e8f0';
        var textColor = isDarkTheme ? '#94a3b8' : '#64748b';
        var maxCurrentConfig = (self.ctx.settings && self.ctx.settings.maxCurrent) ? parseFloat(self.ctx.settings.maxCurrent) : 75.0;

        currentChart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: chartHistoryData.labels,
                datasets: [
                    {{ label: 'Pha A (A)', data: chartHistoryData.ia, borderColor: isDarkTheme ? '#ef4444' : '#dc2626', backgroundColor: 'rgba(239, 68, 68, 0.1)', borderWidth: 2, tension: 0.3, fill: true }},
                    {{ label: 'Pha B (A)', data: chartHistoryData.ib, borderColor: isDarkTheme ? '#eab308' : '#d97706', backgroundColor: 'rgba(234, 179, 8, 0.1)', borderWidth: 2, tension: 0.3, fill: true }},
                    {{ label: 'Pha C (A)', data: chartHistoryData.ic, borderColor: isDarkTheme ? '#3b82f6' : '#2563eb', backgroundColor: 'rgba(59, 130, 246, 0.1)', borderWidth: 2, tension: 0.3, fill: true }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ labels: {{ color: isDarkTheme ? '#f8fafc' : '#0f172a', boxWidth: 12, font: {{ size: 12 }} }} }}
                }},
                scales: {{
                    x: {{ ticks: {{ color: textColor, font: {{ size: 10 }} }}, grid: {{ color: gridColor }} }},
                    y: {{ ticks: {{ color: textColor, font: {{ size: 10 }} }}, grid: {{ color: gridColor }}, suggestedMax: maxCurrentConfig }}
                }}
            }}
        }});
    }}

    function updateChartTheme() {{
        if (!currentChart) return;
        var gridColor = isDarkTheme ? '#334155' : '#e2e8f0';
        var textColor = isDarkTheme ? '#94a3b8' : '#64748b';
        var legendColor = isDarkTheme ? '#f8fafc' : '#0f172a';

        currentChart.options.plugins.legend.labels.color = legendColor;
        currentChart.options.scales.x.ticks.color = textColor;
        currentChart.options.scales.x.grid.color = gridColor;
        currentChart.options.scales.y.ticks.color = textColor;
        currentChart.options.scales.y.grid.color = gridColor;
        currentChart.update();
    }}

    // Event listeners
    $('#btn-theme-toggle', $container).on('click', function() {{
        toggleTheme();
    }});

    $('#btn-tab-gauge', $container).on('click', function() {{
        switchView('gauge');
    }});

    $('#btn-tab-chart', $container).on('click', function() {{
        switchView('chart');
    }});

    // Initial update
    updateTelemetryData();
    self.updateTelemetryData = updateTelemetryData;
}};

self.onDataUpdated = function() {{
    if (typeof self.updateTelemetryData === 'function') {{
        self.updateTelemetryData();
    }}
}};

self.typeParameters = function() {{
    return {{
        maxDatasources: 1,
        singleEntity: true,
        dataKeysOptional: true,
        hideDataByDefault: false,
        hasDataPageSize: false
    }};
}};"""

    # 13 Function DataKeys with settings: { hideDataByDefault: False }
    data_keys_config = [
        {"name": "maxCurrent", "type": "function", "label": "maxCurrent", "settings": {"hideDataByDefault": False}, "funcBody": "return 75.0;"},
        {"name": "Current_A", "type": "function", "label": "Current_A", "settings": {"hideDataByDefault": False}, "funcBody": "return (44 + Math.random()*3).toFixed(1);"},
        {"name": "Current_B", "type": "function", "label": "Current_B", "settings": {"hideDataByDefault": False}, "funcBody": "return (43.5 + Math.random()*3).toFixed(1);"},
        {"name": "Current_C", "type": "function", "label": "Current_C", "settings": {"hideDataByDefault": False}, "funcBody": "return (45 + Math.random()*3).toFixed(1);"},
        {"name": "currentA", "type": "function", "label": "currentA", "settings": {"hideDataByDefault": False}, "funcBody": "return (44 + Math.random()*3).toFixed(1);"},
        {"name": "currentB", "type": "function", "label": "currentB", "settings": {"hideDataByDefault": False}, "funcBody": "return (43.5 + Math.random()*3).toFixed(1);"},
        {"name": "currentC", "type": "function", "label": "currentC", "settings": {"hideDataByDefault": False}, "funcBody": "return (45 + Math.random()*3).toFixed(1);"},
        {"name": "voltageA", "type": "function", "label": "voltageA", "settings": {"hideDataByDefault": False}, "funcBody": "return (220 + Math.random()*2).toFixed(1);"},
        {"name": "voltageB", "type": "function", "label": "voltageB", "settings": {"hideDataByDefault": False}, "funcBody": "return (220.5 + Math.random()*2).toFixed(1);"},
        {"name": "voltageC", "type": "function", "label": "voltageC", "settings": {"hideDataByDefault": False}, "funcBody": "return (221 + Math.random()*2).toFixed(1);"},
        {"name": "powerTotal", "type": "function", "label": "powerTotal", "settings": {"hideDataByDefault": False}, "funcBody": "return (29 + Math.random()*2).toFixed(1);"},
        {"name": "energyTotal", "type": "function", "label": "energyTotal", "settings": {"hideDataByDefault": False}, "funcBody": "return (124582.6 + Math.random()*1).toFixed(1);"},
        {"name": "energyToday", "type": "function", "label": "energyToday", "settings": {"hideDataByDefault": False}, "funcBody": "return (342.5 + Math.random()*2).toFixed(1);"},
        {"name": "energyYesterday", "type": "function", "label": "energyYesterday", "settings": {"hideDataByDefault": False}, "funcBody": "return (391.2).toFixed(1);"},
        {"name": "energyWeek", "type": "function", "label": "energyWeek", "settings": {"hideDataByDefault": False}, "funcBody": "return (2350.0 + Math.random()*10).toFixed(1);"},
        {"name": "energyLastWeek", "type": "function", "label": "energyLastWeek", "settings": {"hideDataByDefault": False}, "funcBody": "return (3150.0).toFixed(1);"}
    ]

    default_config = {
        "datasources": [
            {
                "type": "function",
                "name": "function",
                "dataKeys": data_keys_config
            }
        ],
        "showTitle": False,
        "backgroundColor": "rgba(0, 0, 0, 0)",
        "color": "rgba(0, 0, 0, 0.87)",
        "padding": "0px",
        "settings": {
            "cardCss": card_css,
            "cardHtml": card_html,
            "maxCurrent": 75.0,
            "widgetTitle": name
        },
        "title": name,
        "dropShadow": False,
        "enableFullscreen": True
    }

    widget_json = {
        "alias": alias,
        "name": name,
        "descriptor": {
            "type": "latest",
            "sizeX": 8,
            "sizeY": 7,
            "resources": [
                {
                    "url": "https://cdn.jsdelivr.net/npm/chart.js"
                }
            ],
            "templateHtml": card_html,
            "templateCss": card_css,
            "controllerScript": controller_js,
            "settingsDirective": "",
            "settingsForm": [
                {
                    "id": "maxCurrent",
                    "name": "Dòng điện tối đa (Max Current - A)",
                    "type": "number",
                    "default": 75,
                    "required": False,
                    "fieldClass": "flex"
                },
                {
                    "id": "widgetTitle",
                    "name": "Tên đồng hồ tùy chỉnh (Tùy chọn)",
                    "type": "text",
                    "default": "",
                    "required": False,
                    "fieldClass": "flex"
                }
            ],
            "defaultConfig": json.dumps(default_config),
            "typeParameters": {
                "maxDatasources": 1,
                "singleEntity": True,
                "dataKeysOptional": True,
                "hideDataByDefault": False,
                "hasDataPageSize": False
            }
        }
    }
    return widget_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Electric 3-Phase Meter Widget JSON")
    parser.add_argument("--out", default="/tmp/electric_3phase_meter.json", help="Output file path")
    parser.add_argument("--theme", choices=["dual", "light", "dark"], default="dual", help="Theme variant: dual, light, dark")
    args = parser.parse_args()

    widget = generate_electric_3phase_widget(theme_mode=args.theme)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(widget, f, indent=2)
    print(f"✅ Generated Electric 3-Phase Meter Widget JSON ({args.theme}) at: {args.out}")
