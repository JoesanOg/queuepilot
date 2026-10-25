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
            status_code = status.HTTP_400_BAD_REQUEST,
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


@app.get("/v1/jobs/{job_id}")
async def get_job(job_id):
    
    job = database.get_job(job_id)
    
    if job is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "job not found, please enter a job that exists"
        )
    
    return database.get_job(job_id)