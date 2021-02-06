@echo off
setlocal enabledelayedexpansion
pushd "%~dp0"
git status||(
    echo="git status errored."
    goto lastline
)
for /f "usebackq delims=" %%i in (`git status^|findstr /C:"nothing to commit, working tree clean"`) do (
    echo="working tree clean."
    goto lastline
)
git add .&&git commit -m m
echo="add and commit finished."

:lastline
popd
