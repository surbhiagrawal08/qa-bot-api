# Zania QA Bot API

A production-ready Question-Answering bot API built with FastAPI and LangChain that answers questions based on document content. The API supports both PDF and JSON documents and uses OpenAI's GPT-4o-mini model for generating answers.

## Features

- **Multi-format Support**: Process PDF and JSON documents
- **Question Processing**: Accept questions in JSON format
- **AI-Powered**: Uses OpenAI's GPT-4o-mini model via LangChain
- **Vector Search**: Leverages ChromaDB for efficient document retrieval
- **FastAPI**: Modern, fast, and production-ready API framework
- **Tested**: Includes comprehensive test suite

## Technology Stack

- **Python 3.x**
- **FastAPI** - Web framework
- **LangChain** - LLM framework
- **OpenAI** (gpt-4o-mini) - Language model
- **ChromaDB** - Vector database
- **PyPDF** - PDF processing

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Zania
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   if # Fix for pip install Issues (or all requirements.txt arent fully downloaded)

      ## Problem
      `pip install -r requirements.txt` doesn't install all packages due to:
      - Version conflicts between packages
      - Missing dependencies
      - Installation order issues
      - Compatibility problems

      ## Solutions

      ### Solution 1: Use Fixed Installation Script (Recommended)
      ```bash
      ./install_fixed.sh

      Try installing again:
      ```bash
      pip install --upgrade pip setuptools wheel
      pip install -r requirements.txt

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```bash
   ./setup_env.sh #In this edit your_key in the key placeholder
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   **⚠️ Important**: Never commit `.env` file or API keys to Git!

## Usage

### Starting the Server

3. **Run the server**:
   ```
   ./run.sh

5. **In another terminal**:
```bash
curl -X POST "http://localhost:8000/qa" \
  -F "questions_file=@sample_questions.json" \
  -F "document_file=@soc2-type2.pdf" \
  -o results.json
```
Added Information
The API will be available at `http://localhost:8000`

### API Documentation 

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### 1. Health Check
```bash
GET /health
```

#### 2. Process Questions and Document
```bash
POST /qa
```

**Request:**
- `questions_file` (file): JSON file containing a list of questions
- `document_file` (file): PDF or JSON file containing the document


**Response:**
```json
{
  "results": {
    "Question 1?": "Answer 1",
    "Question 2?": "Answer 2"
  }
}
```

#### 3. Batch Processing (for testing)
```bash
POST /qa/batch
```

**Request Body:**
```json
{
  "questions": ["Question 1?", "Question 2?"],
  "document_text": "Your document text here..."
}
```

### Question File Format

The questions file should be a JSON file with one of these formats:

**Format 1 - Simple list:**
```json
["Question 1?", "Question 2?", "Question 3?"]
```

**Format 2 - List of objects:**
```json
[
  {"question": "Question 1?"},
  {"question": "Question 2?"}
]
```

**Format 3 - Dictionary with questions key:**
```json
{
  "questions": ["Question 1?", "Question 2?"]
}
```

### Document File Format

- **PDF**: Standard PDF files (text-based PDFs work best)
- **JSON**: Any JSON structure will be converted to readable text

## Project Structure

```
Zania/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── document_loader.py   # PDF and JSON loaders
│   └── qa_service.py        # LangChain QA service
├── tests/
│   ├── __init__.py
│   ├── test_document_loader.py
│   └── test_api.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Running Tests

```bash
pytest tests/
```

For verbose output:
```bash
pytest tests/ -v
```

## Development

### Code Quality

The project follows best practices for production code:
- Type hints
- Docstrings
- Error handling
- Environment variable management
- Comprehensive tests


## Limitations

- The API key has a $5 limit - use judiciously
- Only GPT-4o-mini model is used (as per requirements)
- ChromaDB data is persisted locally in `./chroma_db/`


## License

This project is created for the Zania coding challenge.
