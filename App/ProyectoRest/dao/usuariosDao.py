from model.usuariosModel import UsuarioInsert, Salida, UsuarioBaja, UsuarioSalida
from fastapi.encoders import jsonable_encoder
from bson import  ObjectId

class UsuarioDAO:
    def __init__(self,db):
        self.db = db
    def autenticar(self,email,password):
        respuesta =UsuarioSalida(estatus="",mensaje="",usuario=None)
        try:
            usuario=self.db.user.find_one({'email':email, "password":password,"estatus":True})
            if usuario:
                respuesta.estatus= "OK"
                respuesta.mensaje = "Usuario autenticado"
                respuesta.usuario = usuario
            else:
                respuesta.estatus = "ERROR"
                respuesta.mensaje = "Datos Incorrectos"
        except Exception as e:
            print(e)
            respuesta.estatus = "ERROR"
            respuesta.mensaje = "Error al consultar al usuario, contacta con el administrador."
        return respuesta
    def agregarUsuario(self, usuario:UsuarioInsert):
        salida = Salida(estatus="", mensaje="")
        try:
           result= self.db.user.insert_one(jsonable_encoder(usuario))
           salida.estatus = "OK"
           salida.mensaje = "Usuario agregado con exito con el id: " + str(result.inserted_id)
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al agregar usuario, consulta al administrador."
        return salida

    def modificarUsuario(self,idUser:str, usuario:UsuarioInsert):
        salida = Salida(estatus="", mensaje="")
        try:
            identificador = self.db.user.find_one({"_id":ObjectId(idUser)})
            if identificador:
                estado =  self.db.user.find_one({"_id": ObjectId(idUser)}, projection={"estatus": True})
                if estado:
                    self.db.user.update_one( {"_id": ObjectId(idUser)},
                                             {"$set": {"nombre":usuario.nombre,
                                                       "email":usuario.email,
                                                       "password":usuario.password}})
                    salida.estatus = "OK"
                    salida.mensaje = "Usuario modificado con exito"
                else:
                    salida.estatus = "ERROR"
                    salida.mensaje = "El usuario no esta activo."
            else:
                salida.estatus = "ERROR"
                salida.mensaje = "El usuario no existe."
        except Exception as e:
            print(e)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al modificar usuario, consulta al administrador."
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

