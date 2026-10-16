"""
File Parsing Utilities
Supports text extraction from PDF, Markdown, and TXT files
"""

import os
from pathlib import Path
from typing import List, Optional


def _read_text_with_fallback(file_path: str) -> str:
    """
    Read text file with automatic encoding fallback.
    
    Fallback strategy:
    1. Try standard UTF-8 decode
    2. Use charset_normalizer to detect encoding
    3. Fallback to chardet
    4. Ultimate fallback: UTF-8 with errors='replace'
    
    Args:
        file_path: File system path
        
    Returns:
        Decoded text string
    """
    data = Path(file_path).read_bytes()
    
    # Try UTF-8 first
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        pass
    
    # Try charset_normalizer
    encoding = None
    try:
        from charset_normalizer import from_bytes
        best = from_bytes(data).best()
        if best and best.encoding:
            encoding = best.encoding
    except Exception:
        pass
    
    # Fallback to chardet
    if not encoding:
        try:
            import chardet
            result = chardet.detect(data)
            encoding = result.get('encoding') if result else None
        except Exception:
            pass
    
    if not encoding:
        encoding = 'utf-8'
    
    return data.decode(encoding, errors='replace')


import logging

logger = logging.getLogger(__name__)


class FileParser:
    """File parsing utility class"""
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.md', '.markdown', '.txt', '.png', '.jpg', '.jpeg', '.webp'}
    
    @classmethod
    def is_supported(cls, file_path: str) -> bool:
        """Check if file format is supported"""
        suffix = Path(file_path).suffix.lower()
        return suffix in cls.SUPPORTED_EXTENSIONS
    
    @classmethod
    def extract_text(cls, file_path: str) -> str:
        """Extract text from file"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = path.suffix.lower()
        
        if suffix not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file format: {suffix}")
        
        if suffix == '.pdf':
            return cls._extract_from_pdf(file_path)
        elif suffix in {'.md', '.markdown'}:
            return cls._extract_from_md(file_path)
        elif suffix == '.txt':
            return cls._extract_from_txt(file_path)
        elif suffix in {'.png', '.jpg', '.jpeg', '.webp'}:
            return cls._extract_from_image(file_path)
        
        raise ValueError(f"Unable to process format: {suffix}")

    @classmethod
    def _extract_from_image(cls, file_path: str) -> str:
        """Extract text from image using Gemma 4 multimodal or fallback metadata"""
        path = Path(file_path)
        suffix = path.suffix.lower()
        mime_map = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.webp': 'image/webp'
        }
        mime_type = mime_map.get(suffix, 'image/jpeg')

        try:
            from ..services.gemma_service import GemmaService
            service = GemmaService()
            with open(file_path, 'rb') as f:
                img_bytes = f.read()

            result = service.analyze_notice(image_bytes=img_bytes, mime_type=mime_type)
            if result.get("success") and result.get("data"):
                data = result["data"]
                lines = [
                    f"Notice Title: {data.get('title') or path.stem}",
                    f"Category: {data.get('category') or 'General'}",
                    f"Summary: {data.get('summary') or ''}",
                    f"Organizer: {data.get('organizer') or 'N/A'}",
                    f"Event Date: {data.get('event_date') or 'N/A'}",
                    f"Registration Deadline: {data.get('registration_deadline') or 'N/A'}",
                    f"Venue: {data.get('venue') or 'N/A'}"
                ]
                if data.get('eligibility'):
                    lines.append(f"Eligibility: {', '.join(data['eligibility'])}")
                if data.get('requirements'):
                    lines.append(f"Requirements: {', '.join(data['requirements'])}")
                if data.get('action_items'):
                    action_texts = [f"- {item.get('task')} (Deadline: {item.get('deadline', 'N/A')})" for item in data['action_items']]
                    lines.append("Action Items:\n" + "\n".join(action_texts))
                if data.get('source_evidence'):
                    lines.append("Source Text & Evidence:\n" + "\n".join(data['source_evidence']))
                return "\n\n".join(lines)
        except Exception as e:
            logger.warning(f"Image text extraction via Gemma failed for {file_path}: {e}")

        return f"[Campus Notice Poster: {path.name} (Format: {suffix.upper()})]"
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF using PyMuPDF"""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError("PyMuPDF required: pip install PyMuPDF")
        
        text_parts = []
        with fitz.open(file_path) as doc:
            for page in doc:
                text = page.get_text()
                if text.strip():
                    text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    @staticmethod
    def _extract_from_md(file_path: str) -> str:
        """Extract text from Markdown file"""
        return _read_text_with_fallback(file_path)
    
    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        return _read_text_with_fallback(file_path)
    
    @classmethod
    def extract_from_multiple(cls, file_paths: List[str]) -> str:
        """Extract and concatenate text from multiple files"""
        all_texts = []
        
        for i, file_path in enumerate(file_paths, 1):
            try:
                text = cls.extract_text(file_path)
                filename = Path(file_path).name
                all_texts.append(f"=== Document {i}: {filename} ===\n{text}")
            except Exception as e:
                all_texts.append(f"=== Document {i}: {file_path} (Extraction failed: {str(e)}) ===")
        
        return "\n\n".join(all_texts)


def split_text_into_chunks(
    text: str, 
    chunk_size: int = 500, 
    overlap: int = 50
) -> List[str]:
    """
    Split text into chunks with overlap
    
    Args:
        text: Raw source text
        chunk_size: Target characters per chunk
        overlap: Character overlap between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text] if text.strip() else []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        if end < len(text):
            # Try splitting at sentence boundaries
            for sep in ['\n\n', '. ', '! ', '? ', '.\n', '!\n', '?\n', '。', '！', '？']:
                last_sep = text[start:end].rfind(sep)
                if last_sep != -1 and last_sep > chunk_size * 0.3:
                    end = start + last_sep + len(sep)
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap if end < len(text) else len(text)
    
    return chunks
