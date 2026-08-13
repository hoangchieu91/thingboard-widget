import json
import argparse
import os

def generate_solar_inverter_widget():
    card_html = """<div class="solar-card-container">
  <!-- Header -->
  <div class="solar-card-header">
    <div class="header-title-group">
      <span class="status-indicator"></span>
      <span class="device-name">${entityLabel}</span>
    </div>
    <div class="header-badge">CYBERPUNK INVERTER v1.0</div>
  </div>

  <!-- Section 1: Top 4 Metrics -->
  <div class="top-metrics-grid">
    <div class="metric-card">
      <div class="metric-label">ACTIVE POWER</div>
      <div class="metric-value color-neon-green">${active_power} <span class="metric-unit">kW</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-label">DAILY ENERGY</div>
      <div class="metric-value color-green">${daily_energy} <span class="metric-unit">kWh</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-label">RUNNING TIME</div>
      <div class="metric-value color-pink">${running_time} <span class="metric-unit">h</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-label">POWER FACTOR</div>
      <div class="metric-value color-blue">${power_factor}</div>
    </div>
  </div>

  <!-- Section 2: General Specs & MPPT Channels -->
  <div class="middle-section-grid">
    <!-- General Specs / AC Grid -->
    <div class="sub-panel">
      <div class="panel-title">⚡ GENERAL SPECS & AC GRID</div>
      <div class="panel-body">
        <div class="spec-row">
          <span class="spec-label">Phase A Voltage</span>
          <span class="spec-value color-blue">${voltage_phase_a} V</span>
        </div>
        <div class="spec-row">
          <span class="spec-label">Phase B Voltage</span>
          <span class="spec-value color-blue">${voltage_phase_b} V</span>
        </div>
        <div class="spec-row">
          <span class="spec-label">Phase C Voltage</span>
          <span class="spec-value color-blue">${voltage_phase_c} V</span>
        </div>
        <div class="spec-row">
          <span class="spec-label">Grid Frequency</span>
          <span class="spec-value">${frequency} Hz</span>
        </div>
      </div>
    </div>

    <!-- MPPT Inverter -->
    <div class="sub-panel">
      <div class="panel-title">☀️ MPPT CHANNELS</div>
      <div class="panel-body">
        <div class="mppt-row">
          <span class="mppt-tag">MPPT 1</span>
          <span class="mppt-detail">${mppt1_voltage}V | ${mppt1_current}A</span>
          <span class="mppt-power color-neon-green">${mppt1_power} kW</span>
        </div>
        <div class="mppt-row">
          <span class="mppt-tag">MPPT 2</span>
          <span class="mppt-detail">${mppt2_voltage}V | ${mppt2_current}A</span>
          <span class="mppt-power color-neon-green">${mppt2_power} kW</span>
        </div>
        <div class="mppt-row">
          <span class="mppt-tag">MPPT 3</span>
          <span class="mppt-detail">${mppt3_voltage}V | ${mppt3_current}A</span>
          <span class="mppt-power color-neon-green">${mppt3_power} kW</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Section 3: String Inverter Grid (S1 - S6) -->
  <div class="strings-section">
    <div class="panel-title">🔗 STRING INVERTER GRID (S1 - S6)</div>
    <div class="strings-grid">
      <div class="string-card">
        <div class="string-header">STRING 1</div>
        <div class="string-metrics">
          <div><span class="lbl">V:</span> <span class="val">${pv1_voltage} V</span></div>
          <div><span class="lbl">I:</span> <span class="val">${pv1_current} A</span></div>
        </div>
      </div>
      <div class="string-card">
        <div class="string-header">STRING 2</div>
        <div class="string-metrics">
          <div><span class="lbl">V:</span> <span class="val">${pv2_voltage} V</span></div>
          <div><span class="lbl">I:</span> <span class="val">${pv2_current} A</span></div>
        </div>
      </div>
      <div class="string-card">
        <div class="string-header">STRING 3</div>
        <div class="string-metrics">
          <div><span class="lbl">V:</span> <span class="val">${pv3_voltage} V</span></div>
          <div><span class="lbl">I:</span> <span class="val">${pv3_current} A</span></div>
        </div>
      </div>
      <div class="string-card">
        <div class="string-header">STRING 4</div>
        <div class="string-metrics">
          <div><span class="lbl">V:</span> <span class="val">${pv4_voltage} V</span></div>
          <div><span class="lbl">I:</span> <span class="val">${pv4_current} A</span></div>
        </div>
      </div>
      <div class="string-card">
        <div class="string-header">STRING 5</div>
        <div class="string-metrics">
          <div><span class="lbl">V:</span> <span class="val">${pv5_voltage} V</span></div>
          <div><span class="lbl">I:</span> <span class="val">${pv5_current} A</span></div>
        </div>
      </div>
      <div class="string-card">
        <div class="string-header">STRING 6</div>
        <div class="string-metrics">
          <div><span class="lbl">V:</span> <span class="val">${pv6_voltage} V</span></div>
          <div><span class="lbl">I:</span> <span class="val">${pv6_current} A</span></div>
        </div>
      </div>
    </div>
  </div>
</div>"""

    card_css = """.solar-card-container {
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 16px;
  color: #c9d1d9;
  font-family: 'Inter', Roboto, Arial, sans-serif;
  height: 100%;
  box-sizing: border-box;
  overflow-y: auto;
}

.solar-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid #21262d;
}

.header-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #00ffb9;
  box-shadow: 0 0 10px #00ffb9;
}

.device-name {
  font-size: 16px;
  font-weight: 700;
  color: #f0f6fc;
  letter-spacing: 0.5px;
}

.header-badge {
  font-size: 11px;
  background: rgba(88, 166, 255, 0.15);
  color: #58a6ff;
  border: 1px solid rgba(88, 166, 255, 0.3);
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 600;
}

.top-metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 16px;
}

.metric-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.metric-label {
  font-size: 11px;
  color: #8b949e;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.metric-value {
  font-size: 20px;
  font-weight: 700;
  line-height: 1.2;
}

.metric-unit {
  font-size: 12px;
  color: #8b949e;
  font-weight: 400;
}

.color-neon-green { color: #00ffb9; text-shadow: 0 0 8px rgba(0, 255, 185, 0.3); }
.color-green { color: #32a852; }
.color-pink { color: #e91e63; }
.color-blue { color: #58a6ff; }

.middle-section-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.sub-panel {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 12px;
}

.panel-title {
  font-size: 12px;
  font-weight: 700;
  color: #8b949e;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
  padding-bottom: 6px;
  border-bottom: 1px solid #21262d;
}

.panel-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.spec-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.spec-label {
  color: #8b949e;
}

.spec-value {
  font-weight: 600;
}

.mppt-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  background: rgba(13, 17, 23, 0.6);
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #21262d;
}

.mppt-tag {
  font-weight: 700;
  color: #f0f6fc;
  font-size: 11px;
}

.mppt-detail {
  color: #8b949e;
  font-size: 12px;
}

.mppt-power {
  font-weight: 700;
}

.strings-section {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 12px;
}

.strings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.string-card {
  background: #0d1117;
  border: 1px solid #21262d;
  border-radius: 6px;
  padding: 8px 10px;
}

.string-header {
  font-size: 11px;
  font-weight: 700;
  color: #58a6ff;
  margin-bottom: 4px;
}

.string-metrics {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.string-metrics .lbl {
  color: #8b949e;
}

.string-metrics .val {
  font-weight: 600;
  color: #c9d1d9;
}
"""

    controller_js = """self.onInit = function() {
    self.ctx.varsRegex = /\\$\\{([^\\}]*)\\}/g;
    self.ctx.htmlSet = false;
    
    var cssParser = new cssjs();
    cssParser.testMode = false;
    var namespace = 'solar-inv-detail-' + hashCode(self.ctx.settings.cardCss || '');
    cssParser.cssPreviewNamespace = namespace;
    cssParser.createStyleElement(namespace, self.ctx.settings.cardCss || '');
    self.ctx.$container.addClass(namespace);
    
    self.ctx.html = self.ctx.settings.cardHtml || '';
    self.ctx.replaceInfo = processHtmlPattern(self.ctx.html, self.ctx.data);
    
    updateHtml();
    
    function hashCode(str) {
        var hash = 0, i, char;
        if (!str || str.length === 0) return hash;
        for (i = 0; i < str.length; i++) {
            char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return hash;
    }
    
    function processHtmlPattern(pattern, data) {
        var match = self.ctx.varsRegex.exec(pattern);
        var replaceInfo = { variables: [] };
        while (match !== null) {
            var variableInfo = { dataKeyIndex: -1 };
            var variable = match[0];
            var label = match[1];
            var valDec = 2;
            var splitVals = label.split(':');
            if (splitVals.length > 1) {
                label = splitVals[0];
                valDec = parseFloat(splitVals[1]);
            }
            variableInfo.variable = variable;
            variableInfo.valDec = valDec;
            if (label == 'entityName') {
                variableInfo.isEntityName = true;
            } else if (label == 'entityLabel') {
                variableInfo.isEntityLabel = true;
            } else if (label.startsWith('#')) {
                var keyIndexStr = label.substring(1);
                var n = Math.floor(Number(keyIndexStr));
                if (String(n) === keyIndexStr && n >= 0) {
                    variableInfo.dataKeyIndex = n;
                }
            }
            if (!variableInfo.isEntityName && !variableInfo.isEntityLabel && variableInfo.dataKeyIndex === -1 && data) {
                for (var i = 0; i < data.length; i++) {
                     var datasourceData = data[i];
                     if (datasourceData && datasourceData.dataKey) {
                         var dataKey = datasourceData.dataKey;
                         if (dataKey.label === label || dataKey.name === label) {
                             variableInfo.dataKeyIndex = i;
                             break;
                         }
                     }
                }
            }
            replaceInfo.variables.push(variableInfo);
            match = self.ctx.varsRegex.exec(pattern);
        }
        return replaceInfo;
    }

    function updateHtml() {
        var text = self.ctx.html || '';
        if (self.ctx.replaceInfo && self.ctx.replaceInfo.variables) {
            for (var v in self.ctx.replaceInfo.variables) {
                var variableInfo = self.ctx.replaceInfo.variables[v];
                var txtVal = '-';
                if (variableInfo.dataKeyIndex > -1 && self.ctx.data && self.ctx.data[variableInfo.dataKeyIndex]) {
                    var varData = self.ctx.data[variableInfo.dataKeyIndex].data;
                    if (varData && varData.length > 0) {
                        var val = varData[varData.length - 1][1];
                        txtVal = val;
                    }
                } else if (variableInfo.isEntityName) {
                    txtVal = (self.ctx.defaultSubscription && self.ctx.defaultSubscription.datasources.length) ? self.ctx.defaultSubscription.datasources[0].entityName : 'SOLAR INVERTER 01';
                } else if (variableInfo.isEntityLabel) {
                    txtVal = (self.ctx.defaultSubscription && self.ctx.defaultSubscription.datasources.length) ? (self.ctx.defaultSubscription.datasources[0].entityLabel || self.ctx.defaultSubscription.datasources[0].entityName) : 'SOLAR INVERTER 01';
                }
                text = text.split(variableInfo.variable).join(txtVal);
            }
        }
        self.ctx.$container.html(text);
    }
};

self.onDataUpdated = function() {
    if (typeof updateHtml === 'function') updateHtml();
};

self.typeParameters = function() {
    return {
        maxDatasources: 1,
        singleEntity: true,
        dataKeysOptional: true,
        hideDataByDefault: false,
        hasDataPageSize: false
    };
};"""

    # 29 Function DataKeys with settings: { hideDataByDefault: False }
    data_keys_config = [
        {"name": "active_power", "type": "function", "label": "active_power", "settings": {"hideDataByDefault": False}, "funcBody": "return (45 + Math.random()*10).toFixed(2);"},
        {"name": "daily_energy", "type": "function", "label": "daily_energy", "settings": {"hideDataByDefault": False}, "funcBody": "return (280 + Math.random()*5).toFixed(1);"},
        {"name": "running_time", "type": "function", "label": "running_time", "settings": {"hideDataByDefault": False}, "funcBody": "return (1240 + Math.floor(Math.random()*2)).toFixed(0);"},
        {"name": "power_factor", "type": "function", "label": "power_factor", "settings": {"hideDataByDefault": False}, "funcBody": "return (0.97 + Math.random()*0.02).toFixed(2);"},
        {"name": "voltage_phase_a", "type": "function", "label": "voltage_phase_a", "settings": {"hideDataByDefault": False}, "funcBody": "return (228 + Math.random()*4).toFixed(1);"},
        {"name": "voltage_phase_b", "type": "function", "label": "voltage_phase_b", "settings": {"hideDataByDefault": False}, "funcBody": "return (230 + Math.random()*4).toFixed(1);"},
        {"name": "voltage_phase_c", "type": "function", "label": "voltage_phase_c", "settings": {"hideDataByDefault": False}, "funcBody": "return (229 + Math.random()*4).toFixed(1);"},
        {"name": "frequency", "type": "function", "label": "frequency", "settings": {"hideDataByDefault": False}, "funcBody": "return (49.95 + Math.random()*0.1).toFixed(2);"},
        {"name": "mppt1_voltage", "type": "function", "label": "mppt1_voltage", "settings": {"hideDataByDefault": False}, "funcBody": "return (610 + Math.random()*20).toFixed(1);"},
        {"name": "mppt1_current", "type": "function", "label": "mppt1_current", "settings": {"hideDataByDefault": False}, "funcBody": "return (12 + Math.random()*2).toFixed(1);"},
        {"name": "mppt1_power", "type": "function", "label": "mppt1_power", "settings": {"hideDataByDefault": False}, "funcBody": "return (7.5 + Math.random()*1).toFixed(2);"},
        {"name": "mppt2_voltage", "type": "function", "label": "mppt2_voltage", "settings": {"hideDataByDefault": False}, "funcBody": "return (605 + Math.random()*20).toFixed(1);"},
        {"name": "mppt2_current", "type": "function", "label": "mppt2_current", "settings": {"hideDataByDefault": False}, "funcBody": "return (11.8 + Math.random()*2).toFixed(1);"},
        {"name": "mppt2_power", "type": "function", "label": "mppt2_power", "settings": {"hideDataByDefault": False}, "funcBody": "return (7.3 + Math.random()*1).toFixed(2);"},
        {"name": "mppt3_voltage", "type": "function", "label": "mppt3_voltage", "settings": {"hideDataByDefault": False}, "funcBody": "return (612 + Math.random()*20).toFixed(1);"},
        {"name": "mppt3_current", "type": "function", "label": "mppt3_current", "settings": {"hideDataByDefault": False}, "funcBody": "return (12.2 + Math.random()*2).toFixed(1);"},
        {"name": "mppt3_power", "type": "function", "label": "mppt3_power", "settings": {"hideDataByDefault": False}, "funcBody": "return (7.6 + Math.random()*1).toFixed(2);"},
        {"name": "pv1_voltage", "type": "function", "label": "pv1_voltage", "settings": {"hideDataByDefault": False}, "funcBody": "return (608 + Math.random()*15).toFixed(1);"},
        {"name": "pv1_current", "type": "function", "label": "pv1_current", "settings": {"hideDataByDefault": False}, "funcBody": "return (6.1 + Math.random()*1).toFixed(1);"},
        {"name": "pv2_voltage", "type": "function", "label": "pv2_voltage", "settings": {"hideDataByDefault": False}, "funcBody": "return (610 + Math.random()*15).toFixed(1);"},
        {"name": "pv2_current", "type": "function", "label": "pv2_current", "settings": {"hideDataByDefault": False}, "funcBody": "return (6.0 + Math.random()*1).toFixed(1);"},
        {"name": "pv3_voltage", "type": "function", "label": "pv3_voltage", "settings": {"hideDataByDefault": False}, "funcBody": "return (604 + Math.random()*15).toFixed(1);"},
        {"name": "pv3_current", "type": "function", "label": "pv3_current", "settings": {"hideDataByDefault": False}, "funcBody": "return (5.9 + Math.random()*1).toFixed(1);"},
        {"name": "pv4_voltage", "type": "function", "label": "pv4_voltage", "settings": {"hideDataByDefault": False}, "funcBody": "return (606 + Math.random()*15).toFixed(1);"},
        {"name": "pv4_current", "type": "function", "label": "pv4_current", "settings": {"hideDataByDefault": False}, "funcBody": "return (5.9 + Math.random()*1).toFixed(1);"},
        {"name": "pv5_voltage", "type": "function", "label": "pv5_voltage", "settings": {"hideDataByDefault": False}, "funcBody": "return (611 + Math.random()*15).toFixed(1);"},
        {"name": "pv5_current", "type": "function", "label": "pv5_current", "settings": {"hideDataByDefault": False}, "funcBody": "return (6.1 + Math.random()*1).toFixed(1);"},
        {"name": "pv6_voltage", "type": "function", "label": "pv6_voltage", "settings": {"hideDataByDefault": False}, "funcBody": "return (613 + Math.random()*15).toFixed(1);"},
        {"name": "pv6_current", "type": "function", "label": "pv6_current", "settings": {"hideDataByDefault": False}, "funcBody": "return (6.2 + Math.random()*1).toFixed(1);"}
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
            "widgetTitle": "Solar Inverter Detail"
        },
        "title": "Solar Inverter Detail",
        "dropShadow": False,
        "enableFullscreen": True
    }

    widget_json = {
        "alias": "solar_inverter_detail",
        "name": "Solar Inverter Detail",
        "descriptor": {
            "type": "latest",
            "sizeX": 10,
            "sizeY": 8,
            "resources": [],
            "templateHtml": "",
            "templateCss": "",
            "controllerScript": controller_js,
            "settingsDirective": "tb-html-card-widget-settings",
            "settingsForm": [],
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
    parser = argparse.ArgumentParser(description="Generate Solar Inverter Detail Widget JSON")
    parser.add_argument("--out", default="/tmp/solar_inverter_detail.json", help="Output file path")
    args = parser.parse_args()

    widget = generate_solar_inverter_widget()
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(widget, f, indent=2)
    print(f"✅ Generated Solar Inverter Detail Widget JSON at: {args.out}")
