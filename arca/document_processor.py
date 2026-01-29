# document_processor.py
"""
ARCA System: Document Preprocessing Module

Handles PDF and TXT file processing:
1. Extract text from PDF or TXT files
2. Clean text (remove artifacts, fix formatting)
3. Summarize long documents using LLM
4. Prepare text for ARCA pipeline

Dependencies: pdfplumber, dotenv, langchain_google_genai
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, Optional
import pdfplumber
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

load_dotenv()

# LLM Configuration
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,  # Slightly creative for summarization
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


class DocumentProcessor:
    """
    Process regulation documents (PDF, TXT) for ARCA analysis
    """
    
    def __init__(self):
        """Initialize the document processor"""
        self.llm = llm
        self.max_words = 2000  # API limit
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text from a PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If PDF extraction fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        try:
            text_content = []
            
            with pdfplumber.open(file_path) as pdf:
                print(f"📄 Extracting text from PDF ({len(pdf.pages)} pages)...")
                
                for i, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                    
                    if i % 10 == 0:
                        print(f"   Processed {i}/{len(pdf.pages)} pages...")
            
            full_text = "\n\n".join(text_content)
            
            if not full_text.strip():
                raise ValueError("No text could be extracted from PDF (possibly scanned image)")
            
            print(f"✅ Extracted {len(full_text)} characters from PDF")
            return full_text
            
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {e}")
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """
        Extract text from a TXT file
        
        Args:
            file_path: Path to TXT file
            
        Returns:
            File content as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"TXT file not found: {file_path}")
        
        try:
            # Try UTF-8 first, then fallback to other encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        text = f.read()
                    print(f"✅ Read TXT file ({len(text)} characters, encoding: {encoding})")
                    return text
                except UnicodeDecodeError:
                    continue
            
            raise ValueError("Could not decode file with any supported encoding")
            
        except Exception as e:
            raise ValueError(f"Failed to read TXT file: {e}")
    
    def clean_text(self, raw_text: str) -> str:
        """
        Clean extracted text by removing artifacts and normalizing formatting
        
        Args:
            raw_text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        text = raw_text
        
        # Remove page numbers (common patterns)
        text = re.sub(r'\n\s*Page\s+\d+\s*\n', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        # Remove excessive whitespace
        text = re.sub(r' +', ' ', text)  # Multiple spaces to single
        text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple newlines to double
        
        # Remove common OCR artifacts
        text = re.sub(r'[▪•●○■□]', '', text)  # Bullet points
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Remove header/footer patterns (common in legal docs)
        text = re.sub(r'\n\s*-\s*\d+\s*-\s*\n', '\n', text)
        
        # Trim whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        # Final cleanup
        text = text.strip()
        
        print(f"🧹 Text cleaned ({len(text)} characters)")
        return text
    
    def summarize_and_extract_requirements(self, text: str, max_words: int = 2000) -> str:
        """
        Summarize long regulation text and extract key requirements using LLM
        
        Args:
            text: Full regulation text
            max_words: Maximum words in summary (default: 2000)
            
        Returns:
            Summarized text with key requirements
        """
        word_count = len(text.split())
        
        # If already under limit, return cleaned text
        if word_count <= max_words:
            print(f"✅ Text already within limit ({word_count} words)")
            return text
        
        print(f"📝 Summarizing text ({word_count} words → target: {max_words} words)...")
        
        prompt = f"""You are a legal document analyst. Summarize this regulation document and extract ONLY the key regulatory requirements.

Your summary must:
1. Focus on obligations, prohibitions, and compliance requirements
2. Include specific deadlines, timeframes, and numeric requirements
3. Preserve exact quotes for critical requirements
4. Omit preambles, background, definitions, and administrative procedures
5. Be under {max_words} words
6. Maintain the legal tone and precision

REGULATION TEXT:
{text}

