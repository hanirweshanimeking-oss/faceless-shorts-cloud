# Antigravity Stop Hook Interceptor (autonomous_loop.ps1)
# Controls autonomous continuation based on pending backlog items

try {
    $workspace = "C:\Users\DESKTOP\Downloads\money"
    $modeFlag = Join-Path $workspace ".agents\autonomous_mode.enabled"
    
    # If autonomous mode is not explicitly enabled, exit cleanly
    if (-not (Test-Path $modeFlag)) {
        Write-Output "{}"
        exit 0
    }

    $backlogPath = Join-Path $workspace "task_backlog.json"
    if (Test-Path $backlogPath) {
        $backlog = Get-Content $backlogPath -Raw | ConvertFrom-Json
        $pending = $backlog.tasks | Where-Object { $_.status -eq "in_progress" -or $_.status -eq "pending" }
        
        if ($pending -and $pending.Count -gt 0) {
            $nextTask = $pending[0]
            $resp = @{
                decision = "continue"
                reason = "TAIDE Autonomous Loop Active: Task '$($nextTask.id) - $($nextTask.title)' is pending. Continuing execution."
            }
            Write-Output ($resp | ConvertTo-Json -Compress)
            exit 0
        }
    }

    # All tasks completed
    Write-Output "{}"
} catch {
    Write-Output "{}"
}
