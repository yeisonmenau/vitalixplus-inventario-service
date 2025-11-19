from fastapi import APIRouter
from service.imagen_service import ImagenService

router = APIRouter(prefix="/imagen", tags=["imagen"])

servicio = ImagenService()

@router.get("/")
def listar():
    return servicio.listar_todo()

@router.get("/{item_id}")
def buscar_por_id(item_id: int):
    return servicio.buscar_por_id(item_id)
