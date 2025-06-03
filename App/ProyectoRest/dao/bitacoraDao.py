from datetime import datetime

from dao.autoDao import AutoDAO
from dao.gasolinerasDao import GasolineraDAO
from model.bitacoraModel import BitacoraInsert, RecargasCombustible, BitacoraSalida, BitacoraSalidaAuto
from model.usuariosModel import Salida
from fastapi.encoders import jsonable_encoder
from bson import  ObjectId

class BitacoraDAO:
    def __init__(self, db):
        self.db = db

    def agregarBitacora(self, bitacora: BitacoraInsert):
        salida = Salida(estatus="", mensaje="")
        gasolina = bitacora.recargasCombustibles
        try:
            bitacora.fecha = datetime.today()
            autoDao = AutoDAO(self.db)
            gasDao = GasolineraDAO(self.db)
            auto =autoDao.comprobarAuto(bitacora.auto)
            if auto == True:
                idGas = [d.gasolinera for d in gasolina]
                gasolin =  gasDao.comprobarGas(idGas)
                if gasolin != None:
                    self.db.bitacora.insert_one(jsonable_encoder(bitacora))
                    salida.estatus = "OK"
                    salida.mensaje = "Bitacora agregada con exito."
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "La gasolinera no existe, agregue una antes."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El auto no existe, cree un auto antes."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al agregar pedido, consulta al administrador."
        return salida

    def agregarRecarga(self,idBit,recarga:RecargasCombustible):
        salida = Salida(estatus="", mensaje="")
        try:
            bitacora= self.db.bitacora.find_one({"_id":ObjectId(idBit)})
            if bitacora:
                self.db.bitacora.update_one({"_id":ObjectId(idBit)},
                                            {"$push": {
                                                "recargasCombustible": {
                                                    "gasolinera": ObjectId(recarga.gasolinera),
                                                    "cantidadLitros": recarga.cantidadLitros,
                                                    "tipoCombustible": recarga.tipoCombustible,
                                                    "precioLitro": recarga.precioLitro,
                                                    "subtotal": recarga.subtotal,
                                                    "rendimientoKml": recarga.rendimientoKml
                                                }
                                            }})
                salida.estatus = "OK"
                salida.mensaje = "Se agrego la recarga con exito."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "La bitacora no existe."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al agregar pedido, consulta al administrador."
        return salida

    def consultaGeneral(self):
        salida = BitacoraSalida(estatus="",mensaje="",viajes=[])
        try:
            listatmp = list(self.db.bitacoraView.find())
            lista = []
            for p in listatmp:
                p['idBitacora']=str(p['idBitacora'])
                lista.append(p)
            salida.estatus ="OK"
            salida.mensaje = "Historial de Viajes."
            salida.viajes = lista
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar la bitacora"
        return salida

    def consultaDestino(self, origen: str,destino:str):
        salida = BitacoraSalida(estatus="", mensaje="", viajes=[])
        try:
            print(origen,"-",destino)
            listatmp = list(self.db.bitaRuView.find({"origen": origen,"destino":destino}))
            lista = []
            for p in listatmp:
                lista.append(p)
            salida.estatus = "OK"
            salida.mensaje = f"Viajes encontrados: '{origen}-{destino}'."
            salida.viajes = lista
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "No existe un viaje con esa ruta."
        return salida

    def consultaAuto(self, marca:str,modelo:str, auto: str = None):
        salida = BitacoraSalidaAuto(estatus="", mensaje="", viajes=[])
        try:
            print(marca,modelo)
            filtro = {
                "auto.marca": marca,
                "auto.modelo": modelo
            }
            if auto:
                filtro["auto.idAuto"] = auto
            listatmp = list(self.db.autoBView.find(filtro))
            lista = []
            if listatmp:
                for p in listatmp:
                    lista.append(p)
                salida.estatus = "OK"
                salida.mensaje = "Viajes encontrados."
                salida.viajes = lista
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "No se encontraron viajes con los criterios dados."
        except Exception as e:
            print("Error en consultaAuto:", e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar por auto."
        return salida
