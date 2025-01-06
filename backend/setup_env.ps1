# PowerShell Script: setup_env.ps1

# Step 1: Change Execution Policy Temporarily
Set-ExecutionPolicy RemoteSigned -Scope Process -Force

# Step 2: Activate Virtual Environment
.\venv\Scripts\Activate

# Step 3: Install Requirements
if (Test-Path -Path "requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
} else {
    Write-Host "requirements.txt not found. Skipping dependency installation."
}

# Step 4: Start Flask Application
$env:FLASK_APP="main.py"
$env:FLASK_ENV="development"
Write-Host "Starting Flask server..."

# Optional: Revert Execution Policy after exiting Flask
# Uncomment the next line if you want to enforce the original setting
# Set-ExecutionPolicy Restricted -Scope Process