import platform
import sys

from goliath.config import load_config
from goliath.logger import info, error


class GoliathCore:

    def __init__(self):
        self.config = load_config()
        self.name = self.config["name"]
        self.version = self.config["version"]
        self.system = platform.system()
        self.python = platform.python_version()
        self.modules = {}

    def initialize(self):
        print("=" * 48)
        print("       GOLIATH SECURITY PROTOCOL")
        print("              CORE ENGINE")
        print("=" * 48)

        print(f"\n[+] Version: {self.version}")
        print(f"[+] Operating System: {self.system}")
        print(f"[+] Python: {self.python}")
        print(f"[+] Executable: {sys.executable}")

        info("GOLIATH Core initialized")

        print("\n[+] CORE STATUS: RUNNING")
        print("=" * 48)

        return True

    def register_module(self, name, module):
        if name in self.modules:
            return False

        self.modules[name] = module
        info(f"Module registered: {name}")
        return True

    def get_status(self):
        return {
            "name": self.name,
            "version": self.version,
            "system": self.system,
            "python": self.python,
            "modules": list(self.modules.keys()),
            "status": "RUNNING"
        }