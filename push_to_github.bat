@echo off
title Push Code to GitHub
echo ===================================================
echo   Pushing code to https://github.com/phanthiwa/affiliate-ai-platform.git
echo ===================================================
echo.
git remote remove origin 2>nul
git remote add origin https://github.com/phanthiwa/affiliate-ai-platform.git
git branch -M main
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo ===================================================
    echo   PUSH สำเร็จเรียบร้อยแล้ว! (SUCCESS)
    echo ===================================================
) else (
    echo [ERROR] หากเกิดข้อผิดพลาด ให้ตรวจสอบการล็อกอิน GitHub
)
pause
