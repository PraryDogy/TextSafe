import json
import os

class Cfg:
    app_name = "TextSafe"
    app_ver = "1.0.0"

    app_support = os.path.join(
        os.path.expanduser("~"),
        "Library",
        "Application Support",
        app_name
        )

    json_file = os.path.join(
        app_support,
        "cfg.json"
        )

    os.makedirs(app_support, exist_ok=True)

    if not os.path.exists(json_file):
        with open(json_file, mode="w", encoding="utf-8") as file:
            data: list = []
            json.dump(data, file)
    else:
        with open(json_file, mode="r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    @staticmethod
    def save_json(data: list):
        with open(Cfg.json_file, mode="w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)