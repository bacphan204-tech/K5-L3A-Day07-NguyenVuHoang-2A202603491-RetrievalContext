param(
    [Parameter(Mandatory=$true)][string]$Question,
    [ValidateSet(0,3,4)][int]$Chapter = 0,
    [ValidateSet('all','dense','bm25','hybrid')][string]$Method = 'all',
    [ValidateRange(1,183)][int]$TopK = 3,
    [ValidateRange(1,183)][int]$CandidateK = 20,
    [string]$LexicalQuery = '',
    [string]$OutputPath = '',
    [string]$Day6Path = ''
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
if (-not $Day6Path) {
    $Day6Path = Join-Path (Split-Path $projectRoot -Parent) 'K5-L3A-Day06-NguyenVuHoang-2A202603491-DataIngestionEngineering'
}
if ($CandidateK -lt $TopK) { throw 'CandidateK must be at least TopK.' }
if ($Method -eq 'bm25') {
    $pythonPath = (Get-Command python -ErrorAction Stop).Source
} else {
    $pythonPath = Join-Path $Day6Path 'starter\.venv\Scripts\python.exe'
}
if (-not (Test-Path -LiteralPath $pythonPath)) { throw "Python environment not found: $pythonPath" }
$runArgs = @('-B', '-X', 'utf8', (Join-Path $projectRoot 'src\compare_retrieval.py'), '--question', $Question, '--method', $Method, '--top-k', "$TopK", '--candidate-k', "$CandidateK", '--day6', $Day6Path)
if ($Chapter -ne 0) { $runArgs += @('--chapter', "$Chapter") }
if ($LexicalQuery) { $runArgs += @('--lexical-query', $LexicalQuery) }
if ($OutputPath) { $runArgs += @('--output', $OutputPath) }
& $pythonPath @runArgs
if ($LASTEXITCODE -ne 0) { throw "Retrieval comparison failed (exit $LASTEXITCODE). See the output trace." }
