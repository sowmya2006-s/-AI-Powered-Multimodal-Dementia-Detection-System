$baseUrl = "http://127.0.0.1:8000/api"

# 1. Login
Write-Host "Attempting Login..."
$loginBody = @{
    email = "testuser@example.com"
    password = "TestPass123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/accounts/login/" -Method POST -Body $loginBody -Headers @{ "Content-Type" = "application/json" }
    $token = $loginResponse.access
    if (-not $token) {
        Write-Error "Login response did not contain access token."
        exit 1
    }
    Write-Host "Login Successful."
} catch {
    Write-Error "Login Failed: $_"
    exit 1
}

# 2. Create Patient
Write-Host "Attempting to Create Patient..."
$patientBody = @{
    name = "John Doe"
    age = 75
    gender = "Male"
    language = "English"
    education = "PhD"
    medical_history = "Hypertension"
} | ConvertTo-Json

try {
    $patientResponse = Invoke-RestMethod -Uri "$baseUrl/patients/create/" -Method POST -Body $patientBody -Headers @{ "Content-Type" = "application/json"; "Authorization" = "Bearer $token" }
    Write-Host "Patient Created Successfully:"
    $patientResponse | Format-List
} catch {
    Write-Error "Patient Creation Failed: $_"
    exit 1
}
