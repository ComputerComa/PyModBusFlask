Write-Host "Building Modbus TCP Client Executable..." -ForegroundColor Green
Write-Host ""

# Clean previous builds
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__" }

Write-Host "Starting PyInstaller build..." -ForegroundColor Yellow

# Build the executable
pyinstaller modbus_client.spec

Write-Host ""
Write-Host "Build complete!" -ForegroundColor Green
Write-Host "Executable is located in the 'dist' folder." -ForegroundColor Cyan
Write-Host ""

# Check if build was successful
if (Test-Path "dist\ModbusTCPClient.exe") {
    Write-Host "✓ ModbusTCPClient.exe created successfully!" -ForegroundColor Green
    $fileSize = (Get-Item "dist\ModbusTCPClient.exe").Length / 1MB
    Write-Host "File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
} else {
    Write-Host "✗ Build failed - executable not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
