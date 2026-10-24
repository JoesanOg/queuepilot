from fastapi import FastAPI, File, UploadFile, HTTPException, status
from app import database
import uuid
from pathlib import Path

app = FastAPI()

@app.get("/health")
async def get_health():
    return {"status": "healthy"}

@app.post("/v1/jobs")
async def upload_job(file: UploadFile = File(...)):
    
    #Validate file extension input
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code = status.HTTp_400_BAD_REQUEST,
            detail = "Invalid file type. Only CSV files are allowed" 
        )
        
    #Generate job id
    job_id = str(uuid.uuid4())
        
    #dir for job uploads
    upload_dir = Path(__file__).resolve().parent.parent/"uploads/"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    #filename
    file_path = upload_dir / f"{job_id}.csv"
    
    #save uploaded file
    contents = await file.read()  
    file_path.write_bytes(contents)
    await file.close()
    

    database.create_job(job_id, "csv_summary", str(file_path))
    
    return {"job_id" : job_id, "status": "pending"}