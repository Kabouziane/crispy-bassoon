@echo off
echo Démarrage en mode debug...
echo.
echo 1. Démarrage du backend Django...
start cmd /k "cd /d %~dp0 && env\Scripts\activate && python manage.py runserver"

echo.
echo 2. Attente de 3 secondes...
timeout /t 3 /nobreak > nul

echo.
echo 3. Démarrage du frontend Vue.js...
start cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo 4. Ouverture de la page debug...
timeout /t 5 /nobreak > nul
start http://localhost:3000/debug

echo.
echo URLs disponibles:
echo - Debug: http://localhost:3000/debug
echo - Login: http://localhost:3000/login  
echo - Backend: http://localhost:8000/admin
echo.
pause