$BaseUrl = "http://127.0.0.1:8000"
$AppName = "workflow_agents"
$UserId = "class02c-user"
$SessionId = "class02c-" + (Get-Date -Format "yyyyMMdd-HHmmss")
$FirstMessage = "Hello"
$SecondMessage = "Ada Lovelace"

# Function to run a message
function Run-Message($message, $outputPath) {
    $body = @{
        appName = $AppName
        userId = $UserId
        sessionId = $SessionId
        newMessage = @{
            role = "user"
            parts = @(
                @{ text = $message }
            )
        }
    } | ConvertTo-Json -Depth 5
    
    $headers = @{
        "Content-Type" = "application/json"
    }
    
    $response = Invoke-RestMethod -Uri "$BaseUrl/run" -Method Post -Body $body -Headers $headers
    
    # Save the raw response to file
    $response | ConvertTo-Json -Depth 100 | Out-File -FilePath $outputPath -Encoding utf8
    
    # Output summary
    $response | ForEach-Object {
        [PSCustomObject]@{
            timestamp = $_.timestamp
            author = $_.author
            id = $_.id
            invocationId = $_.invocationId
        }
    }
}

Write-Host "Creating session $SessionId"
$createSessionUrl = "$BaseUrl/apps/$AppName/users/$UserId/sessions/$SessionId"
$sessionResponse = Invoke-RestMethod -Uri $createSessionUrl -Method Post -Body "{}" -ContentType "application/json"
Write-Host "Session created: $($sessionResponse.id)"

Write-Host "Running first message: $FirstMessage"
$run1 = Run-Message $FirstMessage "class-02C-work\run-01.json"
$run1 | Format-Table

Write-Host "Running second message: $SecondMessage"
$run2 = Run-Message $SecondMessage "class-02C-work\run-02.json"
$run2 | Format-Table

# Retrieve full session and convert events to jsonl
Write-Host "Retrieving session..."
$session = Invoke-RestMethod -Uri "$BaseUrl/apps/$AppName/users/$UserId/sessions/$SessionId"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText([System.IO.Path]::GetFullPath("class-02C-work\session.json"), ($session | ConvertTo-Json -Depth 100), $utf8NoBom)

# Convert events to JSONL
$eventsJsonl = $session.events | ForEach-Object { $_ | ConvertTo-Json -Compress }
[System.IO.File]::WriteAllLines([System.IO.Path]::GetFullPath("class-02C-work\events.jsonl"), $eventsJsonl, $utf8NoBom)

# Write last_session.env
$envContent = @"
BASE_URL=$BaseUrl
APP_NAME=$AppName
USER_ID=$UserId
SESSION_ID=$SessionId
"@
$envContent | Out-File -FilePath "class-02C-work\last_session.env" -Encoding ascii

$eventCount = @($session.events).Count
Write-Host "Recorded $eventCount events"
Write-Host "Recording: class-02C-work\events.jsonl"
