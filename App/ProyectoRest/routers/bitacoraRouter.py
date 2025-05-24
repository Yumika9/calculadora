from fastapi import APIRouter, Request, Depends, HTTPException

from dao.bitacoraDao import BitacoraDAO
from model.bitacoraModel import BitacoraInsert, BitacoraSalida, BitacoraSalidaAuto
from model.usuariosModel import Salida, UsuarioSalida
from routers.usuariosRouter import validarUsuario

router = APIRouter(prefix="/bitacora",tags=["Bitacora"])

@router.post("/", summary="Crear Bitacora", response_model=Salida)
async def agregarBitacora(bitacora:BitacoraInsert,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Usuario'):
        bitacoraDao = BitacoraDAO(request.app.db)
        return bitacoraDao.agregarBitacora(bitacora)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

@router.get("/", response_model=BitacoraSalida, summary="Consulta General")
async def consultaGeneral(request: Request, respuesta:UsuarioSalida=Depends(validarUsuario))->BitacoraSalida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Usuario' or usuario['tipo'] == 'Administrador'):
        bitacoraDao = BitacoraDAO(request.app.db)
        return bitacoraDao.consultaGeneral()
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

@router.get("/consultaAuto", response_model=BitacoraSalidaAuto, summary="Consulta por Auto")
async def consultaAuto(request: Request, idAuto: str = None, marca: str = None, modelo: str = None, respuesta:UsuarioSalida=Depends(validarUsuario)) -> BitacoraSalidaAuto:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Usuario' or usuario['tipo'] == 'Administrador'):
        bitacoraDao = BitacoraDAO(request.app.db)
        return bitacoraDao.consultaAuto(idAuto, marca, modelo)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

@router.get("/bitacora/{destino}", response_model=BitacoraSalida, summary="Consulta por Destino")
async def consultaDestino(destino: str, request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> BitacoraSalida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Usuario' or usuario['tipo'] == 'Administrador'):
        bitacoraDao = BitacoraDAO(request.app.db)
        return bitacoraDao.consultaDestino(destino)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

