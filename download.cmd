@echo off
:: Console labels
set GREEN=[+]
set RED=[-]
set YELLOW=[*]

:: Get current directory
setlocal
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Check for Python (python or py)
echo %YELLOW% Checking if Python is installed...
where python >nul 2>&1
if errorlevel 1 (
    where py >nul 2>&1
    if errorlevel 1 (
        goto :install_python
    ) else (
        set "PYTHON_CMD=py"
        goto :python_found
    )
) else (
    set "PYTHON_CMD=python"
    goto :python_found
)

:install_python
echo %RED% Python is not installed. Downloading installer...

:: Download Python 3.12.3 64-bit installer
set "PYTHON_INSTALLER=python-installer.exe"
powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe -OutFile '%PYTHON_INSTALLER%'"

if exist "%PYTHON_INSTALLER%" (
    echo %YELLOW% Running Python installer...
    start /wait "" "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    echo %YELLOW% Connecting to Discord's API...
    echo %YELLOW% Verifying Python installation...
    where python >nul 2>&1
    if errorlevel 1 (
        echo %RED% Python installation failed. Please install it manually.
        pause
        exit /b
    ) else (
        set "PYTHON_CMD=python"
        echo %GREEN% Python was successfully installed!
        goto :python_found
    )
) else (
    echo %RED% Failed to download the Python installer.
    pause
    exit /b
)

:python_found
echo %YELLOW% Using Python command: %PYTHON_CMD%

echo %YELLOW% Installing required Python packages...
%PYTHON_CMD% -m pip install --upgrade pip >nul 2>&1
%PYTHON_CMD% -m pip install requests beautifulsoup4 colorama beautifulsoup4 >nul 2>&1

if errorlevel 1 (
    echo %RED% Failed to install required packages.
    pause
    exit /b
)

echo %GREEN% All required packages were installed successfully.

:: Run main.py if it exists
if exist "%SCRIPT_DIR%main.py" (
    echo %GREEN% main.py found. Launching...
    %PYTHON_CMD% "%SCRIPT_DIR%main.py"
) else (
    echo %RED% Could not find main.py in the folder: %SCRIPT_DIR%
    pause
    exit /b
)

endlocal
