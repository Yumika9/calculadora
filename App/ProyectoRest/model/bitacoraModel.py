from datetime import datetime

from pydantic import  BaseModel, Field

from model.usuariosModel import Salida


class RecargasCombustible(BaseModel):
    gasolinera: str
    cantidadLitros:int
    tipoCombustible:str
    precioLitro:int
    subtotal:int
    rendimientoKml:int

class BitacoraInsert(BaseModel):
    origen: str
    destino: str
    auto: str
    litrosGas: int
    costo: int
    kilometrosRecorridos: int
    recargasCombustibles:list[RecargasCombustible]
    fecha: datetime | None= datetime.today()
    rendimientoLitro: str

class BitacoraSelect(BaseModel):
    idBitacora:str
    origen: str
    destino: str
    auto: str
    litrosGas: int
    costo: int
    kilometrosRecorridos: int
    recargasCombustible:list[RecargasCombustible]
    fecha: datetime | None= datetime.today()
    rendimientoLitro: str

class BitacoraSalida(Salida):
    viajes:list[BitacoraSelect]

#Modelo para Consulta por Auto
class Auto(BaseModel):
    idAuto:str
    marca:str
    modelo:str
    capacidadTanque: int
    cilindraje: int
    rendimientoGasolina: str
    tipoCombustible: str

class BitacoraAuto(BaseModel):
    idBitacora: str
    origen: str
    destino: str
    litrosGas: int
    costo: int
    kilometrosRecorridos: int
    fecha: datetime | None = datetime.today()
    rendimientoLitro: str
    auto: Auto

class BitacoraSalidaAuto(Salida):
    viajes:list[BitacoraAuto]