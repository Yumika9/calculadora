from pydantic import  BaseModel, Field

from typing import Optional

class UsuarioInsert(BaseModel):
    nombre: str
    email: str
    password: str
    estatus: bool
    tipo:str
class CambiarContra(BaseModel):
    password: str

class EditarUser(BaseModel):
    email: str
    password: str
    estatus:str
    tipo: str

class Salida(BaseModel):
    estatus:str
    mensaje:str

class UsuarioBaja(BaseModel):
    motivoBaja:str

class Login(BaseModel):
    email:str
    password:str

#Usuario Publico:
class Usuario(BaseModel):
    idUsuario: str
    nombre: str
    email: str
    tipo:str

class UsuarioSalida(Salida):
    usuario:Optional[Usuario] = None

#Para las consultas
class UsuarioSalidaR(Salida):
    usuarioR:list[Usuario]