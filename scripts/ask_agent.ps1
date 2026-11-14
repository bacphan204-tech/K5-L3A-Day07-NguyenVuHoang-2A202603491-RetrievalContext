param(
    [string]$Question = '',
    [ValidateSet(0,3,4)][int]$Chapter = 0,
    [ValidateSet('dense','rerank')][string]$Retrieval = 'rerank',
    [switch]$CheckConfig,
    [switch]$CheckApi
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
if ($CheckConfig -or $CheckApi) {
    $pythonPath = (Get-Command python -ErrorAction Stop).Source
} else {
    $day6 = Join-Path (Split-Path $projectRoot -Parent) 'K5-L3A-Day06-NguyenVuHoang-2A202603491-DataIngestionEngineering'
    $pythonPath = Join-Path $day6 'starter\.venv\Scripts\python.exe'
}
$runArgs = @('-B', '-X', 'utf8', (Join-Path $projectRoot 'scripts\ask_agent.py'), '--retrieval', $Retrieval)
if ($CheckConfig) { $runArgs += '--check-config' }
if ($CheckApi) { $runArgs += '--check-api' }
if ($Question) { $runArgs += @('--question', $Question) }
if ($Chapter -ne 0) { $runArgs += @('--chapter', "$Chapter") }
& $pythonPath @runArgs
if ($LASTEXITCODE -ne 0) { throw 'Agent/configuration check failed. Read the error or saved trace.' }
