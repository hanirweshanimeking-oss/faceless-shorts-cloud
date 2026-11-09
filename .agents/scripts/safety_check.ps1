# Antigravity PreToolUse Safety Interceptor (safety_check.ps1)
# Enforces human sovereign approval for destructive/irreversible operations

try {
    $inputRaw = [Console]::In.ReadToEnd()
    if (-not $inputRaw) {
        Write-Output '{"decision":"allow"}'
        exit 0
    }

    $payload = $inputRaw | ConvertFrom-Json
    $toolName = $payload.toolCall.name
    $cmd = $payload.toolCall.args.CommandLine

    if ($toolName -eq "run_command" -and $cmd) {
        $destructivePatterns = @(
            'git\s+push\s+.*--force',
            'git\s+push\s+.*-f\b',
            'git\s+reset\s+--hard',
            'rmdir\s+/s',
            'rd\s+/s',
            'del\s+/[fF]\s+/[sS]',
            'Format-Volume',
            'Remove-Item\s+.*-Recurse\s+.*-Force',
            'Drop\s+Database',
            'drop\s+table',
            'curl\s+.*(@\.env|token|id_rsa)'
        )

        foreach ($pattern in $destructivePatterns) {
            if ($cmd -match $pattern) {
                $reason = "SECURITY GATE TRIGGERED: High-risk command detected ('$cmd'). Explicit human authorization required."
                $resp = @{
                    decision = "force_ask"
                    reason = $reason
                }
                Write-Output ($resp | ConvertTo-Json -Compress)
                exit 0
            }
        }
    }

    Write-Output '{"decision":"allow"}'
} catch {
    # Fail-safe: allow benign operations if parsing fails, but log
    Write-Output '{"decision":"allow"}'
}
