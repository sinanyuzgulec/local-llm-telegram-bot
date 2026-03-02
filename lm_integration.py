import requests
import logging
from typing import Optional, List, Dict
from config import LM_STUDIO_API_URL, LM_STUDIO_MODEL, LM_STUDIO_TIMEOUT, SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class LMStudioAPI:
    """Handles communication with LM Studio API"""
    
    def __init__(self, api_url: str = LM_STUDIO_API_URL, model: str = LM_STUDIO_MODEL):
        self.api_url = api_url
        self.model = model
        self.chat_endpoint = f"{api_url}/chat/completions"
    
    def check_connection(self) -> bool:
        """Check if LM Studio server is running"""
        try:
            response = requests.get(
                f"{self.api_url}/models",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Cannot connect to LM Studio: {e}")
            return False
    
    def send_message(
        self,
        user_message: str,
        chat_history: Optional[List[Dict]] = None,
        system_prompt: str = SYSTEM_PROMPT,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """Send a message to LM Studio and get response"""
        
        try:
            # Build messages array
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add chat history if provided
            if chat_history:
                messages.extend(chat_history)
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            # Send request to LM Studio
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            logger.debug(f"Sending request to LM Studio: {payload}")
            
            response = requests.post(
                self.chat_endpoint,
                json=payload,
                timeout=LM_STUDIO_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result['choices'][0]['message']['content']
                logger.debug(f"Received response from LM Studio")
                return assistant_message
            else:
                logger.error(f"LM Studio error: {response.status_code} - {response.text}")
                return None
                
        except requests.Timeout:
            logger.error("Request to LM Studio timed out")
            return None
        except Exception as e:
            logger.error(f"Error communicating with LM Studio: {e}")
            return None
    
    def analyze_text(self, text: str, prompt: str = None) -> Optional[str]:
        """Analyze text from documents or images"""
        
        analysis_prompt = prompt or f"Aşağıdaki metni özetle:\n\n{text}"
        
        return self.send_message(
            analysis_prompt,
            max_tokens=1000
        )
    
    def list_available_models(self) -> List[str]:
        """Get list of available models from LM Studio"""
        try:
            response = requests.get(
                f"{self.api_url}/models",
                timeout=5
            )
            if response.status_code == 200:
                models = response.json()
                return [model['id'] for model in models.get('data', [])]
        except Exception as e:
            logger.error(f"Error fetching models: {e}")
        
        return []
