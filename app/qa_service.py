"""Question-Answering service using LangChain."""
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
try:
    from langchain.schema import Document
except ImportError:
    from langchain_core.documents import Document

from app.config import OPENAI_API_KEY, OPENAI_MODEL


class QAService:
    """Service for answering questions based on document content."""
    
    def __init__(self):
        """Initialize the QA service with embeddings and LLM."""
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            openai_api_key=OPENAI_API_KEY,
            temperature=0
        )
        self.vectorstore = None
        self.qa_chain = None
        
    def load_document(self, document_text: str):
        """
        Load document text and create vector store.
        
        Args:
            document_text: The text content of the document
        """
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        texts = text_splitter.split_text(document_text)
        documents = [Document(page_content=text) for text in texts]
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )
        
        # Create QA chain with custom prompt
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Be concise and accurate in your response.

        Context: {context}

        Question: {question}

        Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=False
        )
    
    def answer_questions(self, questions: List[str]) -> Dict[str, str]:
        """
        Answer a list of questions based on the loaded document.
        
        Args:
            questions: List of questions to answer
            
        Returns:
            Dictionary mapping questions to answers
        """
        if not self.qa_chain:
            raise ValueError("Document must be loaded before answering questions")
        
        results = {}
        for question in questions:
            try:
                response = self.qa_chain.invoke({"query": question})
                answer = response.get("result", "Unable to generate answer")
                results[question] = answer
            except Exception as e:
                results[question] = f"Error processing question: {str(e)}"
        
        return results
    
    def cleanup(self):
        """Clean up resources."""
        if self.vectorstore:
            # ChromaDB will persist automatically, but we can clear if needed
            pass
