@echo off
setlocal enabledelayedexpansion
for /f "delims=" %%i in ('dir ".\*__pycache__" /s /b /a:d') do (
    rmdir /s /q "%%i"
    echo="%%i has been removed."
)
