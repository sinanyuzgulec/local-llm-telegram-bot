import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Parse allowed users (comma-separated list)
_allowed_users_str = os.getenv('ALLOWED_USERS', '').strip()
if _allowed_users_str:
    try:
        ALLOWED_USERS = [int(uid.strip()) for uid in _allowed_users_str.split(',') if uid.strip()]
    except ValueError:
        ALLOWED_USERS = []
else:
    ALLOWED_USERS = []

# LM Studio Configuration
LM_STUDIO_API_URL = os.getenv('LM_STUDIO_API_URL', 'http://localhost:1234/v1')
LM_STUDIO_MODEL = os.getenv('LM_STUDIO_MODEL', 'local-model')
LM_STUDIO_TIMEOUT = int(os.getenv('LM_STUDIO_TIMEOUT', '60'))

# Chat History Configuration
CHAT_HISTORY_DB = os.getenv('CHAT_HISTORY_DB', 'chat_history.db')
MAX_HISTORY_MESSAGES = int(os.getenv('MAX_HISTORY_MESSAGES', '50'))
MAX_CONTEXT_TOKENS = int(os.getenv('MAX_CONTEXT_TOKENS', '4000'))

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'bot.log')

# File Handling
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '50'))
SUPPORTED_FILE_TYPES = ['pdf', 'txt', 'docx', 'doc', 'jpg', 'png', 'jpeg', 'gif', 'webp']

# Bot System Prompt
SYSTEM_PROMPT = """You are a helpful, polite, and accurate assistant.
Provide clear and understandable answers to user questions.
If you don't know something, clearly state that."""
