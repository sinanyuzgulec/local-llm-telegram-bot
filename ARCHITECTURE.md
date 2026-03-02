# Architecture and Features Overview

## Project Structure

```
local-llm-telegram-bot/
├── main.py                 # Bot application - Telegram command & message handlers
├── config.py               # Configuration - Loads settings from .env file
├── chat_history.py         # Chat history management - SQLite database operations
├── lm_integration.py       # LM Studio API integration - Communication with local model
├── file_handler.py         # File processing - PDF, DOCX, TXT, Images support
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Actual configuration (not in git)
├── .gitignore            # Git ignore rules
├── setup.py              # Python setup script with testing
├── setup.ps1             # Windows PowerShell automated setup
├── run-bot.bat           # Windows batch file to run bot easily
├── QUICKSTART_TR.md      # Quick start guide in Turkish
├── ARCHITECTURE.md       # This file
├── README.md             # Full documentation in Turkish
└── chat_history.db       # SQLite database (auto-created)
```

---

## Core Architecture

### 1. **Main Bot Application** (`main.py`)

**Responsibilities:**
- Telegram bot initialization and command handling
- Message routing and processing
- File upload handling
- Chat interaction with LM Studio

**Key Commands:**
- `/start` - Welcome message
- `/help` - Command help
- `/status` - LM Studio connection check
- `/history` - Show last 10 messages
- `/clear` - Clear chat history
- `/stats` - User statistics

**Features:**
- Async message handling
- File upload processing
- Auto-splitting of long responses (4096 char limit)
- Error handling and logging

---

### 2. **Configuration Management** (`config.py`)

**Loads from `.env` file:**
- Telegram API token
- LM Studio endpoint URL and model name
- Database path and limits
- File handling settings
- Logging configuration

**Environment Variables:**
```env
TELEGRAM_TOKEN              # Telegram bot token
LM_STUDIO_API_URL          # LM Studio server URL
LM_STUDIO_MODEL            # Model name in LM Studio
MAX_HISTORY_MESSAGES       # Messages to retain per user
MAX_FILE_SIZE_MB           # Maximum upload file size
ALLOWED_USERS              # User IDs that can use bot (optional)
```

---

### 3. **Chat History Management** (`chat_history.py`)

**Database Design:**

**Messages Table:**
```sql
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER)
- role (TEXT) - 'user' or 'assistant'
- content (TEXT)
- timestamp (DATETIME)
- file_name (TEXT) - optional
```

**User Stats Table:**
```sql
- user_id (INTEGER PRIMARY KEY)
- first_message (DATETIME)
- message_count (INTEGER)
- last_message (DATETIME)
```

**Key Methods:**
- `add_message()` - Save message to database
- `get_history()` - Retrieve conversation history
- `clear_history()` - Delete user's history
- `clear_all_history()` - Admin: clear all data
- `get_user_stats()` - Retrieve user statistics
- `get_formatted_history()` - Context string for LM

---

### 4. **LM Studio Integration** (`lm_integration.py`)

**API Integration:**
- Communicates with LM Studio via OpenAI-compatible API
- Endpoint: `http://localhost:1234/v1`

**Key Methods:**
- `check_connection()` - Verify LM Studio is running
- `send_message()` - Send message with context history
- `analyze_text()` - Analyze document text
- `list_available_models()` - Get available models

**Features:**
- Includes chat history in context
- System prompt customization
- Configurable temperature and max tokens
- Timeout handling

**Request Format:**
```json
{
  "model": "local-model",
  "messages": [
    {"role": "system", "content": "System prompt"},
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"},
    {"role": "user", "content": "Current message"}
  ],
  "temperature": 0.7,
  "max_tokens": 2000,
  "stream": false
}
```

---

### 5. **File Handling** (`file_handler.py`)

**Supported Formats:**
- **PDF** (.pdf) - Text extraction via PyPDF2
- **Text** (.txt) - Direct file reading
- **Word** (.docx, .doc) - Text extraction via python-docx
- **Images** (.jpg, .png, .gif, .webp) - Metadata via Pillow

**Key Methods:**
- `extract_text_from_pdf()` - PDF to text
- `extract_text_from_txt()` - Text file reading
- `extract_text_from_docx()` - DOCX to text
- `get_image_description()` - Image metadata
- `process_file()` - Universal file processor
- `is_valid_file()` - Validation (type & size)

