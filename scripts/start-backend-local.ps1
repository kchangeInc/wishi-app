param(
    [switch]$IncludeWorker = $true
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$backendRoot = Join-Path $repoRoot 'backend-fastapi'
$venvPython = Join-Path $repoRoot 'venv\Scripts\python.exe'
$envFile = Join-Path $repoRoot '.env'
$envExample = Join-Path $repoRoot '.env.example'

if (-not (Test-Path $venvPython)) {
    throw "Python virtual environment not found at $venvPython"
}

if (-not (Test-Path $envFile)) {
    if (Test-Path $envExample) {
        Copy-Item $envExample $envFile
        Write-Host "Created .env from .env.example at $envFile"
    } else {
        throw ".env not found and .env.example is missing"
    }
}

# Load .env into current process for child terminals.
Get-Content $envFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith('#') -and $line.Contains('=')) {
        $parts = $line.Split('=', 2)
        $key = $parts[0].Trim()
        $value = $parts[1].Trim().Trim('"')
        if ($key) {
            [System.Environment]::SetEnvironmentVariable($key, $value, 'Process')
        }
    }
}

if (-not $env:DB_HOST) {
    $env:DB_HOST = 'localhost'
}

$services = @(
    @{ Name = 'gateway'; Port = 8000; Cmd = "& '$venvPython' -m uvicorn gateway.app.main:app --host 0.0.0.0 --port 8000" },
    @{ Name = 'auth'; Port = 8001; Cmd = "& '$venvPython' -m uvicorn services.auth.app.main:app --host 0.0.0.0 --port 8001" },
    @{ Name = 'wishlist'; Port = 8002; Cmd = "& '$venvPython' -m uvicorn services.wishlist.app.main:app --host 0.0.0.0 --port 8002" },
    @{ Name = 'seller'; Port = 8003; Cmd = "& '$venvPython' -m uvicorn services.seller.app.main:app --host 0.0.0.0 --port 8003" },
    @{ Name = 'matching'; Port = 8004; Cmd = "& '$venvPython' -m uvicorn services.matching.app.main:app --host 0.0.0.0 --port 8004" },
    @{ Name = 'cluster'; Port = 8005; Cmd = "& '$venvPython' -m uvicorn services.cluster.app.main:app --host 0.0.0.0 --port 8005" },
    @{ Name = 'match-engine'; Port = 8006; Cmd = "& '$venvPython' -m uvicorn services.match-engine.app.main:app --host 0.0.0.0 --port 8006" },
    @{ Name = 'validation'; Port = 8007; Cmd = "& '$venvPython' -m uvicorn services.validation.app.main:app --host 0.0.0.0 --port 8007" },
    @{ Name = 'notification'; Port = 8008; Cmd = "& '$venvPython' -m uvicorn services.notification.app.main:app --host 0.0.0.0 --port 8008" },
    @{ Name = 'admin'; Port = 8009; Cmd = "& '$venvPython' -m uvicorn services.admin.app.main:app --host 0.0.0.0 --port 8009" }
)

foreach ($service in $services) {
    $terminalCmd = "Set-Location '$backendRoot'; $($service.Cmd)"
    Start-Process powershell -ArgumentList @('-NoExit', '-Command', $terminalCmd) | Out-Null
    Write-Host ("Started {0} on port {1}" -f $service.Name, $service.Port)
}

if ($IncludeWorker) {
    $workerCmd = "Set-Location '$backendRoot'; & '$venvPython' -m celery -A services.worker.app.tasks worker --beat --loglevel=info"
    Start-Process powershell -ArgumentList @('-NoExit', '-Command', $workerCmd) | Out-Null
    Write-Host 'Started worker with beat scheduler'
}

Write-Host ''
Write-Host 'Backend launch initiated in separate terminals.'
Write-Host 'Gateway docs: http://localhost:8000/docs'
Write-Host 'Auth health:  http://localhost:8001/health'
Write-Host 'Wishlist health: http://localhost:8002/health'
Write-Host ''
Write-Host 'Note: for local DB, use DB_HOST=localhost in .env'
