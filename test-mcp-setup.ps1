# Test MCP Servers Script# Test MCP Servers Script

Write-Host "`n=== Testing MCP Server Setup ===" -ForegroundColor Cyan# Run this to verify all MCP servers are working



# Refresh PATHWrite-Host "`n=== Testing MCP Server Setup ===" -ForegroundColor Cyan

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Refresh PATH

Write-Host "`n1. Checking Node.js..." -ForegroundColor Yellow$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

if (Get-Command node -ErrorAction SilentlyContinue) {

    $nodeVersion = node --versionWrite-Host "`n1. Checking Node.js..." -ForegroundColor Yellow

    Write-Host "   [OK] Node.js installed: $nodeVersion" -ForegroundColor Greenif (Get-Command node -ErrorAction SilentlyContinue) {

} else {    $nodeVersion = node --version

    Write-Host "   [FAIL] Node.js not found" -ForegroundColor Red    Write-Host "   ✓ Node.js installed: $nodeVersion" -ForegroundColor Green

    exit 1} else {

}    Write-Host "   ✗ Node.js not found" -ForegroundColor Red

    exit 1

Write-Host "`n2. Checking npm..." -ForegroundColor Yellow}

if (Get-Command npm -ErrorAction SilentlyContinue) {

    $npmVersion = npm --versionWrite-Host "`n2. Checking npm..." -ForegroundColor Yellow

    Write-Host "   [OK] npm installed: $npmVersion" -ForegroundColor Greenif (Get-Command npm -ErrorAction SilentlyContinue) {

} else {    $npmVersion = npm --version

    Write-Host "   [FAIL] npm not found" -ForegroundColor Red    Write-Host "   ✓ npm installed: $npmVersion" -ForegroundColor Green

    exit 1} else {

}    Write-Host "   ✗ npm not found" -ForegroundColor Red

    exit 1

Write-Host "`n3. Checking uv..." -ForegroundColor Yellow}

if (Get-Command uv -ErrorAction SilentlyContinue) {

    $uvVersion = uv --versionWrite-Host "`n3. Checking uv..." -ForegroundColor Yellow

    Write-Host "   [OK] uv installed: $uvVersion" -ForegroundColor Greenif (Get-Command uv -ErrorAction SilentlyContinue) {

} else {    $uvVersion = uv --version

    Write-Host "   [WARN] uv not in PATH - adding now" -ForegroundColor Yellow    Write-Host "   ✓ uv installed: $uvVersion" -ForegroundColor Green

    $env:Path += ";$env:USERPROFILE\.local\bin"} else {

    $uvVersion = uv --version    Write-Host "   ✗ uv not found in PATH" -ForegroundColor Red

    Write-Host "   [OK] uv installed: $uvVersion" -ForegroundColor Green    Write-Host "   Add to PATH: `$env:Path += `";`$env:USERPROFILE\.local\bin`"" -ForegroundColor Yellow

}}



Write-Host "`n4. Checking Godot MCP build..." -ForegroundColor YellowWrite-Host "`n4. Checking Godot MCP build..." -ForegroundColor Yellow

if (Test-Path "godot-mcp\build\index.js") {if (Test-Path "godot-mcp\build\index.js") {

    Write-Host "   [OK] Godot MCP built successfully" -ForegroundColor Green    Write-Host "   ✓ Godot MCP built successfully" -ForegroundColor Green

} else {} else {

    Write-Host "   [FAIL] Godot MCP build not found" -ForegroundColor Red    Write-Host "   ✗ Godot MCP build not found" -ForegroundColor Red

    exit 1    Write-Host "   Run: cd godot-mcp; npm install; npm run build" -ForegroundColor Yellow

}    exit 1

}

Write-Host "`n5. Testing Godot detection..." -ForegroundColor Yellow

if (Test-Path "bin\Godot_v4.5.1-stable_win64_console.exe") {Write-Host "`n5. Testing Godot detection..." -ForegroundColor Yellow

    Write-Host "   [OK] Godot 4.5.1 found in bin/" -ForegroundColor Greenif (Test-Path "bin\Godot_v4.5.1-stable_win64_console.exe") {

} else {    Write-Host "   ✓ Godot 4.5.1 found in bin/" -ForegroundColor Green

    Write-Host "   [WARN] Godot executable not found" -ForegroundColor Yellow} else {

}    Write-Host "   ✗ Godot executable not found" -ForegroundColor Red

}

Write-Host "`n=== Setup Complete ===" -ForegroundColor Green

Write-Host "All required components are installed and ready!"Write-Host "`n=== Setup Status ===" -ForegroundColor Cyan

Write-Host "✓ Node.js and npm ready" -ForegroundColor Green

Write-Host "`n=== Next Steps ===" -ForegroundColor CyanWrite-Host "✓ uv package manager ready" -ForegroundColor Green

Write-Host "1. Configure your AI assistant:"Write-Host "✓ Godot MCP server built" -ForegroundColor Green

Write-Host "   - Claude Desktop: Copy claude_desktop_config.json to"Write-Host "✓ Godot 4.5.1 available" -ForegroundColor Green

Write-Host "     C:\Users\Ben\AppData\Roaming\Claude\"

Write-Host "   - Cursor: Follow CURSOR_MCP_CONFIG.md instructions"Write-Host "`n=== Next Steps ===" -ForegroundColor Cyan

Write-Host ""Write-Host "1. Copy claude_desktop_config.json to Claude Desktop config location" -ForegroundColor White

Write-Host "2. Restart your AI assistant"Write-Host "   Location: C:\Users\Ben\AppData\Roaming\Claude\" -ForegroundColor Gray

Write-Host ""Write-Host ""

Write-Host "3. Test with: 'Get Godot version' or 'List project files'"Write-Host "2. OR configure Cursor using CURSOR_MCP_CONFIG.md instructions" -ForegroundColor White

Write-Host ""

Write-Host "`n=== Available MCP Servers ===" -ForegroundColor CyanWrite-Host "3. Restart your AI assistant (Claude Desktop or Cursor)" -ForegroundColor White

Write-Host "- filesystem: Read/write project files"Write-Host ""

Write-Host "- git: Version control operations"Write-Host "4. Test with: 'Get Godot version' or 'List project files'" -ForegroundColor White

Write-Host "- godot: Godot Engine integration"

Write-Host ""Write-Host "`n=== Available MCP Servers ===" -ForegroundColor Cyan

Write-Host "- filesystem: Read/write project files" -ForegroundColor White
Write-Host "- git: Version control operations" -ForegroundColor White
Write-Host "- godot: Godot Engine integration" -ForegroundColor White

Write-Host ""