SUMMARIZED REQUIREMENTS (under {max_words} words):"""

        try:
            summary = self.llm.invoke(prompt)
            summary_word_count = len(summary.split())
            
            print(f"✅ Summarized to {summary_word_count} words")
            return summary.strip()
            
        except Exception as e:
            print(f"⚠️  Summarization failed: {e}")
            print(f"   Falling back to truncation method...")
            
            # Fallback: Simple truncation
            words = text.split()
            truncated = ' '.join(words[:max_words])
            return truncated
    
    def process_document(
        self, 
        file_path: str,
        summarize: bool = True,
        max_words: int = 2000
    ) -> Dict[str, Any]:
        """
        Complete document processing pipeline
        
        Args:
            file_path: Path to PDF or TXT file
            summarize: Whether to summarize if text exceeds max_words
            max_words: Maximum words to pass to ARCA pipeline
            
        Returns:
            Dict with:
                - original_file: Original filename
                - file_type: 'pdf' or 'txt'
                - raw_text: Extracted text
                - cleaned_text: Cleaned text
                - processed_text: Final text for ARCA (cleaned + optionally summarized)
                - word_count: Final word count
                - was_summarized: Boolean indicating if summarization occurred
        """
        print("=" * 60)
        print("📂 DOCUMENT PROCESSOR: Starting")
        print("=" * 60)
        print(f"File: {file_path}")
        
        # Determine file type
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            file_type = 'pdf'
            raw_text = self.extract_text_from_pdf(file_path)
        elif file_ext in ['.txt', '.md']:
            file_type = 'txt'
            raw_text = self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}. Use .pdf or .txt")
        
        # Clean text
        cleaned_text = self.clean_text(raw_text)
        
        # Summarize if needed
        was_summarized = False
        processed_text = cleaned_text
        
        if summarize:
            word_count = len(cleaned_text.split())
            if word_count > max_words:
                processed_text = self.summarize_and_extract_requirements(
                    cleaned_text, 
                    max_words=max_words
                )
                was_summarized = True
        
        final_word_count = len(processed_text.split())
        
        result = {
            "original_file": os.path.basename(file_path),
            "file_type": file_type,
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "processed_text": processed_text,
            "word_count": final_word_count,
            "was_summarized": was_summarized
        }
        
        print("\n" + "=" * 60)
        print("✅ DOCUMENT PROCESSING COMPLETE")
        print("=" * 60)
        print(f"Original words: {len(raw_text.split())}")
        print(f"After cleaning: {len(cleaned_text.split())}")
        print(f"Final output: {final_word_count} words")
        print(f"Summarized: {'Yes' if was_summarized else 'No'}")
        print("=" * 60 + "\n")
        
        return result


# ─────────────────────────────────────────────────────────
# CONVENIENCE FUNCTIONS
# ─────────────────────────────────────────────────────────

def process_pdf(file_path: str, summarize: bool = True) -> Dict[str, Any]:
    """
    Quick function to process a PDF file
    
    Usage:
        result = process_pdf("regulation.pdf")
        regulation_text = result["processed_text"]
    """
    processor = DocumentProcessor()
    return processor.process_document(file_path, summarize=summarize)


def process_txt(file_path: str, summarize: bool = True) -> Dict[str, Any]:
    """
    Quick function to process a TXT file
    
    Usage:
        result = process_txt("regulation.txt")
        regulation_text = result["processed_text"]
    """
    processor = DocumentProcessor()
    return processor.process_document(file_path, summarize=summarize)


# ─────────────────────────────────────────────────────────
# TESTING
# ─────────────────────────────────────────────────────────

def test_processor():
    """Test the document processor with sample files"""
    print("\n" + "🧪 TESTING DOCUMENT PROCESSOR" + "\n")
    
    # Test with PDF if available
    pdf_path = "agents/new_regulation.pdf"
    if os.path.exists(pdf_path):
        print(f"\nTest 1: Processing PDF file...")
        result = process_pdf(pdf_path)
        print(f"Success! Processed {result['word_count']} words")
    else:
        print(f"⚠️  No test PDF found at {pdf_path}")
    
    # Test with sample text
    print(f"\nTest 2: Processing sample text...")
    
    # Create a sample text file
    sample_text = """
    Article 1: Data Protection Requirements
    
    All companies must delete customer personal data within 30 days of 
    receiving a deletion request. Automated deletion systems are mandatory.
    
    Page 1
    
    Article 2: Compliance Deadline
    
    This regulation takes effect on June 1, 2025. Companies have 6 months
    to implement compliant systems.
    
    Page 2
    """
    
    temp_file = "temp_test.txt"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(sample_text)
    
    result = process_txt(temp_file)
    
    print(f"\nCleaned text preview:")
    print("-" * 60)
    print(result['processed_text'][:500])
    print("-" * 60)
    
    # Cleanup
    os.remove(temp_file)
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    test_processor()
