from idlelib.pyshell import use_subprocess
from json import JSONEncoder
from types import NoneType

from model.usuariosModel import (UsuarioInsert, Salida, UsuarioBaja, UsuarioSalida,
                                 Login, Usuario, CambiarContra, EditarUser, UsuarioSalidaR)
from fastapi.encoders import jsonable_encoder
from bson import  ObjectId

class UsuarioDAO:
    def __init__(self,db):
        self.db = db

    def autenticar(self, correo: str, contrasena: str):
        respuesta = UsuarioSalida(estatus="", mensaje="", usuario= None)
        try:
            usuario = self.db.userViews.find_one(
                {"email": correo, "password": contrasena, "estatus": True})
            if usuario:
                projecion=self.db.userViews.find_one({"email": correo},{"idUsuario": 1, "nombre": 1, "email": 1, "tipo": 1})
                respuesta.estatus = "OK"
                respuesta.mensaje = "Usuario autenticado"
                respuesta.usuario =Usuario(**projecion)
            else:
                respuesta.estatus = "ERROR"
                respuesta.mensaje = "Datos incorrectos o usuario inactivo."
        except Exception as e:
            print(e)
            respuesta.estatus = "ERROR"
            respuesta.mensaje = "Error al consultar usuario."
        return respuesta

    def agregarUsuario(self, usuario:UsuarioInsert):
        salida = Salida(estatus="", mensaje="")
        try:
            email= self.db.user.find_one({"email":usuario.email},projection={"estatus": True})
            if(email):
               salida.estatus = "ERROR"
               salida.mensaje= "El email ya existe!!"
            else:
                if len(usuario.password) >= 8:
                    nuevoUser = {
                        "nombre": usuario.nombre,
                        "email": usuario.email,
                        "password": usuario.password,
                        "estatus": True,  # siempre verdadero al registrar
                        "tipo": "Usuario"  # solo el admin puede cambiar esto luego
                    }
                    result= self.db.user.insert_one(jsonable_encoder(nuevoUser))
                    salida.estatus = "OK"
                    salida.mensaje = "Usuario agregado con exito con el id: " + str(result.inserted_id)
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "La contraseña debe tener al menos 8 caracteres."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al agregar usuario, consulta al administrador."
        return salida

    def modificarPasswrd(self, idUser: str, key:CambiarContra, tipo: str):
        salida = Salida(estatus="", mensaje="")
        try:
            estado = self.db.userViews.find_one({"idUsuario": idUser,"estatus":True})
            if estado:
                if estado["tipo"] != tipo:
                    # El usuario intenta cambiar la key de otro tipo de cuenta
                    salida.estatus = "ERROR"
                    salida.mensaje = "No puede cambiar la contraseña de otro usuario."
                else:
                    if len(key.password) >= 8:
                        self.db.user.update_one(
                            {"_id": ObjectId(idUser)},
                            {"$set": {"password": key.password}}
                        )
                        salida.estatus = "OK"
                        salida.mensaje = "Contraseña actualizada."
                    else:
                        salida.estatus = "ERROR"
                        salida.mensaje = "La contraseña debe tener al menos 8 caracteres."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El usuario no está activo."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al modificar al usuario."
        return salida

    def modificarUser(self, idUser: str, user: EditarUser):
        salida = Salida(estatus="", mensaje="")
        try:
            datos= self.db.user.find_one({"_id":ObjectId(idUser)})
            if datos:
                usuario={}
                usuario["email"] = datos["email"] if user.email == "string" else user.email
                usuario["password"] = datos["password"] if user.password == "string" else user.password
                usuario["tipo"] = datos["tipo"] if user.tipo == "string" else user.tipo

                self.db.user.update_one(
                    {"_id": ObjectId(idUser)},
                    {"$set": usuario}
                )
                salida.estatus = "OK"
                salida.mensaje = "Usuario Actualizado con Exito."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El usuario con ese ID no existe."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al modificar al usuario."
        return salida

    def eliminarUsuario(self,idUser:str, usuario:UsuarioBaja):
        salida = Salida(estatus="", mensaje="")
        try:
            identificador = self.db.user.find_one({"_id": ObjectId(idUser)})
            if identificador:
                estado = self.db.user.find_one({"_id": ObjectId(idUser)}, projection={"estatus": True})
                if estado:
                    self.db.user.update_one({"_id": ObjectId(idUser)},
                                            {"$set": {"estatus": False, "motivoBaja":usuario.motivoBaja}})
                    salida.estatus = "OK"
                    salida.mensaje = "El usuario se dio de baja correctamente."
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "El usuario no esta activo."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El usuario no existe."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al dar de baja al usuario, consulta al administrador."
        return salida

    def consultaGeneral(self):
        salida = UsuarioSalidaR(estatus="",mensaje="",usuarioR=[])
        try:
            proyeccion = {"idUsuario": 1, "nombre": 1, "email": 1, "tipo": 1, "estatus": 1}
            listatmp =self.db.userViews.find({}, proyeccion)
            lista=[]
            for p in listatmp:
                p['idUsuario'] = str(p['idUsuario'])
                lista.append(p)
            salida.estatus ="OK"
            salida.mensaje = "Consulta general de usuarios."
            salida.usuarioR = lista
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al consultar los usuarios."
        return salida

    def consultaIndividual(self, idUser: str, tipo: str):
        salida = UsuarioSalida(estatus="", mensaje="", usuario=None)
        try:
            result = self.db.userViews.find_one({"idUsuario": idUser, "estatus": True})
            if result:
                if result["tipo"] != tipo:
                    #El usuario intenta consultar datos de otro tipo de cuenta
                    salida.estatus = "ERROR"
                    salida.mensaje = "No está autorizado para consultar otros usuarios."
                else:
                    salida.estatus = "OK"
                    salida.mensaje = "Consulta exitosa."
                    result['idUsuario'] = str(result['idUsuario'])  # asegúrate de serializar si es ObjectId
                    salida.usuario = Usuario(**result)
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "Usuario inactivo o no encontrado."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error en la consulta individual."
        return salida


