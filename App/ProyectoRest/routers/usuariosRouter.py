from http.client import responses

from fastapi import APIRouter,Request

from dao import usuariosDao
from dao.bitacoraDao import BitacoraDAO
from dao.usuariosDao import UsuarioDAO
from model.usuariosModel import UsuarioInsert, Salida, UsuarioBaja

router = APIRouter(prefix="/usuarios",tags=["Usuarios"])

@router.post("/", summary="Crear Usuario", response_model=Salida)
async def agregarUsuario(usuario:UsuarioInsert,request: Request) -> Salida:
    usuarios = UsuarioDAO(request.app.db)
    return usuarios.agregarUsuario(usuario)

@router.put("/{idUser}/modificar", summary="Editar Usuario", response_model=Salida)
async def modificarUsuario(idUser:str,usuario:UsuarioInsert,request: Request) -> Salida:
    usuarios = UsuarioDAO(request.app.db)
    return usuarios.modificarUsuario(idUser, usuario )

@router.delete("/{idUser}/eliminar",response_model=Salida,summary="Eliminar Usuario")
async def eliminarUsuario(idUser:str,usuario:UsuarioBaja,request: Request) -> Salida:
    usuarios = UsuarioDAO(request.app.db)
    return usuarios.eliminarUsuario(idUser, usuario)
