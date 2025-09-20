from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import pandas as pd
import io
from pathlib import Path

app = FastAPI()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB max
ALLOWED_EXTENSIONS = {".csv", ".xlsx"}

EXPECTED_SCHEMA = {
    "StudentID": "int64",
    "Name": "object",
    "Attendance": "float64",
    "Score": "float64",
    "FeesPaid": "float64"
}

def validate_file_extension(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def validate_schema(df: pd.DataFrame):
    missing_columns = [col for col in EXPECTED_SCHEMA if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    for col, expected_dtype in EXPECTED_SCHEMA.items():
        actual_dtype = str(df[col].dtype)
        if expected_dtype != actual_dtype:
            # Allow int to float relaxation
            if expected_dtype.startswith("float") and actual_dtype.startswith("int"):
                continue
            raise ValueError(f"Column '{col}' is {actual_dtype}, expected {expected_dtype}")

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File {file.filename} exceeds 5MB limit")

        if not validate_file_extension(file.filename):
            raise HTTPException(status_code=400, detail=f"Invalid file extension for {file.filename}")

        try:
            if file.filename.lower().endswith(".csv"):
                df = pd.read_csv(io.BytesIO(content))
            else:
                df = pd.read_excel(io.BytesIO(content))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse {file.filename}: {str(e)}")

        try:
            validate_schema(df)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Schema error in {file.filename}: {str(e)}")

        results.append(f"{file.filename} uploaded and validated successfully")

    return JSONResponse(content={"messages": results})

@app.get("/")
async def health_check():
    return {"message": "File Upload & Validation API running"}
