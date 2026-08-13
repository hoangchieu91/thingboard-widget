import json
import argparse
import os
import sys

def generate_electric_3phase_row_widget(theme_mode="dual"):
    alias = "electric_3phase_row"
    name = "Electric 3-Phase Row Strip Meter"

    card_css = """
.tb-electric-row-widget {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    width: 100%;
    height: 100%;
    border-radius: 12px;
    padding: 10px 16px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.tb-electric-row-widget.dark-theme {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #f8fafc;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.tb-electric-row-widget.light-theme {
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
    color: #0f172a;
    border-color: #e2e8f0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

/* Device Info Left */
.row-device-info {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 220px;
}

.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #22c55e;
    box-shadow: 0 0 8px rgba(34, 197, 94, 0.6);
}

.device-title-wrapper {
    display: flex;
    flex-direction: column;
}

.device-name {
    font-size: 15px;
    font-weight: 700;
    letter-spacing: -0.2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 170px;
}

.device-subtitle {
    font-size: 11px;
    opacity: 0.65;
}

/* Lifetime Energy Badge */
.energy-badge {
    background: rgba(59, 130, 246, 0.12);
    border: 1px solid rgba(59, 130, 246, 0.3);
    color: #3b82f6;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
}
.dark-theme .energy-badge { color: #60a5fa; background: rgba(96, 165, 250, 0.15); }

/* Phases Section Middle */
.row-phases-wrapper {
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1;
    justify-content: space-around;
}

.phase-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
}

.phase-badge {
    font-size: 10px;
    font-weight: 800;
    padding: 1px 6px;
    border-radius: 4px;
    text-transform: uppercase;
}
.badge-pa { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
.badge-pb { background: rgba(234, 179, 8, 0.2); color: #eab308; }
.badge-pc { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }

.phase-val {
    font-size: 13px;
    font-weight: 700;
}

.phase-sub {
    font-size: 10px;
    opacity: 0.6;
}

/* Right Section Power & Load Progress */
.row-power-wrapper {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 4px;
    min-width: 140px;
}

.power-main {
    font-size: 16px;
    font-weight: 800;
    color: #10b981;
}

.progress-track {
    width: 100px;
    height: 6px;
    background: rgba(148, 163, 184, 0.2);
    border-radius: 3px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background: #10b981;
    width: 0%;
    border-radius: 3px;
    transition: width 0.4s ease;
}

.load-pct-text {
    font-size: 10px;
    font-weight: 600;
    opacity: 0.7;
}

/* Theme Toggle Button */
.btn-theme {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: inherit;
    border-radius: 6px;
    padding: 4px 8px;
    cursor: pointer;
    font-size: 12px;
}
"""

    card_html = """
<div class="tb-electric-row-widget dark-theme">
    <div class="row-device-info">
        <div class="status-dot"></div>
        <div class="device-title-wrapper">
            <span class="device-name title-text">⚡ 54A_TDH_CH03</span>
            <span class="device-subtitle">Tủ Điện 3 Pha Realtime</span>
        </div>
    </div>

    <div class="energy-badge">
        <span id="val-total-energy">387,196.0 kWh</span>
    </div>

    <div class="row-phases-wrapper">
        <div class="phase-item">
            <span class="phase-badge badge-pa">PHA A</span>
            <span class="phase-val" id="val-ia">657.0 A</span>
            <span class="phase-sub" id="val-va">392.5 V</span>
        </div>

        <div class="phase-item">
            <span class="phase-badge badge-pb">PHA B</span>
            <span class="phase-val" id="val-ib">656.4 A</span>
            <span class="phase-sub" id="val-vb">395.4 V</span>
        </div>

        <div class="phase-item">
            <span class="phase-badge badge-pc">PHA C</span>
            <span class="phase-val" id="val-ic">685.3 A</span>
            <span class="phase-sub" id="val-vc">395.7 V</span>
        </div>
    </div>

    <div class="row-power-wrapper">
        <span class="power-main" id="val-power">728.8 kW</span>
        <div class="progress-track">
            <div class="progress-bar" id="bar-load"></div>
        </div>
        <span class="load-pct-text" id="txt-load-pct">Tải: 83.3%</span>
    </div>

    <button class="btn-theme" id="btn-theme-toggle">🌙</button>
</div>
"""

    controller_js = """
self.onInit = function() {
    var $container = self.ctx.$container;
    var isDarkTheme = true;

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

    function updateWidgetTitle() {
        var title = '';
        if (self.ctx.defaultSubscription && self.ctx.defaultSubscription.datasources.length > 0) {
            var ds = self.ctx.defaultSubscription.datasources[0];
            if (ds.type !== 'function') {
                title = ds.entityLabel || ds.entityName || '';
            }
        }
        if (!title && self.ctx.settings && self.ctx.settings.widgetTitle) {
            title = self.ctx.settings.widgetTitle;
        }
        if (!title) {
            title = '⚡ Đồng hồ đo điện';
        }
        $('.title-text', $container).text(title);
    }

    function toggleTheme() {
        isDarkTheme = !isDarkTheme;
        var widgetEl = $('.tb-electric-row-widget', $container);
        var toggleBtn = $('#btn-theme-toggle', $container);
        
        if (isDarkTheme) {
            widgetEl.removeClass('light-theme').addClass('dark-theme');
            toggleBtn.text('🌙');
        } else {
            widgetEl.removeClass('dark-theme').addClass('light-theme');
            toggleBtn.text('☀️');
        }
    }

    function updateTelemetryData() {
        updateWidgetTitle();

        var isFunctionPreview = false;
        if (self.ctx.defaultSubscription && self.ctx.defaultSubscription.datasources.length > 0) {
            if (self.ctx.defaultSubscription.datasources[0].type === 'function') {
                isFunctionPreview = true;
            }
        }

        var dataMap = {};
        if (self.ctx.data && self.ctx.data.length > 0) {
            for (var i = 0; i < self.ctx.data.length; i++) {
                var ds = self.ctx.data[i];
                if (ds && ds.dataKey && ds.data && ds.data.length > 0) {
                    var latestVal = ds.data[ds.data.length - 1][1];
                    if (ds.dataKey.name) dataMap[normalizeKey(ds.dataKey.name)] = latestVal;
                    if (ds.dataKey.label) dataMap[normalizeKey(ds.dataKey.label)] = latestVal;
                }
            }
        }

        function renderTelemetryMap() {
            function getVal(aliasList, defaultPreviewVal) {
                for (var i = 0; i < aliasList.length; i++) {
                    var norm = normalizeKey(aliasList[i]);
                    if (dataMap.hasOwnProperty(norm) && dataMap[norm] !== undefined && dataMap[norm] !== null && dataMap[norm] !== '') {
                        var num = parseFloat(dataMap[norm]);
                        return isNaN(num) ? dataMap[norm] : num;
                    }
                }
                return isFunctionPreview ? defaultPreviewVal : null;
            }

            var maxCurrentConfig = (self.ctx.settings && self.ctx.settings.maxCurrent) ? parseFloat(self.ctx.settings.maxCurrent) : 75.0;
            var maxCurrentVal = getVal(['maxCurrent', 'ratedCurrent', 'max_current', 'rated_current', 'imax', 'i_max'], maxCurrentConfig);
            var maxCurrent = (maxCurrentVal !== null && maxCurrentVal > 0) ? maxCurrentVal : maxCurrentConfig;

            var ia = getVal(['currentA', 'current_a', 'ia', 'i_a', 'i_phase_a', 'l1_current', 'i1'], 45.2);
            var ib = getVal(['currentB', 'current_b', 'ib', 'i_b', 'i_phase_b', 'l2_current', 'i2'], 44.8);
            var ic = getVal(['currentC', 'current_c', 'ic', 'i_c', 'i_phase_c', 'l3_current', 'i3'], 46.1);

            var maxI = Math.max(ia || 0, ib || 0, ic || 0);
            if (maxI > maxCurrent) {
                maxCurrent = Math.ceil(maxI * 1.2);
            }

            var va = getVal(['voltageA', 'voltage_a', 'va', 'v_a', 'uan', 'u_an', 'l1_voltage', 'ua'], 220.1);
            var vb = getVal(['voltageB', 'voltage_b', 'vb', 'v_b', 'ubn', 'u_bn', 'l2_voltage', 'ub'], 220.5);
            var vc = getVal(['voltageC', 'voltage_c', 'vc', 'v_c', 'ucn', 'u_cn', 'l3_voltage', 'uc'], 220.8);

            var powerTotal = getVal(['powerTotal', 'power_total', 'activePower', 'active_power', 'Power_Active_Total', 'power_active_total', 'poweractivetotal', 'ptotal', 'p_total', 'kw', 'power', 'p', 'w'], null);
            if (powerTotal === null && va !== null && vb !== null && vc !== null && ia !== null && ib !== null && ic !== null) {
                powerTotal = parseFloat((((va * ia + vb * ib + vc * ic) * 0.92) / 1000).toFixed(1));
            } else if (powerTotal === null && ia !== null && ib !== null && ic !== null) {
                powerTotal = parseFloat((((220 * (ia + ib + ic)) * 0.92) / 1000).toFixed(1));
            }

            var energyTotal = getVal(['energyTotal', 'energy_total', 'totalEnergy', 'total_energy', 'total_kwh', 'totalkwh', 'kwh', 'energy', 'active_energy', 'etotal', 'e_total'], 124582.6);

            // Render Values
            $('#val-total-energy', $container).text(energyTotal !== null ? formatNumber(energyTotal, 1) + ' kWh' : 'N/A');

            $('#val-ia', $container).text(ia !== null ? formatNumber(ia, 1) + ' A' : 'N/A');
            $('#val-ib', $container).text(ib !== null ? formatNumber(ib, 1) + ' A' : 'N/A');
            $('#val-ic', $container).text(ic !== null ? formatNumber(ic, 1) + ' A' : 'N/A');

            $('#val-va', $container).text(va !== null ? formatNumber(va, 1) + ' V' : 'N/A');
            $('#val-vb', $container).text(vb !== null ? formatNumber(vb, 1) + ' V' : 'N/A');
            $('#val-vc', $container).text(vc !== null ? formatNumber(vc, 1) + ' V' : 'N/A');

            $('#val-power', $container).text(powerTotal !== null ? formatNumber(powerTotal, 1) + ' kW' : 'N/A');

            var pct = (maxI > 0 && maxCurrent > 0) ? ((maxI / maxCurrent) * 100).toFixed(1) : '0.0';
            $('#bar-load', $container).css('width', Math.min(parseFloat(pct), 100) + '%');
            $('#txt-load-pct', $container).text('Tải: ' + pct + '%');
        }

        renderTelemetryMap();

        // REST API Fallback
        if (!isFunctionPreview && self.ctx.defaultSubscription && self.ctx.defaultSubscription.datasources.length > 0) {
            var ds0 = self.ctx.defaultSubscription.datasources[0];
            if (ds0.entityId && ds0.entityType) {
                var http = self.ctx.http || (self.ctx.$scope && self.ctx.$scope.$injector ? self.ctx.$scope.$injector.get('$http') : null);
                if (http && !self.ctx._fetchedLatestApi) {
                    self.ctx._fetchedLatestApi = true;
                    var apiUrl = '/api/plugins/telemetry/' + ds0.entityType + '/' + ds0.entityId + '/values/timeseries';
                    function handleLatestData(latestObj) {
                        if (latestObj) {
                            for (var key in latestObj) {
                                if (latestObj.hasOwnProperty(key)) {
                                    var arr = latestObj[key];
                                    if (arr && arr.length > 0) {
                                        var val = arr[arr.length - 1].value;
                                        dataMap[normalizeKey(key)] = val;
                                    }
                                }
                            }
                            renderTelemetryMap();
                        }
                    }

                    var httpOpts = { headers: { ignoreErrors: 'true' } };
                    var req = http.get(apiUrl, httpOpts);
                    if (req && typeof req.subscribe === 'function') {
                        req.subscribe(function(res) {
                            handleLatestData(res && res.data ? res.data : res);
                        }, function(e) {});
                    } else if (req && typeof req.then === 'function') {
                        req.then(function(res) {
                            handleLatestData(res && res.data ? res.data : res);
                        }).catch(function(e) {});
                    }
                }
            }
        }
    }

    $('#btn-theme-toggle', $container).on('click', function() {
        toggleTheme();
    });

    updateTelemetryData();
    self.updateTelemetryData = updateTelemetryData;
};

self.onDataUpdated = function() {
    if (typeof self.updateTelemetryData === 'function') {
        self.updateTelemetryData();
    }
};

self.typeParameters = function() {
    return {
        maxDatasources: 1,
        singleEntity: true,
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
            "sizeY": 2,
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
                    "name": "Tên đồng hồ tùy chỉnh",
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
    parser = argparse.ArgumentParser(description="Generate Electric 3-Phase Row Strip Widget JSON")
    parser.add_argument("--out", default="/tmp/electric_3phase_row.json", help="Output file path")
    parser.add_argument("--theme", choices=["dual", "light", "dark"], default="dual", help="Theme variant")
    args = parser.parse_args()

    widget = generate_electric_3phase_row_widget(theme_mode=args.theme)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(widget, f, indent=2)
    print(f"✅ Generated Electric 3-Phase Row Strip Widget JSON ({args.theme}) at: {args.out}")
