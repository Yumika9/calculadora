
from datetime import datetime

from model.autoModel import AutoInsert, AutoBaja, AutoSalida
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

    def agregarAuto(self, auto: AutoInsert):
        salida = Salida(estatus="", mensaje="")
        try:
            usuario = self.db.user.find_one({"_id":ObjectId(auto.usuario)})
            if usuario:
               self.db.auto.insert_one(jsonable_encoder(auto))
               salida.estatus = "OK"
               salida.mensaje = "Vehiculo agregado con exito. "
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El usuario no existe. "
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al agregar vehiculo, consulta al administrador."
        return salida

    def modificarAuto(self,idAuto:str, auto:AutoInsert):
        salida = Salida(estatus="", mensaje="")
        try:
            identificador = self.db.auto.find_one({"_id":ObjectId(idAuto)})
            if identificador:
                estado =  self.db.auto.find_one({"_id": ObjectId(idAuto)}, projection={"estatus": True})
                if estado:
                    self.db.auto.update_one( {"_id": ObjectId(idAuto)},
                                             {"$set": {"marca":auto.marca,
                                                       "alias":auto.alias,
                                                       "capacidadTanque":auto.capacidadTanque,
                                                       "cilindraje":auto.cilindraje,
                                                       "modelo":auto.modelo,
                                                       "rendimientoGasolina":auto.rendimientoGasolina,
                                                       "tipoCombustible":auto.tipoCombustible}})
                    salida.estatus = "OK"
                    salida.mensaje = "Vehiculo modificado con exito"
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "El vehiculo no esta activo."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El Vehiculo no existe."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al modificar usuario, consulta al administrador."
        return salida

    def eliminarAuto(self,idAuto:str, auto:AutoBaja ):
        salida = Salida(estatus="", mensaje="")
        try:
            identificador = self.db.auto.find_one({"_id": ObjectId(idAuto)})
            if identificador:
                estado = self.db.auto.find_one({"_id": ObjectId(idAuto)}, projection={"estatus": True})
                if estado:
                    self.db.auto.update_one({"_id": ObjectId(idAuto)},
                                            {"$set": {"estatus": False, "motivoBaja":auto.motivoBaja}})
                    salida.estatus = "OK"
                    salida.mensaje = "El vehiculo se dio de baja correctamente."
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "El vehiculo no esta activo."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El vehiculo no existe."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al dar de baja el vehiculo, consulta al administrador."
        return salida

    def consultaGeneral(self):
        salida = AutoSalida(estatus="",mensaje="",autos=[])
        try:
            listatmp = list(self.db.autoView.find())
            lista = []
            for p in listatmp:
                p['idAuto']=str(p['idAuto'])
                lista.append(p)
            salida.estatus ="OK"
            salida.mensaje = "Consulta general de vehiculos."
            salida.autos = lista
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar los vehiculos"
        return salida

    def consultaIndividual(self, idAuto: str):
        salida = AutoSalida(estatus="",mensaje="", autos=[])
        try:
            result=self.db.autoView.find_one({"idAuto": idAuto})
            salida.estatus = "OK"
            salida.mensaje = "Vehiculo encontrado."
            salida.autos = result
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error en la consulta individual."
        return salida
