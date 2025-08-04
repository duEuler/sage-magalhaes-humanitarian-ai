@echo off
chcp 65001 >nul
title Git Helper - Sage duEuler

:: Verificar se foi passado um comando
if "%1"=="" goto menu

:: Comandos rápidos
if /i "%1"=="pull" goto pull
if /i "%1"=="push" goto push
if /i "%1"=="status" goto status
if /i "%1"=="commit" goto commit
if /i "%1"=="help" goto help

echo ❌ Comando desconhecido: %1
echo 💡 Use 'git_quick.bat help' para ver opções
goto end

:menu
echo.
echo 🚀 Git Helper - Sage duEuler
echo ================================
echo.
echo Comandos disponíveis:
echo   pull    - Fazer pull do GitHub
echo   push    - Push rápido automático
echo   status  - Ver status do repositório
echo   commit  - Commit interativo
echo   help    - Mostrar esta ajuda
echo.
set /p comando="Digite o comando: "
if /i "%comando%"=="pull" goto pull
if /i "%comando%"=="push" goto push
if /i "%comando%"=="status" goto status
if /i "%comando%"=="commit" goto commit
if /i "%comando%"=="help" goto help
goto menu

:pull
echo 🔄 Fazendo pull do GitHub...
git pull origin main
if %errorlevel%==0 (
    echo ✅ Pull realizado com sucesso!
) else (
    echo ❌ Erro no pull
)
goto end

:push
echo ⚡ Push rápido automático...
python tools/git_helper.py push
goto end

:status
echo 📊 Status do repositório...
python tools/git_helper.py status
goto end

:commit
echo 💾 Commit interativo...
python tools/git_helper.py
goto end

:help
echo.
echo 🔧 Git Helper - Comandos Disponíveis:
echo.
echo git_quick.bat pull     - Fazer pull do GitHub
echo git_quick.bat push     - Push rápido automático
echo git_quick.bat status   - Ver status do repositório
echo git_quick.bat commit   - Commit interativo
echo git_quick.bat help     - Mostrar esta ajuda
echo.
echo 💡 Dica: Execute sem parâmetros para menu interativo!
echo.
goto end

:end
pause 