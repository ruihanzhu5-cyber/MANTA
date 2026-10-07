[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# The experiment ID is historical; PlanCraft was cancelled before it started.
& (Join-Path $PSScriptRoot 'launch_manta_experiment.ps1') `
    -ExperimentId 'manta_dsflash_4bench_utf8_20261005_2030' `
    -ScheduledAtIso '2026-10-05T20:30:00+08:00' `
    -Benchmarks @('browsecomp', 'workbench', 'math500') `
    -ExpectedRunCount 270
