@echo off
setlocal
set "ROOT=%~dp0"
set "PLAYWRIGHT_BROWSERS_PATH=%ROOT%ms-playwright"
cd /d "%ROOT%"

powershell -NoExit -ExecutionPolicy Bypass -Command "& '.\url2pdf-run.exe'"
