$body = @{
    provider = "openai"
    model = "gpt-3.5"
    prompt = "Hello world!"
} | ConvertTo-Json -Depth 10

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/chat/completions" -Method POST -ContentType "application/json" -Body $body

Write-Output $response
