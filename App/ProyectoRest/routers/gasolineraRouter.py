from fastapi import APIRouter,Request, Depends, HTTPException

from dao.gasolinerasDao import GasolineraDAO
from model.gasolineraModel import GasolineraInsert, GasolineraBaja, GasolineraSalida
from model.usuariosModel import Salida, UsuarioSalida
from routers.usuariosRouter import validarUsuario

router = APIRouter(prefix="/gasolineras",tags=["Gasolineras"])

@router.post("/", summary="Agregar Gasolinera", response_model=Salida)
async def agregarGasolinera(gasolina:GasolineraInsert,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Administrador'):
        gasDao = GasolineraDAO(request.app.db)
        return gasDao.agregarGasolinera(gasolina)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")
@router.put("/{idGas}/modificar", summary="Actualizar Gasolinera", response_model=Salida)
async def modificarGasolinera(idGas:str,gasolina:GasolineraInsert,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Administrador'):
        gasDao = GasolineraDAO(request.app.db)
        return gasDao.modificarGasolinera(idGas, gasolina )
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")
@router.delete("/{idGas}/eliminar",response_model=Salida,summary="Dar de baja Gasolinera")
async def eliminarGasolinera(idGas:str,gasB:GasolineraBaja,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario)) -> Salida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Administrador'):
        gasDao = GasolineraDAO(request.app.db)
        return gasDao.eliminarGasolinera(idGas, gasB)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")
@router.get("/consulta", response_model=GasolineraSalida, summary="Consulta General")
async def consultaGeneral(request: Request, respuesta:UsuarioSalida=Depends(validarUsuario))->GasolineraSalida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Administrador' or usuario['tipo'] == 'Usuario'):
        gasDao = GasolineraDAO(request.app.db)
        return gasDao.consultaGeneral()
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")
@router.get("/{idGasolinera}/consultaInd", response_model=GasolineraSalida, summary="Consulta Individual")
async def consultaIndividual(idGas:str,request: Request, respuesta:UsuarioSalida=Depends(validarUsuario))->GasolineraSalida:
    usuario = respuesta.usuario
    if (respuesta.estatus == 'OK' and usuario['tipo'] == 'Administrador' or usuario['tipo'] == 'Usuario'):
        gasDao = GasolineraDAO(request.app.db)
        return gasDao.consultaIndividual(idGas)
    else:
        raise HTTPException(status_code=404, detail="Sin autorizacion.")