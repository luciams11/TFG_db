from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
    

class DispositivoBase(BaseModel):
    hashed_mac: str
    primera_fecha_hora: datetime
    ultima_fecha_hora: datetime
    latitud: Decimal
    longitud: Decimal

class DispositivoCreate(DispositivoBase):
    pass

class Dispositivo(DispositivoBase):
    id: int 
    
    class Config:
        orm_mode = True