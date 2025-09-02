@echo off
REM NeuroWeave Knowledge Graph - Docker Compose Script for Windows
REM This script uses Docker Compose to run the complete NeuroWeave stack

echo =============================================================
echo 🧠 NeuroWeave Knowledge Graph - Docker Compose
echo =============================================================

REM Check if .env file exists
if not exist .env (
    echo.
    echo ⚠️  WARNING: .env file not found!
    echo    Copy .env.example to .env and add your API keys
    echo    cp .env.example .env
    echo.
    pause
    exit /b 1
)

echo.
echo 🚀 Starting NeuroWeave with Docker Compose...
echo    Building images if needed...
echo    Starting all services...

docker-compose up -d --build

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ NeuroWeave stack started successfully!
    echo.
    echo 🌐 Access your app at:
    echo    http://localhost:8501
    echo.
    echo 📊 Service status:
    docker-compose ps
    echo.
    echo 🔧 Useful commands:
    echo    docker-compose logs -f           ^(view logs^)
    echo    docker-compose down              ^(stop all services^)
    echo    docker-compose restart           ^(restart services^)
    echo    docker-compose exec neuroweave-app bash ^(access app shell^)
) else (
    echo.
    echo ❌ Failed to start services!
    echo Please check the error messages above.
)

echo.
echo =============================================================
pause