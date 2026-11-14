param(
    [Parameter(Mandatory=$true)][string]$Question,
    [ValidateSet(0,3,4)][int]$Chapter = 0,
    [ValidateRange(1,183)][int]$TopK = 3,
    [string]$Day6Path = ""
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
if (-not $Day6Path) {
    $Day6Path = Join-Path (Split-Path $projectRoot -Parent) 'K5-L3A-Day06-NguyenVuHoang-2A202603491-DataIngestionEngineering'
}
$pythonPath = Join-Path $Day6Path 'starter\.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw "Day 6 Python environment not found: $pythonPath"
}
$runArgs = @('-B', '-X', 'utf8', (Join-Path $projectRoot 'src\dense_retrieval.py'), '--question', $Question, '--top-k', "$TopK", '--day6', $Day6Path)
if ($Chapter -ne 0) { $runArgs += @('--chapter', "$Chapter") }
& $pythonPath @runArgs
if ($LASTEXITCODE -ne 0) { throw "Dense retrieval failed (exit $LASTEXITCODE). See results/part02/dense-last.json." }
