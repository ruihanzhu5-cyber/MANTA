[CmdletBinding()]
param(
    [string]$ExperimentId = "manta_dsflash_4bench_20261005_1800",
    [string]$ScheduledAtIso = "2026-10-05T18:00:00+08:00",
    [string]$ConfigRelative = "config\manta_deepseek_flash.toml",
    [string]$SkillStateRelative = "artifacts\deepseek_flash_state\topology_skill.md",
    [string[]]$Benchmarks = @("browsecomp", "workbench", "plancraft", "math500"),
    [int]$TaskLimit = 30,
    [int]$TaskOffset = 0,
    [int]$RunsPerTask = 3,
    [int]$Seed = 42,
    [int]$ExpectedRunCount = 360
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$MonitorDir = Join-Path $RepoRoot "artifacts\monitor\$ExperimentId"
$StatusPath = Join-Path $MonitorDir "status.json"
$LogPath = Join-Path $MonitorDir "runner.log"
$Runner = Join-Path $PSScriptRoot "run_deepseek_flash_paper.ps1"
$ExperimentRoot = Join-Path $RepoRoot "artifacts\full_experiment\$ExperimentId"
$ScheduledAt = [DateTimeOffset]::Parse($ScheduledAtIso)
$StartedAtUtc = $null

New-Item -ItemType Directory -Force -Path $MonitorDir | Out-Null

function Write-Status {
    param([string]$State, [string]$Message, [int]$ExitCode = 0)
    $payload = [ordered]@{
        experiment_id = $ExperimentId
        state = $State
        message = $Message
        scheduled_at = $ScheduledAt.ToString("o")
        started_at_utc = $StartedAtUtc
        updated_at_utc = (Get-Date).ToUniversalTime().ToString("o")
        finished_at_utc = if ($State -in @("completed", "failed")) { (Get-Date).ToUniversalTime().ToString("o") } else { $null }
        pid = $PID
        exit_code = $ExitCode
    }
    $temporary = "$StatusPath.tmp"
    $payload | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $temporary -Encoding utf8
    Move-Item -LiteralPath $temporary -Destination $StatusPath -Force
}

try {
    $delay = [math]::Ceiling(($ScheduledAt - [DateTimeOffset]::Now).TotalSeconds)
    if ($delay -gt 0) {
        Write-Status -State "scheduled" -Message "等待北京时间 18:00 启动"
        Start-Sleep -Seconds $delay
    }
    $existing = Get-Content -LiteralPath $StatusPath -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($existing -and $existing.state -in @("running", "completed")) {
        Add-Content -LiteralPath $LogPath -Value "LAUNCH_SKIPPED Experiment is already $($existing.state)."
        exit 0
    }
    $StartedAtUtc = (Get-Date).ToUniversalTime().ToString("o")
    Write-Status -State "running" -Message "实验运行中"
    & $Runner -ExperimentId $ExperimentId -TaskLimit $TaskLimit -TaskOffset $TaskOffset -RunsPerTask $RunsPerTask -Seed $Seed -ConfigRelative $ConfigRelative -SkillStateRelative $SkillStateRelative -Benchmarks $Benchmarks -ResetSkill *>> $LogPath
    if ($LASTEXITCODE -ne 0) {
        throw "Runner returned exit code $LASTEXITCODE"
    }
    if (-not (Test-Path -LiteralPath (Join-Path $ExperimentRoot "experiment_summary.json"))) {
        throw "Experiment summary was not produced."
    }
    $runCount = (Get-ChildItem -LiteralPath $ExperimentRoot -Filter "run_*.eval.json" -Recurse -File | Measure-Object).Count
    if ($runCount -ne $ExpectedRunCount) {
        throw "Expected $ExpectedRunCount evaluated runs, found $runCount."
    }
    Write-Status -State "completed" -Message "实验完成，$runCount/$ExpectedRunCount 次结果已写入"
}
catch {
    $message = $_.Exception.Message
    Add-Content -LiteralPath $LogPath -Value "LAUNCH_ERROR $message"
    Write-Status -State "failed" -Message $message -ExitCode 1
    exit 1
}
