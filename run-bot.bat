@echo off
REM Local LLM Telegram Bot - Windows Batch Dosyası
REM Bu dosya bot'u kolay çalıştırmanız için yapılmıştır

setlocal enabledelayedexpansion

echo.
echo ╔═══════════════════════════════════════════╗
echo ║   Local LLM Telegram Bot                  ║
echo ╚═══════════════════════════════════════════╝
echo.

REM Sanal ortamın var olup olmadığını kontrol et
if not exist "venv" (
    echo.
    echo ⚠️  venv klasörü bulunamadı!
    echo.
    echo Lütfen önce setup.ps1 dosyasını çalıştırın:
    echo   PowerShell'i açıp şunu yazın: .\setup.ps1
    echo.
    pause
    exit /b 1
)

REM .env dosyasını kontrol et
if not exist ".env" (
    echo.
    echo ⚠️  .env dosyası bulunamadı!
    echo.
    echo .env.example dosyasını kopyalıyorum...
    copy .env.example .env
    echo ✅ .env dosyası oluşturuldu
    echo.
    echo ⚠️  UYARI: .env dosyasını düzenleyiniz!
    echo   1. Notepad ile .env dosyasını açın
    echo   2. TELEGRAM_TOKEN yerine token'inizi yazın
    echo.
    pause
)

REM Sanal ortamı etkinleştir
echo 🔗 Sanal ortam etkinleştiriliyor...
call venv\Scripts\activate.bat

REM Bağımlılıkları kontrol et
echo 📦 Bağımlılıklar kontrol ediliyor...
pip show python-telegram-bot > nul
if errorlevel 1 (
    echo.
    echo ⚠️  Bağımlılıklar yüklenmemiş!
    echo.
    echo pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Bot'u çalıştır
echo.
echo 🚀 Bot başlatılıyor...
echo.
echo 💡 Bot çalışıyor. Çıkmak için Ctrl+C basın.
echo.

python main.py

REM Hata oluştuysa
if errorlevel 1 (
    echo.
    echo ❌ Bot hata ile durdu!
    echo.
    echo Kontrol Listesi:
    echo 1. LM Studio açık mı? (http://localhost:1234)
    echo 2. .env dosyasında TELEGRAM_TOKEN var mı?
    echo 3. bot.log dosyasında hata var mı?
    echo.
    pause
)

endlocal
