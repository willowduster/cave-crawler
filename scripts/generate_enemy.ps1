# Generate Enemy Sprites using PixelLab API
# Usage: .\scripts\generate_enemy.ps1 -Name "goblin" -Description "small brown goblin creature"

param(
    [Parameter(Mandatory=$true)]
    [string]$Name,
    
    [Parameter(Mandatory=$true)]
    [string]$Description,
    
    [string]$OutputDir = "assets/enemies",
    [int]$Size = 64
)

$pythonScript = ".\scripts\generate_enemy_pixellab.py"
$venvPython = ".\.venv\Scripts\python.exe"

Write-Host "Generating enemy: $Name" -ForegroundColor Cyan
Write-Host "Description: $Description" -ForegroundColor Gray
Write-Host ""

# Check if virtual environment Python exists
if (Test-Path $venvPython) {
    $pythonCmd = $venvPython
    Write-Host "Using virtual environment Python" -ForegroundColor Gray
} else {
    # Try to find python
    try {
        $pythonCmd = (Get-Command python -ErrorAction Stop).Source
        Write-Host "Using system Python" -ForegroundColor Yellow
    } catch {
        Write-Host "Error: Python not found. Please install Python 3.7+" -ForegroundColor Red
        exit 1
    }
}

# Check if pixellab library is installed
& $pythonCmd -c "import pixellab" 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing required Python packages..." -ForegroundColor Yellow
    & $pythonCmd -m pip install pixellab
}

# Run the generator
& $pythonCmd $pythonScript `
    --name $Name `
    --description $Description `
    --output-dir $OutputDir `
    --size $Size

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nEnemy sprites generated successfully!" -ForegroundColor Green
    Write-Host "Importing into Godot..." -ForegroundColor Cyan
    
    # Auto-import the new sprites
    .\scripts\import_assets.ps1 -WaitSeconds 10
    
    Write-Host "`nDone! Enemy '$Name' is ready to use." -ForegroundColor Green
} else {
    Write-Host "`nFailed to generate enemy sprites" -ForegroundColor Red
    exit 1
}
