import os, sqlite3,uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel


APP_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(APP_DIR, "uploads")

DB_PATH = os.path.join(APP_DIR, "app.db")

os.makedirs(UPLOAD_DIR, exist_ok=True)

app  = FastAPI(title = "网络知识问答系统", version = "1.0.0")