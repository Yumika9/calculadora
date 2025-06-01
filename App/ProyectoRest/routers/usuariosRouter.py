from http.client import responses

from fastapi import APIRouter,Request, Depends,HTTPException, Body
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from typing import Union, Annotated
from dao import usuariosDao
from dao.bitacoraDao import BitacoraDAO
from dao.usuariosDao import UsuarioDAO
from model.usuariosModel import UsuarioInsert, Salida, UsuarioBaja, UsuarioSalida, Login, CambiarContra, EditarUser, \
    UsuarioSalidaR

router = APIRouter(prefix="/usuarios",tags=["Usuarios"])
security = HTTPBasic()
@router.post("/autenticar", response_model=UsuarioSalida, summary="Autenticar Usuario")
async def autenticar(login:Login, request:Request)->UsuarioSalida:
    usuariosDao=UsuarioDAO(request.app.db)
    correo= login.email
    contrasena= login.password
    return usuariosDao.autenticar(correo, contrasena)

async def validarUsuario(request:Request, credenciales:HTTPBasicCredentials=Depends(security))-> UsuarioSalida:
    usuariosDao = UsuarioDAO(request.app.db)
    return usuariosDao.autenticar(credenciales.username, credenciales.password)
@router.post("/", summary="Crear Usuario", response_model=Salida)
async def agregarUsuario(usuarioU:UsuarioInsert,request: Request) -> Salida:
    usuarioDao = UsuarioDAO(request.app.db)
    return usuarioDao.agregarUsuario(usuarioU)


@router.put("/{idUser}/modificar", summary="Cambiar Contraseña", response_model=Salida)
async def modificarPasswrd(idUser: str,key:CambiarContra, request: Request,respuesta: UsuarioSalida = Depends(validarUsuario)) -> Salida:
    tipor=respuesta.usuario.tipo
    if respuesta.estatus == 'OK' and respuesta.usuario.idUsuario == idUser:
        usuarioDao = UsuarioDAO(request.app.db)
        return usuarioDao.modificarPasswrd(idUser, key,tipor)
    else:
        raise HTTPException(status_code=403, detail="Sin autorización.")
@router.delete("/{idUser}/eliminar",response_model=Salida,summary="Eliminar Usuario")
async def eliminarUsuario(idUser:str,usuarioB:UsuarioBaja,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Administrador'):
        usuarioDao = UsuarioDAO(request.app.db)
        return usuarioDao.eliminarUsuario(idUser, usuarioB)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")
@router.get("/usuarios/consulta", response_model=UsuarioSalidaR, summary="Consulta General")
async def consultaGeneral(request: Request,respuesta: UsuarioSalida = Depends(validarUsuario)) -> UsuarioSalidaR:
    usuario = respuesta.usuario
    if respuesta.estatus == 'OK' and usuario.tipo == 'Administrador':
        usuarioDao = UsuarioDAO(request.app.db)
        return usuarioDao.consultaGeneral()
    else:
        raise HTTPException(status_code=403, detail="Sin autorización.")

@router.get("/usuarios/{idUser}", response_model=UsuarioSalida, summary="Consulta Individual")
async def consultaIndividual(idUser: str,request: Request,respuesta: UsuarioSalida = Depends(validarUsuario)) -> UsuarioSalida:
    usuario = respuesta.usuario
    tipos=usuario.tipo
    if respuesta.estatus == 'OK':
        usuarioDao = UsuarioDAO(request.app.db)
        return usuarioDao.consultaIndividual(idUser, tipos)
    else:
        raise HTTPException(status_code=403, detail="Sin autorización.")
