import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import logging
from config import CHAT_HISTORY_DB, MAX_HISTORY_MESSAGES

logger = logging.getLogger(__name__)


class ChatHistory:
    """Manages chat history for users"""
    
    def __init__(self, db_path: str = CHAT_HISTORY_DB):
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self):
        """Create database tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    file_name TEXT
                )
            ''')
            
            # Create user stats table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_stats (
                    user_id INTEGER PRIMARY KEY,
                    first_message DATETIME DEFAULT CURRENT_TIMESTAMP,
                    message_count INTEGER DEFAULT 0,
                    last_message DATETIME
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def add_message(self, user_id: int, role: str, content: str, file_name: Optional[str] = None):
        """Add a message to chat history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert message
            cursor.execute('''
                INSERT INTO messages (user_id, role, content, file_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, role, content, file_name))
            
            # Update user stats
            cursor.execute('''
                INSERT INTO user_stats (user_id, message_count, last_message)
                VALUES (?, 1, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET
                    message_count = message_count + 1,
                    last_message = CURRENT_TIMESTAMP
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            logger.debug(f"Message added for user {user_id}")
        except Exception as e:
            logger.error(f"Error adding message: {e}")
    
    def get_history(self, user_id: int, limit: int = MAX_HISTORY_MESSAGES) -> List[Dict]:
        """Get chat history for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT role, content, timestamp, file_name
                FROM messages
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    'role': row[0],
                    'content': row[1],
                    'timestamp': row[2],
                    'file_name': row[3]
                })
            
            conn.close()
            # Return in chronological order (oldest first)
            return list(reversed(messages))
        except Exception as e:
            logger.error(f"Error retrieving history: {e}")
            return []
    
    def clear_history(self, user_id: int) -> bool:
        """Clear chat history for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM messages WHERE user_id = ?', (user_id,))
            conn.commit()
            conn.close()
            
            logger.info(f"Chat history cleared for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
            return False
    
    def clear_all_history(self) -> bool:
        """Clear all chat history (admin only)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM messages')
            cursor.execute('DELETE FROM user_stats')
            conn.commit()
            conn.close()
            
            logger.warning("All chat history cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing all history: {e}")
            return False
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get statistics for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT first_message, message_count, last_message
                FROM user_stats
                WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'first_message': result[0],
                    'message_count': result[1],
                    'last_message': result[2]
                }
            return {}
        except Exception as e:
            logger.error(f"Error retrieving user stats: {e}")
            return {}
    
    def get_formatted_history(self, user_id: int, max_chars: int = 2000) -> str:
        """Get formatted history for context"""
        history = self.get_history(user_id)
        formatted = []
        char_count = 0
        
        for msg in history:
            role = "Siz" if msg['role'] == 'user' else "Asistan"
            text = f"{role}: {msg['content'][:100]}..."  # Kısalt
            
            if char_count + len(text) > max_chars:
                break
            
            formatted.append(text)
            char_count += len(text)
        
        return "\n".join(formatted)
