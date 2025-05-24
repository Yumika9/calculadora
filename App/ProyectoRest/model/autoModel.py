from datetime import datetime

from pydantic import  BaseModel

from model.usuariosModel import Salida


class AutoInsert(BaseModel):
    usuario:str
    marca:str
    modelo:str
    alias:str
    cilindraje:int
    capacidadTanque:int
    rendimientoGasolina:str
    tipoCombustible:str
    estatus:bool | None= True

class AutoBaja(BaseModel):
    motivoBaja:str

class AutoSelect(BaseModel):
    idAuto:str
    usuario: str
    marca: str
    modelo: str
    alias: str
    cilindraje: int
    capacidadTanque: int
    rendimientoGasolina: str
    tipoCombustible: str
    estatus: bool | None = True

class AutoSalida(Salida):
    autos: list[AutoSelect]