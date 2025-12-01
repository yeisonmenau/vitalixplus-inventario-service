import pandas as pd
import os

class InventarioService:
    def buscar_por_categoria(self, categoria: str):
        if self.df is None:
            raise RuntimeError(f"No se puede buscar productos. {self.error or 'Datos no disponibles'}")
        
        if 'categoría' not in self.df.columns:
            raise KeyError("La columna 'categoría' no existe en el archivo Excel.")
        
        if not categoria or len(categoria.strip()) < 2:
            raise ValueError("El nombre de la categoría debe tener al menos 2 caracteres.")
        
        resultado = self.df[self.df['categoría'].str.lower() == categoria.lower()]
        return resultado.to_dict(orient="records")

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(base_dir, '..', 'files', 'data', 'inventario_vitalix_plus.xlsx')

        try:
            df = pd.read_excel(archivo)
            
            # Validar que el archivo no esté vacío
            if df.empty:
                raise ValueError("El archivo Excel está vacío. No hay datos para cargar.")
            
            # Normalizar nombres de columnas
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
            
            # Validar columnas críticas
            columnas_requeridas = ['código', 'descripción']
            columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
            
            if columnas_faltantes:
                raise ValueError(f"Faltan columnas requeridas en el Excel: {', '.join(columnas_faltantes)}")
            
            # Si no existe la columna 'categoría', la agrega vacía
            if 'categoría' not in df.columns:
                df['categoría'] = ''
            
            self.df = df
            self.error = None
            
        except FileNotFoundError:
            error_msg = f"No se encontró el archivo en la ruta: {archivo}"
            print(f"Error: {error_msg}")
            self.df = None
            self.error = error_msg
            
        except ValueError as e:
            error_msg = f"Error de validación: {str(e)}"
            print(f"Error: {error_msg}")
            self.df = None
            self.error = error_msg
            
        except Exception as e:
            error_msg = f"Error inesperado al cargar el inventario: {str(e)}"
            print(f"Error: {error_msg}")
            self.df = None
            self.error = error_msg

    def listar_todo(self):
        if self.df is None:
            raise RuntimeError(f"No se puede listar el inventario. {self.error or 'Datos no disponibles'}")
        return self.df.to_dict(orient="records")

    def buscar_por_id(self, valor_id: int):
        if self.df is None:
            raise RuntimeError(f"No se puede buscar productos. {self.error or 'Datos no disponibles'}")
        
        if 'código' not in self.df.columns:
            raise KeyError("La columna 'código' no existe en el archivo Excel.")
        
        if not isinstance(valor_id, int) or valor_id <= 0:
            raise ValueError("El código del producto debe ser un número entero positivo.")
        
        resultado = self.df[self.df['código'] == valor_id]
        return resultado.to_dict(orient="records")

    def buscar_por_nombre(self, nombre: str):
        if self.df is None:
            raise RuntimeError(f"No se puede buscar productos. {self.error or 'Datos no disponibles'}")
        
        if 'descripción' not in self.df.columns:
            raise KeyError("La columna 'descripción' no existe en el archivo Excel.")
        
        if not nombre or len(nombre.strip()) < 2:
            raise ValueError("El término de búsqueda debe tener al menos 2 caracteres.")
        
        resultado = self.df[self.df['descripción'].str.contains(nombre, case=False, na=False)]
        return resultado.to_dict(orient="records")
    
    def columnas_disponibles(self):
        if self.df is None:
            raise RuntimeError(f"No se puede obtener columnas. {self.error or 'Datos no disponibles'}")
        return self.df.columns.tolist()