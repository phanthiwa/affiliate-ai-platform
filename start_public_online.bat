@echo off
title Affiliate Growth OS - Online Public Launcher
echo ===================================================
echo   Affiliate Growth OS (Public Online Link Generator)
echo   (ฟรี 100% ไม่ต้องมี Server, ไม่ต้องผูกบัตรเครดิต)
echo ===================================================
echo.

echo [1/3] Starting Backend API on port 8000...
start "Backend API" cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

echo [2/3] Starting Frontend Studio on port 3001...
start "Frontend Studio" cmd /k "cd frontend && npm run dev"

timeout /t 5 /nobreak > nul

echo [3/3] Creating Free Public HTTPS Tunnel...
echo.
echo กำลังสร้างลิงก์ออนไลน์สำหรับเปิดผ่านมือถือ/อุปกรณ์อื่นๆ...
echo.
npx localtunnel --port 3001
pause
