
from fastapi import APIRouter
from service.inventario_service import InventarioService

router = APIRouter(prefix="/inventario", tags=["Inventario"])

servicio = InventarioService()

@router.get("/")
def listar():
    return servicio.listar_todo()

@router.get("/codigo/{item_id}")
def buscar_por_id(item_id: int):
    return servicio.buscar_por_id(item_id)

@router.get("/nombre/{nombre}")
def buscar_por_nombre(nombre: str):
    return servicio.buscar_por_nombre(nombre)


# Nuevo endpoint para buscar por categoría
@router.get("/categoria/{categoria}")
def buscar_por_categoria(categoria: str):
    return servicio.buscar_por_categoria(categoria)