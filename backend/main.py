from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os

app = FastAPI()

# Allow your Frontend VM/Browser IP to make API calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify your exact Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    # These match the environment variables we will set in Kubernetes
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql-service"), 
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "rootpassword"),
        database=os.getenv("DB_NAME", "mydb"),
        port=int(os.getenv("DB_PORT", 3306))
    )

@app.get("/")
def read_root():
    return {"status": "FastAPI backend is running"}

@app.get("/db-check")
def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        return {"status": "Connected to MySQL successfully!", "mysql_version": version[0]}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

