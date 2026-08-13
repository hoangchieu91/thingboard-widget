import json
import argparse
import os
import sys

def generate_electric_3phase_table_widget(theme_mode="dual"):
    alias = "electric_3phase_table"
    name = "Electric 3-Phase Multi-Meter Table"

    card_css = """
.tb-multi-meter-table-widget {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    width: 100%;
    height: 100%;
    border-radius: 12px;
    padding: 16px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 14px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.tb-multi-meter-table-widget.dark-theme {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #f8fafc;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.tb-multi-meter-table-widget.light-theme {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    color: #0f172a;
    border-color: #e2e8f0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

/* Header & Control Bar */
.tb-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

.header-title-group {
    display: flex;
    align-items: center;
    gap: 10px;
}

.header-title-group h2 {
    font-size: 17px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.3px;
}

/* Summary Badges Bar */
.summary-kpi-bar {
    display: flex;
    gap: 12px;
    align-items: center;
}

.kpi-badge {
    background: rgba(148, 163, 184, 0.12);
    border: 1px solid rgba(148, 163, 184, 0.25);
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 12px;
    display: flex;
    gap: 6px;
    align-items: center;
}
.kpi-val { font-weight: 800; color: #3b82f6; }
.dark-theme .kpi-val { color: #60a5fa; }

.search-box {
    position: relative;
    display: flex;
    align-items: center;
}

.search-input {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(148, 163, 184, 0.3);
    color: inherit;
    padding: 6px 12px 6px 30px;
    border-radius: 8px;
    font-size: 12px;
    outline: none;
    width: 200px;
    transition: all 0.2s ease;
}
.light-theme .search-input {
    background: #ffffff;
    border-color: #cbd5e1;
}

.search-icon {
    position: absolute;
    left: 10px;
    font-size: 12px;
    opacity: 0.6;
}

/* Table Container */
.table-container {
    flex: 1;
    overflow-y: auto;
    border-radius: 8px;
    border: 1px solid rgba(148, 163, 184, 0.2);
}

.meters-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    text-align: left;
}

.meters-table th {
    background: rgba(15, 23, 42, 0.8);
    padding: 10px 14px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #94a3b8;
    position: sticky;
    top: 0;
    z-index: 2;
    border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}
.light-theme .meters-table th {
    background: #f1f5f9;
    color: #64748b;
}

.meters-table td {
    padding: 12px 14px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    vertical-align: middle;
}

.meters-table tr:hover {
    background: rgba(59, 130, 246, 0.08);
}

/* Row elements */
.td-device-info {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
}

.mini-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22c55e;
}

.phase-text {
    font-size: 12px;
    font-weight: 600;
}

.pa-text { color: #ef4444; }
.pb-text { color: #eab308; }
.pc-text { color: #3b82f6; }

.power-val {
    font-weight: 800;
    color: #10b981;
}

.progress-track {
    width: 80px;
    height: 6px;
    background: rgba(148, 163, 184, 0.2);
    border-radius: 3px;
    overflow: hidden;
    display: inline-block;
    vertical-align: middle;
    margin-right: 6px;
}

.progress-bar {
    height: 100%;
    background: #10b981;
    border-radius: 3px;
}

.btn-action {
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.4);
    color: #3b82f6;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
}
.btn-action:hover {
    background: #3b82f6;
    color: #ffffff;
}

.btn-theme {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: inherit;
    border-radius: 6px;
    padding: 4px 10px;
    cursor: pointer;
    font-size: 12px;
}
"""

    card_html = """
<div class="tb-multi-meter-table-widget dark-theme">
    <div class="tb-header-bar">
        <div class="header-title-group">
            <h2 class="title-text">📊 Bảng Tổng Hợp Đồng Hồ Điện 3 Pha</h2>
        </div>

        <div class="summary-kpi-bar">
            <div class="kpi-badge">
                <span>Số tủ điện:</span>
                <span class="kpi-val" id="kpi-count">0</span>
            </div>
            <div class="kpi-badge">
                <span>Tổng P:</span>
                <span class="kpi-val" id="kpi-total-power">0 kW</span>
            </div>
            <div class="kpi-badge">
                <span>Tổng Điện năng:</span>
                <span class="kpi-val" id="kpi-total-energy">0 kWh</span>
            </div>
        </div>

        <div style="display: flex; gap: 10px; align-items: center;">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" class="search-input" id="search-filter" placeholder="Tìm kiếm tủ điện...">
            </div>
            <button class="btn-theme" id="btn-theme-toggle">🌙</button>
        </div>
    </div>

    <div class="table-container">
        <table class="meters-table">
            <thead>
                <tr>
                    <th>Tên Tủ Điện / Đồng Hồ</th>
                    <th>Điện Năng Tổng (kWh)</th>
                    <th>Pha A (A)</th>
                    <th>Pha B (A)</th>
                    <th>Pha C (A)</th>
                    <th>Công Suất (kW)</th>
                    <th>Mức Tải (%)</th>
                    <th>Thao Tác</th>
                </tr>
            </thead>
            <tbody id="meters-table-body">
                <!-- Dynamically Rendered Rows -->
            </tbody>
        </table>
    </div>
</div>
"""

    controller_js = """
self.onInit = function() {
    var $container = self.ctx.$container;
    var isDarkTheme = true;
    var filterText = '';

    function formatNumber(num, decimals) {
        if (num === null || num === undefined || isNaN(num)) return 'N/A';
        return parseFloat(num).toLocaleString('en-US', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }

    function normalizeKey(k) {
        if (!k) return '';
        return String(k).toLowerCase().replace(/[^a-z0-9]/g, '');
    }

    function toggleTheme() {
        isDarkTheme = !isDarkTheme;
        var widgetEl = $('.tb-multi-meter-table-widget', $container);
        var toggleBtn = $('#btn-theme-toggle', $container);
        
        if (isDarkTheme) {
            widgetEl.removeClass('light-theme').addClass('dark-theme');
            toggleBtn.text('🌙');
        } else {
            widgetEl.removeClass('dark-theme').addClass('light-theme');
            toggleBtn.text('☀️');
        }
    }

    function updateWidgetTitle() {
        var title = '';
        if (self.ctx.settings && self.ctx.settings.widgetTitle) {
            title = self.ctx.settings.widgetTitle;
        }
        if (!title) {
            title = '📊 Bảng Tổng Hợp Đồng Hồ Điện 3 Pha';
        }
        $('.title-text', $container).text(title);
    }

    function renderMetersTable() {
        updateWidgetTitle();

        // Map data by Entity
        var entityMap = {};
        if (self.ctx.data && self.ctx.data.length > 0) {
            for (var i = 0; i < self.ctx.data.length; i++) {
                var ds = self.ctx.data[i];
                if (ds && ds.datasource && ds.dataKey && ds.data && ds.data.length > 0) {
                    var entityId = ds.datasource.entityId || 'entity_' + i;
                    var entityName = ds.datasource.entityLabel || ds.datasource.entityName || ('Tủ ' + (i+1));
                    var entityType = ds.datasource.entityType || 'DEVICE';

                    if (!entityMap[entityId]) {
                        entityMap[entityId] = {
                            id: entityId,
                            name: entityName,
                            type: entityType,
                            telemetry: {}
                        };
                    }

                    var latestVal = ds.data[ds.data.length - 1][1];
                    if (ds.dataKey.name) entityMap[entityId].telemetry[normalizeKey(ds.dataKey.name)] = latestVal;
                    if (ds.dataKey.label) entityMap[entityId].telemetry[normalizeKey(ds.dataKey.label)] = latestVal;
                }
            }
        }

        // Preview Fallback if in editor or empty data
        var entityList = Object.values(entityMap);
        if (entityList.length === 0) {
            entityList = [
                { id: 'demo1', name: '54A_TDH_CH01', type: 'DEVICE', telemetry: { currenta: 450.2, currentb: 448.0, currentc: 461.5, voltagea: 220, powertotal: 298.5, energytotal: 128450.0 } },
                { id: 'demo2', name: '54A_TDH_CH02', type: 'DEVICE', telemetry: { currenta: 320.5, currentb: 318.2, currentc: 325.0, voltagea: 220, powertotal: 211.0, energytotal: 94210.0 } },
                { id: 'demo3', name: '54A_TDH_CH03', type: 'DEVICE', telemetry: { currenta: 657.0, currentb: 656.4, currentc: 685.3, voltagea: 392, powertotal: 728.8, energytotal: 387262.0 } }
            ];
        }

        var tbody = $('#meters-table-body', $container);
        tbody.empty();

        var totalPowerSum = 0;
        var totalEnergySum = 0;
        var matchedCount = 0;

        entityList.forEach(function(item) {
            if (filterText && item.name.toLowerCase().indexOf(filterText.toLowerCase()) === -1) {
                return;
            }
            matchedCount++;

            function getVal(aliasList, defaultVal) {
                for (var j = 0; j < aliasList.length; j++) {
                    var norm = normalizeKey(aliasList[j]);
                    if (item.telemetry.hasOwnProperty(norm) && item.telemetry[norm] !== undefined && item.telemetry[norm] !== null) {
                        var num = parseFloat(item.telemetry[norm]);
                        return isNaN(num) ? item.telemetry[norm] : num;
                    }
                }
                return defaultVal;
            }

            var ia = getVal(['currentA', 'current_a', 'ia', 'i1'], null);
            var ib = getVal(['currentB', 'current_b', 'ib', 'i2'], null);
            var ic = getVal(['currentC', 'current_c', 'ic', 'i3'], null);
            var va = getVal(['voltageA', 'voltage_a', 'va', 'u_an', 'uan'], 220);
            var vb = getVal(['voltageB', 'voltage_b', 'vb', 'u_bn'], 220);
            var vc = getVal(['voltageC', 'voltage_c', 'vc', 'u_cn'], 220);

            var maxI = Math.max(ia || 0, ib || 0, ic || 0);
            var maxCurrent = (self.ctx.settings && self.ctx.settings.maxCurrent) ? parseFloat(self.ctx.settings.maxCurrent) : 75.0;
            if (maxI > maxCurrent) {
                maxCurrent = Math.ceil(maxI * 1.2);
            }

            var powerTotal = getVal(['powerTotal', 'power_total', 'activePower', 'active_power', 'Power_Active_Total', 'kw', 'power', 'p'], null);
            if (powerTotal === null && ia !== null && ib !== null && ic !== null) {
                powerTotal = parseFloat((((va * ia + vb * ib + vc * ic) * 0.92) / 1000).toFixed(1));
            }

            var energyTotal = getVal(['energyTotal', 'energy_total', 'totalEnergy', 'total_energy', 'kwh', 'energy'], null);

            if (powerTotal !== null) totalPowerSum += powerTotal;
            if (energyTotal !== null) totalEnergySum += energyTotal;

            var pct = (maxI > 0 && maxCurrent > 0) ? ((maxI / maxCurrent) * 100).toFixed(1) : '0.0';

            var tr = $('<tr></tr>');
            tr.append('<td><div class="td-device-info"><div class="mini-dot"></div><span>' + item.name + '</span></div></td>');
            tr.append('<td>' + (energyTotal !== null ? formatNumber(energyTotal, 1) : 'N/A') + '</td>');
            tr.append('<td class="phase-text pa-text">' + (ia !== null ? formatNumber(ia, 1) + ' A' : 'N/A') + '</td>');
            tr.append('<td class="phase-text pb-text">' + (ib !== null ? formatNumber(ib, 1) + ' A' : 'N/A') + '</td>');
            tr.append('<td class="phase-text pc-text">' + (ic !== null ? formatNumber(ic, 1) + ' A' : 'N/A') + '</td>');
            tr.append('<td class="power-val">' + (powerTotal !== null ? formatNumber(powerTotal, 1) + ' kW' : 'N/A') + '</td>');
            tr.append('<td><div class="progress-track"><div class="progress-bar" style="width:' + Math.min(parseFloat(pct), 100) + '%"></div></div><span>' + pct + '%</span></td>');
            
            var btnAction = $('<button class="btn-action">👁️ Chi tiết</button>');
            btnAction.on('click', function(evt) {
                if (self.ctx.actionsApi) {
                    var entityIdObj = { id: item.id, entityType: item.type };
                    var descriptors = self.ctx.actionsApi.getActionDescriptors('elementClick');
                    if (descriptors && descriptors.length > 0) {
                        self.ctx.actionsApi.handleWidgetAction(evt, descriptors[0], entityIdObj, item.name, {}, item.name);
                    }
                }
            });
            var tdAction = $('<td></td>').append(btnAction);
            tr.append(tdAction);

            tbody.append(tr);
        });

        $('#kpi-count', $container).text(matchedCount);
        $('#kpi-total-power', $container).text(formatNumber(totalPowerSum, 1) + ' kW');
        $('#kpi-total-energy', $container).text(formatNumber(totalEnergySum, 1) + ' kWh');
    }

    $('#search-filter', $container).on('input', function() {
        filterText = $(this).val();
        renderMetersTable();
    });

    $('#btn-theme-toggle', $container).on('click', function() {
        toggleTheme();
    });

    renderMetersTable();
    self.updateTelemetryData = renderMetersTable;
};

self.onDataUpdated = function() {
    if (typeof self.updateTelemetryData === 'function') {
        self.updateTelemetryData();
    }
};

self.typeParameters = function() {
    return {
        maxDatasources: -1,
        singleEntity: false,
        dataKeysOptional: true,
        hideDataByDefault: false,
        hasDataPageSize: false
    };
};
"""

    data_keys_config = [
        {"name": "Current_A", "type": "function", "label": "Current_A", "settings": {"hideDataByDefault": False}, "funcBody": "return (44 + Math.random()*3).toFixed(1);"},
        {"name": "Current_B", "type": "function", "label": "Current_B", "settings": {"hideDataByDefault": False}, "funcBody": "return (43.5 + Math.random()*3).toFixed(1);"},
        {"name": "Current_C", "type": "function", "label": "Current_C", "settings": {"hideDataByDefault": False}, "funcBody": "return (45 + Math.random()*3).toFixed(1);"},
        {"name": "voltageA", "type": "function", "label": "voltageA", "settings": {"hideDataByDefault": False}, "funcBody": "return (220 + Math.random()*2).toFixed(1);"},
        {"name": "powerTotal", "type": "function", "label": "powerTotal", "settings": {"hideDataByDefault": False}, "funcBody": "return (29 + Math.random()*2).toFixed(1);"},
        {"name": "energyTotal", "type": "function", "label": "energyTotal", "settings": {"hideDataByDefault": False}, "funcBody": "return (124582.6 + Math.random()*1).toFixed(1);"}
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
            "sizeX": 12,
            "sizeY": 6,
            "resources": [],
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
                    "name": "Tiêu đề Bảng đồng hồ tùy chỉnh",
                    "type": "text",
                    "default": "",
                    "required": False,
                    "fieldClass": "flex"
                }
            ],
            "defaultConfig": json.dumps(default_config),
            "typeParameters": {
                "maxDatasources": -1,
                "singleEntity": False,
                "dataKeysOptional": True,
                "hideDataByDefault": False,
                "hasDataPageSize": False
            }
        }
    }
    return widget_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Electric 3-Phase Multi-Meter Table Widget JSON")
    parser.add_argument("--out", default="/tmp/electric_3phase_table.json", help="Output file path")
    parser.add_argument("--theme", choices=["dual", "light", "dark"], default="dual", help="Theme variant")
    args = parser.parse_args()

    widget = generate_electric_3phase_table_widget(theme_mode=args.theme)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(widget, f, indent=2)
    print(f"✅ Generated Electric 3-Phase Multi-Meter Table Widget JSON ({args.theme}) at: {args.out}")
