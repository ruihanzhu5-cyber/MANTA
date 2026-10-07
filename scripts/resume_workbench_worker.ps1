[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateRange(0,5)][int]$Index)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$groupId = 'manta_dsflash_workbench6_20261005_2145'
$offset = 5 * $Index

& (Join-Path $PSScriptRoot 'launch_manta_experiment.ps1') `
    -ExperimentId "${groupId}_w$Index" `
    -ScheduledAtIso '2026-10-05T21:45:00+08:00' `
    -ConfigRelative "config\manta_deepseek_flash_workbench6_w$Index.toml" `
    -SkillStateRelative "artifacts\deepseek_flash_workbench_parallel_state\worker_$Index\topology_skill.md" `
    -Benchmarks @('workbench') `
    -TaskLimit 5 `
    -TaskOffset $offset `
    -RunsPerTask 3 `
    -Seed (42 + 1000 * $offset) `
    -ExpectedRunCount 15
