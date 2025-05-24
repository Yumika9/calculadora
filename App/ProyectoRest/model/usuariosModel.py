from pydantic import  BaseModel, Field


class UsuarioInsert(BaseModel):
    nombre: str
    email: str
    password: str
    estatus: bool = True
    tipo:str

class Salida(BaseModel):
    estatus:str
    mensaje:str

class UsuarioBaja(BaseModel):
    motivoBaja:str

class Login(BaseModel):
    email:str
    password:str

class Usuario(BaseModel):
    idUsuario:int = Field(alias="_id")
    nombre: str
    email: str
    password: str
    estatus: bool = True
    tipo: str

class UsuarioSalida(Salida):
    usuario:Usuario | None =None