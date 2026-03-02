# Local LLM Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org/)
[![LM Studio](https://img.shields.io/badge/LM%20Studio-Compatible-orange.svg)](https://lmstudio.ai/)

LM Studio'da çalışan yerel bir dil modelini Telegram üzerinde kullanmanıza olanak sağlayan Python tabanlı bir bot.

## Özellikler

- **Sohbet** - Doğal dil ile modelinizle konuşun
- **Dosya Desteği** - PDF, TXT, DOCX, resim dosyalarını yükleyip analiz edin
- **Sohbet Geçmişi** - Otomatik olarak tüm konuşmalar kaydedilir
- **Geçmiş Yönetimi** - Dilediğiniz zaman sohbet geçmişini temizleyin
- **Güvenlik** - Belirli kullanıcılara erişim sınırlaması
- **İstatistikler** - Sohbet istatistiklerini görüntüleyin
- **Hızlı Entegrasyon** - LM Studio ile otomatik bağlantı

## Gereksinimler

- Python 3.9+
- LM Studio (yerel model sunucusu)
- Telegram Bot Token

## Kurulum

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/sinanyuzgulec/local-llm-telegram-bot.git
cd local-llm-telegram-bot
```

### 2. Sanal Ortam Oluşturun

```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Ayarlayın

`.env.example` dosyasını kopyalayarak `.env` dosyası oluşturun:

```bash
copy .env.example .env
```

Sonra `.env` dosyasını düzenleyin:

```env
TELEGRAM_TOKEN=YOUR_TOKEN_HERE
LM_STUDIO_API_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=local-model
ALLOWED_USERS=123456789,987654321
```

## Kullanım

### LM Studio'yu Başlatın

1. LM Studio'yu açın
2. Bir model yükleyin
3. Server'in çalıştığını kontrol edin (http://localhost:1234)

### Bot'u Çalıştırın

```bash
python main.py
```

Bot çalışmaya başladığında, Telegram'da bot'u bularak başlayabilirsiniz.

## Telegram Komutları

| Komut | Açıklama |
|-------|----------|
| `/start` | Hoş geldiniz mesajı |
| `/help` | Tüm komutları göster |
| `/status` | LM Studio bağlantı durumu |
| `/history` | Son 10 mesajı göster |
| `/clear` | Sohbet geçmişini sil |
| `/stats` | Sohbet istatistikleri |

## Dosya Desteği

Aşağıdaki dosya tiplerini gönderebilirsiniz:

- **Metin**: `.txt` - Sade metin dosyaları
- **PDF**: `.pdf` - PDF dokümanları
- **Word**: `.docx`, `.doc` - Word dokümanları
- **Resim**: `.jpg`, `.png`, `.gif`, `.webp` - Görüntü dosyaları

**Maksimum dosya boyutu**: 50MB (`.env` dosyasında ayarlanabilir)

## Proje Yapısı

```
local-llm-telegram-bot/
├── main.py                 # Ana bot kodu
├── config.py              # Konfigürasyon ayarları
├── chat_history.py        # Sohbet geçmişi yönetimi
├── lm_integration.py      # LM Studio API entegrasyonu
├── file_handler.py        # Dosya işleme
├── requirements.txt       # Python bağımlılıkları
├── .env.example          # Ortam değişkenleri örneği
└── README.md            # Bu dosya
```

## Dosya Açıklamaları

### `main.py`
Ana bot uygulaması. Telegram komutlarını işler ve mesajları yönetir.

### `config.py`
Tüm konfigürasyon ayarlarını içerir. `.env` dosyasından değerleri okur.

### `chat_history.py`
SQLite veritabanı kullanarak sohbet geçmişini yönetir. Mesajları saklar, geçmişi temizler.

### `lm_integration.py`
LM Studio API'si ile iletişim. Mesajları gönderir ve yanıtları alır.

### `file_handler.py`
PDF, DOCX, TXT ve resim dosyalarını işler. Metni çıkartır ve analiz eder.

## ⚙️ Konfigürasyon Seçenekleri

### LM Studio Ayarları

```env
# API endpoint (varsayılan)
LM_STUDIO_API_URL=http://localhost:1234/v1

# Model adı (LM Studio'daki model adı)
LM_STUDIO_MODEL=local-model

# Timeout (saniye)
LM_STUDIO_TIMEOUT=60
```

## Konfigürasyon Seçenekleri

### LM Studio Ayarları

```env
LM_STUDIO_API_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=local-model
LM_STUDIO_TIMEOUT=60
```

### Sohbet Ayarları

```env
MAX_HISTORY_MESSAGES=50
MAX_CONTEXT_TOKENS=4000
```

### Dosya Ayarları

```env
MAX_FILE_SIZE_MB=50
```

### Güvenlik

```env
ALLOWED_USERS=123456789,987654321
```

## Sorun Giderme

### "LM Studio bağlantısı başarısız"

1. LM Studio'nun açık olduğunu kontrol edin
2. Bir model yüklendiğini doğrulayın
3. URL doğru olduğunu kontrol edin: `http://localhost:1234`

### "Telegram Token bulunamadı"

1. `.env` dosyasının mevcut olduğunu kontrol edin
2. `TELEGRAM_TOKEN` değerinin boş olmadığını kontrol edin
3. Token'i https://t.me/BotFather adresinden alın

### "Dosya işlenemedi"

- Dosya türünün desteklendiğini kontrol edin
- Dosya boyutunun limiti aşmadığını kontrol edin
- Gerekli kütüphanelerin yüklü olduğunu kontrol edin

## Veritabanı

Sohbet geçmişi `chat_history.db` dosyasında SQLite veritabanı olarak saklanır.

### Tablo Yapısı

**Messages Tablosu:**
- `id` - Mesaj ID'si
- `user_id` - Kullanıcı ID'si (Telegram)
- `role` - 'user' veya 'assistant'
- `content` - Mesaj içeriği
- `timestamp` - Zaman damgası
- `file_name` - Dosya adı (varsa)

**User Stats Tablosu:**
- `user_id` - Kullanıcı ID'si
- `first_message` - İlk mesaj zamanı
- `message_count` - Toplam mesaj sayısı
- `last_message` - Son mesaj zamanı

## Güvenlik Notları

1. **Token Gizliliği**: `.env` dosyasını git'e commit etmeyin
2. **Kullanıcı Kısıtlaması**: Güvenli kullanmak için `ALLOWED_USERS` ayarlayın
3. **Dosya Kontrolleri**: Maksimum dosya boyutunu sınırlayın
4. **Günlükler**: Hassas bilgileri günlüklere yazılı olmayacak şekilde ayarlayın

## Katkıda Bulunma

Geliştirmeler ve düzeltmeler için issue açabilir veya PR gönderebilirsiniz.

## Lisans

Bu proje MIT lisansı altındadır. Serbestçe kullanabilirsiniz.

**S: Birden fazla model kullanabilir miyim?**
A: Evet, `LM_STUDIO_MODEL` değerini değiştirerek başka modeller kullanabilirsiniz.

**S: Geçmiş tamamen silinir mi?**
A: Evet, `/clear` komutu kullanıcının tüm geçmişini siler.

**S: Türkçe destekler mi?**
A: Evet, tamamen Türkçe desteklidir. Modeliniz Türkçe destekliyse yanıtlar da Türkçe olur.

**S: Offline çalışır mı?**
A: Evet, tamamen offline çalışır. Sadece Telegram'a bağlantı gerekli (API call için).

## Sınırlamalar

- Dosya boyutu 50MB ile sınırlıdır (yapılandırılabilir)
- Telegram mesajı 4096 karakterle sınırlıdır (bot otomatik böler)
- Sohbet geçmişi varsayılan 50 mesajla sınırlıdır

## Destek

Sorun yaşarsanız `bot.log` dosyasını kontrol edin ve GitHub issues'de soru açabilirsiniz.

---

Made with Python and LM Studio
