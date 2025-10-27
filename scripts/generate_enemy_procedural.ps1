# PowerShell wrapper to run the procedural generator using the project's virtualenv
param(
    [string]$Name,
    [string]$Description = "",
    [int]$Size = 64,
    [string]$OutputDir = "assets/enemies",
    [int]$Seed = 42
)

$venvPython = ".\.venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $pythonCmd = $venvPython
} else {
    $pythonCmd = (Get-Command python).Source
}

if (-not $Name) {
    Write-Host "Usage: .\generate_enemy_procedural.ps1 -Name goblin [-Description '...']"
    exit 1
}

$script = Join-Path $PSScriptRoot "generate_enemy_procedural.py"
& $pythonCmd $script --name $Name --description $Description --output-dir $OutputDir --size $Size --seed $Seed
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Procedural generation complete for $Name"
