# Portable Blender script runner
# Usage: .\scripts\run_blender.ps1 <blender_script.py>
#
# This script finds the Blender executable in ./bin/ and runs the specified Python script

param(
    [Parameter(Mandatory=$true)]
    [string]$BlenderScript
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$BinDir = Join-Path $ProjectRoot "bin"

# Find Blender executable in bin directory
$BlenderExe = Get-ChildItem -Path $BinDir -Filter "blender.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if (-not $BlenderExe) {
    Write-Host "ERROR: Blender executable not found in ./bin/" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Blender to ./bin/ directory:" -ForegroundColor Yellow
    Write-Host "  1. Download Blender 4.5+ portable from https://www.blender.org/download/"
    Write-Host "  2. Extract to: ./bin/blender-4.x.x-windows-x64/"
    Write-Host "  3. Executable should be at: ./bin/blender-4.x.x-windows-x64/blender.exe"
    Write-Host ""
    Write-Host "Example structure:" -ForegroundColor Cyan
    Write-Host "  cave-crawler/"
    Write-Host "    bin/"
    Write-Host "      blender-4.5.0-windows-x64/"
    Write-Host "        blender.exe  <-- Found here"
    Write-Host "      Godot_v4.5.1-stable_win64.exe"
    exit 1
}

Write-Host "Found Blender: $($BlenderExe.FullName)" -ForegroundColor Green

# Resolve the script path
$BlenderScriptsDir = Join-Path $ProjectRoot "blender_scripts"
$ScriptPath = Join-Path $BlenderScriptsDir $BlenderScript

if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: Script not found: $ScriptPath" -ForegroundColor Red
    Write-Host "Looking in: $BlenderScriptsDir" -ForegroundColor Yellow
    exit 1
}

Write-Host "Running: $BlenderScript" -ForegroundColor Cyan
Write-Host "Script path: $ScriptPath" -ForegroundColor Gray
& $BlenderExe.FullName --background --python "$ScriptPath"
