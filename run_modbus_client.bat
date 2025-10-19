@echo off
echo Starting Modbus TCP Client...
echo.
echo The web interface will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
dist\ModbusTCPClient.exe
pause
