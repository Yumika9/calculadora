class UsuarioDAO:
    def __init__(self,db):
        self.db = db
    def comprobarUsuario(self,idUsuario:int):
        respuesta =False
        try:
            usuario= self.db.user.find_one({'_id':idUsuario, "estatus":True})
            if usuario:
                respuesta= True
        except:
            respuesta= False
        return respuesta

