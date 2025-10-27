# detect-tools.ps1
# PowerShell script to detect development tools and generate configuration

param(
    [string]$OutputPath = "config/detected-tools.json"
)

# Import .NET assemblies for registry access
Add-Type -AssemblyName System.Management

Write-Host "Detecting development tools on Windows..." -ForegroundColor Cyan

# Tool detection results
$detectedTools = @{
    "timestamp" = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    "tools" = @{}
}

# Godot detection
function Find-Godot {
    Write-Host "`nSearching for Godot Engine..." -ForegroundColor Yellow
    
    $godotPaths = @()
    
    # Check registry (installed version)
    try {
        $regPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"
        $apps = Get-ItemProperty $regPath -ErrorAction SilentlyContinue
        
        foreach ($app in $apps) {
            if ($app.DisplayName -like "*Godot*") {
                $exePath = Join-Path $app.InstallLocation "godot.exe"
                if (Test-Path $exePath) {
                    $godotPaths += $exePath
                    Write-Host "  Found in registry: $exePath" -ForegroundColor Green
                }
            }
        }
    }
    catch {
        Write-Host "  Registry check failed: $_" -ForegroundColor DarkGray
    }
    
    # Check PATH environment variable
    $pathDirs = $env:Path -split ";"
    foreach ($dir in $pathDirs) {
        if ($dir) {
            $exePath = Join-Path $dir "godot.exe"
            if (Test-Path $exePath) {
                if ($godotPaths -notcontains $exePath) {
                    $godotPaths += $exePath
                    Write-Host "  Found in PATH: $exePath" -ForegroundColor Green
                }
            }
            # Also check for console version
            $consoleExe = Join-Path $dir "godot_console.exe"
            if (Test-Path $consoleExe) {
                if ($godotPaths -notcontains $consoleExe) {
                    $godotPaths += $consoleExe
                    Write-Host "  Found in PATH: $consoleExe" -ForegroundColor Green
                }
            }
        }
    }
    
    # Check common installation paths
    $commonPaths = @(
        "C:\Program Files\Godot",
        "C:\Program Files (x86)\Godot",
        "$env:LOCALAPPDATA\Godot",
        "$env:APPDATA\Godot",
        "C:\Godot",
        "D:\Godot"
    )
    
    foreach ($basePath in $commonPaths) {
        if (Test-Path $basePath) {
            $exes = Get-ChildItem -Path $basePath -Filter "godot*.exe" -Recurse -ErrorAction SilentlyContinue
            foreach ($exe in $exes) {
                if ($godotPaths -notcontains $exe.FullName) {
                    $godotPaths += $exe.FullName
                    Write-Host "  Found in common path: $($exe.FullName)" -ForegroundColor Green
                }
            }
        }
    }
    
    # Check Steam installation
    $steamPath = "C:\Program Files (x86)\Steam\steamapps\common\Godot"
    if (Test-Path $steamPath) {
        $exes = Get-ChildItem -Path $steamPath -Filter "godot*.exe" -ErrorAction SilentlyContinue
        foreach ($exe in $exes) {
            if ($godotPaths -notcontains $exe.FullName) {
                $godotPaths += $exe.FullName
                Write-Host "  Found in Steam: $($exe.FullName)" -ForegroundColor Green
            }
        }
    }
    
    if ($godotPaths.Count -eq 0) {
        Write-Host "  No Godot installations found" -ForegroundColor Red
        return $null
    }
    
    # Get version from first found executable
    $firstExe = $godotPaths[0]
    $version = "unknown"
    
    try {
        $versionOutput = & $firstExe --version 2>&1 | Out-String
        if ($versionOutput -match "v?(\d+\.\d+(\.\d+)?)") {
            $version = $matches[1]
            Write-Host "  Version: $version" -ForegroundColor Cyan
        }
    }
    catch {
        Write-Host "  Could not determine version" -ForegroundColor DarkGray
    }
    
    return @{
        "name" = "Godot Engine"
        "version" = $version
        "paths" = $godotPaths
        "primary_path" = $godotPaths[0]
    }
}

