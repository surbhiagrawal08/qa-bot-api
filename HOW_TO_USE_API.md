# How to Use the QA Bot API

## What is http://localhost:8000/docs?

The `/docs` endpoint is **FastAPI's automatic interactive API documentation** (Swagger UI). It provides:
- A visual interface to see all available endpoints
- Interactive testing - you can test the API directly from your browser
- Request/response schemas
- Try it out functionality

## Getting Question-Answer Results

### Method 1: Using the Interactive Docs (Easiest) ⭐

1. **Start the server** (if not already running):
   ```bash
   ./run.sh
   # Or: uvicorn app.main:app --reload
   ```

2. **Open the docs**: http://localhost:8000/docs

3. **Find the `/qa` endpoint**:
   - Scroll down to see "POST /qa"
   - Click on it to expand

4. **Click "Try it out"** button

5. **Upload your files**:
   - **questions_file**: Click "Choose File" and select your JSON file with questions
   - **document_file**: Click "Choose File" and select your PDF or JSON document

6. **Click "Execute"**

7. **See the results**: The response will show question-answer pairs in JSON format

### Method 2: Using curl Command

```bash
curl -X POST "http://localhost:8000/qa" \
  -F "questions_file=@sample_questions.json" \
  -F "document_file=@soc2-type2.pdf"
```

### Method 3: Using Python Script

See `test_api.py` script below.

### Method 4: Using the Batch Endpoint (for testing)

```bash
curl -X POST "http://localhost:8000/qa/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "questions": ["What is the main topic?", "Who is the author?"],
    "document_text": "Your document text here..."
  }'
```

## Expected Response Format

```json
{
  "results": {
    "Question 1?": "Answer based on document content...",
    "Question 2?": "Answer based on document content...",
    "Question 3?": "Answer based on document content..."
  }
}
```

## File Format Requirements

### Questions File (JSON)
Your questions file should be one of these formats:

**Format 1 - Simple list:**
```json
[
  "Question 1?",
  "Question 2?",
  "Question 3?"
]
```

**Format 2 - List of objects:**
```json
[
  {"question": "Question 1?"},
  {"question": "Question 2?"}
]
```

**Format 3 - Dictionary:**
```json
{
  "questions": ["Question 1?", "Question 2?"]
}
```

### Document File
- **PDF**: Any text-based PDF file
- **JSON**: Any JSON file (will be converted to text)

## Example Workflow

1. **Prepare your files**:
   - Create `my_questions.json` with your questions
   - Have your document ready (PDF or JSON)

2. **Start the server**:
   ```bash
   ./run.sh
   ```

3. **Test the API**:
   - Go to http://localhost:8000/docs
   - Use the interactive interface to upload files
   - Get your results!

4. **Or use curl**:
   ```bash
   curl -X POST "http://localhost:8000/qa" \
     -F "questions_file=@my_questions.json" \
     -F "document_file=@soc2-type2.pdf" \
     -o results.json
   ```

## Troubleshooting

### "422 Unprocessable Entity"
- Check that both files are uploaded
- Verify file formats (questions must be JSON, document must be PDF or JSON)

### "400 Bad Request"
- Questions file is empty or invalid JSON
- Document file is empty or cannot be processed

### "500 Internal Server Error"
- Check that OpenAI API key is set in `.env`
- Verify the document has readable text content
- Check server logs for detailed error messages

## Sample Files

- `sample_questions.json` - Example questions file included in the project
- You can download sample PDF from: https://productfruits.com/docs/soc2-type2.pdf
