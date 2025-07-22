$projectRoot = "."

# Define project structure
$folders = @(
    "backend/data_pipeline",
    "backend/ai_model",
    "frontend",
    "backend/dashboard"
)

$files = @(
    "backend/data_pipeline/fetch_data.py",
    "backend/data_pipeline/database.py",
    "backend/ai_model/train_model.py",
    "backend/ai_model/predict.py",
    "backend/requirements.txt",
    "backend/dashboard/app.py",
    "backend/dashboard/config.py",
    "Dockerfile",
    "README.md",
    "run.ps1"
)

# Create directories
foreach ($folder in $folders) {
    New-Item -Path "$projectRoot/$folder" -ItemType Directory -Force
}

# Create files with placeholder content
foreach ($file in $files) {
    $filePath = "$projectRoot/$file"
    if (-Not (Test-Path $filePath)) {
        New-Item -Path $filePath -ItemType File -Force | Out-Null
        Set-Content -Path $filePath -Value "# Auto-generated file"
    }
}

Write-Host "✅ Project structure created successfully!"
