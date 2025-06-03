
from datetime import datetime

from model.bitacoraModel import BitacoraInsert, RecargasCombustible
from model.gasolineraModel import GasolineraInsert, GasolineraBaja, GasolineraSalida, Combustibles
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

    def agregarGasolinera(self, gasolinera: GasolineraInsert):
        salida = Salida(estatus="", mensaje="")
        try:
            self.db.gasolineras.insert_one(jsonable_encoder(gasolinera))
            salida.estatus = "OK"
            salida.mensaje = "Gasolinera agregada con exito."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al agregar una nueva gasolinera, consulta al administrador."
        return salida
    def agregarCombustible(self,idGas:str, combustible:Combustibles ):
        salida = Salida(estatus="", mensaje="")
        try:
            estado=self.db.gasolineraView.find_one({"idGasolinera":idGas, "estatus": True})
            if estado:
                self.db.gasolineras.update_one({"_id": ObjectId(idGas)},{"$push":
                                                                             {"combustibles":{
                                                                                 "nombre":combustible.nombre,
                                                                                 "precio":combustible.precio
                                                                             }
                                                                        }})
                salida.estatus = "OK"
                salida.mensaje = "Combustible agregado con exito."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "La gasolinera no existe/ esta inactiva."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al añadir nuevo combustible, consulta al administrador."
        return salida

    def modificarGasolinera(self,idGas:str, gasolinera: GasolineraInsert):
        salida = Salida(estatus="", mensaje="")
        try:
            estado = self.db.gasolineras.find_one({"_id":ObjectId(idGas), "estatus": True})
            if estado:
                gas = {}
                gas["nombre"] = estado["nombre"] if gasolinera.nombre == "string" else gasolinera.nombre
                gas["municipio"] = estado["municipio"] if gasolinera.municipio == "string" else gasolinera.municipio
                gas["estado"] = estado["estado"] if gasolinera.estado == "string" else gasolinera.estado
                gas["direccion"] = estado["direccion"] if gasolinera.direccion == "string" else gasolinera.direccion

                # Filtrar combustibles válidos
                combustiblesV = [
                    c for c in gasolinera.combustibles
                    if c.nombre != "string" and c.precio > 0
                ]
                if combustiblesV:
                    gas["combustibles"] = jsonable_encoder(combustiblesV)
                else:
                    gas["combustibles"] = estado["combustibles"]
                #Se actualiza.
                self.db.gasolineras.update_one( {"_id": ObjectId(idGas)},
                                             {"$set": gas})
                salida.estatus = "OK"
                salida.mensaje = "Gasolinera actualizada con exito"
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El Gasolinera no existe o esta inactivo."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al actualizar gasolinera, consulta al administrador."
        return salida

    def eliminarGasolinera(self,idGas:str, gasolinera:GasolineraBaja ):
        salida = Salida(estatus="", mensaje="")
        try:
            identificador = self.db.gasolineras.find_one({"_id": ObjectId(idGas)})
            if identificador:
                estado = self.db.gasolineras.find_one({"_id": ObjectId(idGas)}, projection={"estatus": True})
                if estado:
                    self.db.gasolineras.update_one({"_id": ObjectId(idGas)},
                                            {"$set": {"estatus": False, "motivoBaja":gasolinera.motivoBaja}})
                    salida.estatus = "OK"
                    salida.mensaje = "La gasolinera se dio de baja correctamente."
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "La gasolinera no esta activa."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "La gasolinera no existe."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al dar de baja la gasolinera, consulta al administrador."
        return salida

    def consultaGeneral(self):
        salida = GasolineraSalida(estatus="",mensaje="",gasolineras=[])
        try:
            listatmp = list(self.db.gasolineraView.find())
            lista = []
            for p in listatmp:
                p['idGasolinera']=str(p['idGasolinera'])
                lista.append(p)
            salida.estatus ="OK"
            salida.mensaje = "Consulta general de Gasolineras."
            salida.gasolineras = lista
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar las gasolineras."
        return salida

    def consultaIndividual(self, idGas: str):
        salida = GasolineraSalida(estatus="",mensaje="",gasolineras=[])
        try:
            result = self.db.gasolineraView.find_one({"idGasolinera": idGas})
            salida.estatus = "OK"
            salida.mensaje = "Gasolinera encontrado."
            salida.gasolineras = result
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error en la consulta individual, la gasolinera no existe."
        return salida