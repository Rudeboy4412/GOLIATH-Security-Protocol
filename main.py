from goliath.core import GoliathCore

from goliath.modules import (
    apache_monitor,
    file_scan,
    firewall_check,
    security_audit
)

def main():
    core = GoliathCore()
    core.initialize()

    modules = {
        "1": ("Apache Monitor", apache_monitor),
        "2": ("File Scanner", file_scan),
        "3": ("Firewall Check", firewall_check),
        "4": ("Security Audit", security_audit)
    }

    for name, module in modules.values():
        core.register_module(name, module)

    while True:
        print("\n" + "=" * 42)
        print("       GOLIATH SECURITY PROTOCOL")
        print("=" * 42)
        print("[1] Apache Monitor")
        print("[2] File Scanner")
        print("[3] Firewall Check")
        print("[4] Security Audit")
        print("[0] Salir")
        print("=" * 42)

        option = input("GOLIATH >> ").strip()

        if option in modules:
            name, module = modules[option]
            print(f"\n[+] {name}")

            try:
                module.run()
            except Exception as error:
                print(f"[-] Error: {error}")

        elif option == "0":
            print("\n[GOLIATH] Cerrando sistema...")
            break

        else:
            print("\n[-] Opción no válida.")


if __name__ == "__main__":
    main()