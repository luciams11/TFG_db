from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/dispositivos/", response_model=schemas.DispositivoCreate)
def create_dispositivo(dispositivo: schemas.DispositivoCreate, db: Session = Depends(get_db)):
    db_dispositivo = crud.get_dispositivo(db, hashed_mac=dispositivo.hashed_mac, fecha_hora=dispositivo.fecha_hora, latitud=dispositivo.latitud, longitud=dispositivo.longitud)
    if db_dispositivo:
        raise HTTPException(status_code=400, detail="Hashed mac already registered")
    return crud.create_dispositivo(db=db, dispositivo=dispositivo)


@app.get("/dispositivos/", response_model=list[schemas.Dispositivo])
def read_dispositivos(skip: int = 0, limit: int = 100000, db: Session = Depends(get_db)):
    dispositivos = crud.get_dispositivos(db, skip=skip, limit=limit)
    return dispositivos

