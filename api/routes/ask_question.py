from fastapi import APIRouter, Form, HTTPException
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from typing import Dict

router = APIRouter()

UPLOAD_DIR = "uploaded_csvs"

@router.post("/ask_question")
async def ask_question(session_id: str = Form(...), question: str = Form(...)) -> Dict[str, str]:

    if not session_id.strip():
        raise HTTPException(status_code=400, detail="Session ID cannot be empty.")
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    try:
        # Find the uploaded file
        matching_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(session_id + "_")]
        if not matching_files:
            return {"error": "No uploaded CSV found for this session."}
        
        # Get the absolute path of the file
        file_path = os.path.abspath(os.path.join(UPLOAD_DIR, matching_files[0]))
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="Uploaded file not found.")
        
        # Convert CSV to text
        with open(file_path, "r", encoding="utf-8") as file:
            csv_text = file.read()

        splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)
        documents = [Document(page_content=chunk) for chunk in splitter.split_text(csv_text)]

        # Embedding and retrieval
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(documents, embeddings)
        retriever = vectorstore.as_retriever()

        # QA chain
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name="gpt-4o-min", temperature=0),
            retriever=retriever
        )

        answer = qa.run(question)
        return {"answer": answer}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
