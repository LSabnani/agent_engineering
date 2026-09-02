param(
    [string]$recording = "class-02C-work\events.jsonl",
    [double]$delay = 0.75
)

if (-not (Test-Path $recording)) {
    Write-Error "Recording not found: $recording"
    exit 1
}

$events = Get-Content $recording
foreach ($eventLine in $events) {
    if ([string]::IsNullOrWhiteSpace($eventLine)) { continue }
    $event = $eventLine | ConvertFrom-Json
    
    $parts = ""
    if ($event.content -and $event.content.parts) {
        $partKeys = $event.content.parts | ForEach-Object { $_.psobject.properties.name } | Select-Object -Unique
        $parts = $partKeys -join ","
    }
    if ([string]::IsNullOrEmpty($parts)) {
        $parts = "event"
    }
    
    $author = if ($event.author) { $event.author } else { 'unknown' }
    Write-Host "[$author] $parts"
    Start-Sleep -Seconds $delay
}
