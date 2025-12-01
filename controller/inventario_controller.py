
from fastapi import APIRouter, HTTPException
from service.inventario_service import InventarioService

router = APIRouter(prefix="/inventario", tags=["Inventario"])

servicio = InventarioService()

@router.get("/")
def listar():
    """Lista todos los productos del inventario"""
    try:
        return servicio.listar_todo()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/codigo/{item_id}")
def buscar_por_id(item_id: int):
    """Busca un producto por su código"""
    try:
        resultado = servicio.buscar_por_id(item_id)
        if not resultado:
            raise HTTPException(status_code=404, detail=f"No se encontró ningún producto con el código {item_id}")
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/nombre/{nombre}")
def buscar_por_nombre(nombre: str):
    """Busca productos por nombre (coincidencia parcial)"""
    try:
        resultado = servicio.buscar_por_nombre(nombre)
        if not resultado:
            raise HTTPException(status_code=404, detail=f"No se encontraron productos que coincidan con '{nombre}'")
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Nuevo endpoint para buscar por categoría
@router.get("/categoria/{categoria}")
def buscar_por_categoria(categoria: str):
    """Busca productos por categoría"""
    try:
        resultado = servicio.buscar_por_categoria(categoria)
        if not resultado:
            raise HTTPException(status_code=404, detail=f"No se encontraron productos en la categoría '{categoria}'")
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")