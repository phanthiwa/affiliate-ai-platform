@echo off
title Affiliate Growth OS Launcher
echo ===================================================
echo   Affiliate Growth OS (ระบบ AI ผลิตคลิปนายหน้า 15 คลิป/วัน)
echo ===================================================
echo.
echo [1/2] Starting Backend API on http://localhost:8000 ...
start "Backend API" cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

echo [2/2] Starting Frontend Studio on http://localhost:3001 ...
start "Frontend Studio" cmd /k "cd frontend && npm run dev"

echo.
echo All services launched!
echo Waiting for servers to initialize...
timeout /t 4 /nobreak > nul

echo Opening browser at http://localhost:3001 ...
start http://localhost:3001

echo.
echo ===================================================
echo   ระบบพร้อมใช้งานแล้วบนเบราว์เซอร์ของคุณ!
echo ===================================================
