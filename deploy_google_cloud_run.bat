@echo off
title Deploy to Google Cloud Run (Free Tier)
echo ===================================================
echo   Deploy Affiliate Growth OS to Google Cloud Run
echo   (Free Tier: Scales to 0 instances when idle = $0)
echo ===================================================
echo.

:: 1. Check if gcloud CLI is installed
where gcloud >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] gcloud CLI not found on this computer.
    echo.
    echo Please install Google Cloud CLI from:
    echo https://cloud.google.com/sdk/docs/install
    echo.
    echo Or you can deploy directly in your browser using Google Cloud Shell!
    echo See docs\GOOGLE_CLOUD_RUN_GUIDE.md for browser deployment steps.
    pause
    exit /b 1
)

echo [1/3] Setting Google Cloud Region to Singapore (asia-southeast1)...
set REGION=asia-southeast1

echo.
echo [2/3] Deploying Backend API to Cloud Run...
cd backend
call gcloud run deploy affiliate-backend --source . --region %REGION% --min-instances 0 --max-instances 2 --memory 512Mi --allow-unauthenticated --quiet

:: Get Backend URL
for /f "tokens=*" %%i in ('gcloud run services describe affiliate-backend --region %REGION% --format "value(status.url)"') do set BACKEND_URL=%%i
echo.
echo Backend deployed successfully at: %BACKEND_URL%
cd ..

echo.
echo [3/3] Deploying Frontend Studio to Cloud Run...
cd frontend
call gcloud run deploy affiliate-frontend --source . --region %REGION% --min-instances 0 --max-instances 2 --memory 512Mi --set-env-vars NEXT_PUBLIC_API_URL=%BACKEND_URL%/api/v1 --allow-unauthenticated --quiet

for /f "tokens=*" %%i in ('gcloud run services describe affiliate-frontend --region %REGION% --format "value(status.url)"') do set FRONTEND_URL=%%i
echo.
echo ===================================================
echo   DEPLOYMENT COMPLETE! (สำเร็จเรียบร้อย)
echo ===================================================
echo.
echo Your Live Dashboard URL: %FRONTEND_URL%
echo Your Live Backend API URL: %BACKEND_URL%
echo.
echo Opening your live Web App in browser...
start %FRONTEND_URL%
pause