# Blender detection
function Find-Blender {
    Write-Host "`nSearching for Blender..." -ForegroundColor Yellow
    
    $blenderPaths = @()
    
    # Check registry
    try {
        $regPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"
        $apps = Get-ItemProperty $regPath -ErrorAction SilentlyContinue
        
        foreach ($app in $apps) {
            if ($app.DisplayName -like "*Blender*") {
                $exePath = Join-Path $app.InstallLocation "blender.exe"
                if (Test-Path $exePath) {
                    $blenderPaths += $exePath
                    Write-Host "  Found in registry: $exePath" -ForegroundColor Green
                }
            }
        }
    }
    catch {
        Write-Host "  Registry check failed: $_" -ForegroundColor DarkGray
    }
    
    # Check PATH
    $pathDirs = $env:Path -split ";"
    foreach ($dir in $pathDirs) {
        if ($dir) {
            $exePath = Join-Path $dir "blender.exe"
            if (Test-Path $exePath) {
                if ($blenderPaths -notcontains $exePath) {
                    $blenderPaths += $exePath
                    Write-Host "  Found in PATH: $exePath" -ForegroundColor Green
                }
            }
        }
    }
    
    # Check common paths
    $commonPaths = @(
        "C:\Program Files\Blender Foundation",
        "C:\Program Files (x86)\Blender Foundation",
        "$env:LOCALAPPDATA\Programs\Blender Foundation",
        "C:\Blender"
    )
    
    foreach ($basePath in $commonPaths) {
        if (Test-Path $basePath) {
            $exes = Get-ChildItem -Path $basePath -Filter "blender.exe" -Recurse -ErrorAction SilentlyContinue
            foreach ($exe in $exes) {
                if ($blenderPaths -notcontains $exe.FullName) {
                    $blenderPaths += $exe.FullName
                    Write-Host "  Found in common path: $($exe.FullName)" -ForegroundColor Green
                }
            }
        }
    }
    
    if ($blenderPaths.Count -eq 0) {
        Write-Host "  No Blender installations found" -ForegroundColor Red
        return $null
    }
    
    # Get version
    $firstExe = $blenderPaths[0]
    $version = "unknown"
    
    try {
        $versionOutput = & $firstExe --version 2>&1 | Out-String
        if ($versionOutput -match "Blender (\d+\.\d+(\.\d+)?)") {
            $version = $matches[1]
            Write-Host "  Version: $version" -ForegroundColor Cyan
        }
    }
    catch {
        Write-Host "  Could not determine version" -ForegroundColor DarkGray
    }
    
    return @{
        "name" = "Blender"
        "version" = $version
        "paths" = $blenderPaths
        "primary_path" = $blenderPaths[0]
    }
}

# GIMP detection
function Find-GIMP {
    Write-Host "`nSearching for GIMP..." -ForegroundColor Yellow
    
    $gimpPaths = @()
    
    # Check registry
    try {
        $regPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"
        $apps = Get-ItemProperty $regPath -ErrorAction SilentlyContinue
        
        foreach ($app in $apps) {
            if ($app.DisplayName -like "*GIMP*") {
                $exePath = Join-Path $app.InstallLocation "bin\gimp-2.10.exe"
                if (Test-Path $exePath) {
                    $gimpPaths += $exePath
                    Write-Host "  Found in registry: $exePath" -ForegroundColor Green
                }
            }
        }
    }
    catch {
        Write-Host "  Registry check failed: $_" -ForegroundColor DarkGray
    }
    
    # Check common paths
    $commonPaths = @(
        "C:\Program Files\GIMP 2\bin",
        "C:\Program Files (x86)\GIMP 2\bin",
        "$env:LOCALAPPDATA\Programs\GIMP 2\bin"
    )
    
    foreach ($basePath in $commonPaths) {
        if (Test-Path $basePath) {
            $exes = Get-ChildItem -Path $basePath -Filter "gimp-*.exe" -ErrorAction SilentlyContinue
            foreach ($exe in $exes) {
                if ($gimpPaths -notcontains $exe.FullName) {
                    $gimpPaths += $exe.FullName
                    Write-Host "  Found in common path: $($exe.FullName)" -ForegroundColor Green
                }
            }
        }
    }
    
    if ($gimpPaths.Count -eq 0) {
        Write-Host "  No GIMP installations found" -ForegroundColor Red
        return $null
    }
    
    # Get version
    $firstExe = $gimpPaths[0]
    $version = "unknown"
    
    try {
        $versionOutput = & $firstExe --version 2>&1 | Out-String
        if ($versionOutput -match "version (\d+\.\d+(\.\d+)?)") {
            $version = $matches[1]
            Write-Host "  Version: $version" -ForegroundColor Cyan
        }
    }
    catch {
        Write-Host "  Could not determine version" -ForegroundColor DarkGray
    }
    
    return @{
        "name" = "GIMP"
        "version" = $version
        "paths" = $gimpPaths
        "primary_path" = $gimpPaths[0]
    }
}

# Run detection for all tools
$godot = Find-Godot
if ($godot) {
    $detectedTools.tools["godot"] = $godot
}

$blender = Find-Blender
if ($blender) {
    $detectedTools.tools["blender"] = $blender
}

$gimp = Find-GIMP
if ($gimp) {
    $detectedTools.tools["gimp"] = $gimp
}

# Save results to JSON
Write-Host "`nSaving results to $OutputPath..." -ForegroundColor Cyan

# Ensure config directory exists
$configDir = Split-Path -Path $OutputPath -Parent
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

# Convert to JSON with proper formatting
$json = $detectedTools | ConvertTo-Json -Depth 10
$json | Set-Content -Path $OutputPath -Encoding UTF8

Write-Host "Detection complete! Found $($detectedTools.tools.Count) tools." -ForegroundColor Green

# Display summary
Write-Host "`nSummary:" -ForegroundColor Cyan
foreach ($tool in $detectedTools.tools.Keys) {
    $info = $detectedTools.tools[$tool]
    Write-Host "  $($info.name) $($info.version) - $($info.primary_path)" -ForegroundColor White
}

exit 0
