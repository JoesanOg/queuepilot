import sqlite3
from pathlib import Path

#ensure db location
db_path = Path(__file__).resolve().parent.parent/"queuepilot.db"

#db initialization function
def init_db():

    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            job_type TEXT NOT NULL,
            input_path TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
            CHECK (status IN (
                'pending',
                'running',
                'completed',
                'failed',
                'retry_pending'
                )),
                result TEXT,
                error_message TEXT
                )""")

    finally:
        con.commit()
        con.close()
        
        

#create jobs function
def create_job(job_id, job_type, input_path):
    
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("""INSERT INTO jobs (id, job_type, input_path)
                    VALUES (?, ?, ?)""", (job_id, job_type, input_path))
        
        con.commit()
    except sqlite3.Error:
        con.rollback()
        raise
    
    finally:
        con.close()