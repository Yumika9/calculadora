
from datetime import datetime

from model.bitacoraModel import BitacoraInsert, RecargasCombustible
from model.usuariosModel import Salida
from fastapi.encoders import jsonable_encoder
from bson import  ObjectId

class AutoDAO:
    def __init__(self, db):
        self.db = db
    def comprobarAuto(self, idAuto: str):
        respuesta = False
        try:
            auto = self.db.auto.find_one({"_id":ObjectId(idAuto) , "estatus": True})
            if auto:
                respuesta = True
        except:
            respuesta = False
        return respuesta