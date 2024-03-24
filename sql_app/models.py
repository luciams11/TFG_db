from sqlalchemy import Column, DateTime, DECIMAL, Integer, String

from .database import Base

class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hashed_mac = Column(String, index=True)
    fecha_hora = Column(DateTime)
    latitud = Column(DECIMAL)
    longitud = Column(DECIMAL)
    marca = Column(String)

