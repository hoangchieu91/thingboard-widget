import json
import argparse
import os
import shutil
import sys

def main():
    parser = argparse.ArgumentParser(description="Package Commercial Widget with Versioning")
    parser.add_argument("--file", required=True, help="Input Widget JSON file")
    parser.add_argument("--version", default="1.0.0", help="Widget Version (e.g. 1.0.0)")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found!")
        sys.exit(1)

    with open(args.file, "r") as f:
        data = json.load(f)

    alias = data.get("alias", "custom_widget")
    target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "product", "widgets")
    os.makedirs(target_dir, exist_ok=True)

    out_name = f"{alias}_v{args.version}.json"
    out_path = os.path.join(target_dir, out_name)

    # Remove string "version" from top-level JSON because ThingsBoard backend requires version to be java.lang.Long or omitted
    if "version" in data and isinstance(data["version"], str):
        del data["version"]

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ SUCCESSFULLY PACKAGED WIDGET FOR PRODUCTION!")
    print(f" -> Version: v{args.version}")
    print(f" -> Output File: {out_path}")

if __name__ == "__main__":
    main()
