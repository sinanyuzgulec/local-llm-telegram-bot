import os
import logging
from typing import Optional, Tuple
from pathlib import Path
import io

logger = logging.getLogger(__name__)

try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("PyPDF2 not installed, PDF support disabled")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("Pillow not installed, Image support disabled")

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    logger.warning("python-docx not installed, DOCX support disabled")


class FileHandler:
    """Handles file processing for various formats"""
    
    SUPPORTED_FORMATS = {
        'pdf': 'application/pdf',
        'txt': 'text/plain',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'doc': 'application/msword',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> Optional[str]:
        """Extract text from PDF file"""
        if not PDF_AVAILABLE:
            logger.warning("PDF support not available")
            return None
        
        try:
            text = []
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            
            result = "\n".join(text)
            logger.info(f"Extracted text from PDF: {len(result)} characters")
            return result
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            return None
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> Optional[str]:
        """Read text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            logger.info(f"Read text file: {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"Error reading text file: {e}")
            return None
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> Optional[str]:
        """Extract text from DOCX file"""
        if not DOCX_AVAILABLE:
            logger.warning("DOCX support not available (install python-docx)")
            return None
        
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            logger.info(f"Extracted text from DOCX: {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"Error extracting DOCX text: {e}")
            return None
    
    @staticmethod
    def get_image_description(file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """Get basic image information"""
        if not PIL_AVAILABLE:
            logger.warning("Image support not available (install Pillow)")
            return None, None
        
        try:
            image = Image.open(file_path)
            info = f"Görüntü türü: {image.format}, Boyut: {image.size}, Mod: {image.mode}"
            logger.info(f"Image processed: {info}")
            return file_path, info
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return None, None
    
    @staticmethod
    def process_file(file_path: str, file_type: str) -> Optional[str]:
        """Process any supported file and extract text content"""
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        
        file_type = file_type.lower()
        
        if file_type in ['pdf']:
            return FileHandler.extract_text_from_pdf(file_path)
        elif file_type in ['txt']:
            return FileHandler.extract_text_from_txt(file_path)
        elif file_type in ['docx', 'doc']:
            return FileHandler.extract_text_from_docx(file_path)
        elif file_type in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            _, description = FileHandler.get_image_description(file_path)
            if description:
                return f"[Görüntü: {description}] - Lütfen bu görseli analiz et."
            return "[Görüntü dosyası işlendi]"
        else:
            logger.warning(f"Unsupported file type: {file_type}")
            return None
    
    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """Get file size in MB"""
        try:
            return os.path.getsize(file_path) / (1024 * 1024)
        except Exception as e:
            logger.error(f"Error getting file size: {e}")
            return 0
    
    @staticmethod
    def is_valid_file(file_path: str, max_size_mb: int = 50) -> Tuple[bool, str]:
        """Validate file type and size"""
        
        if not os.path.exists(file_path):
            return False, "Dosya bulunamadı"
        
        # Check file extension
        file_ext = Path(file_path).suffix.lower().lstrip('.')
        if file_ext not in FileHandler.SUPPORTED_FORMATS:
            return False, f"Desteklenmeyen dosya tipi: {file_ext}"
        
        # Check file size
        file_size_mb = FileHandler.get_file_size_mb(file_path)
        if file_size_mb > max_size_mb:
            return False, f"Dosya çok büyük ({file_size_mb:.2f}MB > {max_size_mb}MB)"
        
        return True, "OK"
