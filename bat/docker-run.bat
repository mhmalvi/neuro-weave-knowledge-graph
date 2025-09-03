@echo off
REM NeuroWeave Knowledge Graph - Docker Run Script for Windows
REM This script runs the Docker container for the NeuroWeave application

echo =============================================================
echo 🧠 NeuroWeave Knowledge Graph - Docker Run
echo =============================================================

REM Check if .env file exists
if not exist .env (
    echo.
    echo ⚠️  WARNING: .env file not found!
    echo    Copy .env.example to .env and add your API keys
    echo    cp .env.example .env
    echo.
    echo 📝 Required environment variables:
    echo    - OPENAI_API_KEY: Your OpenAI API key
    echo    - GITHUB_TOKEN: Your GitHub token ^(optional^)
    echo.
    pause
    exit /b 1
)

echo.
echo 🚀 Starting NeuroWeave container...
echo    Container name: neuroweave-app
echo    Port mapping: 8501:8501
echo    Environment: Loading from .env file

docker run -d ^
    --name neuroweave-app ^
    --env-file .env ^
    -p 8501:8501 ^
    -v neuroweave-visualizations:/app/static/visualizations ^
    -v neuroweave-temp:/app/temp_repos ^
    --restart unless-stopped ^
    neuroweave-knowledge-graph:latest

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ Container started successfully!
    echo.
    echo 🌐 Access your NeuroWeave app at:
    echo    http://localhost:8501
    echo.
    echo 📊 Useful Docker commands:
    echo    docker logs neuroweave-app          ^(view logs^)
    echo    docker stop neuroweave-app          ^(stop container^)
    echo    docker rm neuroweave-app            ^(remove container^)
    echo    docker exec -it neuroweave-app bash ^(access container shell^)
    echo.
    echo 🔍 Container status:
    docker ps --filter name=neuroweave-app
) else (
    echo.
    echo ❌ Failed to start container!
    echo Please check the error messages above.
)

echo.
echo =============================================================
pause