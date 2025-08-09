@echo off
echo Démarrage du système de notes collaboratives...

echo.
echo Démarrage du serveur Django...
start cmd /k "cd /d %~dp0 && env\Scripts\activate && python manage.py runserver"

echo.
echo Attente de 3 secondes...
timeout /t 3 /nobreak > nul

echo.
echo Démarrage du serveur Vue.js...
start cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo Les serveurs sont en cours de démarrage...
echo Django: http://localhost:8000
echo Vue.js: http://localhost:3000
echo.
pause