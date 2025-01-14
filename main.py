from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from utils import query

app = FastAPI()

# Add CORS middleware to allow requests from other origins (in this case, localhost:5500)
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
def upload(file: UploadFile = File(...)):
    try:
        file_location = f"tmp/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        return {"message": f"Successfully uploaded {file.filename}", "file_name": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        file.file.close()

@app.post("/caption")
async def caption_image(file_name: str):
    try:
        file_path = f"tmp/{file_name}"
        with open(file_path, "rb") as f:
            data = f.read()
        response = query(data)  # Assuming `query` generates the caption
        os.remove(file_path)  # Delete the file after processing
        return {"caption": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
