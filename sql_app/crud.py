from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime as dt
from sqlalchemy import func

from . import models, schemas

import json



def get_dispositivo(db: Session, hashed_mac: str, dispositivo: schemas.DispositivoCreate):
 return db.query(models.Dispositivo).filter(models.Dispositivo.hashed_mac == hashed_mac, func.date(models.Dispositivo.primera_fecha_hora) == func.date(dispositivo["primera_fecha_hora"]), models.Dispositivo.latitud == dispositivo["latitud"], models.Dispositivo.longitud == dispositivo["longitud"]).first()

def get_dispositivo_by_hashed_mac(db: Session, hashed_mac: str):
    return db.query(models.Dispositivo).filter(models.Dispositivo.hashed_mac == hashed_mac).first()


def get_dispositivos(db: Session, skip: int = 0, limit: int = 100000):
    return db.query(models.Dispositivo).offset(skip).limit(limit).all()

def create_dispositivo(db: Session, dispositivo_mac, dispositivo: schemas.DispositivoCreate):
    primera_fecha_hora_cambio = dt.strptime(dispositivo["primera_fecha_hora"], "%Y-%m-%d %H:%M:%S")
    ultima_fecha_hora_cambio = dt.strptime(dispositivo["ultima_fecha_hora"], "%Y-%m-%d %H:%M:%S")

    # Crear el dispositivo en la base de datos
    db_dispositivo = models.Dispositivo(
        hashed_mac=dispositivo_mac,
        primera_fecha_hora=primera_fecha_hora_cambio,
        ultima_fecha_hora=ultima_fecha_hora_cambio,
        latitud=dispositivo["latitud"],
        longitud=dispositivo["longitud"],
    )
    db.add(db_dispositivo)
    print("Dispositivo creado")

def analyze_data(decoded_data: str, db: Session):
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
        db_dispositivo = get_dispositivo(db, dispositivo_mac, dispositivo_data)
        if db_dispositivo:

            # obtener solo la fecha y no la hora
            fecha_actual = db_dispositivo.ultima_fecha_hora.date()
            print("fecha_actual: ", fecha_actual)
            fecha_nueva = dt.strptime(dispositivo_data["ultima_fecha_hora"], "%Y-%m-%d %H:%M:%S").date()
            print("fecha_nueva: ", fecha_nueva)

            round_db_latitud = float(round(db_dispositivo.latitud,6))
            round_dispositivo_latitud = float(round(dispositivo_data["latitud"],6))
            tolerance = 1e-10
            if abs(round_db_latitud - round_dispositivo_latitud) > tolerance:
                print("round_db_latitud: ", round_db_latitud)
                print("round_dispositivo_latitud: ", round_dispositivo_latitud)
                print("Latitud diferente")
            else:
                print("Latitud igual")

            round_db_longitud = float(round(db_dispositivo.longitud,6))
            round_dispositivo_longitud = float(round(dispositivo_data["longitud"],6))
            tolerance = 1e-10
            if abs(round_db_longitud - round_dispositivo_longitud) > tolerance:
                # the numbers are different
                print("db_dispositivo.longitud: ", round_db_longitud)
                print("db_dispositivo.longitud type: ", type(round_dispositivo_longitud))
                print("dispositivo_data[longitud]: ", round_dispositivo_longitud)
                print("dispositivo_data[longitud] type: ", type(round_dispositivo_longitud))
                print("Longitud diferente")
            else:
                print("Longitud igual")

            if fecha_actual != fecha_nueva:
                print("fecha_actual: ", fecha_actual)
                print("fecha_nueva: ", fecha_nueva)
                print("Fecha diferente")
            else:
                print("Fecha igual")
            
            # Si la latitud, longitud o la fecha han cambiado, crea un nuevo dispositivo
            if round_db_latitud != round_dispositivo_latitud or round_db_longitud != round_dispositivo_longitud or fecha_actual != fecha_nueva:
                create_dispositivo(db, dispositivo_mac, dispositivo_data)
            else:
                print("ultima_fecha_hora_anterior: ", db_dispositivo.ultima_fecha_hora)
                # Modifica la ultima fecha y hora del dispositivo
                db_dispositivo.ultima_fecha_hora = dt.strptime(dispositivo_data["ultima_fecha_hora"], "%Y-%m-%d %H:%M:%S")
                db.commit()
                print("Dispositivo actualizado")
                print("db_dispositivo.ultima_fecha_hora: ", db_dispositivo.ultima_fecha_hora)
                continue
        else:
            create_dispositivo(db, dispositivo_mac, dispositivo_data)

    db.commit()
    return "Dispositivos creados exitosamente"
