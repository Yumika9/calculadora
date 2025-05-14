from pydantic import  BaseModel


class UsuarioInsert(BaseModel):
    nombre: str
    email: str
    password: str
    estatus: bool = True

class Salida(BaseModel):
    estatus:str
    mensaje:str

class UsuarioBaja(BaseModel):
    motivoBaja:str