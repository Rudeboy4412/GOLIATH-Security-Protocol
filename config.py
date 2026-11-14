import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"

DEFAULT_CONFIG = {
    "name": "GOLIATH",
    "version": "0.1.0",
    "language": "en",
    "logging": True
}

def load_config():
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            config = json.load(file)

        if not isinstance(config, dict):
            raise ValueError("Invalid configuration format")

        return {**DEFAULT_CONFIG, **config}

    except (json.JSONDecodeError, OSError, ValueError):
        return DEFAULT_CONFIG.copy()


def save_config(config):
    CONFIG_FILE.write_text(
        json.dumps(config, indent=4),
        encoding="utf-8"
    )