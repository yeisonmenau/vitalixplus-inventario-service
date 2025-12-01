from fastapi import APIRouter, HTTPException
from service.imagen_service import ImagenService

router = APIRouter(prefix="/imagen", tags=["imagen"])

servicio = ImagenService()

@router.get("/")
def listar():
    """Lista todas las imágenes"""
    try:
        return servicio.listar_todo()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/{item_id}")
def buscar_por_id(item_id: int):
    """Busca una imagen por código"""
    try:
        resultado = servicio.buscar_por_id(item_id)
        if not resultado:
            raise HTTPException(status_code=404, detail=f"No se encontró ninguna imagen con el código {item_id}")
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
