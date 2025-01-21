import os 
from fastapi import FastAPI, File, Request, UploadFile, HTTPException 
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates 
from utils import query  

app = FastAPI() 
app.mount("/static", StaticFiles(directory="static"), name="static")
# Create temp directory if it doesn't exist
os.makedirs("temp", exist_ok=True)
templates = Jinja2Templates(directory="templates")




# Add root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/caption/") 
async def caption_image(file: UploadFile = File(...)): 
    try: 
        # Save the uploaded file temporarily 
        file_path = f"temp/{file.filename}" 
        content = await file.read()
        with open(file_path, "wb") as f: 
            f.write(content) 
 
        # Generate caption
        caption = query(file_path) 
        print(caption[0]["generated_text"]) 
        
        # Clean up
        os.remove(file_path)
        
        return {"caption": caption[0]["generated_text"]}
 
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"Error during captioning: {str(e)}")