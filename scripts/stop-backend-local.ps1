$ErrorActionPreference = 'Stop'

$targets = @(
    'uvicorn gateway.app.main:app',
    'uvicorn services.auth.app.main:app',
    'uvicorn services.wishlist.app.main:app',
    'uvicorn services.seller.app.main:app',
    'uvicorn services.matching.app.main:app',
    'uvicorn services.cluster.app.main:app',
    'uvicorn services.match-engine.app.main:app',
    'uvicorn services.validation.app.main:app',
    'uvicorn services.notification.app.main:app',
    'uvicorn services.admin.app.main:app',
    'celery -A services.worker.app.tasks worker'
)

$processes = Get-CimInstance Win32_Process |
    Where-Object {
        if ($_.Name -ne 'powershell.exe' -or -not $_.CommandLine) {
            return $false
        }

        $cmd = $_.CommandLine.ToLower()
        foreach ($target in $targets) {
            if ($cmd.Contains($target.ToLower())) {
                return $true
            }
        }
        return $false
    }

if (-not $processes) {
    Write-Host 'No backend service PowerShell processes found.'
    exit 0
}

$stopped = 0
foreach ($proc in $processes) {
    try {
        Stop-Process -Id $proc.ProcessId -Force
        $stopped++
    } catch {
        Write-Warning ("Failed to stop PID {0}: {1}" -f $proc.ProcessId, $_.Exception.Message)
    }
}

Write-Host ("Stopped {0} backend service terminal process(es)." -f $stopped)
