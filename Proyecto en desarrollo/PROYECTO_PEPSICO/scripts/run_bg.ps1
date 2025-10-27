$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Join-Path $root ".."
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$logdir = Join-Path $projectRoot "logs"
New-Item -ItemType Directory -Path $logdir -Force | Out-Null
 $out = Join-Path $logdir "server_out.log"
 $err = Join-Path $logdir "server_err.log"
Write-Output "Using python: $python"
Write-Output "Logging to: $log"
Start-Process -FilePath $python -ArgumentList "app.py" -RedirectStandardOutput $out -RedirectStandardError $err -NoNewWindow -PassThru | Select-Object Id,StartTime | Format-List
Write-Output "Server started (detached). Check logs with: Get-Content -Tail 100 .\logs\server_out.log ; Get-Content -Tail 100 .\logs\server_err.log"