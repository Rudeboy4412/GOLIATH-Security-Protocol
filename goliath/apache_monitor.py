import urllib.request
import urllib.error
import time
from urllib.parse import urlparse


def run():
    print("\n" + "=" * 42)
    print("       GOLIATH APACHE MONITOR")
    print("=" * 42)

    url = input("[?] Introduce la URL del portal: ").strip()

    if not url.startswith(("http://", "https://")):
        print("[-] Introduce una URL HTTP o HTTPS válida.")
        return

    try:
        parsed = urlparse(url)

        if not parsed.netloc:
            print("[-] URL no válida.")
            return

        print("\n[+] Conectando con el servidor...")

        start = time.perf_counter()

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "GOLIATH/0.1"}
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            elapsed = (time.perf_counter() - start) * 1000

            print("\n[+] SERVIDOR DISPONIBLE")
            print(f"[+] URL: {url}")
            print(f"[+] HTTP STATUS: {response.status}")
            print(f"[+] RESPONSE TIME: {elapsed:.2f} ms")

    except urllib.error.HTTPError as error:
        print(f"\n[!] El servidor respondió con HTTP {error.code}")

    except Exception as error:
        print(f"\n[-] Error de conexión: {error}")

    print("\n" + "=" * 42)
    input("Presiona ENTER para regresar a GOLIATH...")