**Security:**
- File type validation
- Size limits (default 50MB)
- Safe file path handling

---

## Data Flow

### Text Message Flow:

```
User Telegram Message
        ↓
[main.py] handle_text()
        ↓
[chat_history.py] get_history() → Load context
        ↓
[lm_integration.py] send_message() → Send to LM Studio
        ↓
LM Studio (Local Model)
        ↓
[lm_integration.py] Parse response
        ↓
[chat_history.py] add_message() → Save to database
        ↓
[main.py] Reply to user
```

### File Upload Flow:

```
User uploads File
        ↓
[main.py] handle_file()
        ↓
[file_handler.py] process_file() → Extract text
        ↓
[lm_integration.py] send_message() → Send to LM Studio
        ↓
LM Studio (Local Model)
        ↓
[chat_history.py] add_message() → Save with file_name
        ↓
[main.py] Reply to user with analysis
```

---

## Deployment Scenarios

### Local Machine (Windows)

1. **Setup Phase:**
   ```powershell
   .\setup.ps1
   ```

2. **Run Phase:**
   ```powershell
   python main.py
   # or
   .\run-bot.bat
   ```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python main.py
```

---

## Security Considerations

1. **Token Safety:**
   - `.env` file excluded from git (`.gitignore`)
   - Tokens not logged or exposed

2. **User Restrictions:**
   - Optional `ALLOWED_USERS` whitelist
   - Per-user history isolation

3. **File Validation:**
   - File type checking
   - Size limit enforcement
   - Safe path handling

4. **Data Privacy:**
   - All data stays on local machine
   - No cloud storage
   - Offline operation

---

## Error Handling

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "LM Studio connection failed" | LM Studio not running | Start LM Studio, check http://localhost:1234 |
| "TELEGRAM_TOKEN not found" | Missing `.env` file | Create `.env` from `.env.example` |
| "File processing failed" | Required library missing | Run `pip install -r requirements.txt` |
| "Timeout error" | LM Studio too slow | Increase `LM_STUDIO_TIMEOUT` in `.env` |
| "Memory error" | Context too large | Reduce `MAX_HISTORY_MESSAGES` |

---

## Performance Optimization

### Chat History Limits

Default: 50 messages (configurable)

```env
MAX_HISTORY_MESSAGES=50
```

Larger values = better context but slower responses.

### Token Limits

Default: 4000 tokens max context

```env
MAX_CONTEXT_TOKENS=4000
```

### Timeout Settings

Default: 60 seconds for API calls

```env
LM_STUDIO_TIMEOUT=60
```

---

## Future Enhancements

Possible improvements:

1. **Multiple Users:** Single bot instance for multiple Telegram users ✅ (Already implemented)
2. **Database Options:** PostgreSQL, MongoDB support
3. **Prompt Engineering:** Advanced system prompts
4. **Rate Limiting:** Control usage per user
5. **Webhooks:** Remove polling dependency
6. **Docker:** Container deployment
7. **Testing:** Unit tests and integration tests
8. **Monitoring:** Prometheus metrics
9. **Admin Panel:** Web UI for management
10. **Multi-language:** Support more languages

---

## Dependencies Explanation

### Core Dependencies:
- **python-telegram-bot** - Telegram Bot API wrapper
- **requests** - HTTP client for LM Studio API
- **python-dotenv** - Environment variable management

### File Processing:
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing
- **Pillow** - Image processing

### Optional/Future:
- **aiohttp** - Async HTTP (prepared for webhooks)
- **python-magic** - File type detection

---

## Logging

Logs are written to `bot.log`:

```
2024-03-02 12:34:56,789 - lm_integration - INFO - Sending request to LM Studio
2024-03-02 12:34:57,890 - main - DEBUG - User 123456: Hello world...
2024-03-02 12:34:58,991 - chat_history - INFO - Message added for user 123456
```

### Log Levels (in `.env`):
- `DEBUG` - Detailed information
- `INFO` - General information ✅ (Default)
- `WARNING` - Warning messages
- `ERROR` - Error messages

---

## Testing LM Studio Connection

Quick test script in PowerShell:

```powershell
# Check if LM Studio is running
curl http://localhost:1234/v1/models

# Expected response:
# {"data":[{"id":"local-model","object":"model"}]}
```

---

## License

This project is open source and free to use.

---

**Last Updated:** March 2, 2024
