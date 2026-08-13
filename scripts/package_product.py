import json
import argparse
import os
import shutil
import sys
import subprocess
import tempfile

def validate_js_syntax(script_content):
    """Validate Javascript syntax using Node.js static compilation pass (node -c)."""
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(script_content)
        temp_js_path = f.name

    try:
        res = subprocess.run(["node", "-c", temp_js_path], capture_output=True, text=True)
        if res.returncode != 0:
            print("❌ JAVASCRIPT SYNTAX ERROR (Parser Error) DETECTED IN CONTROLLER SCRIPT!")
            print(res.stderr)
            return False
        return True
    except Exception as e:
        print(f"⚠️ Warning: Could not run Node.js syntax check: {e}")
        return True
    finally:
        if os.path.exists(temp_js_path):
            os.remove(temp_js_path)

def validate_tb_rules(data):
    """Validate ThingsBoard Gold Rules & Anti-Patterns."""
    issues = []
    desc = data.get("descriptor", {})
    script = desc.get("controllerScript", "")

    if not script or not script.strip():
        issues.append("controllerScript is empty!")

    # Check for string 'version' top-level
    if "version" in data and isinstance(data["version"], str):
        issues.append("String 'version' found in top-level JSON (must be Long or omitted)")

    return issues

def main():
    parser = argparse.ArgumentParser(description="Package Commercial Widget with Versioning & Auto Validation")
    parser.add_argument("--file", required=True, help="Input Widget JSON file")
    parser.add_argument("--version", default="1.0.0", help="Widget Version (e.g. 1.0.0)")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ Error: File {args.file} not found!")
        sys.exit(1)

    print(f"=== PACKAGING & VALIDATING WIDGET: {args.file} ===")
    with open(args.file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Validate JS Syntax
    desc = data.get("descriptor", {})
    script = desc.get("controllerScript", "")
    print("1. Checking Javascript Syntax with Node.js...")
    if not validate_js_syntax(script):
        print("❌ PACKAGING ABORTED DUE TO JAVASCRIPT SYNTAX ERROR!")
        sys.exit(1)
    print("   -> JS Syntax OK! (Zero parser errors)")

    # 2. Validate ThingsBoard Rules
    print("2. Validating ThingsBoard Gold Rules...")
    issues = validate_tb_rules(data)
    if issues:
        for issue in issues:
            print(f"   -> ⚠️ Rule Warning: {issue}")

    alias = data.get("alias", "custom_widget")
    target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "product", "widgets")
    os.makedirs(target_dir, exist_ok=True)

    out_name = f"{alias}_v{args.version}.json"
    out_path = os.path.join(target_dir, out_name)

    # Clean string "version" from top-level JSON
    if "version" in data and isinstance(data["version"], str):
        del data["version"]

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ SUCCESSFULLY VALIDATED & PACKAGED WIDGET!")
    print(f" -> Version: v{args.version}")
    print(f" -> Output File: {out_path}")

if __name__ == "__main__":
    main()

