from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String, Boolean, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import sqlite3


Database_URL = 'sqlite:///./database.db'
engine = create_engine(Database_URL, connect_args={"check_same_thread": False})
LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base =  declarative_base()

class Mahasiswa(Base):
    __tablename__ = "mahasiswatb"
    rowid = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    umur = Column(Integer)
    fakultas = Column(String)
    ipk = Column(Float)
    di_skors = Column(Boolean)


app = FastAPI()
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/nama")
def get_all_users(db: Session = Depends(get_db)):
    mhss = db.query(Mahasiswa).all()
    return mhss
