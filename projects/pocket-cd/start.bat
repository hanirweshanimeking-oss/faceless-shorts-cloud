@echo off
title Pocket Creator Director (Pocket CD) Server
echo =========================================================================
echo   POCKET CREATOR DIRECTOR (POCKET CD)
echo   Autonomous AI Video Director, 11 Modular Ingredients & Gyan FFmpeg
echo =========================================================================

cd /d "c:\Users\DESKTOP\Downloads\money\pocket-cd"

set PYTHON_BIN="C:\Users\DESKTOP\AppData\Local\Programs\Python\Python311\python.exe"
set FFMPEG_BIN="C:\Users\DESKTOP\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"

echo [Pocket CD] Checking Python 3.11...
%PYTHON_BIN% --version
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.11 executable not found at %PYTHON_BIN%
    pause
    exit /b 1
)

echo [Pocket CD] Checking Gyan FFmpeg 9.0.2...
%FFMPEG_BIN% -version | findstr "ffmpeg version"

echo [Pocket CD] Starting FastAPI server on http://127.0.0.1:8000 ...
start "" http://127.0.0.1:8000

%PYTHON_BIN% -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
pause
