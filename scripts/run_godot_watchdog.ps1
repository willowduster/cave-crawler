param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$GodotArgs,
    [int]$TimeoutSeconds = 300,
    [int]$NoOutputTimeoutSeconds = 60,
    [string]$GodotBinary = ".\bin\Godot_v4.5.1-stable_win64.exe",
    [string]$LogDir = ".\logs",
    [string]$GodotArgsString = ""
)

if (-not $GodotArgs) { $GodotArgs = @() }

# Backwards-compatible single-string arg form. If the caller provided
# -GodotArgsString, split it into the array form; prefer explicit array
# passed via ValueFromRemainingArguments when available.
if ($GodotArgs.Count -eq 0 -and $GodotArgsString -ne "") {
    $GodotArgs = $GodotArgsString -split ' '
}

# Ensure log dir
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$logFileBase = Join-Path $LogDir "godot_watch_$timestamp"
$stdoutFile = "$logFileBase.stdout"
$stderrFile = "$logFileBase.stderr"
$combinedFile = "$logFileBase.log"

Write-Host "Starting Godot watchdog..." -ForegroundColor Cyan
Write-Host "Godot: $GodotBinary" -ForegroundColor Yellow
Write-Host "Args: $($GodotArgs -join ' ')" -ForegroundColor Gray
Write-Host "Timeout: $TimeoutSeconds s, No-output timeout: $NoOutputTimeoutSeconds s" -ForegroundColor Gray
Write-Host "Logs: $combinedFile" -ForegroundColor Gray

# Prepare process start info
$si = New-Object System.Diagnostics.ProcessStartInfo
$resolved = $null
try { $resolved = (Resolve-Path -LiteralPath $GodotBinary -ErrorAction Stop).ProviderPath } catch { $resolved = $GodotBinary }
$si.FileName = $resolved
$si.Arguments = $GodotArgs -join ' '
$si.UseShellExecute = $false
$si.RedirectStandardOutput = $true
$si.RedirectStandardError = $true
$si.CreateNoWindow = $true
try {
    $si.WorkingDirectory = (Get-Location).Path
} catch {
    # ignore
}

$proc = New-Object System.Diagnostics.Process
$proc.StartInfo = $si

$stdoutLines = New-Object System.Collections.Generic.List[string]
$stderrLines = New-Object System.Collections.Generic.List[string]

$lastOutputLock = New-Object object
$global:lastOutputTime = [DateTime]::UtcNow
$startTime = [DateTime]::UtcNow

# Handlers
$proc.add_OutputDataReceived({ param($o, $d)
    if ($d.Data -ne $null) {
        $line = $d.Data
        $stdoutLines.Add($line) | Out-Null
        Write-Host $line -ForegroundColor Gray
        [System.Threading.Monitor]::Enter($lastOutputLock)
        $global:lastOutputTime = [DateTime]::UtcNow
        [System.Threading.Monitor]::Exit($lastOutputLock)
    }
})
$proc.add_ErrorDataReceived({ param($o, $d)
    if ($d.Data -ne $null) {
        $line = $d.Data
        $stderrLines.Add($line) | Out-Null
        Write-Host $line -ForegroundColor Red
        [System.Threading.Monitor]::Enter($lastOutputLock)
        $global:lastOutputTime = [DateTime]::UtcNow
        [System.Threading.Monitor]::Exit($lastOutputLock)
    }
})

# Start
if (-not (Test-Path $GodotBinary)) {
    Write-Error "Godot binary not found at $GodotBinary"
    exit 2
}

$started = $false
try {
    $started = $proc.Start()
} catch {
    Write-Error "Failed to start process: $_"
    # write a minimal combined log for diagnosis
    $errMsg = "Watchdog: failed to Start() process: $_"
    try { $errMsg | Out-File -FilePath $combinedFile -Encoding utf8 } catch { }
    exit 3
}
if (-not $started) { Write-Error "Failed to start process."; exit 3 }
$proc.BeginOutputReadLine()
$proc.BeginErrorReadLine()

