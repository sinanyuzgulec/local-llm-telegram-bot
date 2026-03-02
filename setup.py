#!/usr/bin/env python3
"""
Setup script for Local LLM Telegram Bot
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("ERROR: Python 3.9+ is required")
        return False
    print(f"OK: Python {sys.version.split()[0]} detected")
    return True

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("WARNING: .env file not found")
        print("INFO: Copying .env.example to .env...")
        
        with open('.env.example', 'r') as src:
            content = src.read()
        with open('.env', 'w') as dst:
            dst.write(content)
        
        print("OK: .env file created")
        print("ACTION REQUIRED: Edit .env file and set TELEGRAM_TOKEN")
        return False
    
    print("OK: .env file found")
    return True

def install_requirements():
    """Install required packages"""
    print("\nINFO: Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("OK: Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install dependencies")
        return False

def test_lm_studio():
    """Test LM Studio connection"""
    print("\nINFO: Testing LM Studio connection...")
    
    try:
        from lm_integration import LMStudioAPI
        api = LMStudioAPI()
        
        if api.check_connection():
            print("OK: LM Studio connection successful")
            models = api.list_available_models()
            if models:
                print(f"INFO: Available models: {', '.join(models)}")
            return True
        else:
            print("WARNING: Cannot connect to LM Studio")
            print("INFO: Make sure LM Studio is running at http://localhost:1234")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_telegram_token():
    """Check Telegram token"""
    print("\nINFO: Checking Telegram token...")
    
    from config import TELEGRAM_TOKEN
    
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "YOUR_TELEGRAM_TOKEN_HERE":
        print("ERROR: TELEGRAM_TOKEN not configured")
        print("INFO: Get token from https://t.me/BotFather")
        print("INFO: Update TELEGRAM_TOKEN in .env file")
        return False
    
    print("OK: TELEGRAM_TOKEN configured")
    return True

def main():
    """Run setup"""
    print("""
===============================================
   Local LLM Telegram Bot - Setup
===============================================
    """)
    
    if not check_python():
        return False
    
    env_ok = check_env_file()
    
    if not install_requirements():
        return False
    
    try:
        lm_ok = test_lm_studio()
    except:
        lm_ok = False
        print("WARNING: Cannot test LM Studio (dependencies may not be installed)")
    
    try:
        tg_ok = test_telegram_token()
    except:
        tg_ok = False
        print("WARNING: Cannot check Telegram token")
    
    print("""
===============================================
   Setup Summary
===============================================
    """)
    
    if not env_ok:
        print("ACTION REQUIRED: Edit .env file and add TELEGRAM_TOKEN")
    
    if not lm_ok:
        print("ACTION REQUIRED: Start LM Studio")
    
    if not tg_ok:
        print("ACTION REQUIRED: Add Telegram token to .env file")
    
    print("""
Setup complete!

To start the bot:
   python main.py

First time setup:
   1. Open LM Studio (http://localhost:1234)
   2. Load a model
   3. Start the bot
   4. Find your bot on Telegram and send /start

For more information, read README.md
    """)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled")
        sys.exit(1)
