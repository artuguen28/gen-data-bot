from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_csvs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/load_csv")
async def load_csv(file: UploadFile = File(...), session_id: str = Form(...)):
    try:
        # Validate session_id
        if not session_id.strip():
            raise HTTPException(status_code=400, detail="Session ID cannot be empty.")

        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

        # Construct the file path
        file_path = os.path.join(UPLOAD_DIR, f"{session_id}_{file.filename}")

        # Save the file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return {
            "message": f"File {file.filename} loaded successfully.",
            "path": file_path
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")