# Monitor loop
$exitReason = "exited"
while (-not $proc.HasExited) {
    Start-Sleep -Seconds 1
    $now = [DateTime]::UtcNow
    [void]([System.Threading.Monitor]::Enter($lastOutputLock))
    try { $lag = ($now - $lastOutputTime).TotalSeconds } finally { [System.Threading.Monitor]::Exit($lastOutputLock) }

    $runtime = ($now - $startTime).TotalSeconds
    if ($runtime -ge $TimeoutSeconds) {
        Write-Host "Timeout ($TimeoutSeconds s) reached — killing process" -ForegroundColor Yellow
        $exitReason = "timeout"
        try { $proc.Kill() } catch { }
        break
    }
    if ($lag -ge $NoOutputTimeoutSeconds) {
        Write-Host "No output for $lag seconds — assuming hang; killing process" -ForegroundColor Yellow
        $exitReason = "no_output_timeout"
        try { $proc.Kill() } catch { }
        break
    }
}

# Wait a short moment for streams to flush
Start-Sleep -Milliseconds 200

# Ensure the process is terminated if we decided to kill it or it didn't exit cleanly
function _ensure_process_terminated($p, $godotBinary, $combinedFile) {
    try {
        if ($p -and -not $p.HasExited) {
            try { $p.Kill() } catch { }
            # Wait a bit for it to die
            $p.WaitForExit(5000) | Out-Null
        }
    } catch {
        # ignore
    }

    # If still running, as a fallback try to terminate via Win32_Process (matches executable path)
    try {
        if ($p -and -not $p.HasExited) {
            $fullPath = ""
            try { $fullPath = (Get-Item $godotBinary).FullName } catch { $fullPath = $godotBinary }
            $procs = Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -and $_.ExecutablePath -ieq $fullPath }
            foreach ($x in $procs) {
                try {
                    $res = $x | Invoke-CimMethod -MethodName Terminate
                    Add-Content -Path $combinedFile -Value "Watchdog: Terminate called on PID $($x.ProcessId) result=$($res.ReturnValue)"
                } catch {
                    Add-Content -Path $combinedFile -Value "Watchdog: Failed to Terminate PID $($x.ProcessId): $_"
                }
            }
        }
    } catch {
        Add-Content -Path $combinedFile -Value "Watchdog: Win32 fallback failed: $_"
    }

    # Final wait and close
    try { if ($p) { $p.WaitForExit(2000) } } catch { }
    try { if ($p) { $p.Close(); $p.Dispose() } } catch { }
}

# Write logs to files
try {
    $stdoutLines | Out-File -FilePath $stdoutFile -Encoding utf8
    $stderrLines | Out-File -FilePath $stderrFile -Encoding utf8
    $combined = @()
    if (Test-Path $stdoutFile) { $combined += Get-Content $stdoutFile }
    $combined += "=== STDERR ==="
    if (Test-Path $stderrFile) { $combined += Get-Content $stderrFile }
    $combined | Out-File -FilePath $combinedFile -Encoding utf8
    Write-Host "Saved logs: $combinedFile" -ForegroundColor Cyan
} catch {
    Write-Warning "Failed to write logs: $_"
}

# Determine exit code
    $exitCode = 1
    if ($proc -and $proc.HasExited) { $exitCode = $proc.ExitCode }

# Annotate log with watchdog reason
Add-Content -Path $combinedFile -Value "\nWatchdog: exit_reason=$exitReason exit_code=$exitCode runtime_s=$runtime last_output_lag_s=$lag"

# Ensure process termination/cleanup
try { _ensure_process_terminated $proc $GodotBinary $combinedFile } catch { Add-Content -Path $combinedFile -Value "Watchdog: _ensure_process_terminated failed: $_" }

if ($exitReason -ne "exited") {
    Write-Host "Process ended due to $exitReason (exit_code=$exitCode)" -ForegroundColor Red
    exit 4
}

Write-Host "Process exited normally (exit_code=$exitCode)" -ForegroundColor Green
exit $exitCode
