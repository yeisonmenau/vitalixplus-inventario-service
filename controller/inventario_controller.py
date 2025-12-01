from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
import os

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


@router.get("/exportar/categoria/{valor}")
def exportar_categoria(valor: str, columna: Optional[str] = None):
    """Exporta los registros de una categoría y devuelve el CSV como descarga.

    Parámetros:
    - valor: valor de la categoría a filtrar (ruta).
    - columna: nombre de la columna de categoría (opcional).
    """
    try:
        ruta = servicio.exportar_por_categoria(valor, columna_categoria=columna)
    except (ValueError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al generar el CSV")

    if not os.path.exists(ruta):
        raise HTTPException(status_code=500, detail="Archivo CSV no fue creado")

    nombre_archivo = os.path.basename(ruta)
    return FileResponse(ruta, media_type='text/csv', filename=nombre_archivo)