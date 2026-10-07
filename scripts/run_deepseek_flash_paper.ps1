[CmdletBinding()]
param(
    [string]$ExperimentId = ("manta_deepseek_flash_" + (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")),
    [int]$TaskLimit = 30,
    [int]$TaskOffset = 0,
    [int]$RunsPerTask = 3,
    [int]$Seed = 42,
    [string]$ConfigRelative = "config\manta_deepseek_flash.toml",
    [string]$SkillStateRelative = "artifacts\deepseek_flash_state\topology_skill.md",
    [string[]]$Benchmarks = @("browsecomp", "workbench", "plancraft", "math500"),
    [switch]$ResetSkill
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$Config = Join-Path $RepoRoot $ConfigRelative
$SkillSeed = Join-Path $RepoRoot "config\topology_skill.md"
$SkillState = Join-Path $RepoRoot $SkillStateRelative
$OutputRoot = Join-Path $RepoRoot "artifacts\full_experiment"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Missing .venv. Run 'uv sync' from $RepoRoot first."
}
if (-not (Test-Path -LiteralPath $Config)) {
    throw "Missing config: $Config"
}

$SkillStateDir = Split-Path -Parent $SkillState
New-Item -ItemType Directory -Force -Path $SkillStateDir | Out-Null
if ($ResetSkill -or -not (Test-Path -LiteralPath $SkillState)) {
    Copy-Item -LiteralPath $SkillSeed -Destination $SkillState -Force
}

# Paper batch settings from scripts/full_experiment.sh. These are explicit so a
# future repository default cannot silently change the run.
$env:MAS_REQUIRE_LIVE_LLM = "1"
$env:MAS_DISABLE_LIVE_LLM = "0"
$env:PYTHONUNBUFFERED = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
$env:HF_HOME = Join-Path $RepoRoot ".cache\huggingface"
$env:DEEPSEEK_REASONING_EFFORT = "medium"
$env:DEEPSEEK_THINKING = "enabled"
$env:DEEPSEEK_MAX_TOKENS = "16384"
$env:MAS_LLM_RETRY_ATTEMPTS = "5"
$env:MAS_LLM_TIMEOUT_RETRY_ATTEMPTS = "2"
$env:MAS_LLM_RETRY_BACKOFF_S = "8"
$env:MAS_LLM_RETRY_MAX_BACKOFF_S = "180"
$env:MAS_TRANSCRIPT_COMPACTION_ENABLED = "1"
$env:MAS_SEARCH_TOOL_FAILURE_CIRCUIT_BREAKER = "2"
$env:MAS_TOOL_CONTEXT_RAW_TURNS = "2"
$env:MAS_TOOL_CONTEXT_SUMMARY_MAX_CHARS = "6000"
$env:MAS_TOOL_CONTEXT_PREVIEW_CHARS = "160"
$env:MAS_TOOL_CONTEXT_DOCUMENT_CHARS = "12000"

# Keep the requested benchmark order within each playbook lineage.

Push-Location $RepoRoot
try {
    foreach ($Benchmark in $Benchmarks) {
        Write-Host "=== MANTA / DeepSeek Flash: $Benchmark ==="
        & $Python main.py run `
            --config $Config `
            --benchmark $Benchmark `
            --task-limit $TaskLimit `
            --task-offset $TaskOffset `
            --runs-per-task $RunsPerTask `
            --seed $Seed `
            --output-dir $OutputRoot `
            --output-layout hierarchical `
            --experiment-id $ExperimentId `
            --system-label self_evolved
        if ($LASTEXITCODE -ne 0) {
            throw "Benchmark '$Benchmark' failed with exit code $LASTEXITCODE."
        }
    }

    $ExperimentRoot = Join-Path $OutputRoot $ExperimentId
    & $Python main.py summarize-experiment --experiment-root $ExperimentRoot
    if ($LASTEXITCODE -ne 0) {
        throw "Experiment summary failed with exit code $LASTEXITCODE."
    }
    Write-Host "Completed: $ExperimentRoot"
}
finally {
    Pop-Location
}
