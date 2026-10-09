@echo off
setlocal
set "ACM_BUNDLED_PY=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%ACM_BUNDLED_PY%" goto bundled
py -3 --version >nul 2>&1
if not errorlevel 1 goto launcher
python --version >nul 2>&1
if not errorlevel 1 goto python
echo Python 3.10 or newer is required.
goto finish
:bundled
"%ACM_BUNDLED_PY%" "%~dp0search_acm.py" --demo
goto finish
:launcher
py -3 "%~dp0search_acm.py" --demo
goto finish
:python
python "%~dp0search_acm.py" --demo
:finish
echo.
pause
