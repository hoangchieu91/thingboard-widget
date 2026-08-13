import json
import argparse
import subprocess
import os
import sys
import time

def main():
    parser = argparse.ArgumentParser(description="AI Agent Offline Widget Automated Testing CLI")
    parser.add_argument("--file", required=True, help="Path to Widget JSON file to test")
    parser.add_argument("--sandbox", default="http://localhost:8099", help="Sandbox Server URL")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ Error: File {args.file} not found!")
        sys.exit(1)

    print(f"=== AI AGENT AUTOMATED OFFLINE TEST: {args.file} ===")
    
    with open(args.file, "r") as f:
        w_json = f.read()

    # Node.js Puppeteer test script
    node_test_code = f"""
const puppeteer = require('/tmp/tb_debug/node_modules/puppeteer-core');
const fs = require('fs');

async function main() {{
    const browser = await puppeteer.launch({{
        executablePath: '/usr/bin/google-chrome',
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1600,1000']
    }});
    const page = await browser.newPage();
    try {{
        await page.goto('{args.sandbox}', {{ waitUntil: 'networkidle2' }});
        const jsonContent = fs.readFileSync('{args.file}', 'utf8');
        await page.evaluate((jsonText) => {{
            document.getElementById('code-json').value = jsonText;
            parseJSONToTabs();
            runWidget();
        }}, jsonContent);

        await new Promise(r => setTimeout(r, 2000));
    }} catch(e) {{
        console.error('Puppeteer test error:', e);
    }} finally {{
        await browser.close();
    }}
}}
main();
"""
    tmp_test_js = "/tmp/ai_sandbox_runner_tmp.js"
    with open(tmp_test_js, "w") as f:
        f.write(node_test_code)

    print("1. Running Headless Chrome against Sandbox...")
    res = subprocess.run(["node", tmp_test_js], capture_output=True, text=True)

    report_path = "/tmp/sandbox_widget_report.json"
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            report = json.load(f)

        print("\n=== AI TEST RESULT ===")
        print(f"Widget Name: {report.get('widgetName')}")
        print(f"Has Errors:  {report.get('hasErrors')}")

        if report.get('hasErrors'):
            print("❌ TEST FAILED WITH ERRORS:")
            for err in report.get('errors', []):
                print(f"   -> {err}")
            sys.exit(1)
        else:
            print("✅ TEST PASSED 100%! ZERO UNCAUGHT EXCEPTIONS DETECTED IN SANDBOX.")
            sys.exit(0)
    else:
        print("⚠️ Warning: Could not find /tmp/sandbox_widget_report.json")
        sys.exit(1)

if __name__ == "__main__":
    main()
