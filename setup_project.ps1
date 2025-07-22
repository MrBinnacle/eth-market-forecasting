
# Set project root directory
$projectRoot = "eth-market-forecasting"


# Define project structure
$folders = @(
    "backend/data_pipeline",
    "backend/ai_model",
    "frontend"
)

$files = @(
    "backend/data_pipeline/fetch_data.py",
    "backend/data_pipeline/database.py",
    "backend/ai_model/train_model.py",
    "backend/ai_model/predict.py",
    "backend/requirements.txt",
    "frontend/dashboard.py",
    "frontend/config.py",
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


# Install Python dependencies
Write-Host "Checking for Python..."
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python is not installed. Please install Python 3.x and rerun this script."
    exit 1
}

$reqPath = "$projectRoot/backend/requirements.txt"
if (Test-Path $reqPath) {
    Write-Host "Installing Python dependencies from $reqPath..."
    try {
        python -m pip install --upgrade pip
        python -m pip install -r $reqPath
        Write-Host "✅ Python dependencies installed successfully."
    } catch {
        Write-Host "❌ Python dependency installation failed. Please check requirements.txt and your Python environment."
        exit 1
    }
} else {
    Write-Host "⚠️ requirements.txt not found at $reqPath. Skipping Python dependency installation."
}


# Install Node.js dependencies for frontend
Write-Host "Checking for Node.js..."
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js is not installed. Please install Node.js and rerun this script."
    exit 1
}

$frontendPath = "$projectRoot/../"
if (Test-Path (Join-Path $frontendPath 'package.json')) {
    Write-Host "Installing Node.js dependencies in $frontendPath..."
    try {
        Push-Location $frontendPath
        npm install
        Pop-Location
        Write-Host "✅ Node.js dependencies installed successfully."
    } catch {
        Write-Host "❌ Node.js dependency installation failed. Please check package.json and your Node.js environment."
        exit 1
    }
} else {
    Write-Host "⚠️ package.json not found in $frontendPath. Skipping Node.js dependency installation."
}


# Final summary and next steps
Write-Host "\n🎉 All setup steps completed!"
Write-Host "- Project structure is ready."
Write-Host "- Python and Node.js dependencies are installed."
Write-Host "- You can now run backend and frontend services as described in the README."
Write-Host "- If you encounter issues, check the logs above or consult the documentation."
Write-Host "\n✅ Project structure and dependencies set up successfully!"
