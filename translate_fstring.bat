@echo off
setlocal enabledelayedexpansion
for /f "delims=" %%i in ('dir "%~dp0*.py" /s /b /a:-d') do (
    :choose_tmp_fil
    set "tmp_fil=%%~dpni.!random!.py"
    if exist "!tmp_fil!" (
        goto choose_tmp_fil
    )
    future-fstrings-show "%%i">"!tmp_fil!"
    set "bsn_fil=%%~nxi"
    del /f /q "%%i"
    ren "!tmp_fil!" "!bsn_fil!"
    echo="%%i has been translated."
)
