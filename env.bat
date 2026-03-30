@echo off
echo ================================================
echo     TAEKWONDO MANAGEMENT SYSTEM
echo ================================================
echo.

:: Go to project folder
cd /d C:\Users\amyru\taekwondo_system

:: Activate virtual environment
call venv\Scripts\activate

echo Virtual Environment Activated!
echo.

:: Get IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4" ^| find "192.168"') do set IP=%%a
set IP=%IP:~1%

echo ================================================
echo Server is starting...
echo ================================================
echo.
echo Access URLs:
echo   Admin Panel: http://127.0.0.1:8000/admin
echo   Parent Portal: http://127.0.0.1:8000/parent
echo   API: http://127.0.0.1:8000/api/
echo.
echo From Other Devices (Android):
echo   http://%IP%:8000/parent
echo.
echo Login Details:
echo   Super Admin: joe / (your password)
echo   Parent: Use IC number / password 123456
echo.
echo ================================================
echo DO NOT CLOSE THIS WINDOW!
echo ================================================
echo.

:: Run server on all interfaces
python manage.py runserver 0.0.0.0:8000

pause