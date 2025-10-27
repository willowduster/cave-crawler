# stop-all-servers.ps1
# PowerShell script to stop all running MCP servers

param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "Stopping MCP Servers..." -ForegroundColor Cyan

# Check for saved PIDs
$pidsFile = "logs/server-pids.json"

if (-not (Test-Path $pidsFile)) {
    Write-Host "No running servers found (no PID file)" -ForegroundColor Yellow
    
    # Try to find processes anyway
    Write-Host "`nSearching for orphaned MCP server processes..." -ForegroundColor Gray
    
    $mcpProcesses = Get-Process -Name "python*" -ErrorAction SilentlyContinue | Where-Object {
        $_.CommandLine -like "*servers.*_server*"
    }
    
    if ($mcpProcesses.Count -eq 0) {
        Write-Host "No MCP server processes found" -ForegroundColor Green
        exit 0
    }
    
    Write-Host "Found $($mcpProcesses.Count) possible MCP processes" -ForegroundColor Yellow
    
    if (-not $Force) {
        $confirm = Read-Host "Stop these processes? (y/N)"
        if ($confirm -ne "y" -and $confirm -ne "Y") {
            Write-Host "Cancelled" -ForegroundColor Gray
            exit 0
        }
    }
    
    foreach ($proc in $mcpProcesses) {
        try {
            Write-Host "  Stopping PID $($proc.Id)..." -ForegroundColor Yellow
            $proc.Kill()
            Write-Host "  Stopped PID $($proc.Id)" -ForegroundColor Green
        }
        catch {
            Write-Host "  Failed to stop PID $($proc.Id): $_" -ForegroundColor Red
        }
    }
    
    exit 0
}

# Load PIDs from file
try {
    $pids = Get-Content $pidsFile -Raw | ConvertFrom-Json
}
catch {
    Write-Host "ERROR: Failed to parse PID file: $_" -ForegroundColor Red
    exit 1
}

# Stop each server
$stopped = 0
$failed = 0

foreach ($serverName in $pids.PSObject.Properties.Name) {
    $processId = $pids.$serverName
    
    Write-Host "  [$serverName] Stopping (PID: $processId)..." -ForegroundColor Yellow
    
    try {
        $process = Get-Process -Id $processId -ErrorAction Stop
        
        if ($Force) {
            $process.Kill()
        }
        else {
            $process.CloseMainWindow() | Out-Null
            
            # Wait up to 5 seconds for graceful shutdown
            $waited = 0
            while (-not $process.HasExited -and $waited -lt 5) {
                Start-Sleep -Milliseconds 500
                $waited += 0.5
            }
            
            # Force kill if still running
            if (-not $process.HasExited) {
                Write-Host "    Process did not exit gracefully, forcing..." -ForegroundColor Yellow
                $process.Kill()
            }
        }
        
        # Wait for process to fully exit
        $process.WaitForExit(2000) | Out-Null
        
        Write-Host "  [$serverName] Stopped" -ForegroundColor Green
        $stopped++
    }
    catch [Microsoft.PowerShell.Commands.ProcessCommandException] {
        Write-Host "  [$serverName] Not running" -ForegroundColor DarkGray
    }
    catch {
        Write-Host "  [$serverName] ERROR: Failed to stop: $_" -ForegroundColor Red
        $failed++
    }
}

# Clean up PID file
Remove-Item $pidsFile -Force -ErrorAction SilentlyContinue

# Summary
Write-Host "`nSummary:" -ForegroundColor Cyan
Write-Host "  Stopped: $stopped" -ForegroundColor Green
if ($failed -gt 0) {
    Write-Host "  Failed: $failed" -ForegroundColor Red
}

Write-Host "`nAll servers stopped." -ForegroundColor Green
exit 0
