import pandas as pd
import os

class ImagenService:

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(base_dir, '..', 'files', 'data', 'imagen.xlsx')

        try:
            df = pd.read_excel(archivo)
            
            # Validar que el archivo no esté vacío
            if df.empty:
                raise ValueError("El archivo Excel de imágenes está vacío. No hay datos para cargar.")
            
            # Normalizar nombres de columnas
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
            
            # Validar columna crítica
            if 'código' not in df.columns:
                raise ValueError("Falta la columna requerida 'código' en el archivo Excel de imágenes")
            
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
            error_msg = f"Error inesperado al cargar imágenes: {str(e)}"
            print(f"Error: {error_msg}")
            self.df = None
            self.error = error_msg

    def listar_todo(self):
        if self.df is None:
            raise RuntimeError(f"No se pueden listar las imágenes. {self.error or 'Datos no disponibles'}")
        return self.df.to_dict(orient="records")

    def buscar_por_id(self, valor_id: int):
        if self.df is None:
            raise RuntimeError(f"No se pueden buscar imágenes. {self.error or 'Datos no disponibles'}")
        
        if 'código' not in self.df.columns:
            raise KeyError("La columna 'código' no existe en el archivo Excel.")
        
        if not isinstance(valor_id, int) or valor_id <= 0:
            raise ValueError("El código debe ser un número entero positivo.")
        
        resultado = self.df[self.df['código'] == valor_id]
        return resultado.to_dict(orient="records")
    
    def columnas_disponibles(self):
        if self.df is None:
            raise RuntimeError(f"No se puede obtener columnas. {self.error or 'Datos no disponibles'}")
        return self.df.columns.tolist()
