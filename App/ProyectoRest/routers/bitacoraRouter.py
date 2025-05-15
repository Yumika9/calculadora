from fastapi import APIRouter, Request

from dao.bitacoraDao import BitacoraDAO
from model.bitacoraModel import BitacoraInsert, BitacoraSalida
from model.usuariosModel import Salida

router = APIRouter(prefix="/bitacora",tags=["Bitacora"])


@router.post("/", summary="Crear Bitacora", response_model=Salida)
async def agregarBitacora(bitacora:BitacoraInsert,request: Request) -> Salida:
    bitacoraDao = BitacoraDAO(request.app.db)
    return bitacoraDao.agregarBitacora(bitacora)

@router.get("/", response_model=BitacoraSalida, summary="Consulta General")
async def consultaGeneral(request: Request)->BitacoraSalida:
    bitacoraDao= BitacoraDAO(request.app.db)
    return bitacoraDao.consultaGeneral()