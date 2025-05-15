
from datetime import datetime

from model.bitacoraModel import BitacoraInsert, RecargasCombustible
from model.usuariosModel import Salida
from fastapi.encoders import jsonable_encoder
from bson import  ObjectId

class GasolineraDAO:
    def __init__(self, db):
        self.db = db
    def comprobarGas(self, idGas: str):
        respuesta = False
        try:
            gas = self.db.gasolineras.find_one({"_id": ObjectId(idGas), "estatus": True})
            if gas:
                respuesta = True
        except:
            respuesta = False
        return respuesta