@echo off
setlocal enabledelayedexpansion
future-fstrings-show -h||(
    echo="future-fstrings is not installed. please use `pip install future-fstrings[rewrite]` to install it."
    goto lastline
)
call git_quickly.bat
for /f "delims=" %%i in ('dir ".\*.py" /s /b /a:-d') do (
    :choose_tmp_fil
    set "tmp_fil=%%~dpni.!random!.py"
    if exist "!tmp_fil!" (
        goto choose_tmp_fil
    )
    future-fstrings-show "%%i">"!tmp_fil!"&&(
        set "bsn_fil=%%~nxi"
        del /f /q "%%i"
        ren "!tmp_fil!" "!bsn_fil!"
        echo="%%i has been translated."
    )||(
        del /f /q "!tmp_fil!"
        echo="%%i has not been translated."
    )
)

:lastline
REM empty statement
