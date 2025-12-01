from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from service.ia_service import IAService

router = APIRouter(prefix="/ia", tags=["IA Asistente"])

ia_service = IAService()


class ConsultaRequest(BaseModel):
    pregunta: str

    @validator('pregunta')
    def validar_pregunta(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('La pregunta debe tener al menos 3 caracteres')
        if len(v) > 500:
            raise ValueError('La pregunta no puede exceder 500 caracteres')
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "pregunta": "¿Cuántos productos hay en el inventario?"
            }
        }


@router.post("/consultar")
def consultar_ia(request: ConsultaRequest):
    """
    Realiza una consulta en lenguaje natural sobre el inventario.
    
    Ejemplos de preguntas:
    - ¿Cuántos productos hay?
    - Dame productos de vitaminas
    - ¿Cuál es el producto más caro?
    - ¿Qué categorías tengo?
    - Muestra productos entre 10000 y 50000
    - ¿Cuál es el precio promedio?
    """
    try:
        resultado = ia_service.procesar_consulta(request.pregunta)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la consulta: {str(e)}")


@router.get("/ejemplos")
def obtener_ejemplos():
    """Retorna ejemplos de preguntas que la IA puede responder"""
    return {
        "ejemplos": [
            "¿Cuántos productos hay en el inventario?",
            "Dame productos de suplementos",
            "¿Cuál es el producto más caro?",
            "¿Cuál es el producto más barato?",
            "¿Qué categorías tengo disponibles?",
            "Muestra productos entre 10000 y 50000",
            "Dame estadísticas del inventario",
            "¿Cuál es el precio promedio?",
            "Busca vitaminas",
            "¿Cuántos productos de proteínas hay?"
        ],
        "intenciones_soportadas": [
            "contar - Contar productos totales o por categoría",
            "buscar - Buscar productos por nombre o categoría",
            "precio - Consultar precios (más caro, más barato, rangos)",
            "categorias - Listar categorías disponibles",
            "estadisticas - Obtener estadísticas del inventario",
            "filtrar - Filtrar productos por rango de precios"
        ]
    }
