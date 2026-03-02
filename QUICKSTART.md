# Quick Start Guide

## 5-Minute Setup

### Step 1: Get Telegram Bot Token

1. Open Telegram and chat with [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "My LLM Assistant")
4. Choose a username (e.g., my_llm_assistant_bot)
5. Copy and save the token

Token format: `123456:ABCDefGHIjklMnOpQrsTuVwXyZaBcDeFg`

---

### Step 2: Clone and Setup Project

```bash
git clone https://github.com/sinanyuzgulec/local-llm-telegram-bot.git
cd local-llm-telegram-bot
```

---

### Step 3: Install Dependencies

**Automated (Windows):**
```powershell
.\setup.ps1
```

**Manual:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### Step 4: Configure Bot Token

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your token:

```env
TELEGRAM_TOKEN=YOUR_TOKEN_HERE
LM_STUDIO_API_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=local-model
```

---

### Step 5: Start LM Studio and Run Bot

1. Open LM Studio
2. Load a model
3. Verify server is running at http://localhost:1234

Run the bot:

```bash
python main.py
```

---

### Step 6: Use Bot on Telegram

1. Open Telegram
2. Find your bot by username
3. Send `/start`
4. Start chatting!

---

## First Commands

```
/start  - Initialize bot
/help   - Show all commands
/status - Check LM Studio connection
```

## File Support

Send these file types:
- PDF documents
- Word files (.docx)
- Text files (.txt)
- Images (.jpg, .png, .gif, .webp)

---

## Troubleshooting

**Bot not responding:**
1. Check LM Studio is running
2. Model is loaded
3. Check bot.log for errors

**"LM Studio connection failed":**
- Open http://localhost:1234 in browser
- Verify LM Studio server is active

**"Token not found":**
- Check .env file exists
- Verify TELEGRAM_TOKEN is set correctly

---

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Customize SYSTEM_PROMPT in config.py

---

Ready to chat with your local LLM via Telegram!
