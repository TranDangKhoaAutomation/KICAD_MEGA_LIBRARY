@echo off
REM ============================================================
REM  KiCad Mega Library - Cập nhật thư viện
REM  Copyright (c) Tran Dang Khoa
REM
REM  Thao tác:
REM   1. Pull cập nhật mới nhất từ 4 nhà sản xuất (Espressif,
REM      SparkFun, DigiKey, JLCPCB-CDFER) vào Sources/
REM   2. Dong bo file moi vao symbols/, footprints/, 3dmodels/
REM   3. Sua model paths 3D
REM   4. Dang ky lai bang thu vien trong KiCad
REM ============================================================
setlocal EnableDelayedExpansion
cd /d "%~dp0"

set "ROOT=D:\KICAD_MEGA_LIBRARY"
set "PYTHON=python"
set "LOG=%ROOT%\logs\update.log"

echo ============================================================
echo  KiCad Mega Library Update
echo  Copyright (c) Tran Dang Khoa
echo ============================================================
echo.

if not exist "%ROOT%\logs" mkdir "%ROOT%\logs" >nul 2>&1
echo [%date% %time%] === Update started === >> "%LOG%"

REM ---- 0. Kiem tra KiCad dang chay ----
tasklist /FI "IMAGENAME eq kicad.exe" 2>nul | find /I "kicad.exe" >nul
if %ERRORLEVEL%==0 (
    echo [CANH BAO] KiCad dang chay. Dong KiCad truoc khi cap nhat.
    echo [%date% %time%] SKIP: KiCad running >> "%LOG%"
    echo.
    pause
    exit /b 2
)

set "FAILED=0"

REM ---- 1. Pull cac repo nguon ----
call :UPDATE_REPO Espressif https://github.com/espressif/kicad-libraries.git
call :UPDATE_REPO SparkFun https://github.com/sparkfun/SparkFun-KiCad-Libraries.git
call :UPDATE_REPO DigiKey https://github.com/Digi-Key/digikey-kicad-library.git
call :UPDATE_REPO JLCPCB-CDFER https://github.com/CDFER/JLCPCB-Kicad-Library.git

echo.

REM ---- 2. Dong bo vao thu muc chung ----
echo [2/4] Dong bo thu vien vao symbols/ footprints/ 3dmodels/...
if exist "%ROOT%\resources\stage_libraries.py" (
    "%PYTHON%" "%ROOT%\resources\stage_libraries.py" >> "%LOG%" 2>&1
)
if exist "%ROOT%\resources\consolidate_3dmodels.py" (
    "%PYTHON%" "%ROOT%\resources\consolidate_3dmodels.py" >> "%LOG%" 2>&1
)
echo.

REM ---- 3. Sua model paths 3D ----
echo [3/4] Sua model paths 3D...
if exist "%ROOT%\resources\fix_3d_paths.py" (
    "%PYTHON%" "%ROOT%\resources\fix_3d_paths.py" >> "%LOG%" 2>&1
)
echo.

REM ---- 4. Dang ky lai bang thu vien ----
echo [4/4] Dang ky bang thu vien trong KiCad...
if exist "%ROOT%\resources\register_libraries.py" (
    "%PYTHON%" "%ROOT%\resources\register_libraries.py" >> "%LOG%" 2>&1
)
echo.

echo [%date% %time%] === Update complete (failed=%FAILED%) === >> "%LOG%"
echo.
echo ============================================================
if "%FAILED%"=="0" (
    echo  HOAN TAT! Thu vien da cap nhat.
) else (
    echo  HOAN TAT voi canh bao. Xem logs\update.log de biet chi tiet.
)
echo ============================================================
echo.
pause
exit /b %FAILED%

REM ============================================================
REM  Ham con: cap nhat 1 repo
REM ============================================================
:UPDATE_REPO
set "REPO=%~1"
set "URL=%~2"
set "DIR=%ROOT%\Sources\%REPO%"
echo.
echo [1/4] Cap nhat: %REPO%
if not exist "%DIR%\.git" (
    echo   - Chua clone, dang clone lan dau...
    git clone --depth 1 "%URL%" "%DIR%" >> "%LOG%" 2>&1
    if errorlevel 1 (
        echo   [LOI] Clone that bai
        set "FAILED=1"
    )
    exit /b
)
REM Kiem tra working tree sach
set "DIRTY="
pushd "%DIR%"
for /f %%L in ('git status --porcelain') do set "DIRTY=1"
popd
if defined DIRTY (
    echo   [CANH BAO] Repo co thay doi local, bo qua de tranh xung dot.
    echo   [%date% %time%] SKIP dirty: %REPO% >> "%LOG%"
    set "FAILED=1"
    exit /b
)
pushd "%DIR%"
git fetch --prune >> "%LOG%" 2>&1
git pull --ff-only >> "%LOG%" 2>&1
if errorlevel 1 (
    echo   [LOI] Pull that bai
    echo   [%date% %time%] FAIL pull: %REPO% >> "%LOG%"
    set "FAILED=1"
) else (
    for /f %%C in ('git rev-parse --short HEAD') do echo   - HEAD: %%C
)
popd
exit /b
