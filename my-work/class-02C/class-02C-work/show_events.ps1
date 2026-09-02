$recording = "class-02C-work\events.jsonl"
if (-not (Test-Path $recording)) {
    Write-Error "Recording not found: $recording"
    exit 1
}

$events = Get-Content $recording | ForEach-Object { $_ | ConvertFrom-Json }

$index = 1
$rows = $events | ForEach-Object {
    $parts = ""
    if ($_.content -and $_.content.parts) {
        $partKeys = $_.content.parts | ForEach-Object { $_.psobject.properties.name } | Select-Object -Unique
        $parts = $partKeys -join ","
    }
    if ([string]::IsNullOrEmpty($parts)) {
        $parts = "event"
    }

    $stateKeys = "-"
    if ($_.actions -and $_.actions.stateDelta) {
        $deltaKeys = $_.actions.stateDelta.psobject.properties.name
        if ($deltaKeys.Count -gt 0) {
            $stateKeys = $deltaKeys -join ","
        }
    }

    [PSCustomObject]@{
        SEQ = $index
        TIME = $_.timestamp
        AUTHOR = $_.author
        "PART TYPES" = $parts
        "STATE KEYS" = $stateKeys
    }
    $index++
}

$rows | Format-Table -AutoSize
