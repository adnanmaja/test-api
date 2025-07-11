from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy import Column, Integer, String, Boolean, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3


Database_URL = 'sqlite:///./database.db'
engine = create_engine(Database_URL, connect_args={"check_same_thread": False})
LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base =  declarative_base()

conn = sqlite3.connect('database.db')
curs = conn.cursor()

class Mahasiswa(Base):
    __tablename__ = "mahasiswatb"
    rowid = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    umur = Column(Integer)
    fakultas = Column(String)
    ipk = Column(Float)
    di_skors = Column(Boolean)
    
    def to_dict(self):
        return {
            "rowid": self.rowid,
            "nama": self.nama,
            "umur": self.umur,
            "fakultas": self.fakultas,
            "ipk": self.ipk,
            "di_skors": self.di_skors
        }

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/all")
async def get_all_users(db: Session = Depends(get_db)):
    result = db.query(Mahasiswa).all()
    if result:
        return result  
    else: 
        raise HTTPException(status_code=404, detail="Gak ada")

@app.get("/search")
async def get_nama(type: str, term: str, db: Session = Depends(get_db)):
    column_mapping = {
        "Search by Name": "nama",
        "Search by ID": "rowid", 
        "Search by Fakultas": "fakultas"  
    }

    column = column_mapping.get(type)
    if not column:
        raise HTTPException(status_code=400, detail="Invalid search type")
    
    if column == "rowid":
        query = f"SELECT rowid, * FROM mahasiswatb WHERE {column} = ?"
        curs.execute(query, (term,))
    else:
        query = f"SELECT rowid, * FROM mahasiswatb WHERE {column} LIKE ? COLLATE NOCASE"
        curs.execute(query, (f"%{term}%",))
    
    results = curs.fetchall()
    return results

@app.post("/add-mahasiswa")
def add_mahasiswa(db : Session = Depends(get_db),
    nama: str = Form(...),
    umur: int = Form(...),
    fakultas: str = Form(...),
    ipk: float = Form(...),
    di_skors: bool = Form(...)
):
    mhs = Mahasiswa(
        nama=nama,
        umur=umur,
        fakultas=fakultas,
        ipk=ipk,
        di_skors=di_skors
    )
    db.add(mhs)
    db.commit()
    db.refresh(mhs)
    db.close()
    return {
    "message": "Mahasiswa added",
    "mahasiswa": {
        "rowid": mhs.rowid,
        "nama": mhs.nama,
        "umur": mhs.umur,
        "fakultas": mhs.fakultas,
        "ipk": mhs.ipk,
        "di_skors": mhs.di_skors
    }}

@app.delete("/delete-mahasiswa")
def delete(nama: str, db: Session = Depends(get_db)):
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.nama == nama).first()
    if not mahasiswa:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")

    db.delete(mahasiswa)
    db.commit()
    return {"message": f"Mahasiswa '{nama}' deleted"}