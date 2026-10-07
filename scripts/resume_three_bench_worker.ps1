[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateRange(0,5)][int]$Index)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$groupId = 'manta_dsflash_parallel3_20261005_2120'
$offset = 5 * $Index

# The original worker may have stopped after a retryable API-format failure or
# may be parked at the cancelled PlanCraft gate. Completed runs resume-skip.
& (Join-Path $PSScriptRoot 'launch_manta_experiment.ps1') `
    -ExperimentId "${groupId}_w$Index" `
    -ScheduledAtIso '2026-10-05T21:20:00+08:00' `
    -ConfigRelative "config\manta_deepseek_flash_parallel3_w$Index.toml" `
    -SkillStateRelative "artifacts\deepseek_flash_parallel3_state\worker_$Index\topology_skill.md" `
    -Benchmarks @('browsecomp', 'workbench') `
    -TaskLimit 5 `
    -TaskOffset $offset `
    -RunsPerTask 3 `
    -Seed (42 + 1000 * $offset) `
    -ExpectedRunCount 30
