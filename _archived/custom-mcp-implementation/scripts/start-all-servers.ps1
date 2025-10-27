# start-all-servers.ps1
# PowerShell script to start all enabled MCP servers

param(
    [string]$ConfigPath = "config/mcp-config.json",
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

Write-Host "Starting MCP Servers..." -ForegroundColor Cyan
Write-Host "Config: $ConfigPath`n" -ForegroundColor Gray

# Check if config exists
if (-not (Test-Path $ConfigPath)) {
    Write-Host "ERROR: Configuration file not found: $ConfigPath" -ForegroundColor Red
    Write-Host "Please create a configuration file or run detect-tools.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Load configuration
try {
    $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
}
catch {
    Write-Host "ERROR: Failed to parse configuration: $_" -ForegroundColor Red
    exit 1
}

# Get Python executable from virtual environment
$pythonExe = ".\venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    Write-Host "ERROR: Python virtual environment not found" -ForegroundColor Red
    Write-Host "Please run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Track started servers
$startedServers = @()
$serverProcesses = @{}

# Function to start a server
function Start-MCPServer {
    param(
        [string]$ServerName,
        [object]$ServerConfig
    )
    
    if (-not $ServerConfig.enabled) {
        Write-Host "  [$ServerName] Disabled in configuration" -ForegroundColor DarkGray
        return $false
    }
    
    if (-not $ServerConfig.executable_path -or -not (Test-Path $ServerConfig.executable_path)) {
        Write-Host "  [$ServerName] ERROR: Executable not found: $($ServerConfig.executable_path)" -ForegroundColor Red
        return $false
    }
    
    Write-Host "  [$ServerName] Starting..." -ForegroundColor Yellow
    
    # Build command
    $logFile = "logs/$ServerName-mcp.log"
    $errorLog = "logs/$ServerName-error.log"
    
    # Ensure logs directory exists
    if (-not (Test-Path "logs")) {
        New-Item -ItemType Directory -Path "logs" -Force | Out-Null
    }
    
    # Start server process
    try {
        $arguments = @(
            "-m", "servers.$ServerName.${ServerName}_server",
            "--config", $ConfigPath
        )
        
        if ($Verbose) {
            $arguments += "--verbose"
        }
        
        $processInfo = Start-Process -FilePath $pythonExe `
            -ArgumentList $arguments `
            -WorkingDirectory (Get-Location) `
            -RedirectStandardOutput $logFile `
            -RedirectStandardError $errorLog `
            -PassThru `
            -NoNewWindow
        
        # Wait a moment to check if process started successfully
        Start-Sleep -Milliseconds 500
        
        if ($processInfo.HasExited) {
            Write-Host "  [$ServerName] ERROR: Process exited immediately" -ForegroundColor Red
            if (Test-Path $errorLog) {
                $errors = Get-Content $errorLog -Tail 5
                Write-Host "    Last errors: $errors" -ForegroundColor Red
            }
            return $false
        }
        
        $script:serverProcesses[$ServerName] = $processInfo
        Write-Host "  [$ServerName] Started (PID: $($processInfo.Id))" -ForegroundColor Green
        
        if ($ServerConfig.working_directory) {
            Write-Host "    Working dir: $($ServerConfig.working_directory)" -ForegroundColor Gray
        }
        
        return $true
    }
    catch {
        Write-Host "  [$ServerName] ERROR: Failed to start: $_" -ForegroundColor Red
        return $false
    }
}

# Start each enabled server
Write-Host "Starting servers..." -ForegroundColor Cyan

foreach ($serverName in $config.servers.PSObject.Properties.Name) {
    $serverConfig = $config.servers.$serverName
    
    if (Start-MCPServer -ServerName $serverName -ServerConfig $serverConfig) {
        $startedServers += $serverName
    }
}

# Summary
Write-Host "`nServer Status:" -ForegroundColor Cyan
Write-Host "  Started: $($startedServers.Count)" -ForegroundColor Green

if ($startedServers.Count -gt 0) {
    Write-Host "`nRunning servers:" -ForegroundColor White
    foreach ($server in $startedServers) {
        $process = $serverProcesses[$server]
        Write-Host "  - $server (PID: $($process.Id))" -ForegroundColor Gray
    }
    
    Write-Host "`nServers are running in the background." -ForegroundColor Cyan
    Write-Host "Use stop-all-servers.ps1 to stop them." -ForegroundColor Gray
    Write-Host "Logs are in the logs/ directory." -ForegroundColor Gray
    
    # Save PIDs to file for stop script
    $pidsFile = "logs/server-pids.json"
    $pids = @{}
    foreach ($server in $startedServers) {
        $pids[$server] = $serverProcesses[$server].Id
    }
    $pids | ConvertTo-Json | Set-Content -Path $pidsFile
    
    exit 0
}
else {
    Write-Host "No servers were started!" -ForegroundColor Red
    exit 1
}
