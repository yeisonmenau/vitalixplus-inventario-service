import re
from typing import Dict, List, Any
import pandas as pd
from service.inventario_service import InventarioService


class IAService:
    """Servicio de IA para consultas inteligentes sobre el inventario"""

    def __init__(self):
        self.inventario_service = InventarioService()
        
        # Diccionario de intenciones con palabras clave
        self.intenciones = {
            'contar': ['cuántos', 'cuantos', 'cantidad', 'total', 'número', 'numero', 'hay'],
            'buscar': ['buscar', 'encontrar', 'dame', 'muestra', 'ver', 'lista', 'productos'],
            'precio': ['precio', 'costo', 'valor', 'caro', 'barato', 'económico', 'economico'],
            'categorias': ['categoría', 'categoria', 'categorías', 'categorias', 'tipo', 'tipos', 'clase'],
            'estadisticas': ['promedio', 'media', 'estadística', 'estadistica', 'análisis', 'analisis'],
            'filtrar': ['entre', 'rango', 'mayor', 'menor', 'desde', 'hasta']
        }

    def procesar_consulta(self, pregunta: str) -> Dict[str, Any]:
        """Procesa una pregunta en lenguaje natural y retorna una respuesta estructurada"""
        
        pregunta_lower = pregunta.lower()
        
        # Detectar intención
        intencion = self._detectar_intencion(pregunta_lower)
        
        # Ejecutar según la intención detectada
        if intencion == 'contar':
            return self._contar_productos(pregunta_lower)
        elif intencion == 'categorias':
            return self._listar_categorias(pregunta_lower)
        elif intencion == 'precio':
            return self._analizar_precios(pregunta_lower)
        elif intencion == 'estadisticas':
            return self._calcular_estadisticas(pregunta_lower)
        elif intencion == 'filtrar':
            return self._filtrar_productos(pregunta_lower)
        elif intencion == 'buscar':
            return self._buscar_productos(pregunta_lower)
        else:
            return {
                "respuesta": "No entendí tu consulta. Intenta preguntar sobre productos, categorías, precios o cantidades.",
                "intencion_detectada": "desconocida",
                "datos": []
            }

    def _detectar_intencion(self, pregunta: str) -> str:
        """Detecta la intención de la pregunta basándose en palabras clave"""
        
        puntuaciones = {}
        
        for intencion, palabras_clave in self.intenciones.items():
            puntuacion = sum(1 for palabra in palabras_clave if palabra in pregunta)
            puntuaciones[intencion] = puntuacion
        
        # Retornar la intención con mayor puntuación
        if max(puntuaciones.values()) > 0:
            return max(puntuaciones, key=puntuaciones.get)
        
        return 'buscar'  # Intención por defecto

    def _extraer_categoria(self, pregunta: str) -> str:
        """Extrae el nombre de una categoría de la pregunta"""
        
        # Obtener todas las categorías disponibles
        df = self.inventario_service.df
        if df is not None and 'categoría' in df.columns:
            categorias = df['categoría'].dropna().unique()
            
            # Buscar si alguna categoría está mencionada en la pregunta
            for cat in categorias:
                if cat.lower() in pregunta:
                    return cat
        
        return None

    def _extraer_numeros(self, pregunta: str) -> List[float]:
        """Extrae números de la pregunta"""
        
        numeros = re.findall(r'\d+(?:\.\d+)?', pregunta)
        return [float(num) for num in numeros]

    def _contar_productos(self, pregunta: str) -> Dict[str, Any]:
        """Cuenta productos según criterios"""
        
        categoria = self._extraer_categoria(pregunta)
        
        if categoria:
            productos = self.inventario_service.buscar_por_categoria(categoria)
            cantidad = len(productos)
            return {
                "respuesta": f"Hay {cantidad} producto(s) en la categoría '{categoria}'",
                "intencion_detectada": "contar",
                "datos": {
                    "cantidad": cantidad,
                    "categoria": categoria,
                    "productos": productos
                }
            }
        else:
            productos = self.inventario_service.listar_todo()
            cantidad = len(productos)
            return {
                "respuesta": f"Hay {cantidad} productos en total en el inventario",
                "intencion_detectada": "contar",
                "datos": {
                    "cantidad": cantidad
                }
            }

    def _listar_categorias(self, pregunta: str) -> Dict[str, Any]:
        """Lista las categorías disponibles"""
        
        df = self.inventario_service.df
        if df is not None and 'categoría' in df.columns:
            categorias = df['categoría'].dropna().unique().tolist()
            categorias_limpias = [cat for cat in categorias if cat != '']
            
            if categorias_limpias:
                categorias_texto = ", ".join(categorias_limpias)
                return {
                    "respuesta": f"Las categorías disponibles son: {categorias_texto}",
                    "intencion_detectada": "categorias",
                    "datos": {
                        "categorias": categorias_limpias,
                        "total": len(categorias_limpias)
                    }
                }
        
        return {
            "respuesta": "No se encontraron categorías en el inventario",
            "intencion_detectada": "categorias",
            "datos": {"categorias": []}
        }

    def _analizar_precios(self, pregunta: str) -> Dict[str, Any]:
        """Analiza precios (más caro, más barato, etc.)"""
        
        df = self.inventario_service.df
        if df is None or df.empty:
            return {
                "respuesta": "No hay datos disponibles",
                "intencion_detectada": "precio",
                "datos": []
            }
        
        # Buscar columna de precio (puede tener diferentes nombres)
        columna_precio = None
        for col in df.columns:
            if 'precio' in col.lower() or 'valor' in col.lower() or 'costo' in col.lower():
                columna_precio = col
                break
        
        if columna_precio is None:
            return {
                "respuesta": "No se encontró información de precios en el inventario",
                "intencion_detectada": "precio",
                "datos": []
            }
        
        # Determinar si busca el más caro o más barato
        if 'caro' in pregunta or 'mayor' in pregunta or 'máximo' in pregunta or 'maximo' in pregunta:
            producto_max = df.loc[df[columna_precio].idxmax()].to_dict()
            precio = producto_max.get(columna_precio, 0)
            nombre = producto_max.get('descripción', 'Producto')
            
            return {
                "respuesta": f"El producto más caro es '{nombre}' con un precio de ${precio:,.0f}",
                "intencion_detectada": "precio",
                "datos": producto_max
            }
        
        elif 'barato' in pregunta or 'menor' in pregunta or 'económico' in pregunta or 'economico' in pregunta or 'mínimo' in pregunta or 'minimo' in pregunta:
            df_filtrado = df[df[columna_precio] > 0]  # Excluir precios 0
            if not df_filtrado.empty:
                producto_min = df_filtrado.loc[df_filtrado[columna_precio].idxmin()].to_dict()
                precio = producto_min.get(columna_precio, 0)
                nombre = producto_min.get('descripción', 'Producto')
                
                return {
                    "respuesta": f"El producto más barato es '{nombre}' con un precio de ${precio:,.0f}",
                    "intencion_detectada": "precio",
                    "datos": producto_min
                }
        
        # Por defecto, mostrar rango de precios
        precio_min = df[df[columna_precio] > 0][columna_precio].min()
        precio_max = df[columna_precio].max()
        
        return {
            "respuesta": f"Los precios van desde ${precio_min:,.0f} hasta ${precio_max:,.0f}",
            "intencion_detectada": "precio",
            "datos": {
                "precio_minimo": float(precio_min),
                "precio_maximo": float(precio_max)
            }
        }

    def _calcular_estadisticas(self, pregunta: str) -> Dict[str, Any]:
        """Calcula estadísticas sobre el inventario"""
        
        df = self.inventario_service.df
        if df is None or df.empty:
            return {
                "respuesta": "No hay datos disponibles",
                "intencion_detectada": "estadisticas",
                "datos": {}
            }
        
        # Buscar columna de precio
        columna_precio = None
        for col in df.columns:
            if 'precio' in col.lower() or 'valor' in col.lower():
                columna_precio = col
                break
        
        estadisticas = {
            "total_productos": len(df)
        }
        
        if columna_precio:
            precios = df[df[columna_precio] > 0][columna_precio]
            estadisticas.update({
                "precio_promedio": float(precios.mean()),
                "precio_mediana": float(precios.median()),
                "precio_minimo": float(precios.min()),
                "precio_maximo": float(precios.max())
            })
        
        if 'categoría' in df.columns:
            categorias = df['categoría'].value_counts().to_dict()
            estadisticas["productos_por_categoria"] = categorias
        
        respuesta = f"Estadísticas del inventario:\n"
        respuesta += f"• Total de productos: {estadisticas['total_productos']}\n"
        
        if columna_precio:
            respuesta += f"• Precio promedio: ${estadisticas['precio_promedio']:,.0f}\n"
            respuesta += f"• Precio mediana: ${estadisticas['precio_mediana']:,.0f}"
        
        return {
            "respuesta": respuesta,
            "intencion_detectada": "estadisticas",
            "datos": estadisticas
        }

    def _filtrar_productos(self, pregunta: str) -> Dict[str, Any]:
        """Filtra productos por rango de precios"""
        
        numeros = self._extraer_numeros(pregunta)
        
        if len(numeros) < 2:
            return {
                "respuesta": "Por favor especifica un rango de precios, por ejemplo: 'productos entre 10000 y 50000'",
                "intencion_detectada": "filtrar",
                "datos": []
            }
        
        df = self.inventario_service.df
        if df is None or df.empty:
            return {
                "respuesta": "No hay datos disponibles",
                "intencion_detectada": "filtrar",
                "datos": []
            }
        
        # Buscar columna de precio
        columna_precio = None
        for col in df.columns:
            if 'precio' in col.lower() or 'valor' in col.lower():
                columna_precio = col
                break
        
        if columna_precio is None:
            return {
                "respuesta": "No se encontró información de precios para filtrar",
                "intencion_detectada": "filtrar",
                "datos": []
            }
        
        precio_min, precio_max = min(numeros[:2]), max(numeros[:2])
        df_filtrado = df[(df[columna_precio] >= precio_min) & (df[columna_precio] <= precio_max)]
        productos = df_filtrado.to_dict(orient='records')
        
        return {
            "respuesta": f"Encontré {len(productos)} producto(s) entre ${precio_min:,.0f} y ${precio_max:,.0f}",
            "intencion_detectada": "filtrar",
            "datos": {
                "cantidad": len(productos),
                "rango": {"minimo": precio_min, "maximo": precio_max},
                "productos": productos
            }
        }

    def _buscar_productos(self, pregunta: str) -> Dict[str, Any]:
        """Busca productos por nombre o categoría"""
        
        # Primero intentar buscar por categoría
        categoria = self._extraer_categoria(pregunta)
        
        if categoria:
            productos = self.inventario_service.buscar_por_categoria(categoria)
            return {
                "respuesta": f"Encontré {len(productos)} producto(s) en la categoría '{categoria}'",
                "intencion_detectada": "buscar",
                "datos": {
                    "cantidad": len(productos),
                    "categoria": categoria,
                    "productos": productos
                }
            }
        
        # Si no hay categoría, intentar extraer palabras clave para buscar por nombre
        palabras_excluir = ['buscar', 'dame', 'muestra', 'ver', 'productos', 'de', 'la', 'el', 'los', 'las', 'un', 'una']
        palabras = [p for p in pregunta.split() if p not in palabras_excluir and len(p) > 2]
        
        if palabras:
            # Buscar por la primera palabra significativa
            palabra_busqueda = palabras[0]
            productos = self.inventario_service.buscar_por_nombre(palabra_busqueda)
            
            if productos:
                return {
                    "respuesta": f"Encontré {len(productos)} producto(s) relacionado(s) con '{palabra_busqueda}'",
                    "intencion_detectada": "buscar",
                    "datos": {
                        "cantidad": len(productos),
                        "termino_busqueda": palabra_busqueda,
                        "productos": productos
                    }
                }
        
        # Si no se encontró nada específico, listar todo
        productos = self.inventario_service.listar_todo()
        return {
            "respuesta": f"Mostrando todos los productos del inventario ({len(productos)} en total)",
            "intencion_detectada": "buscar",
            "datos": {
                "cantidad": len(productos),
                "productos": productos[:10]  # Limitar a 10 para no sobrecargar
            }
        }
