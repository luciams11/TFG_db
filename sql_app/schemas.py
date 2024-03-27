from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

    

class DispositivoBase(BaseModel):
    hashed_mac: str
    fecha_hora: datetime
    latitud: Decimal
    longitud: Decimal

class DispositivoCreate(DispositivoBase):
    pass

class Dispositivo(DispositivoBase):
    id: int 
    
    class Config:
        orm_mode = True