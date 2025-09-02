@echo off
REM NeuroWeave Knowledge Graph - Docker Build Script for Windows
REM This script builds the Docker image for the NeuroWeave application

echo =============================================================
echo 🧠 NeuroWeave Knowledge Graph - Docker Build
echo =============================================================

echo.
echo 🔧 Building Docker image...
docker build -t neuroweave-knowledge-graph:latest .

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ Docker image built successfully!
    echo 📦 Image name: neuroweave-knowledge-graph:latest
    echo.
    echo 🚀 To run the container, use:
    echo    docker-run.bat
    echo.
    echo 🐳 Or with Docker Compose:
    echo    docker-compose up -d
) else (
    echo.
    echo ❌ Docker build failed!
    echo Please check the error messages above.
)

echo.
echo =============================================================
pause