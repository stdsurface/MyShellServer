@echo off
setlocal enabledelayedexpansion
if /i "!PROCESSOR_ARCHITECTURE!" equ "AMD64" (
    set "arch_string=nt64"
) else (
    set "arch_string=nt32"
)

set "servername=myshellserver_!arch_string!"
pyinstaller -F -c -n "!servername!" -i "NONE" "ShellServerRunner.py"
rmdir /s /q "build"
del /f /q "!servername!.spec"
call remove_python_cache.bat
echo="compilation of !servername! finished."

set "servername=myshellclient_!arch_string!"
pyinstaller -F -c -n "!servername!" -i "NONE" "ShellClientLauncher.py"
rmdir /s /q "build"
del /f /q "!servername!.spec"
call remove_python_cache.bat
echo="compilation of !servername! finished."
