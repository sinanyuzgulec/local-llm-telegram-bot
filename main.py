#!/usr/bin/env python3
"""
Local LLM Telegram Bot
Integrates LM Studio with Telegram for chat, file handling, and persistent history
"""

import logging
import os
import asyncio
from pathlib import Path
from telegram import Update, MenuButtonCommands
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
)
from telegram.constants import ChatAction

from config import (
    TELEGRAM_TOKEN, ALLOWED_USERS, MAX_FILE_SIZE_MB, LOG_FILE, LOG_LEVEL
)
from chat_history import ChatHistory
from lm_integration import LMStudioAPI
from file_handler import FileHandler

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize modules
chat_history = ChatHistory()
lm_api = LMStudioAPI()
file_handler = FileHandler()


class TelegramBot:
    """Telegram bot handler"""
    
    def __init__(self):
        self.app = None
        self.chat_history = chat_history
        self.lm_api = lm_api
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        user_id = update.effective_user.id
        
        if ALLOWED_USERS and user_id not in ALLOWED_USERS:
            await update.message.reply_text("Access denied.")
            return
        
        welcome_text = """
*Welcome!*

This bot connects your Telegram to LM Studio running on your local machine.

*Features:*
- Chat with your local LLM
- Analyze PDF, TXT, DOCX files
- Process images
- Automatic chat history
- Clear history anytime

*Commands:*
/help - Show all commands
/history - Recent messages
/clear - Clear chat history
/status - Bot status
/stats - Statistics

Send a PDF, TXT, DOCX, or image to get started!
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
        logger.info(f"User {user_id} started the bot")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        help_text = """
*Commands:*

/start - Welcome message
/help - This message
/status - LM Studio connection status
/history - Show last 10 messages
/clear - Clear chat history
/stats - Chat statistics

*Supported Files:*
- PDF (.pdf)
- Text (.txt)
- Word (.docx, .doc)
- Images (.jpg, .png, .gif, .webp)

