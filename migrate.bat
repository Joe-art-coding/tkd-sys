@echo off
echo ================================================
echo     RUNNING MIGRATIONS
echo ================================================
echo.

cd /d C:\Users\amyru\taekwondo_system
call venv\Scripts\activate

echo Virtual environment activated!
echo.

python manage.py makemigrations schools
echo.
python manage.py makemigrations students
echo.
python manage.py migrate

echo.
echo ================================================
echo MIGRATIONS COMPLETE!
echo ================================================
pause