param(
  [Parameter(Mandatory = $true)]
  [string]$Version
)

$ErrorActionPreference = "Stop"

if ($Version -notmatch '^\d+\.\d+\.\d+$') {
  throw "Version must be in semver format: X.Y.Z"
}

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$pyproject = Join-Path $Root "pyproject.toml"
$initFile = Join-Path $Root "app\__init__.py"

(Get-Content $pyproject -Raw) -replace 'version = "\d+\.\d+\.\d+"', "version = `"$Version`"" | Set-Content $pyproject -Encoding UTF8
(Get-Content $initFile -Raw) -replace '__version__ = "\d+\.\d+\.\d+"', "__version__ = `"$Version`"" | Set-Content $initFile -Encoding UTF8

git add pyproject.toml app/__init__.py
git commit -m "release: v$Version"
git tag "v$Version"

Write-Host "Release prepared:"
Write-Host "  commit: release: v$Version"
Write-Host "  tag: v$Version"
Write-Host ""
Write-Host "Next step:"
Write-Host "  git push origin HEAD --tags"
