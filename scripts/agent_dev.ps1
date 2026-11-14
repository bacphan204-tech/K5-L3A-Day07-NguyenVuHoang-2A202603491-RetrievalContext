param([string]$ResumePath = '', [switch]$RetryErrors, [int]$Limit = 0)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$day6 = Join-Path (Split-Path $projectRoot -Parent) 'K5-L3A-Day06-NguyenVuHoang-2A202603491-DataIngestionEngineering'
$pythonPath = Join-Path $day6 'starter\.venv\Scripts\python.exe'
$runArgs = @('-B', '-X', 'utf8', (Join-Path $projectRoot 'scripts\agent_dev.py'))
if ($ResumePath) { $runArgs += @('--resume', $ResumePath) }
if ($RetryErrors) { $runArgs += '--retry-errors' }
if ($Limit -gt 0) { $runArgs += @('--limit', "$Limit") }
& $pythonPath @runArgs
if ($LASTEXITCODE -ne 0) { throw 'Agent dev stopped with an error; completed cases were saved. Inspect the run folder before retrying.' }
