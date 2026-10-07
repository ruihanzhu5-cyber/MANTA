[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateRange(0,5)][int]$Index)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$GroupId = 'manta_dsflash_parallel3_20261005_2120'
$WorkerId = "${GroupId}_w$Index"
$TaskOffset = 5 * $Index
$Seed = 42 + 1000 * $TaskOffset
$Config = "config\manta_deepseek_flash_parallel3_w$Index.toml"
$Skill = "artifacts\deepseek_flash_parallel3_state\worker_$Index\topology_skill.md"

& (Join-Path $PSScriptRoot 'launch_manta_experiment.ps1') `
    -ExperimentId $WorkerId `
    -ScheduledAtIso '2026-10-05T21:20:00+08:00' `
    -ConfigRelative $Config `
    -SkillStateRelative $Skill `
    -Benchmarks @('browsecomp','workbench','plancraft') `
    -TaskLimit 5 `
    -TaskOffset $TaskOffset `
    -RunsPerTask 3 `
    -Seed $Seed `
    -ExpectedRunCount 45
