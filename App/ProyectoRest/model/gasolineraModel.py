from datetime import datetime

from pydantic import  BaseModel, Field

from model.usuariosModel import Salida

class Combustibles(BaseModel):
    nombre: str
    precio: float

class GasolineraInsert(BaseModel):
    nombre:str
    municipio:str
    estado:str
    direccion:str
    combustibles:list[Combustibles]
    estatus: bool =True

class GasolineraBaja(BaseModel):
    motivoBaja:str

class GasolineraSelect(BaseModel):
    idGasolinera: str
    nombre: str
    municipio: str
    estado: str
    direccion: str
    combustibles: list[Combustibles]
    estatus: bool

class GasolineraSalida(Salida):
    gasolineras: list[GasolineraSelect]

