@echo off
echo Starting BUI Transport Development Environment...
echo.

echo Starting Django Backend...
start "Django Backend" cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver 127.0.0.1:8000"

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting React Frontend...
start "React Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Development servers are starting...
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
pause