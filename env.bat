@echo off
title Taekwondo Management System
color 0A

echo ================================================
echo     TAEKWONDO MANAGEMENT SYSTEM
echo ================================================
echo.

:: Go to project folder
cd /d C:\Users\amyru\taekwondo_system

:: Activate virtual environment
call venv\Scripts\activate

echo [OK] Virtual Environment Activated!
echo.

:: Get IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4" ^| find "192.168"') do set IP=%%a
set IP=%IP:~1%

:: Clean up spaces
set IP=%IP: =%

:: Fallback if no IP found
if "%IP%"=="" set IP=127.0.0.1

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
echo   ---------------
echo   http://127.0.0.1:8000/
echo.
echo   ON TABLET / PHONE (Same WiFi):
echo   ------------------------------
echo   http://%IP%:8000/
echo.
echo ================================================
echo              LOGIN OPTIONS
echo ================================================
echo.
echo   From the home page, you have TWO login options:
echo.
echo   👨‍💼 ADMIN LOGIN:
echo      Username: joe
echo      Password: (your password)
echo.
echo   👨‍👩‍👧 PARENT LOGIN:
echo      IC Number: (student IC)
echo      Password: 123456
echo.
echo ================================================
echo   !!! DO NOT CLOSE THIS WINDOW !!!
echo   Press Ctrl+C to stop the server
echo ================================================
echo.

:: Run server on all interfaces
python manage.py runserver 0.0.0.0:8000

pause