from fastapi import APIRouter, Request

from dao.bitacoraDao import BitacoraDAO
from model.bitacoraModel import BitacoraInsert, BitacoraSalida, BitacoraSalidaAuto
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

@router.get("/consultaAuto", response_model=BitacoraSalidaAuto, summary="Consulta por Auto")
async def consultaAuto(request: Request, idAuto: str = None, marca: str = None, modelo: str = None) -> BitacoraSalidaAuto:
    bitacoraDao = BitacoraDAO(request.app.db)
    return bitacoraDao.consultaAuto(idAuto, marca, modelo)

@router.get("/bitacora/{destino}", response_model=BitacoraSalida, summary="Consulta por Destino")
async def consultaDestino(destino: str, request: Request) -> BitacoraSalida:
    bitacoraDao = BitacoraDAO(request.app.db)
    return bitacoraDao.consultaDestino(destino)