*Max file size:* {0}MB
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check if LM Studio is connected"""
        if self.lm_api.check_connection():
            models = self.lm_api.list_available_models()
            status_text = "LM Studio connected\n\nModels:\n"
            for model in models:
                status_text += f"- {model}\n"
            
            if not models:
                status_text += "- No models loaded"
            
            await update.message.reply_text(status_text)
        else:
            await update.message.reply_text(
                "LM Studio connection failed.\n\n"
                "Make sure LM Studio is running:\n"
                f"http://localhost:1234"
            )
    
    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show chat history"""
        user_id = update.effective_user.id
        history = self.chat_history.get_history(user_id, limit=10)
        
        if not history:
            await update.message.reply_text("No chat history yet.")
            return
        
        history_text = "*Last 10 Messages:*\n\n"
        for i, msg in enumerate(history, 1):
            role = "You" if msg['role'] == 'user' else "Bot"
            content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
            history_text += f"{i}. {role}: {content}\n"
        
        await update.message.reply_text(history_text, parse_mode='Markdown')
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clear chat history"""
        user_id = update.effective_user.id
        self.chat_history.clear_history(user_id)
        await update.message.reply_text("Chat history cleared.")
        logger.info(f"User {user_id} cleared their chat history")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show chat statistics"""
        user_id = update.effective_user.id
        stats = self.chat_history.get_user_stats(user_id)
        
        if not stats:
            await update.message.reply_text("No statistics available yet.")
            return
        
        stats_text = f"""
*Chat Statistics*

User ID: {user_id}
Total Messages: {stats['message_count']}
First Message: {stats['first_message']}
Last Message: {stats['last_message']}
        """
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user_id = update.effective_user.id
        user_message = update.message.text
        
        logger.debug(f"Received text message from user {user_id}: {user_message}")
        
        if ALLOWED_USERS and user_id not in ALLOWED_USERS:
            logger.warning(f"User {user_id} not in allowed users list")
            await update.message.reply_text("❌ Erişim izniniz yok.")
            return
        
        # Show typing indicator
        await update.message.chat.send_action(ChatAction.TYPING)
        
        try:
            logger.debug(f"Getting chat history for user {user_id}")
            # Get chat history for context
            history = self.chat_history.get_history(user_id, limit=10)
            history_messages = [
                {"role": msg['role'], "content": msg['content']} 
                for msg in history
            ]
            
            logger.debug(f"Sending message to LM Studio API")
            # Send to LM Studio
            response = self.lm_api.send_message(
                user_message,
                chat_history=history_messages
            )
            
            if response:
                logger.debug(f"Got response from LM Studio")
                # Save to history
                self.chat_history.add_message(user_id, 'user', user_message)
                self.chat_history.add_message(user_id, 'assistant', response)
                
                # Reply to user
                # Split long responses
                if len(response) > 4096:
                    parts = [response[i:i+4096] for i in range(0, len(response), 4096)]
                    for part in parts:
                        await update.message.reply_text(part)
                else:
                    await update.message.reply_text(response)
                
                logger.info(f"User {user_id}: {user_message[:50]}... → Response sent")
            else:
                logger.error(f"No response from LM Studio")
                await update.message.reply_text(
                    "No response from LM Studio. Please try again later."
                )
        
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            await update.message.reply_text("An error occurred. Please try again later.")
    
    async def handle_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle file uploads (PDF, DOCX, TXT, Images)"""
        user_id = update.effective_user.id
        
        if ALLOWED_USERS and user_id not in ALLOWED_USERS:
            await update.message.reply_text("Access denied.")
            return
        
        # Determine file information
        if update.message.document:
            file_info = update.message.document
            filename = file_info.file_name
        elif update.message.photo:
            file_info = update.message.photo[-1]
            filename = f"photo_{user_id}_{update.message.photo[0].file_id}.jpg"
        else:
            await update.message.reply_text("Unsupported file type.")
            return
        
        # Get file extension
        file_ext = Path(filename).suffix.lower().lstrip('.')
        
        # Validate file
        is_valid, validation_msg = file_handler.is_valid_file(filename, MAX_FILE_SIZE_MB)
        if not is_valid:
            await update.message.reply_text(f"Error: {validation_msg}")
            return
        
        try:
            await update.message.chat.send_action(ChatAction.TYPING)
            
            # Download file
            tg_file = await context.bot.get_file(file_info.file_id)
            file_path = f"temp_{user_id}_{filename}"
            await tg_file.download_to_drive(file_path)
            
            # Process file
            extracted_text = file_handler.process_file(file_path, file_ext)
            
            if extracted_text:
                # Create message for LM Studio
                file_message = f"File: {filename}\n\nContent:\n{extracted_text[:2000]}"
                
                # Get chat history
                history = self.chat_history.get_history(user_id, limit=5)
                history_messages = [
                    {"role": msg['role'], "content": msg['content']} 
                    for msg in history
                ]
                
                # Send to LM Studio
                response = self.lm_api.send_message(
                    file_message,
                    chat_history=history_messages
                )
                
                if response:
                    # Save to history
                    self.chat_history.add_message(user_id, 'user', file_message, filename)
                    self.chat_history.add_message(user_id, 'assistant', response)
                    
                    # Send response
                    reply = f"*{filename}* processed:\n\n{response}"
                    await update.message.reply_text(reply, parse_mode='Markdown')
                else:
                    await update.message.reply_text("Failed to process file.")
            else:
                await update.message.reply_text("Failed to extract file content.")
            
            # Cleanup
            if os.path.exists(file_path):
                os.remove(file_path)
        
        except Exception as e:
            logger.error(f"Error handling file: {e}")
            await update.message.reply_text("File processing error. Please try again.")
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Log errors"""
        logger.error(msg="Exception while handling an update:", exc_info=context.error)
    
    async def post_init(self, application: Application):
        """Post initialization setup"""
        logger.info("Bot initialized successfully")
    
    def setup(self):
        """Setup the bot"""
        
        # Check LM Studio connection
        if not lm_api.check_connection():
            logger.warning("LM Studio is not running. Bot will show connection errors.")
        
        # Create application
        self.app = Application.builder().token(TELEGRAM_TOKEN).post_init(
            self.post_init
        ).build()
        
        # Add handlers
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("history", self.history_command))
        self.app.add_handler(CommandHandler("clear", self.clear_command))
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        
        # File handlers (Document + Photo)
        self.app.add_handler(MessageHandler(
            filters.Document.ALL,
            self.handle_file
        ))
        self.app.add_handler(MessageHandler(
            filters.PHOTO,
            self.handle_file
        ))
        
        # Text handler
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_text
        ))
        
        # Error handler
        self.app.add_error_handler(self.error_handler)
        
        logger.info("Bot setup completed")
    
    async def run(self):
        """Run the bot"""
        logger.info("Starting bot...")
        await self.app.initialize()
        await self.app.start()
        try:
            await self.app.updater.start_polling(allowed_updates=None)
            logger.info("Bot is running. Press Ctrl+C to stop.")
            await asyncio.Event().wait()  # Keep running
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        finally:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
    
    async def stop(self):
        """Stop the bot"""
        logger.info("Stopping bot...")
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()


async def main():
    """Main entry point"""
    
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not found in environment variables!")
        return
    
    bot = TelegramBot()
    bot.setup()
    
    try:
        await bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        await bot.stop()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
