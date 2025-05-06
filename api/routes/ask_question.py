import os
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_openai import OpenAIEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from typing import Dict

router = APIRouter()

UPLOAD_DIR = "uploaded_csvs"

# Define the request model
class QuestionRequest(BaseModel):
    session_id: str
    question: str


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/ask_question")
async def ask_question(request: QuestionRequest) -> Dict[str, str]:
    session_id = request.session_id.strip()
    question = request.question.strip()

    logger.info(f"Received session_id: {session_id}")
    logger.info(f"Received question: {question}")

    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID cannot be empty.")
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        # Find the uploaded file
        matching_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(session_id + "_")]
        logger.info(f"Matching files: {matching_files}")

        if not matching_files:
            raise HTTPException(status_code=404, detail="No uploaded CSV found for this session.")

        # Get the absolute path of the file
        file_path = os.path.abspath(os.path.join(UPLOAD_DIR, matching_files[0]))
        logger.info(f"File path: {file_path}")

        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="Uploaded file not found.")

        # Convert CSV to text
        with open(file_path, "r", encoding="utf-8") as file:
            csv_text = file.read()
        logger.info(f"CSV content: {csv_text[:100]}...")  # Log the first 100 characters

        splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)
        documents = [Document(page_content=chunk) for chunk in splitter.split_text(csv_text)]
        logger.info(f"Number of documents created: {len(documents)}")

        # Embedding and retrieval
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(documents, embeddings)
        retriever = vectorstore.as_retriever()

        # QA chain
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0),
            retriever=retriever
        )

        answer = qa.run(question)
        logger.info(f"Answer: {answer}")
        return {"answer": answer}

    except HTTPException as http_exc:
        logger.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")