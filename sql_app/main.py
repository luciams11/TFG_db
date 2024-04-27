import gzip
from typing import Any
from fastapi import Depends, FastAPI, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

import uvicorn
from fastapi.middleware.gzip import GZipMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

print("¡La aplicación FastAPI se ha iniciado correctamente!")

app.add_middleware(GZipMiddleware, minimum_size=1000)




# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/dispositivos/")
async def create_dispositivo(rec: Request, db: Session = Depends(get_db)):
    print("Hola")
    compressed_data = await rec.body()
    print(compressed_data)

    # Descomprimir los datos recibidos
    if not compressed_data:
        raise HTTPException(status_code=400, detail="No data received")
    decompressed_data = gzip.decompress(compressed_data)
    if not decompressed_data:
        raise HTTPException(status_code=400, detail="Data could not be decompressed")
    
    # Decodificar los datos descomprimidos como una cadena UTF-8
    decoded_data = decompressed_data.decode('utf-8')
    print("decoded_data: ", decoded_data)
    return crud.create_dispositivo(decoded_data, db=db)


@app.get("/dispositivos/", response_model=list[schemas.Dispositivo])
def read_dispositivos(skip: int = 0, limit: int = 100000, db: Session = Depends(get_db)):
    dispositivos = crud.get_dispositivos(db, skip=skip, limit=limit)
    return dispositivos

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")