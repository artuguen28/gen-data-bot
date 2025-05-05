from fastapi import APIRouter, Form
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI

router = APIRouter()

UPLOAD_DIR = "uploaded_csvs"

@router.post("/ask_question")
async def ask_question(session_id: str = Form(...), question: str = Form(...)):
    try:
        # Find the uploaded file
        matching_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(session_id + "_")]
        if not matching_files:
            return {"error": "No uploaded CSV found for this session."}

        # Convert CSV to text
        csv_text = os.path.join(UPLOAD_DIR, matching_files[0])
        splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)
        documents = [Document(page_content=chunk) for chunk in splitter.split_text(csv_text)]

        # Embedding and retrieval
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(documents, embeddings)
        retriever = vectorstore.as_retriever()

        # QA chain
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name="gpt-4", temperature=0),
            retriever=retriever
        )

        answer = qa.run(question)
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}
