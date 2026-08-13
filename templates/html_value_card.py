import json
import sys
import argparse

def generate_widget_json(name, alias, bundle_alias):
    card_html = """<div class="tb-custom-card">
  <div class="tb-card-title">${entityLabel}</div>
  <div class="tb-card-body">
    <div class="tb-metric-row">
      <span class="tb-metric-label">Status</span>
      <span class="tb-metric-value tb-status">${status}</span>
    </div>
    <div class="tb-metric-row">
      <span class="tb-metric-label">Value</span>
      <span class="tb-metric-value">${value} kW</span>
    </div>
  </div>
</div>"""

    card_css = """.tb-custom-card {
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 12px;
  color: #c9d1d9;
  font-family: Roboto, Arial, sans-serif;
  height: 100%;
  box-sizing: border-box;
}
.tb-card-title {
  font-size: 16px;
  font-weight: 700;
  color: #58a6ff;
  margin-bottom: 10px;
  text-align: center;
}
.tb-metric-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 8px;
  border-bottom: 1px solid #21262d;
}
.tb-metric-label { color: #8b949e; }
.tb-metric-value { font-weight: 700; color: #32a852; }"""

    controller_js = """self.onInit = function() {
    self.ctx.varsRegex = /\\$\\{([^\\}]*)\\}/g;
    self.ctx.htmlSet = false;
    
    var cssParser = new cssjs();
    cssParser.testMode = false;
    var namespace = 'html-value-card-' + hashCode(self.ctx.settings.cardCss || '');
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
                    txtVal = (self.ctx.defaultSubscription && self.ctx.defaultSubscription.datasources.length) ? self.ctx.defaultSubscription.datasources[0].entityName : 'DEMO DEVICE';
                } else if (variableInfo.isEntityLabel) {
                    txtVal = (self.ctx.defaultSubscription && self.ctx.defaultSubscription.datasources.length) ? (self.ctx.defaultSubscription.datasources[0].entityLabel || self.ctx.defaultSubscription.datasources[0].entityName) : 'DEMO DEVICE';
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

    default_config = {
        "datasources": [
            {
                "type": "function",
                "name": "function",
                "dataKeys": [
                    {"name": "status", "type": "function", "label": "status", "settings": {"hideDataByDefault": False}, "funcBody": "return 'Running';"},
                    {"name": "value", "type": "function", "label": "value", "settings": {"hideDataByDefault": False}, "funcBody": "return (100 + Math.random()*20).toFixed(2);"}
                ]
            }
        ],
        "showTitle": False,
        "backgroundColor": "rgba(0, 0, 0, 0)",
        "color": "rgba(0, 0, 0, 0.87)",
        "padding": "0px",
        "settings": {
            "cardCss": card_css,
            "cardHtml": card_html,
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
            "sizeY": 6,
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
    parser = argparse.ArgumentParser(description="Generate ThingsBoard HTML Value Card Widget Template")
    parser.add_argument("--name", default="Custom Value Card", help="Widget Name")
    parser.add_argument("--alias", default="custom_value_card", help="Widget Alias")
    parser.add_argument("--bundle", default="amitech_widgets", help="Bundle Alias")
    args = parser.parse_args()

    widget = generate_widget_json(args.name, args.alias, args.bundle)
    out_file = f"{args.alias}.json"
    with open(out_file, "w") as f:
        json.dump(widget, f, indent=2)
    print(f"Generated Widget Template JSON: {out_file}")
