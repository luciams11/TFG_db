from sqlalchemy.orm import Session

from . import models, schemas


#def get_dispositivo(db: Session, dispositivo_id: int):
#    return db.query(models.Dispositivo).filter(models.Dispositivo.id == dispositivo_id).first()


def get_dispositivo_by_hashed_mac(db: Session, hashed_mac: str):
    return db.query(models.Dispositivo).filter(models.Dispositivo.hashed_mac == hashed_mac).first()


def get_dispositivos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dispositivo).offset(skip).limit(limit).all()


def create_dispositivo(db: Session, dispositivo: schemas.Dispositivo):
    db_dispositivo = models.Dispositivo(hashed_mac=dispositivo.hashed_mac, fecha_hora=dispositivo.fecha_hora, latitud=dispositivo.latitud, longitud=dispositivo.longitud)
    db.add(db_dispositivo)
    db.commit()
    db.refresh(db_dispositivo)
    return db_dispositivo
