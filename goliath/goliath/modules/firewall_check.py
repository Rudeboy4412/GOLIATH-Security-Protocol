from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime


def analyze_portal(url):
    print("\n[+] Conectando con el portal...")

    request = Request(
        url,
        headers={"User-Agent": "GOLIATH-SECURITY/0.1.0"},
        method="GET"
    )

    try:
        try:
            response = urlopen(request, timeout=10)
        except HTTPError as error:
            response = error

        with response:
            status = response.status
            headers = response.headers
            final_url = response.url

        print(f"[OK] HTTP Status: {status}")
        print(f"[OK] URL: {final_url}")

        checks = [
            (
                "Content-Security-Policy",
                bool(headers.get("Content-Security-Policy"))
            ),
            (
                "X-Content-Type-Options",
                headers.get("X-Content-Type-Options", "").lower()
                == "nosniff"
            ),
            (
                "X-Frame-Options / CSP frame-ancestors",
                bool(headers.get("X-Frame-Options"))
                or "frame-ancestors" in
                headers.get("Content-Security-Policy", "").lower()
            ),
            (
                "Referrer-Policy",
                bool(headers.get("Referrer-Policy"))
            ),
            (
                "Permissions-Policy",
                bool(headers.get("Permissions-Policy"))
            )
        ]

        secure_connection = final_url.lower().startswith("https://")

        if secure_connection:
            checks.append((
                "Strict-Transport-Security",
                bool(headers.get("Strict-Transport-Security"))
            ))
        else:
            print("[!!] El portal utiliza HTTP, no HTTPS.")

        print("\n========== SECURITY AUDIT ==========")

        passed = 0

        for name, result in checks:
            if result:
                print(f"[OK] {name}")
                passed += 1
            else:
                print(f"[!!] {name}: No detectado")

        total = len(checks)
        percentage = round((passed / total) * 100)

        print("\n========== DIAGNOSTIC ==========")
        print(f"Protecciones detectadas: {passed}/{total}")
        print(f"Resultado: {percentage}%")

        if percentage == 100:
            print("[OK] Todas las comprobaciones pasaron.")
        elif percentage >= 60:
            print("[!!] Configuracion incompleta.")
        else:
            print("[!!] Se necesitan mejoras de seguridad.")

        print("\n[+] Analisis terminado.")
        print("[!] Este analisis no verifica el firewall de red.")

    except (URLError, OSError, ValueError) as error:
        print(f"\n[ERROR] No se pudo analizar el portal: {error}")


def run():
    print("\n" + "=" * 46)
    print("       GOLIATH FIREWALL CHECK")
    print("              CORE 0.1.0")
    print("=" * 46)

    print(f"\n[+] Fecha: {datetime.now()}")

    url = input(
        "\nDireccion del portal "
        ": "
    ).strip()

    if not url:
        url = ""

    if not url.startswith(("http://", "https://")):
        print("[ERROR] Direccion HTTP/HTTPS invalida.")
    else:
        analyze_portal(url)

    input("\nPresiona ENTER para regresar...")


if __name__ == "__main__":
    run()