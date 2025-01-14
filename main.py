import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils import query  # Assuming query is the function to generate captions

app = FastAPI()

origins = [
    "http://localhost:5500",  # your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return {"message": f"Successfully uploaded {file.filename}", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.post("/caption")
async def caption_image(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Assuming query function processes image bytes and returns a caption
        caption = query(file_path)
        os.remove(file_path)  # Clean up by removing the temporary file
        return {"caption": caption[0]["generated_text"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during captioning: {str(e)}")
