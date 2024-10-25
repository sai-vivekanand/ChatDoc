from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
import PyPDF2
import io
from typing import List
import time
import textwrap

# Load environment variables
load_dotenv()

MISTRAL_API_URL = os.getenv("MISTRAL_API_URL")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MAX_FILE_SIZE = 500 * 1024  # 500KB
MAX_CHUNK_SIZE = 4000  # Maximum characters per chunk for API calls

app = FastAPI()

class SummarizeRequest(BaseModel):
    text_content: str

class QuestionRequest(BaseModel):
    text_content: str
    question: str

def chunk_text(text: str) -> List[str]:
    """Split text into smaller chunks for API processing."""
    return textwrap.wrap(
        text,
        MAX_CHUNK_SIZE,
        break_long_words=False,
        break_on_hyphens=False
    )

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF using PyPDF2."""
    try:
        with io.BytesIO(file_bytes) as file_stream:
            reader = PyPDF2.PdfReader(file_stream)
            text = ""
            for page_num, page in enumerate(reader.pages):
                text += f"\n--- Page {page_num + 1} ---\n"
                page_text = page.extract_text() or ""
                text += page_text
            return text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error extracting text from PDF: {str(e)}"
        )

def call_mistral_api(messages: List[dict], max_retries: int = 3) -> str:
    """Call Mistral API with retries and rate limiting."""
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mistral-tiny",
        "messages": messages,
        "max_tokens": 1000
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(MISTRAL_API_URL, json=data, headers=headers)
            
            if response.status_code == 429:  # Rate limit exceeded
                wait_time = (attempt + 1) * 2  # Exponential backoff
                time.sleep(wait_time)
                continue
                
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise HTTPException(
                    status_code=500,
                    detail=f"Mistral AI API error: {str(e)}"
                )
            time.sleep(2)  # Wait before retry
    
    raise HTTPException(status_code=500, detail="Maximum retries exceeded")

def process_text_with_chunks(text: str, process_type: str, question: str = None) -> str:
    """Process text in chunks with rate limiting."""
    chunks = chunk_text(text)
    results = []
    
    for i, chunk in enumerate(chunks):
        # Add delay between chunks to respect rate limits
        if i > 0:
            time.sleep(2)
        
        if process_type == "summarize":
            messages = [
                {"role": "system", "content": "You are a helpful assistant that summarizes text clearly and concisely."},
                {"role": "user", "content": f"Please summarize part {i+1} of {len(chunks)} of the following text:\n\n{chunk}"}
            ]
        else:  # question
            messages = [
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided text."},
                {"role": "user", "content": f"Using part {i+1} of {len(chunks)} of the following text as context:\n\n{chunk}\n\nPlease answer this question: {question}"}
            ]
        
        chunk_result = call_mistral_api(messages)
        results.append(chunk_result)
    
    # Combine chunk results
    if len(chunks) > 1:
        if process_type == "summarize":
            combine_prompt = f"Please combine these summaries into one coherent summary:\n\n{' '.join(results)}"
        else:
            combine_prompt = f"Please combine these answers into one coherent answer for the question '{question}':\n\n{' '.join(results)}"
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that combines multiple text segments coherently."},
            {"role": "user", "content": combine_prompt}
        ]
        
        time.sleep(2)  # Rate limiting before final combination
        return call_mistral_api(messages)
    
    return results[0]

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Handle PDF upload and text extraction."""
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    # Check file size
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    
    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size ({size / 1024:.1f}KB) exceeds maximum limit of {MAX_FILE_SIZE / 1024:.1f}KB"
        )
    
    try:
        contents = await file.read()
        text = extract_text_from_pdf(contents)
        
        if not text:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF"
            )
        
        return {
            "extracted_text": text,
            "char_count": len(text)
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    """Generate summary of the text using chunking."""
    try:
        summary = process_text_with_chunks(request.text_content, "summarize")
        return {"summary": summary.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask-question")
async def ask_question(request: QuestionRequest):
    """Answer questions about the text using chunking."""
    try:
        answer = process_text_with_chunks(request.text_content, "question", request.question)
        return {"answer": answer.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}