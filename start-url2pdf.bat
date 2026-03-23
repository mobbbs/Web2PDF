@echo off
setlocal
set "ROOT=%~dp0"

powershell -NoExit -ExecutionPolicy Bypass -Command ^
  "Set-Location -LiteralPath '%ROOT%';" ^
  "if (Test-Path '.\.venv\Scripts\python.exe') {" ^
  "  & '.\.venv\Scripts\python.exe' -m app.interactive" ^
  "} else {" ^
  "  python -m app.interactive" ^
  "}"
