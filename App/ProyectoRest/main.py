import uvicorn

from fastapi import FastAPI
from dao.database import Conexion

from routers import bitacoraRouter, usuariosRouter, autoRouter

app = FastAPI()
app.include_router(bitacoraRouter.router)
app.include_router(usuariosRouter.router)

app.include_router(autoRouter.router)
@app.get("/")
async def home():
    salida = {"mensaje":"Bienvenido a Calculadora REST"}
    return salida

@app.on_event("startup")
async def startup():
    print("Conectando a MongoDB")
    conexion = Conexion()
    app.conexion = conexion
    app.db = conexion.getDB()

@app.on_event("shutdown")
async def shutdown():
    print("Cerrando la conexion a MongoDB")
    app.conexion.cerrar()



if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', reload=True)