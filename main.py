from fastapi import FastAPI

app = FastAPI()

murids = {
    1: {
        "nama": "Rapla",
        "umur": "18",
        "fakultas": "ipa"
    }
}

@app.get("/")
def index():
    return{"nama": "first data"}

@app.get("/get-murid/{murid_id}")
def get_id(murid_id: int):
    return murids[murid_id]

@app.get("/murid-nama")
def get_nama(nama: str):
    for murid_id in murids:
        if murids[murid_id]["nama"] == nama:
            return murids[murid_id]
        else:
            return {"Gak ada"}