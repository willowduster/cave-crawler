# Import assets in Godot and automatically close the editor
# Usage: .\scripts\import_assets.ps1 [-WaitSeconds 10]

param(
    [int]$WaitSeconds = 10,
    [string]$AssetPath = ""
)

$godotPath = ".\bin\Godot_v4.5.1-stable_win64.exe"
$projectPath = "."

Write-Host "Opening Godot editor to import assets..." -ForegroundColor Cyan

# Start Godot editor
$process = Start-Process -FilePath $godotPath -ArgumentList "--path", $projectPath, "--editor" -PassThru

# Monitor for import completion
Write-Host "Waiting for asset imports to complete..." -ForegroundColor Yellow

# Initial wait for editor to start
Start-Sleep -Seconds 3

# Track the .godot/imported folder for changes
$importFolder = Join-Path $projectPath ".godot\imported"
$lastCount = 0

for ($i = 0; $i -lt $WaitSeconds; $i++) {
    Start-Sleep -Seconds 1
    
    if (Test-Path $importFolder) {
        $currentCount = (Get-ChildItem -Path $importFolder -Recurse -File -ErrorAction SilentlyContinue).Count
        
        # Show progress
        if ($currentCount -gt $lastCount) {
            Write-Host "  Importing... ($currentCount files imported)" -ForegroundColor Gray
            $lastCount = $currentCount
            # Reset counter if we're still importing
            $i = 0
        }
    }
}

# Give it a bit more time to finish any pending imports
Start-Sleep -Seconds 2

# Close Godot
Write-Host "Closing Godot editor..." -ForegroundColor Cyan
try {
    if (!$process.HasExited) {
        $process.CloseMainWindow() | Out-Null
        Start-Sleep -Seconds 1
        
        if (!$process.HasExited) {
            $process.Kill()
        }
    }
    Write-Host "Assets imported successfully!" -ForegroundColor Green
} catch {
    Write-Host "Note: Godot may have already closed" -ForegroundColor Yellow
}
