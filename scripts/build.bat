@echo off
rem Build thehumanfrequency.net from _src/ Jinja2 templates to root HTML.
rem Usage:
rem   scripts\build.bat            Build everything
rem   scripts\build.bat --check    Render + diff, no writes
setlocal
set "PY=C:\Python314\python.exe"
set "REPO=%~dp0.."
cd /d "%REPO%"
"%PY%" "scripts\build.py" %*
endlocal
