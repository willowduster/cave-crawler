# Run Godot with full output logging to a timestamped file
# Usage: .\scripts\run_godot_logged.ps1 [godot_args...]
# Example: .\scripts\run_godot_logged.ps1 --path . scenes/levels/procedural_cave.tscn
# Example: .\scripts\run_godot_logged.ps1 --path . --editor

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$GodotArgs
)

$godotPath = ".\bin\Godot_v4.5.1-stable_win64.exe"
$logDir = ".\logs"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$logFile = Join-Path $logDir "godot_$timestamp.log"

# Create logs directory if it doesn't exist
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
    Write-Host "Created logs directory: $logDir" -ForegroundColor Green
}

Write-Host "Starting Godot with logging..." -ForegroundColor Cyan
Write-Host "Log file: $logFile" -ForegroundColor Yellow
Write-Host "Command: $godotPath $($GodotArgs -join ' ')" -ForegroundColor Gray
Write-Host ""

# Run Godot and capture all output
try {
    # Start the process and redirect output
    $process = Start-Process -FilePath $godotPath `
                            -ArgumentList $GodotArgs `
                            -NoNewWindow `
                            -RedirectStandardOutput "$logFile.stdout" `
                            -RedirectStandardError "$logFile.stderr" `
                            -PassThru `
                            -Wait
    
    # Combine stdout and stderr into single log file
    $output = @()
    if (Test-Path "$logFile.stdout") {
        $output += Get-Content "$logFile.stdout"
    }
    if (Test-Path "$logFile.stderr") {
        $output += "=== STDERR ===" 
        $output += Get-Content "$logFile.stderr"
    }
    
    $output | Set-Content $logFile
    
    # Clean up temp files
    Remove-Item "$logFile.stdout" -ErrorAction SilentlyContinue
    Remove-Item "$logFile.stderr" -ErrorAction SilentlyContinue
    
    $exitCode = $process.ExitCode
    
    Write-Host ""
    Write-Host "Godot exited with code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
    Write-Host "Full log saved to: $logFile" -ForegroundColor Cyan
    
    # Show last 20 lines of log
    Write-Host "`nLast 20 lines of output:" -ForegroundColor Yellow
    Get-Content $logFile -Tail 20 | ForEach-Object { Write-Host $_ -ForegroundColor Gray }
    
    # If there were errors, highlight them
    $errors = Select-String -Path $logFile -Pattern "ERROR|Error|error|FATAL|Fatal|fatal|crash|Crash|CRASH" -SimpleMatch
    if ($errors) {
        Write-Host "`n!!! Found $($errors.Count) error/warning lines in log !!!" -ForegroundColor Red
        Write-Host "Check $logFile for details" -ForegroundColor Red
    }
    
    exit $exitCode
    
} catch {
    Write-Host "Failed to run Godot: $_" -ForegroundColor Red
    exit 1
}
