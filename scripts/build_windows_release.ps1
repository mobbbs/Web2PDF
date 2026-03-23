param(
  [string]$Version = "dev"
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$ReleaseRoot = Join-Path $Root "release\windows"
$BundleRoot = Join-Path $ReleaseRoot "url2pdf-ai-reader-$Version-windows-x64"

if (Test-Path $ReleaseRoot) {
  Remove-Item -Recurse -Force $ReleaseRoot
}

python -m pip install -r requirements.txt
python -m pip install pyinstaller
python -m playwright install chromium

python -m PyInstaller `
  --noconfirm `
  --onefile `
  --name url2pdf-run `
  --collect-all playwright `
  app\interactive.py

New-Item -ItemType Directory -Force $BundleRoot | Out-Null
Copy-Item ".\dist\url2pdf-run.exe" "$BundleRoot\url2pdf-run.exe"
Copy-Item ".\start-url2pdf-release.bat" "$BundleRoot\start-url2pdf.bat"

$browserSource = Join-Path $env:LOCALAPPDATA "ms-playwright"
if (-not (Test-Path $browserSource)) {
  throw "ms-playwright not found at $browserSource"
}

Copy-Item $browserSource "$BundleRoot\ms-playwright" -Recurse

if (-not (Test-Path "$BundleRoot\url2pdf-run.exe")) {
  throw "Portable exe was not created: $BundleRoot\url2pdf-run.exe"
}

Compress-Archive -Path "$BundleRoot\*" -DestinationPath "$ReleaseRoot\url2pdf-ai-reader-$Version-windows-x64.zip" -Force

Write-Host "Release bundle created:"
Write-Host "  $ReleaseRoot\url2pdf-ai-reader-$Version-windows-x64.zip"
