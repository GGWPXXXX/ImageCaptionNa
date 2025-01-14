import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from utils import query

app = FastAPI()

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open("uploaded_" + file.filename, "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}


@app.post("/caption")
async def caption_image(file: UploadFile = File(...)):
    try:
        # Use a temporary directory
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            # Write the uploaded file content to the temporary file
            temp_file.write(await file.read())

        # Pass the temporary file path to your query function
        response = query(temp_file_path)

        # Clean up: Delete the temporary file after processing
        os.remove(temp_file_path)

        return {"caption": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
