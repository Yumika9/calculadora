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