from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from service.inventario_service import InventarioService

router = APIRouter(prefix="/inventario", tags=["Inventario"])

servicio = InventarioService()

@router.get("/")
def listar() -> List[Dict[str, Any]]:
    """Lista todos los productos del inventario"""
    try:
        return servicio.listar_todo()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/codigo/{item_id}")
def buscar_por_id(item_id: int) -> Dict[str, Any]:
    """Busca un producto por su código"""
    try:
        resultado = servicio.buscar_por_id(item_id)
        if not resultado:
            raise HTTPException(status_code=404, detail=f"No se encontró ningún producto con el código {item_id}")
        return resultado
    except HTTPException:
        raise
    except (ValueError, RuntimeError, KeyError) as e:
        status_code = {
            ValueError: 400,
            RuntimeError: 503,
            KeyError: 500
        }[type(e)]
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/nombre/{nombre}")
def buscar_por_nombre(nombre: str) -> List[Dict[str, Any]]:
    """Busca productos por nombre (coincidencia parcial)"""
    try:
        resultado = servicio.buscar_por_nombre(nombre)
        if not resultado:
            raise HTTPException(status_code=404, detail=f"No se encontraron productos que coincidan con '{nombre}'")
        return resultado
    except HTTPException:
        raise
    except (ValueError, RuntimeError, KeyError) as e:
        status_code = {
            ValueError: 400,
            RuntimeError: 503,
            KeyError: 500
        }[type(e)]
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/categoria/{categoria}")
def buscar_por_categoria(categoria: str) -> List[Dict[str, Any]]:
    """Busca productos por categoría"""
    try:
        resultado = servicio.buscar_por_categoria(categoria)
        if not resultado:
            raise HTTPException(status_code=404, detail=f"No se encontraron productos en la categoría '{categoria}'")
        return resultado
    except HTTPException:
        raise
    except (ValueError, RuntimeError, KeyError) as e:
        status_code = {
            ValueError: 400,
            RuntimeError: 503,
            KeyError: 500
        }[type(e)]
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")