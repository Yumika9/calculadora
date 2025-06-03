from fastapi import APIRouter, Request, Depends, HTTPException

from dao.bitacoraDao import BitacoraDAO
from model.bitacoraModel import BitacoraInsert, BitacoraSalida, BitacoraSalidaAuto, RecargasCombustible
from model.usuariosModel import Salida, UsuarioSalida
from routers.usuariosRouter import validarUsuario

router = APIRouter(prefix="/bitacora",tags=["Bitacora"])

@router.post("/", summary="Crear Bitacora", response_model=Salida)
async def agregarBitacora(bitacora:BitacoraInsert,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario.tipo == 'Usuario'):
        bitacoraDao = BitacoraDAO(request.app.db)
        return bitacoraDao.agregarBitacora(bitacora)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")
@router.post("/recarga/{idBita}", summary="Agregar Recarga", response_model=Salida)
async def agregarRecarga(idBita:str,bitacora:RecargasCombustible,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario.tipo == 'Usuario'):
        bitacoraDao = BitacoraDAO(request.app.db)
        return bitacoraDao.agregarRecarga(idBita,bitacora)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

@router.get("/", response_model=BitacoraSalida, summary="Consulta General")
async def consultaGeneral(request: Request, respuesta:UsuarioSalida=Depends(validarUsuario))->BitacoraSalida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario.tipo == 'Usuario' or usuario.tipo == 'Administrador'):
        bitacoraDao = BitacoraDAO(request.app.db)
        return bitacoraDao.consultaGeneral()
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

@router.get("/consultaAuto", response_model=BitacoraSalidaAuto, summary="Consulta Autos en Bitacora")
async def consultaAuto(request: Request,marca: str , modelo: str, idAuto: str = None , respuesta:UsuarioSalida=Depends(validarUsuario)) -> BitacoraSalidaAuto:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario.tipo == 'Usuario' or usuario.tipo == 'Administrador'):
        bitacoraDao = BitacoraDAO(request.app.db)
        return bitacoraDao.consultaAuto(marca, modelo,idAuto)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

@router.get("/cunsultaRuta", response_model=BitacoraSalida, summary="Consulta por Origen-Destino.")
async def consultaDestino(origen:str,destino: str, request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> BitacoraSalida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario.tipo == 'Usuario' or usuario.tipo == 'Administrador'):
        bitacoraDao = BitacoraDAO(request.app.db)
        return bitacoraDao.consultaDestino(origen, destino)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

