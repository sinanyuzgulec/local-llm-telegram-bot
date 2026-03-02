# 🚀 Hızlı Başlangıç Kılavuzu

## 5 Dakikada Kurulum

### Adım 1: Telegram Bot Token'i Alın

1. **Telegram**'da [@BotFather](https://t.me/BotFather) ile sohbet başlatın
2. `/newbot` yazın
3. Bot'a bir ad verin (örn: "LLM Asistanım")
4. Sizin kullanıcı adını yazın (örn: llm_assistant_bot)
5. Token'i kopyalayın ve saklayın

Token şöyle gözükür: `123456:ABCDefGHIjklMnOpQrsTuVwXyZaBcDeFg`

---

### Adım 2: Projeyi Hazırlayın

Komut satırını açın (PowerShell veya CMD) ve proje dizinine gelin:

```powershell
cd c:\Users\sinan\Desktop\GitHub\local-llm-telegram-bot
```

---

### Adım 3: Otomatik Kurulum (Windows)

**Sanal ortam oluştur ve bağımlılıkları yükle:**

```powershell
# PowerShell'de çalıştırun
.\setup.ps1
```

Veya **manuel olarak**:

```powershell
# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı etkinleştir
.\venv\Scripts\Activate.ps1

# Bağımlılıkları yükle
pip install -r requirements.txt
```

---

### Adım 4: Bot Token'ini Yapılandırın

**`.env` dosyasını oluştur/düzenle:**

```powershell
# İlk deyişse dosya oluşturulur
copy .env.example .env

# Notepad ile aç ve düzenle
notepad .env
```

Dosyanın içine bunu yazın:

```env
# Adım 1'de aldığınız token
TELEGRAM_TOKEN=123456:ABCDefGHIjklMnOpQrsTuVwXyZaBcDeFg

# Diğer ayarlar (varsayıland iyi)
LM_STUDIO_API_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=local-model
```

Dosyayı kaydedin ve kapatın.

---

### Adım 5: LM Studio'yu Başlatın

1. **LM Studio**'yu açın
2. Ana sayfadan bir model yükleyin
3. Model indirildikten sonra, **"Load model"** tuşuna basın
4. **http://localhost:1234** adresini ziyaret ederek sunucunun çalıştığını kontrol edin

---

### Adım 6: Bot'u Çalıştırın

```powershell
# Sanal ortamda iseniz
python main.py

# Çıktı şöyle gözükmelidir:
# 2024-03-02 12:34:56,789 - __main__ - INFO - Starting bot...
# 2024-03-02 12:34:57,890 - __main__ - INFO - Bot is running. Press Ctrl+C to stop.
```

---

### Adım 7: Telegram'da Bot'u Kullanmaya Başlayın

1. **Telegram**'u açın
2. Kurulum sırasında seçtiğiniz bot adını arayın
3. `/start` yazıp gönder
4. Bot size hoş geldiniz mesajı gönder

---

## ✨ İlk Mesajınız

```
Bot'a yazın:  "Merhaba! Nasılsın?"

Bot yanıtlar: "Merhaba! Ben bir AI asistanım. Size nasıl yardımcı olabilirim?"
```

---

## 📁 Dosya Yükleme

Telegrama şunları yapıştırabilirsiniz:

### PDF Dosya
```
Dosya: bildiri.pdf → Bot otomatik özet yapar
```

### Resim
```
Fotoğraf gönderin → Bot açıklaması yapılır
```

### Word Dosyası
```
Dosya: rapor.docx → Metni çıkarır ve analiz eder
```

---

## 🗑️ Sohbet Geçmişini Temizlemek

```
/clear  →  "✅ Sohbet geçmişiniz silindi."
```

---

## 🆘 Sorun Giderme

### Bot yanıt vermiyor

**1. LM Studio açık mı?**
```powershell
# Şu adresi tarayıcıda açın
http://localhost:1234
```

**2. Model yüklü mü?**
- LM Studio'da "Load model" tuşu gözüküyorsa model yüklenmiş demektir

**3. TELEGRAM_TOKEN doğru mu?**
```powershell
# .env dosyasını kontrol et
notepad .env
```

### "LM Studio bağlantısı başarısız" hatası

```powershell
# Bot günlüğünü kontrol et
notepad bot.log
```

Genellikle sebepleri:
- LM Studio kapalı
- Yanlış URL (`http://localhost:1234/v1` doğru mu?)
- Model yüklenmemiş

---

## 💡 Kullanışlı Komutlar

| Komut | Yapması |
|-------|---------|
| `/start` | Hoş geldiniz mesajı |
| `/help` | Tüm komutları göster |
| `/status` | LM Studio'nun açık olup olmadığını göster |
| `/history` | Son 10 mesajı göster |
| `/clear` | Sohbet geçmişini sil |
| `/stats` | Kaç mesaj yazdığını göster |

---

## ⚙️ Gelişmiş Ayarlar

`.env` dosyasında bu ayarları değiştirebilirsiniz:

```env
# Kaç mesaj hatırlanacak
MAX_HISTORY_MESSAGES=50

# Maksimum dosya boyutu (MB)
MAX_FILE_SIZE_MB=50

# Sadece belirli kişiler kullansın
ALLOWED_USERS=123456789,987654321
```

---

## 🔐 Güvenlik: Sadece Siz Kullansın

Başka kimsenin bot'u kullanmasını istemiyorsanız:

1. Telegram ID'nizi bulun (@userinfobot yazın Telegram'da)
2. `.env` dosyasında bunu yapın:

```env
ALLOWED_USERS=123456789
```

---

## 📝 Notlar

- Chat geçmişi otomatik kaydedilir
- Hiçbir verisi sunucuya gönderilmez (offline)
- Sadece yerel bilgisayarınızda çalışır

---

## 🎉 Kurulum Tamamlandı!

Artık Telegram'da yerel LLM modeliniz ile sohbet edebilirsiniz! 🤖

### Sonraki Adımlar:

1. ✅ Bot'u `/start` ile test et
2. ✅ Farklı mesajlar gönder
3. ✅ Dosya yükle ve analiz ettir
4. ✅ `/clear` ile geçmiş temizle

**Eğer sorun yaşarsanız:**
- Günlük dosyasını kontrol edin: `bot.log`
- README.md dosyasını okuyun
- LM Studio'nun çalışıp çalışmadığını kontrol edin

---

**Happy chatting! 🚀**
