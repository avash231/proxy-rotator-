#!/bin/bash
echo "========================================="
echo "🔄 Proxy Rotator - One Line Installer"
echo "========================================="

if command -v python3 &> /dev/null; then
    PYTHON=python3
    PIP=pip3
else
    PYTHON=python
    PIP=pip
fi

echo "✅ Found "

echo ""
echo "📦 Cloning repository..."
if [ -d "proxy-rotator-" ]; then
    cd proxy-rotator-
    git pull
else
    git clone https://github.com/avash231/proxy-rotator-.git
    cd proxy-rotator-
fi

echo ""
echo "📦 Installing dependencies..."
 install --user -r requirements.txt

echo ""
echo "📦 Installing Proxy Rotator..."
 install --user -e .

echo ""
echo "========================================="
echo "✅ Installation Complete!"
echo "========================================="
echo ""
echo "Run the tool with: proxy-rotator"
