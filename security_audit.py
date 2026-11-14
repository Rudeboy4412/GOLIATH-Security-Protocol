from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime
from urllib.parse import urljoin, urlparse


SENSITIVE_PATHS = [
    ".env",
    ".git/HEAD",
    "config.php",
    "backup.zip",
    "database.sql"
]


def check_portal(url):
    print("\n[1] PORTAL CONNECTIVITY")

    request = Request(
        url,
        headers={"User-Agent": "GOLIATH-SECURITY/0.1.0"}
    )

    try:
        response = urlopen(request, timeout=10)

        with response:
            status = response.status
            headers = response.headers
            final_url = response.url

        print(f"[OK] HTTP Status: {status}")
        print(f"[OK] Portal: {final_url}")

        return headers, final_url

    except HTTPError as error:
        print(f"[!!] HTTP Error: {error.code}")
        return error.headers, url

    except (URLError, OSError, ValueError) as error:
        print(f"[ERROR] Connection failed: {error}")
        return None, url


def check_https(url, headers):
    print("\n[2] HTTPS SECURITY")

    if urlparse(url).scheme == "https":
        print("[OK] HTTPS connection detected.")

        if headers.get("Strict-Transport-Security"):
            print("[OK] HSTS detected.")
        else:
            print("[!!] HSTS not detected.")

        return True

    print("[!!] Portal is using HTTP.")
    print("[!!] HTTPS protection is unavailable.")

    return False


def check_headers(headers):
    print("\n[3] HTTP SECURITY HEADERS")

    security_headers = {
        "Content-Security-Policy": "CSP",
        "X-Content-Type-Options": "MIME protection",
        "X-Frame-Options": "Clickjacking protection",
        "Referrer-Policy": "Referrer protection",
        "Permissions-Policy": "Browser permissions"
    }

    passed = 0

    for header, description in security_headers.items():
        value = headers.get(header)

        if value:
            print(f"[OK] {header}: {value}")
            passed += 1
        else:
            print(f"[!!] Missing: {header}")

    return passed, len(security_headers)


def check_sensitive_files(url):
    print("\n[4] SENSITIVE FILE EXPOSURE")

    exposed = 0

    for path in SENSITIVE_PATHS:
        target = urljoin(url.rstrip("/") + "/", path)

        request = Request(
            target,
            headers={"User-Agent": "GOLIATH-SECURITY/0.1.0"},
            method="GET"
        )

        try:
            response = urlopen(request, timeout=5)

            with response:
                status = response.status

            if status == 200:
                print(f"[!!] Review exposure: {path}")
                exposed += 1
            else:
                print(f"[OK] Not accessible: {path}")

        except HTTPError as error:
            if error.code in (401, 403, 404, 410):
                print(f"[OK] Not accessible: {path}")
            else:
                print(f"[??] Review {path}: HTTP {error.code}")

        except (URLError, OSError, ValueError) as error:
            print(f"[??] Could not verify {path}: {error}")

    return exposed


def run():
    print("\n" + "=" * 50)
    print("          GOLIATH SECURITY AUDIT")
    print("                  CORE 0.1.0")
    print("=" * 50)

    print(f"\n[+] Date: {datetime.now()}")

    url = input(
        "\nPortal URL: "
    ).strip()

    if not url:
        url = ""

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        print("\n[ERROR] Invalid portal URL.")
        input("\nPress ENTER to return...")
        return

    headers, final_url = check_portal(url)

    if headers is None:
        input("\nPress ENTER to return...")
        return

    https_ok = check_https(final_url, headers)

    header_passed, header_total = check_headers(headers)

    exposed = check_sensitive_files(final_url)

    print("\n" + "=" * 50)
    print("             FINAL AUDIT REPORT")
    print("=" * 50)

    total = header_total + 2
    passed = header_passed

    if https_ok:
        passed += 1

    if exposed == 0:
        passed += 1

    percentage = round((passed / total) * 100)

    print(f"\nSecurity checks passed: {passed}/{total}")
    print(f"Security score: {percentage}%")

    if exposed:
        print("[!!] Review potentially exposed files.")

    if percentage >= 80 and exposed == 0:
        print("[OK] Basic security checks look good.")
    elif percentage >= 50:
        print("[!!] Security improvements recommended.")
    else:
        print("[!!] Several security checks need attention.")

    print("\n[!] This is a basic security audit.")
    print("[!] It does not guarantee that the portal is secure.")
    print("\n[+] Audit completed.")

    input("\nPress ENTER to return...")


if __name__ == "__main__":
    run()