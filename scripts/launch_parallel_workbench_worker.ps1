[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateRange(0,5)][int]$Index)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$env:NUMEXPR_NUM_THREADS = '1'
$GroupId = 'manta_dsflash_workbench6_20261005_2145'
$WorkerId = "${GroupId}_w$Index"
$TaskOffset = 5 * $Index
$Seed = 42 + 1000 * $TaskOffset

& (Join-Path $PSScriptRoot 'launch_manta_experiment.ps1') `
    -ExperimentId $WorkerId `
    -ScheduledAtIso '2026-10-05T21:44:00+08:00' `
    -ConfigRelative "config\manta_deepseek_flash_workbench6_w$Index.toml" `
    -SkillStateRelative "artifacts\deepseek_flash_workbench_parallel_state\worker_$Index\topology_skill.md" `
    -Benchmarks @('workbench') `
    -TaskLimit 5 `
    -TaskOffset $TaskOffset `
    -RunsPerTask 3 `
    -Seed $Seed `
    -ExpectedRunCount 15
