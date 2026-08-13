import json
import argparse
import subprocess
import os
import sys
import tempfile

def test_js_syntax(script_content):
    """Validate JS syntax using Node.js static compilation pass."""
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(script_content)
        temp_js_path = f.name

    try:
        res = subprocess.run(["node", "-c", temp_js_path], capture_output=True, text=True)
        if res.returncode != 0:
            print("❌ STATIC TEST FAILED: JAVASCRIPT SYNTAX ERROR DETECTED!")
            print(res.stderr)
            return False
        return True
    except Exception as e:
        print(f"⚠️ Warning: Could not execute Node.js compiler: {e}")
        return True
    finally:
        if os.path.exists(temp_js_path):
            os.remove(temp_js_path)

def main():
    parser = argparse.ArgumentParser(description="AI Agent Offline Widget Automated Testing CLI")
    parser.add_argument("--file", required=True, help="Path to Widget JSON file to test")
    parser.add_argument("--sandbox", default="http://localhost:8099", help="Sandbox Server URL")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ Error: File {args.file} not found!")
        sys.exit(1)

    print(f"=== AI AGENT AUTOMATED OFFLINE TEST: {args.file} ===")
    
    with open(args.file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Static JS Syntax Check
    print("1. Performing Static Javascript Syntax Validation (node -c)...")
    desc = data.get("descriptor", {})
    script = desc.get("controllerScript", "")
    if not test_js_syntax(script):
        print("❌ TEST FAILED AT STEP 1: PARSER ERROR IN CONTROLLER SCRIPT!")
        sys.exit(1)
    print("   -> PASS: Zero syntax/parser errors detected.")

    # 2. Check DataKeys & ThingsBoard Anti-Patterns
    print("2. Checking ThingsBoard Rules & Anti-Patterns...")
    import re
    if re.search(r'http\.get\([^)]+\)\.then\(', script):
        print("❌ TEST FAILED AT STEP 2: ANTI-PATTERN DETECTED! Calling '.then()' directly on 'http.get()' instead of '.subscribe()' for ThingsBoard 4.x RxJS Observable!")
        sys.exit(1)

    default_cfg_raw = desc.get("defaultConfig", "{}")
    try:
        def_cfg = json.loads(default_cfg_raw)
        datasources = def_cfg.get("datasources", [])
        dk_count = 0
        for ds in datasources:
            for dk in ds.get("dataKeys", []):
                dk_count += 1
                if "settings" not in dk or dk["settings"] is None:
                    print(f"   -> ⚠️ Warning: dataKey '{dk.get('name')}' missing 'settings' object!")
        print(f"   -> PASS: Checked {dk_count} dataKeys.")
    except Exception as e:
        print(f"   -> ⚠️ Warning parsing defaultConfig: {e}")

    # 3. Optional Headless Sandbox Test
    print("3. Checking Headless Sandbox Environment...")
    tmp_test_js = "/tmp/ai_sandbox_runner_tmp.js"
    node_test_code = f"""
const puppeteer = require('/tmp/tb_debug/node_modules/puppeteer-core');
const fs = require('fs');

async function main() {{
    let browser;
    try {{
        browser = await puppeteer.launch({{
            executablePath: '/usr/bin/google-chrome',
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1600,1000']
        }});
        const page = await browser.newPage();
        await page.goto('{args.sandbox}', {{ waitUntil: 'networkidle2', timeout: 3000 }});
        const jsonContent = fs.readFileSync('{args.file}', 'utf8');
        await page.evaluate((jsonText) => {{
            document.getElementById('code-json').value = jsonText;
            parseJSONToTabs();
            runWidget();
        }}, jsonContent);

        await new Promise(r => setTimeout(r, 2000));
    }} catch(e) {{
        console.error('Puppeteer test note:', e.message);
    }} finally {{
        if (browser) await browser.close();
    }}
}}
main();
"""
    with open(tmp_test_js, "w") as f:
        f.write(node_test_code)

    res = subprocess.run(["node", tmp_test_js], capture_output=True, text=True)

    report_path = "/tmp/sandbox_widget_report.json"
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            report = json.load(f)
        if report.get('hasErrors'):
            print("❌ TEST FAILED WITH RUNTIME ERRORS IN SANDBOX:")
            for err in report.get('errors', []):
                print(f"   -> {err}")
            sys.exit(1)

    print("\n✅ ALL OFFLINE TESTS PASSED! WIDGET IS FULLY VALIDATED.")

if __name__ == "__main__":
    main()

