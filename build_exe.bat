@echo off
echo Building Modbus TCP Client Executable...
echo.

REM Clean previous builds
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "__pycache__" rmdir /s /q __pycache__

REM Build the executable
pyinstaller modbus_client.spec

echo.
echo Build complete! 
echo Executable is located in the 'dist' folder.
echo.
pause
