
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

    def agregarAuto(self, idUser: str, auto: AutoInsert):
        salida = Salida(estatus="", mensaje="")
        try:
            usuario = self.db.user.find_one({"_id": ObjectId(idUser)})
            if usuario:
                autos = {
                    "usuario": ObjectId(idUser),
                    "marca": auto.marca,
                    "modelo": auto.modelo,
                    "alias": auto.alias,
                    "cilindraje": auto.cilindraje,
                    "capacidadTanque": auto.capacidadTanque,
                    "rendimientoGasolina": auto.rendimientoGasolina,
                    "tipoCombustible": "Gasolina",
                    "estatus": True
                }
                self.db.auto.insert_one(autos)

                salida.estatus = "OK"
                salida.mensaje = "Vehículo agregado con éxito."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El usuario no existe."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al agregar vehículo, consulta al administrador."
        return salida

    def modificarAuto(self,idUser:str, tipo:str,idAuto:str, auto:AutoInsert):
        salida = Salida(estatus="", mensaje="")
        try:
            identi = self.db.auto.find_one({"_id":ObjectId(idAuto)}) #si esta activo el auto.
            if identi:
                # Si no es administrador.
                if tipo != "Administrador" and str(identi["usuario"]) != idUser:
                    salida.estatus = "ERROR"
                    salida.mensaje = "El vehículo no le pertenece."
                    return salida
                autos = {}
                autos["marca"] = identi["marca"] if auto.marca == "string" else auto.marca
                autos["modelo"] = identi["modelo"] if auto.modelo == "string" else auto.modelo
                autos["alias"] = identi["alias"] if auto.alias == "string" else auto.alias
                autos["cilindraje"] = identi["cilindraje"] if auto.cilindraje == 0 else auto.cilindraje
                autos["capacidadTanque"] = identi[
                    "capacidadTanque"] if auto.capacidadTanque == 0 else auto.capacidadTanque
                autos["rendimientoGasolina"] = identi[
                    "rendimientoGasolina"] if auto.rendimientoGasolina == "string" else auto.rendimientoGasolina
                autos["tipoCombustible"] = identi[
                    "tipoCombustible"] if auto.tipoCombustible == "string" else auto.tipoCombustible
                self.db.auto.update_one({"_id": ObjectId(idAuto)},
                                        {"$set": autos})
                salida.estatus = "OK"
                salida.mensaje = "Vehiculo modificado con exito"
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El vehiculo no esta activo/no existe."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al modificar usuario, consulta al administrador."
        return salida

    def eliminarAuto(self,idUser:str,tipo:str,idAuto:str, auto:AutoBaja ):
        salida = Salida(estatus="", mensaje="")
        try:
            #verifica si existe o esta activo.
            vehiculo = self.db.auto.find_one({"_id": ObjectId(idAuto)} ,projection={"estatus": True,"usuario": True})
            if vehiculo:
                if tipo != "Administrador" and str(vehiculo["usuario"]) != idUser:
                    salida.estatus = "ERROR"
                    salida.mensaje = "El vehículo no le pertenece."
                    return salida
                self.db.auto.update_one({"_id": ObjectId(idAuto)},
                                        {"$set": {"estatus": False, "motivoBaja": auto.motivoBaja}})
                salida.estatus = "OK"
                salida.mensaje = "El vehiculo se dio de baja correctamente."
            else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "El vehiculo no existe/no esta activo."
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

    def consultaIndividual(self,idUser:str,tipo:str, idAuto: str):
        salida = AutoSalida(estatus="",mensaje="", autos=[])
        try:
            result = self.db.autoView.find_one({"idAuto": idAuto})
            if result:
                if idUser ==result["usuario"] and tipo=="Usuario":
                    usuarios=self.db.autoView.find_one({"idAuto": idAuto},
                                                       {"idAuto":1,"marca":1,"modelo":1,
                                                        "alias":1,"cilindraje":1,"capacidadTanque":1,
                                                        "rendimientoGasolina":1,"tipoCombustible":1})
                    salida.estatus = "OK"
                    salida.mensaje = "Vehiculo encontrado."
                    salida.autos = usuarios
                else:
                    admin = self.db.autoView.find_one({"idAuto": idAuto})
                    salida.estatus = "OK"
                    salida.mensaje = "Vehiculo encontrado."
                    salida.autos = admin
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El vehiculo no existe/revise el id."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error en la consulta individual."
        return salida
