param(
    [ValidateRange(3,183)][int]$CandidateK = 20,
    [string]$Day6Path = ''
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
if (-not $Day6Path) {
    $Day6Path = Join-Path (Split-Path $projectRoot -Parent) 'K5-L3A-Day06-NguyenVuHoang-2A202603491-DataIngestionEngineering'
}
$pythonPath = Join-Path $Day6Path 'starter\.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { throw "Day 6 Python environment not found: $pythonPath" }
& $pythonPath -B -X utf8 (Join-Path $projectRoot 'scripts\benchmark_dev.py') --day6 $Day6Path --candidate-k $CandidateK
if ($LASTEXITCODE -ne 0) { throw 'Dev run failed or recorded errors. Inspect the reported results directory.' }
