@echo off
setlocal
set "ROOT=%~dp0"
set "PLAYWRIGHT_BROWSERS_PATH=%ROOT%ms-playwright"
cd /d "%ROOT%"

if exist ".\url2pdf-run.exe" (
  powershell -NoExit -ExecutionPolicy Bypass -Command "& '.\url2pdf-run.exe'"
) else (
  echo [WARN] url2pdf-run.exe not found in current folder.
  echo [INFO] Fallback to python interactive mode.
  powershell -NoExit -ExecutionPolicy Bypass -Command "if (Test-Path '.\.venv\Scripts\python.exe') { & '.\.venv\Scripts\python.exe' -m app.interactive } else { python -m app.interactive }"
)
