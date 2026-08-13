import requests
import json
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Deploy Widget to ThingsBoard Server")
    parser.add_argument("--server", default="http://10.25.7.152:8080", help="ThingsBoard Server URL")
    parser.add_argument("--username", default="admin_assa@inergy.vn", help="Admin Username")
    parser.add_argument("--password", default="Amitech@123", help="Admin Password")
    parser.add_argument("--bundle", default="amitech_widgets", help="Widget Bundle Alias")
    parser.add_argument("--file", required=True, help="Path to Widget JSON file")
    args = parser.parse_args()

    print(f"=== DEPLOYING WIDGET TO {args.server} ===")
    r = requests.post(f"{args.server}/api/auth/login", json={"username": args.username, "password": args.password}, timeout=10)
    if r.status_code != 200:
        print("Login failed:", r.text)
        sys.exit(1)

    token = r.json()["token"]
    headers = {"X-Authorization": f"Bearer {token}"}

    with open(args.file, "r") as f:
        w_payload = json.load(f)

    desc = w_payload.get("descriptor", {})
    if "typeParameters" not in desc or not desc["typeParameters"]:
        desc["typeParameters"] = {}
    desc["typeParameters"]["hideDataByDefault"] = False
    desc["typeParameters"]["hasDataPageSize"] = False
    desc["typeParameters"]["dataKeysOptional"] = True

    if "defaultConfig" in desc:
        try:
            def_cfg = json.loads(desc["defaultConfig"])
            def_cfg["hideDataByDefault"] = False
            def_cfg["hasDataPageSize"] = False
            if "settings" not in def_cfg:
                def_cfg["settings"] = {}
            def_cfg["settings"]["hideDataByDefault"] = False

            if "datasources" in def_cfg:
                for ds in def_cfg["datasources"]:
                    if "dataKeys" in ds:
                        for dk in ds["dataKeys"]:
                            if "settings" not in dk or dk["settings"] is None:
                                dk["settings"] = {"hideDataByDefault": False}

            desc["defaultConfig"] = json.dumps(def_cfg)
        except Exception as e:
            print("Warning while parsing defaultConfig:", e)

    w_payload["descriptor"] = desc

    print(f"1. Posting Widget Type '{w_payload.get('name')}' (alias: {w_payload.get('alias')})...")
    r_post = requests.post(f"{args.server}/api/widgetType", json=w_payload, headers=headers, timeout=10)
    if r_post.status_code == 200:
        saved_widget = r_post.json()
        wid = saved_widget.get("id", {}).get("id")
        print(f" -> Widget Type saved successfully! ID: {wid}")

        print(f"2. Adding Widget to Bundle '{args.bundle}'...")
        r_b = requests.get(f"{args.server}/api/widgetsBundle/{args.bundle}", headers=headers, timeout=5)
        if r_b.status_code == 200:
            bundle_obj = r_b.json()
            bid = bundle_obj.get("id", {}).get("id")
            r_bind = requests.post(f"{args.server}/api/widgetsBundle/{bid}/widgetType/{wid}", headers=headers, timeout=5)
            print(f" -> Bound to Bundle status: {r_bind.status_code}")
        else:
            print(f" -> Warning: Could not find bundle '{args.bundle}'")

        print("=== DEPLOYMENT COMPLETE ===")
    else:
        print("Failed to deploy widget:", r_post.text)

if __name__ == "__main__":
    main()
