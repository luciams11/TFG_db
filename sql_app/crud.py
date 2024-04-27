from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime as dt

from . import models, schemas

import gzip
import json


#def get_dispositivo(db: Session, dispositivo_id: int):
#    return db.query(models.Dispositivo).filter(models.Dispositivo.id == dispositivo_id).first()

def get_dispositivo(db: Session, hashed_mac: str, fecha_hora: str, latitud: str, longitud: str):
 return db.query(models.Dispositivo).filter(models.Dispositivo.hashed_mac == hashed_mac, models.Dispositivo.fecha_hora == fecha_hora, models.Dispositivo.latitud == latitud, models.Dispositivo.longitud == longitud).first()

def get_dispositivo_by_hashed_mac(db: Session, hashed_mac: str):
    return db.query(models.Dispositivo).filter(models.Dispositivo.hashed_mac == hashed_mac).first()


def get_dispositivos(db: Session, skip: int = 0, limit: int = 100000):
    return db.query(models.Dispositivo).offset(skip).limit(limit).all()

print("En crud.py pero fuera de las funciones")

def create_dispositivo(decoded_data: str, db: Session):
    
    # Convertir los datos en una lista de diccionarios Python
    dispositivos_data = json.loads(decoded_data)
    print("dispositivos_data: ", dispositivos_data)
    
    # Iterar sobre cada dispositivo en la lista de datos
    for dispositivo_mac, dispositivo_data in dispositivos_data.items():

        print("Al inicio del for de dispositivos_data")
        print("dispositivo_mac: ", dispositivo_mac)
        print("dispositivo_data: ", dispositivo_data)
        print("primera_fecha_hora: ", dispositivo_data["primera_fecha_hora"])

        # Comprueba si existe el dispositivo en la base de datos
        db_dispositivo = get_dispositivo_by_hashed_mac(db, dispositivo_mac)
        if db_dispositivo:
            print("ultima_fecha_hora_anterior: ", db_dispositivo.ultima_fecha_hora)
            # Modifica la ultima fecha y hora del dispositivo
            db_dispositivo.ultima_fecha_hora = dt.strptime(dispositivo_data["ultima_fecha_hora"], "%Y-%m-%d %H:%M:%S")
            db.commit()
            print("Dispositivo actualizado")
            print("db_dispositivo.ultima_fecha_hora: ", db_dispositivo.ultima_fecha_hora)
            continue

        primera_fecha_hora_cambio = dt.strptime(dispositivo_data["primera_fecha_hora"], "%Y-%m-%d %H:%M:%S")
        ultima_fecha_hora_cambio = dt.strptime(dispositivo_data["ultima_fecha_hora"], "%Y-%m-%d %H:%M:%S")

        # Crear el dispositivo en la base de datos
        db_dispositivo = models.Dispositivo(
            hashed_mac=dispositivo_mac,
            primera_fecha_hora=primera_fecha_hora_cambio,
            ultima_fecha_hora=ultima_fecha_hora_cambio,
            latitud=dispositivo_data["latitud"],
            longitud=dispositivo_data["longitud"],
        )
        db.add(db_dispositivo)
        print("Dispositivo creado")
        
    db.commit()
    return "Dispositivos creados exitosamente"
