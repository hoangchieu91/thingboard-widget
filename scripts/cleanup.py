import os
import glob

def main():
    print("=== SWEEPING TEMPORARY FILES ===")
    tmp_files = glob.glob("/tmp/agent_widget_*.png") + glob.glob("/tmp/*.json_tmp")
    cleaned = 0
    for f in tmp_files:
        try:
            os.remove(f)
            cleaned += 1
            print(f" -> Removed: {f}")
        except Exception as e:
            print(f" -> Could not remove {f}: {e}")
    print(f"Cleaned {cleaned} temporary files.")

if __name__ == "__main__":
    main()
