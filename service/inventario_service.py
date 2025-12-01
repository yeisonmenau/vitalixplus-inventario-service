import pandas as pd
import os

class InventarioService:
    def buscar_por_categoria(self, categoria: str):
        if self.df is not None:
            if 'categoría' not in self.df.columns:
                raise KeyError("La columna 'categoría' no existe en el archivo Excel.")
            resultado = self.df[self.df['categoría'].str.lower() == categoria.lower()]
            return resultado.to_dict(orient="records")
        return []

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(base_dir, '..', 'files', 'data', 'inventario_vitalix_plus.xlsx')

        try:
            df = pd.read_excel(archivo)
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
            # Si no existe la columna 'categoría', la agrega vacía
            if 'categoría' not in df.columns:
                df['categoría'] = ''
            self.df = df
        except FileNotFoundError:
            print("Error: No se encontró el archivo en la ruta especificada.")
            self.df = None

    def listar_todo(self):
        if self.df is not None:
            return self.df.to_dict(orient="records")
        return []

    def buscar_por_id(self, valor_id: int):
        if self.df is not None:
            if 'código' not in self.df.columns:
                raise KeyError("La columna 'código' no existe en el archivo Excel.")

            resultado = self.df[self.df['código'] == valor_id]
            return resultado.to_dict(orient="records")
        return []

    def buscar_por_nombre(self, nombre: str):
        if self.df is not None:
            if 'descripción' not in self.df.columns:
                raise KeyError("La columna 'descripción' no existe en el archivo Excel.")

            resultado = self.df[self.df['descripción'].str.contains(nombre, case=False, na=False)]
            return resultado.to_dict(orient="records")
        return []
    
    def columnas_disponibles(self):
        if self.df is not None:
            return self.df.columns.tolist()
        return []