from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel
from typing import List, Annotated
from fastapi.middleware.cors import CORSMiddleware
from routes import chats
from sqlalchemy.orm import Session,sessionmaker
from routes import check_database, auth, report # Import the user router
import psycopg2,os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from database.models import Base
from database.conn import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Updated to allow all origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chats.router, prefix="/api/conversation", tags=["chats"])
app.include_router(check_database.router, prefix="/api/data", tags=["database"])
app.include_router(auth.router, prefix="/api/user", tags=["auth"])
app.include_router(report.router, prefix="/api/report", tags=["report"])

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable (Railway sets this), default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # host must be "0.0.0.0" for cloud deployments
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)