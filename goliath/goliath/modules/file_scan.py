import os
from datetime import datetime

MEDIA_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp",
    ".bmp", ".svg", ".ico", ".tiff",
    ".mp4", ".mkv", ".avi", ".mov", ".webm",
    ".mp3", ".wav", ".ogg", ".flac", ".m4a"
}


def format_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"
    return f"{size / (1024 ** 3):.2f} GB"


def run():
    print("\n" + "=" * 50)
    print("          GOLIATH FILE SCAN")
    print("=" * 50)

    folder = input("\n[?] Introduce la ruta del portal: ")
    folder = folder.strip().strip('"')

    if not os.path.isdir(folder):
        print("\n[-] ERROR: Directorio no encontrado.")
        input("\nPresiona ENTER para regresar...")
        return

    total_files = 0
    total_size = 0
    errors = 0
    results = []

    print("\n[+] Iniciando escaneo multimedia...")
    print("[+] Analizando directorios...\n")

    for root, dirs, files in os.walk(folder):
        for filename in files:
            extension = os.path.splitext(filename)[1].lower()

            if extension not in MEDIA_EXTENSIONS:
                continue

            filepath = os.path.join(root, filename)

            try:
                size = os.path.getsize(filepath)

                total_files += 1
                total_size += size

                results.append({
                    "name": filename,
                    "extension": extension,
                    "size": size,
                    "path": filepath
                })

                print(f"[FILE] {filename}")
                print(f"  TYPE: {extension}")
                print(f"  SIZE: {format_size(size)}")
                print(f"  PATH: {filepath}")
                print("-" * 50)

            except OSError:
                errors += 1

    print("\n" + "=" * 50)
    print("             SCAN REPORT")
    print("=" * 50)
    print(f"FILES FOUND: {total_files}")
    print(f"TOTAL SIZE: {format_size(total_size)}")
    print(f"READ ERRORS: {errors}")
    print("=" * 50)

    save = input("\n[?] ¿Guardar informe? (s/n): ").strip().lower()

    if save == "s":
        report_path = os.path.join(folder, "goliath_scan_report.txt")

        try:
            with open(report_path, "w", encoding="utf-8") as report:
                report.write("GOLIATH FILE SCAN REPORT\n")
                report.write(f"Date: {datetime.now()}\n")
                report.write(f"Directory: {folder}\n\n")

                for item in results:
                    report.write(f"File: {item['name']}\n")
                    report.write(f"Type: {item['extension']}\n")
                    report.write(f"Size: {format_size(item['size'])}\n")
                    report.write(f"Path: {item['path']}\n")
                    report.write("-" * 40 + "\n")

                report.write(f"\nTotal files: {total_files}\n")
                report.write(f"Total size: {format_size(total_size)}\n")
                report.write(f"Errors: {errors}\n")

            print("\n[+] Informe guardado correctamente.")

        except OSError as error:
            print(f"\n[-] Error guardando informe: {error}")

    input("\nPresiona ENTER para regresar a GOLIATH...")


if __name__ == "__main__":
    run()