@echo off
title Proxy Rotator - Windows Installer
color 0A

echo =========================================
echo ?? Proxy Rotator - Windows Installer
echo =========================================
echo.

echo Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ? Python not found! Please install Python 3.6+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ? Python found!

echo.
echo ?? Cloning repository...
if exist proxy-rotator- (
    echo Directory exists, updating...
    cd proxy-rotator-
    git pull
) else (
    git clone https://github.com/avash231/proxy-rotator-.git
    cd proxy-rotator-
)

echo.
echo ?? Installing dependencies...
pip install --user -r requirements.txt

echo.
echo ?? Installing Proxy Rotator...
pip install --user -e .

echo.
echo =========================================
echo ? Installation Complete!
echo =========================================
echo.
echo Run the tool with: proxy-rotator
echo.
pause
