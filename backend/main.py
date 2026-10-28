from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql-service"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "rootpassword"),
        database=os.getenv("DB_NAME", "mydb"),
        port=int(os.getenv("DB_PORT", 3306))
    )

@app.on_event("startup")
def setup_db():
    # Automatically bootstrap a working table structure
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """)
        cursor.execute("SELECT COUNT(*) FROM users;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (name) VALUES ('Kubernetes Worker Machine'), ('Jenkins Automation Engine');")
            conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database bootstrap deferred: {e}")

@app.get("/api/data")
def fetch_from_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"status": "success", "data": rows}
    except Exception as e:
        return {"status": "error", "message": str(e)}

