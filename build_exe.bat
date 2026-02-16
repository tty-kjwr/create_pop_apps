@echo off
echo ========================================
echo ポップ作成ツール EXE ビルドスクリプト
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo エラー: Pythonがインストールされていません
    echo Python 3.8以上をインストールしてください
    pause
    exit /b 1
)

echo 1. 必要なライブラリをインストールしています...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo 2. EXEファイルを作成しています...
pyinstaller --onefile --windowed --name "ポップ作成ツール" --icon=NONE pop_creator.py

echo.
echo ========================================
echo ビルド完了！
echo ========================================
echo.
echo EXEファイルの場所: dist\ポップ作成ツール.exe
echo.
pause
