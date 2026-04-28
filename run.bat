@echo off
title Taekwondo Management System
color 0A

:: Go to project folder
cd /d C:\Users\amyru\taekwondo_system

:: Check if virtual environment exists, if not create it
if not exist "venv\Scripts\python.exe" (
    echo [INFO] Virtual environment not found. Creating...
    python -m venv venv
    echo [OK] Virtual environment created!
)

:: Activate virtual environment
call venv\Scripts\activate

:: Check if Django is installed
python -c "import django" 2>nul
if errorlevel 1 (
    echo [INFO] Installing requirements...
    pip install -r requirements.txt
)

:: Get IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4" ^| find "192.168"') do set IP=%%a
set IP=%IP:~1%
set IP=%IP: =%

if "%IP%"=="" set IP=127.0.0.1

:MAIN_MENU
cls
echo ================================================
echo        TAEKWONDO MANAGEMENT SYSTEM
echo ================================================
echo.
echo   [1] Start Server (Normal)
echo   [2] Start Server (Auto-Restart on Crash)
echo   [3] Run Migrations
echo   [4] Reset Superuser Password
echo   [5] Generate Monthly Fees (Manual)
echo   [6] Show User Manual
echo   [7] Kill Process on Port 8000
echo   [8] Exit
echo.
echo ================================================
set /p choice="Select option (1-8): "

if "%choice%"=="1" goto NORMAL_SERVER
if "%choice%"=="2" goto AUTO_RESTART_SERVER
if "%choice%"=="3" goto RUN_MIGRATIONS
if "%choice%"=="4" goto RESET_SUPERUSER
if "%choice%"=="5" goto GENERATE_FEES
if "%choice%"=="6" goto SHOW_MANUAL
if "%choice%"=="7" goto KILL_PORT_8000
if "%choice%"=="8" goto EXIT

echo Invalid option!
timeout /t 2 >nul
goto MAIN_MENU


:NORMAL_SERVER
cls
echo ================================================
echo     TAEKWONDO MANAGEMENT SYSTEM
echo ================================================
echo.
echo [OK] Server starting at: %date% %time%
echo.
echo ================================================
echo              ACCESS URLs
echo ================================================
echo.
echo   ON THIS LAPTOP:
echo   http://127.0.0.1:8000/
echo.
echo   ON TABLET / PHONE (Same WiFi):
echo   http://%IP%:8000/
echo.
echo ================================================
echo              LOGIN OPTIONS
echo ================================================
echo.
echo   ADMIN LOGIN:
echo      Username: joe
echo      Password: (your password)
echo.
echo   PARENT LOGIN:
echo      IC Number: (student IC)
echo      Password: 123456
echo.
echo ================================================
echo   !!! DO NOT CLOSE THIS WINDOW !!!
echo   Press Ctrl+C to stop the server
echo ================================================
echo.
python manage.py runserver 0.0.0.0:8000
echo.
echo [INFO] Server stopped.
pause
goto MAIN_MENU


:AUTO_RESTART_SERVER
cls
echo ================================================
echo     AUTO-RESTART MODE (WATCHDOG ENABLED)
echo ================================================
echo.
echo Server will automatically restart if it crashes!
echo Press Ctrl+C TWICE to stop.
echo.
echo ================================================
echo              ACCESS URLs
echo ================================================
echo.
echo   ON THIS LAPTOP:
echo   http://127.0.0.1:8000/
echo.
echo   ON TABLET / PHONE (Same WiFi):
echo   http://%IP%:8000/
echo.
echo ================================================
echo.

:LOOP
echo [%time%] Starting server...
python manage.py runserver 0.0.0.0:8000
echo [%time%] WARNING: Server crashed or stopped!
echo Restarting in 5 seconds...
timeout /t 5 >nul
goto LOOP


:RUN_MIGRATIONS
cls
echo ================================================
echo     RUNNING DATABASE MIGRATIONS
echo ================================================
echo.
python manage.py makemigrations
python manage.py migrate
echo.
echo [OK] Migrations completed!
pause
goto MAIN_MENU


:RESET_SUPERUSER
cls
echo ================================================
echo     RESET SUPERUSER PASSWORD
echo ================================================
echo.
echo Only ONE superuser allowed for the whole system.
echo Use this to reset password if you forgot it.
echo.
set /p username="Enter superuser username (default: joe): "
if "%username%"=="" set username=joe

echo.
echo Resetting password for: %username%
echo.
python manage.py changepassword %username%
echo.
echo [OK] Password reset completed!
pause
goto MAIN_MENU


:GENERATE_FEES
cls
echo ================================================
echo     GENERATE MONTHLY FEES
echo ================================================
echo.
echo Generating fees for current month...
python manage.py generate_monthly_fees
echo.
echo [OK] Fees generation completed!
pause
goto MAIN_MENU


:SHOW_MANUAL
cls
echo ================================================
echo     OPENING USER MANUAL
echo ================================================
echo.
echo Starting manual server on port 5000...
start python user_manual.py
echo.
echo Manual opened in your browser!
echo If it doesn't open, go to: http://127.0.0.1:5000
echo.
pause
goto MAIN_MENU


:KILL_PORT_8000
cls
echo ================================================
echo     KILLING PROCESS ON PORT 8000
echo ================================================
echo.

:: Find PID using port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do set PID=%%a

if "%PID%"=="" (
    echo [INFO] No process found using port 8000.
) else (
    echo [INFO] Found process with PID: %PID%
    echo [INFO] Killing process...
    taskkill /f /pid %PID% >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Failed to kill process. Try running as Administrator.
    ) else (
        echo [OK] Process on port 8000 has been terminated.
    )
)

:: Also kill any orphaned python processes related to this project
echo.
echo [INFO] Checking for orphaned runserver processes...
for /f "tokens=2" %%a in ('tasklist /fi "imagename eq python.exe" /fo csv ^| find "manage.py"') do (
    set ORPHAN_PID=%%~a
    echo [INFO] Found orphaned process: %ORPHAN_PID%
    taskkill /f /pid %ORPHAN_PID% >nul 2>&1
)

echo.
pause
goto MAIN_MENU


:EXIT
cls
echo ================================================
echo     Thank you for using TAEKWONDO SYSTEM!
echo ================================================
exit