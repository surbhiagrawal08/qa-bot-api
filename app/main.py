"""FastAPI application for Question-Answering bot."""
import os
import tempfile
from typing import Dict, List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.document_loader import load_pdf, load_json, load_questions
from app.qa_service import QAService

app = FastAPI(
    title="Zania QA Bot API",
    description="Question-Answering bot API using LangChain and OpenAI",
    version="1.0.0"
)

# Global QA service instance
qa_service = QAService()


class QuestionAnswerResponse(BaseModel):
    """Response model for question-answer pairs."""
    results: Dict[str, str]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Zania QA Bot API",
        "version": "1.0.0",
        "endpoints": {
            "POST /qa": "Process questions and documents",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/qa", response_model=QuestionAnswerResponse)
async def process_qa(
    questions_file: UploadFile = File(..., description="JSON file containing questions"),
    document_file: UploadFile = File(..., description="PDF or JSON file containing the document")
):
    """
    Process questions and document to generate answers.
    
    Args:
        questions_file: JSON file containing a list of questions
        document_file: PDF or JSON file containing the document content
        
    Returns:
        JSON response with question-answer pairs
    """
    # Validate file types
    if not questions_file.filename.endswith('.json'):
        raise HTTPException(
            status_code=400,
            detail="Questions file must be a JSON file"
        )
    
    doc_ext = os.path.splitext(document_file.filename)[1].lower()
    if doc_ext not in ['.pdf', '.json']:
        raise HTTPException(
            status_code=400,
            detail="Document file must be a PDF or JSON file"
        )
    
    # Save uploaded files temporarily
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save questions file
        questions_path = os.path.join(temp_dir, "questions.json")
        with open(questions_path, "wb") as f:
            content = await questions_file.read()
            f.write(content)
        
        # Save document file
        doc_path = os.path.join(temp_dir, f"document{doc_ext}")
        with open(doc_path, "wb") as f:
            content = await document_file.read()
            f.write(content)
        
        try:
            # Load questions
            questions = load_questions(questions_path)
            
            if not questions:
                raise HTTPException(
                    status_code=400,
                    detail="No questions found in the questions file"
                )
            
            # Load document
            if doc_ext == '.pdf':
                document_text = load_pdf(doc_path)
            else:
                document_text = load_json(doc_path)
            
            if not document_text or not document_text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Document file is empty or could not be processed"
                )
            
            # Process with QA service
            qa_service.load_document(document_text)
            results = qa_service.answer_questions(questions)
            
            return QuestionAnswerResponse(results=results)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing files: {str(e)}"
            )


@app.post("/qa/batch")
async def process_qa_batch(
    questions: List[str],
    document_text: str
):
    """
    Process questions with document text directly (for testing).
    
    Args:
        questions: List of questions
        document_text: Document text content
        
    Returns:
        JSON response with question-answer pairs
    """
    try:
        qa_service.load_document(document_text)
        results = qa_service.answer_questions(questions)
        return QuestionAnswerResponse(results=results)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
