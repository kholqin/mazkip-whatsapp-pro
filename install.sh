#!/bin/bash
R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'
C='\033[0;36m'; W='\033[0m'; H='\033[1m'

echo -e "${R}${H}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║   MAZKIP WHATSAPP PRO v2.0 — INSTALLER                  ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${W}"

echo -e "${Y}[*] Memulai instalasi...${W}"

if [[ "$OSTYPE" == "linux-android" ]]; then
    pkg update -y && pkg upgrade -y
    pkg install python python-pip git termux-api curl wget -y
else
    sudo apt update -y
    sudo apt install python3 python3-pip git curl wget -y
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
pip install --upgrade pip 2>/dev/null
pip install -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || pip3 install -r "$SCRIPT_DIR/requirements.txt"

if [[ "$OSTYPE" == "linux-android" ]]; then
    echo -e "${C}[*] Setup chromedriver...${W}"
    mkdir -p $PREFIX/tmp/chromedriver
    cd $PREFIX/tmp/chromedriver
    curl -sL "https://github.com/joanmassot/termux-chromedriver/releases/download/latest/chromedriver_arm64.zip" -o chromedriver.zip 2>/dev/null
    unzip -o chromedriver.zip 2>/dev/null
    chmod +x chromedriver 2>/dev/null
    cp chromedriver $PREFIX/bin/ 2>/dev/null || true
    cd "$SCRIPT_DIR"
fi

mkdir -p modules payloads sessions output
touch modules/__init__.py
touch payloads/.gitkeep sessions/.gitkeep output/.gitkeep

cat > config.json << 'EOF'
{
    "default_mode": "clipboard",
    "delay_between_messages": 2,
    "max_messages_per_session": 500,
    "use_proxy": false,
    "proxy_list": [],
    "session_persistence": true,
    "auto_rotate_vectors": true
}
EOF

echo -e "${G}${H}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║   ✅ INSTALASI SELESAI!                                 ║"
echo "║   Jalankan: python mwp.py                                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${W}"
