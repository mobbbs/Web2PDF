@echo off
setlocal
set "ROOT=%~dp0"
set "PLAYWRIGHT_BROWSERS_PATH=%ROOT%ms-playwright"
cd /d "%ROOT%"

if exist ".\url2pdf-run.exe" (
  ".\url2pdf-run.exe"
) else (
  if exist ".\.venv\Scripts\python.exe" (
    ".\.venv\Scripts\python.exe" -m app.interactive
  ) else (
    python -m app.interactive
  )
)

if errorlevel 1 (
  echo.
  echo [ERROR] Start failed. Press any key to exit.
  pause >nul
)
