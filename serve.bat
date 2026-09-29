@echo off
title RestBox Local Server
echo ========================================================
echo   RestBox - Gruvbox Dark API Client ^& cURL Executor
echo ========================================================
echo.
echo Menjalankan RestBox di local server...
echo.
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Menjalankan server Python dengan Local CORS Proxy...
    python server.py 8000
    if %errorlevel% equ 0 goto done
)

where npx >nul 2>&1
if %errorlevel% equ 0 (
    echo Menjalankan via npx serve...
    npx serve restbox
    if %errorlevel% equ 0 goto done
)

echo Mencoba python http.server bawaan...
python -m http.server 8000 -d restbox

:done
pause
