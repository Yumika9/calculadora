from datetime import datetime

from dao.autoDao import AutoDAO
from dao.gasolinerasDao import GasolineraDAO
from model.bitacoraModel import BitacoraInsert, RecargasCombustible, BitacoraSalida
from model.usuariosModel import Salida
from fastapi.encoders import jsonable_encoder


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

    def consultaDestino(self, destino: str):
        salida = BitacoraSalida(estatus="", mensaje="", viajes=[])
        try:
            # Usamos la vista ya creada en MongoDB
            listatmp = list(self.db.ConsultaPorDestino.find({"destino": {"$regex": f"{destino}", "$options": "i"}}))
            lista = []
            for p in listatmp:
                # Convertir idBitacora a string si viene como ObjectId
                if "_id" in p:
                    print("encontre algo")
                    p["idBitacora"] = str(p["_id"])
                lista.append(p)
            salida.estatus = "OK"
            salida.mensaje = f"{len(lista)} viaje(s) encontrados con destino '{destino}'."
            salida.viajes = lista
        except Exception as e:
            print("Error en consulta_por_destino:", e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar por destino."
        return salida

    def consultaAuto(self, auto: str):
        salida = BitacoraSalida(estatus="", mensaje="", viajes=[])
        try:
            # Filtramos en la vista por la propiedad marca o modelo dentro del array auto
            autos_coincidentes = list(self.db.auto.find({
                "$or": [
                    {"marca": {"$regex": auto, "$options": "i"}},
                    {"modelo": {"$regex": auto, "$options": "i"}},
                    {"alias": {"$regex": auto, "$options": "i"}}
                ]
            }))
            # Obtener los alias de los autos encontrados
            alias_autos = [a["alias"] for a in autos_coincidentes if "alias" in a]

            # Buscar en bitacora los viajes con esos autos
            listatmp = list(self.db.bitacora.find({"auto": {"$in": alias_autos}}))

            lista = []
            for p in listatmp:
                if "_id" in p:
                    p["idBitacora"] = str(p["_id"])
                # Agregar información del auto
                auto_info = next((a for a in autos_coincidentes if a.get("alias") == p["auto"]), None)
                if auto_info:
                    p["auto_info"] = {
                        "marca": auto_info.get("marca", ""),
                        "modelo": auto_info.get("modelo", "")
                    }
                lista.append(p)

            salida.estatus = "OK"
            salida.mensaje = f"{len(lista)} viaje(s) encontrados para auto '{auto}'."
            salida.viajes = lista
        except Exception as e:
            print("Error en consulta_por_auto:", e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar por auto."
        return salida