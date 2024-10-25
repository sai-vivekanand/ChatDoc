# PDF Analysis with Mistral AI
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Mistral AI](https://img.shields.io/badge/Mistral_AI-black?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTV6Ii8+PHBhdGggZD0iTTIgMTdsMTAgNSAxMC01Ii8+PHBhdGggZD0iTTIgMTJsMTAgNSAxMC01Ii8+PC9zdmc+)](https://mistral.ai)

A web application that enables users to upload PDF documents, extract text content, generate summaries, and ask questions about the content using Mistral AI's powerful language model. The application features a FastAPI backend for robust API handling and a user-friendly Streamlit frontend interface.

## Project Tree:

```
.
├── README.md
├── backend
│   └── main.py
├── frontend
│   └── app.py
└── requirements.txt
```

## Architechture Diagram:
![pdf_analysis_with_mistral_ai](https://github.com/user-attachments/assets/9fa5e73d-e06d-4645-a07a-4f2f99d1d787)


## Features

- **PDF Text Extraction**: 
  - Supports PDF files up to 500KB (set a small limit to have quick usage and testing)
  - Preserves page structure and formatting
  - Shows complete extracted text

- **AI-Powered Analysis**:
  - Text summarization using Mistral AI
  - Question & Answer functionality
  - Intelligent chunking for large texts

- **User Interface**:
  - Clean and intuitive design
  - Real-time processing feedback
  - Download options for extracted text
  - Error handling with clear messages

## Technology Stack

- **Backend**:
  - FastAPI (Python web framework)
  - PyPDF2 (PDF processing)
  - Mistral AI API (Language model)

- **Frontend**:
  - Streamlit (UI framework)
  - Python requests (API communication)

## Prerequisites

- Python 3.8 or higher
- Mistral AI API key
- Internet connection for AI features

## Installation

1. **Clone the repository**:
```bash
git clone git@github.com:sai-vivekanand/ChatDoc.git
cd ChatDoc
```

2. **Create a virtual environment**:
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**:

```bash
cd ChatDoc
pip install -r requirements.txt
```

4. **Set up environment variables**:

Create a `.env` file in root directory (ChatDoc):

```env
MISTRAL_API_URL=https://api.mistral.ai/v1/chat/completions
MISTRAL_API_KEY=your_mistral_api_key
MAX_CHUNK_SIZE=4000  # Adjust based on your needs
MAX_FILE_SIZE=209715200  # 200MB in bytes
RATE_LIMIT_DELAY=1
MAX_RETRIES=3
API_URL=http://localhost:8000
```

## Running the Application

1. **Start the backend server**:
```bash
cd backend
uvicorn main:app --reload
```

2. **Start the frontend application** (in a new terminal):
```bash
cd frontend
streamlit run app.py
```

3. **Access the application**:
- Open your web browser
- Navigate to `http://localhost:8501`

## Usage Guide

1. **Upload PDF**:
   - Click the "Upload a PDF" button
   - Select a PDF file (max 500KB)
   - Wait for text extraction

2. **View Extracted Text**:
   - The complete extracted text will be displayed
   - Use the download button to save the text

3. **Generate Summary**:
   - Click "Generate Summary" button
   - Wait for AI processing
   - View the generated summary

4. **Ask Questions**:
   - Enter your question in the text input
   - Click "Get Answer"
   - View the AI-generated response

## API Endpoints

- `POST /upload-pdf`: Upload and process PDF files
  ```python
  files = {"file": ("example.pdf", file_bytes, "application/pdf")}
  response = requests.post(f"{API_URL}/upload-pdf", files=files)
  ```

- `POST /summarize`: Generate text summary
  ```python
  data = {"text_content": "your text here"}
  response = requests.post(f"{API_URL}/summarize", json=data)
  ```

- `POST /ask-question`: Answer questions about the text
  ```python
  data = {"text_content": "your text here", "question": "your question"}
  response = requests.post(f"{API_URL}/ask-question", json=data)
  ```

## Error Handling

The application handles various error scenarios:
- File size exceeding 500KB
- Invalid file types
- API rate limiting
- Text extraction failures
- Network connectivity issues

## Limitations

- Maximum file size: 500KB
- Supported format: PDF only
- Rate limiting: Follows Mistral AI API limits
- Text extraction: May vary based on PDF structure

## Future Improvements

- Support for larger PDF files
- Additional file format support
- Batch processing capabilities
- Enhanced error recovery
- User authentication
- Result caching

## Contributing

1. Clone the repository
2. Create your feature branch (`git checkout -b AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request (`Rebase and merge`)

## Acknowledgments

- [Mistral AI](https://mistral.ai/) for their powerful language model
- [FastAPI](https://fastapi.tiangolo.com/) for the efficient backend framework
- [Streamlit](https://streamlit.io/) for the intuitive frontend framework

## Contact

Your Name - [saivivekred@gmail.com](mailto:saivivekred@gmail.com)

Project Demo Link: [Drive Link](https://drive.google.com/file/d/1oj0LHsYCn7FVxzbxr-2IQErs7-Tzg6nA/view?usp=sharing)

