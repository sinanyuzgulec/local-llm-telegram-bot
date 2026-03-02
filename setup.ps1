# Local LLM Telegram Bot - Windows Kurulum Scripti
# Bu script otomatik olarak venv oluşturur ve bağımlılıkları yükler

Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Local LLM Telegram Bot - Windows Kur   ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Python versiyonu kontrol et
Write-Host "🐍 Python versiyonu kontrol ediliyor..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "  $pythonVersion" -ForegroundColor Green

# Sanal ortam oluştur
if (Test-Path "venv") {
    Write-Host "✅ venv klasörü zaten var" -ForegroundColor Green
} else {
    Write-Host "⚙️  Sanal ortam oluşturuluyor..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Sanal ortam oluşturuldu" -ForegroundColor Green
    } else {
        Write-Host "❌ Sanal ortam oluşturulamadı" -ForegroundColor Red
        exit 1
    }
}

# Sanal ortamı etkinleştir
Write-Host "🔗 Sanal ortam etkinleştiriliyor..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Bağımlılıkları yükle
Write-Host "📦 Bağımlılıkları yüklüyorum..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Bağımlılıklar yüklendi" -ForegroundColor Green
} else {
    Write-Host "❌ Bağımlılıklar yüklenemedi" -ForegroundColor Red
    exit 1
}

# .env dosyası kontrol et
if (!(Test-Path ".env")) {
    Write-Host "⚠️  .env dosyası bulunamadı" -ForegroundColor Yellow
    Write-Host "📝 .env.example dosyasını kopyalıyorum..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env dosyası oluşturuldu" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  UYARI: Lütfen .env dosyasını düzenleyiniz!" -ForegroundColor Magenta
    Write-Host "   1. Notepad ile .env dosyasını açın" -ForegroundColor Cyan
    Write-Host "   2. TELEGRAM_TOKEN yerine bot token'inizi yazın" -ForegroundColor Cyan
    Write-Host "   3. Token şu adresten alınız: https://t.me/BotFather" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Kurulum Tamamlandı!                    ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 Bot'u başlatmak için:" -ForegroundColor Green
Write-Host "   python main.py" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Başlamadan önce kontrol edin:" -ForegroundColor Yellow
Write-Host "   1. ✅ LM Studio açık mı? (http://localhost:1234)" -ForegroundColor Cyan
Write-Host "   2. ✅ Bir model yüklü mü?" -ForegroundColor Cyan
Write-Host "   3. ✅ .env dosyasında TELEGRAM_TOKEN var mı?" -ForegroundColor Cyan
Write-Host ""

Write-Host "💡 İpucu: 'python main.py' yazarak bot'u başlatabilirsiniz" -ForegroundColor Green
