#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/Rudeboy4412/GOLIATH-Security-Protocol.git"
INSTALL_DIR="/opt/goliath"

echo "=================================="
echo "   GOLIATH SECURITY PROTOCOL"
echo "        INSTALADOR LINUX"
echo "=================================="

if [ "$EUID" -ne 0 ]; then
    echo "Ejecuta este instalador con sudo."
    exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
    echo "Este instalador requiere Debian, Ubuntu o Kali Linux."
    exit 1
fi

echo "[1/4] Instalando dependencias..."
apt-get update
apt-get install -y git python3 python3-venv

echo "[2/4] Descargando GOLIATH..."
if [ -d "$INSTALL_DIR/.git" ]; then
    git -C "$INSTALL_DIR" pull --ff-only
else
    rm -rf "$INSTALL_DIR"
    git clone "$REPO" "$INSTALL_DIR"
fi

echo "[3/4] Preparando entorno Python..."
python3 -m venv "$INSTALL_DIR/venv"

if [ -f "$INSTALL_DIR/requirements.txt" ]; then
    "$INSTALL_DIR/venv/bin/pip" install -r "$INSTALL_DIR/requirements.txt"
fi

echo "[4/4] Creando comando..."
cat > /usr/local/bin/goliath <<'EOF'
#!/usr/bin/env bash
exec /opt/goliath/venv/bin/python /opt/goliath/main.py "$@"
EOF

chmod +x /usr/local/bin/goliath

echo "=================================="
echo "GOLIATH instalado correctamente."
echo "Ejecuta: goliath"
echo "=================================="
