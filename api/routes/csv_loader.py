from fastapi import APIRouter, UploadFile, File, Form
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_csvs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/load_csv")
async def load_csv(file: UploadFile = File(...), session_id: str = Form(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, f"{session_id}_{file.filename}")
        
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return {
            "message": f"File {file.filename} loaded successfully.",
            "path": file_path
        }
    except Exception as e:
        return {"error": str(e)}
