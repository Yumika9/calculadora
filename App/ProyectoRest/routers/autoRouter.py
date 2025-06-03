from fastapi import APIRouter,Request, Depends, HTTPException

from dao import usuariosDao
from dao.autoDao import AutoDAO
from dao.bitacoraDao import BitacoraDAO
from model.autoModel import AutoInsert, AutoBaja, AutoSalida

from model.usuariosModel import Salida, UsuarioSalida
from routers.usuariosRouter import validarUsuario

router = APIRouter(prefix="/autos",tags=["Autos"])

@router.post("/", summary="Crear Auto", response_model=Salida)
async def agregarAuto(idUser:str, autos:AutoInsert,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario.tipo == 'Usuario' and usuario.idUsuario ==idUser):
        auto = AutoDAO(request.app.db)
        return auto.agregarAuto(idUser,autos)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

@router.put("/{idAuto}/modificar", summary="Editar Auto", response_model=Salida)
async def modificarAuto(idAuto:str,auto:AutoInsert,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario.tipo == 'Usuario' or usuario.tipo == 'Administrador'):
        autoDao = AutoDAO(request.app.db)
        return autoDao.modificarAuto(usuario.idUsuario,usuario.tipo,idAuto, auto )
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

@router.delete("/{idAuto}/eliminar",response_model=Salida,summary="Eliminar Auto")
async def eliminarAuto(idAuto:str,autoB:AutoBaja,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    idUser=respuesta.usuario.idUsuario
    tipor=respuesta.usuario.tipo
    if (respuesta.estatus == 'OK' and tipor == 'Administrador' or tipor=="Usuario"):
        autoDao = AutoDAO(request.app.db)
        return autoDao.eliminarAuto(idUser,tipor,idAuto, autoB)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

@router.get("/consultaGeneral", response_model=AutoSalida, summary="Consulta General")
async def consultaGeneral(request: Request, respuesta:UsuarioSalida=Depends(validarUsuario))->AutoSalida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario.tipo == 'Administrador'):
        autoDao = AutoDAO(request.app.db)
        return autoDao.consultaGeneral()
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

@router.get("/consulta/{idAuto}", response_model=AutoSalida, summary="Consulta Individual")
async def consultaIndividual(idAuto:str,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario))->AutoSalida:
    idUser = respuesta.usuario.idUsuario
    tipor = respuesta.usuario.tipo
    if (respuesta.estatus == 'OK' and tipor == 'Administrador' or tipor == 'Usuario'):
        autoDao = AutoDAO(request.app.db)
        return autoDao.consultaIndividual(idUser,tipor,idAuto)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")