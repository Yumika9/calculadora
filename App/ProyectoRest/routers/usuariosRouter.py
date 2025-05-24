from http.client import responses

from fastapi import APIRouter,Request, Depends,HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from dao import usuariosDao
from dao.bitacoraDao import BitacoraDAO
from dao.usuariosDao import UsuarioDAO
from model.usuariosModel import UsuarioInsert, Salida, UsuarioBaja, UsuarioSalida, Login

router = APIRouter(prefix="/usuarios",tags=["Usuarios"])
security = HTTPBasic()
@router.post("/autenticar", response_model=UsuarioSalida, summary="Autenticar Usuario")
async def autenticar(login:Login, request:Request)->UsuarioSalida:
    usuariosDao=UsuarioDAO(request.app.db)
    return usuariosDao.autenticar(login.email,login.password)

async def validarUsuario(request:Request, credenciales:HTTPBasicCredentials=Depends(security))-> UsuarioSalida:
    usuariosDao = UsuarioDAO(request.app.db)
    return usuariosDao.autenticar(credenciales.username, credenciales.password)
@router.post("/", summary="Crear Usuario", response_model=Salida)
async def agregarUsuario(usuarioU:UsuarioInsert,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Usuario'):
        usuarioDao = UsuarioDAO(request.app.db)
        return usuarioDao.agregarUsuario(usuarioU)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")

@router.put("/{idUser}/modificar", summary="Editar Usuario", response_model=Salida)
async def modificarUsuario(idUser:str,usuarioI:UsuarioInsert,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Usuario'):
        usuarioDao = UsuarioDAO(request.app.db)
        return usuarioDao.modificarUsuario(idUser, usuarioI )
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")


@router.delete("/{idUser}/eliminar",response_model=Salida,summary="Eliminar Usuario")
async def eliminarUsuario(idUser:str,usuarioB:UsuarioBaja,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Administrador'):
        usuarioDao = UsuarioDAO(request.app.db)
        return usuarioDao.eliminarUsuario(idUser, usuarioB)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")
