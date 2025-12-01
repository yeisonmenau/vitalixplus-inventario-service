import pandas as pd
import os

class InventarioService:

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(base_dir, '..', 'files', 'data', 'inventario_vitalix_plus.xlsx')

        try:
            df = pd.read_excel(archivo)

            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

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

    def exportar_por_categoria(self, nombre_categoria, columna_categoria=None, output_dir=None, filename=None, include_index=False):
        """Exporta los registros filtrados por categoría a un archivo CSV.

        Parámetros:
        - nombre_categoria: valor de la categoría a filtrar (str o numérico).
        - columna_categoria: nombre de la columna a usar como categoría (opcional).
        - output_dir: directorio donde guardar el CSV (opcional). Por defecto `files/exports`.
        - filename: nombre del archivo CSV (opcional). Si no se suministra, se genera uno.
        - include_index: si True incluye el índice en el CSV.

        Retorna:
        - ruta absoluta del archivo CSV creado (str).
        - Si no hay DataFrame cargado, lanza ValueError.
        """
        if self.df is None:
            raise ValueError("No hay datos cargados para exportar.")

        # Determinar columna de categoría
        cols = self.df.columns.tolist()

        # Si el usuario especificó columna, usarla (si existe)
        if columna_categoria:
            if columna_categoria in cols:
                col = columna_categoria
            else:
                # intentar normalizar entrada del usuario (minusculas, espacios->_)
                alt = columna_categoria.strip().lower().replace(" ", "_")
                if alt in cols:
                    col = alt
                else:
                    raise KeyError(f"La columna especificada '{columna_categoria}' no existe en el DataFrame.")
        else:
            # Lista de candidatos comunes (ya se normalizaron columnas al cargar)
            candidatos = [
                'categoría', 'categoria', 'category', 'tipo', 'clase', 'categoria_producto',
                'categoria_producto'
            ]
            # Normaliza candidatos a la forma que usamos en df (minusculas y guiones bajos)
            candidatos = list(dict.fromkeys([c.strip().lower().replace(' ', '_') for c in candidatos]))
            col = None
            for c in candidatos:
                if c in cols:
                    col = c
                    break

            if col is None:
                # Si no se encuentra ningún candidato, intentar usar columna llamada 'categoria' sin acento
                if 'categoria' in cols:
                    col = 'categoria'
                else:
                    raise KeyError("No se encontró una columna de categoría conocida en el DataFrame. Por favor, especifica 'columna_categoria'.")

        # Filtrado (soporta comparaciones case-insensitive para texto)
        serie = self.df[col]
        if pd.api.types.is_string_dtype(serie):
            mask = serie.astype(str).str.strip().str.lower() == str(nombre_categoria).strip().lower()
        else:
            mask = serie == nombre_categoria

        resultado = self.df[mask]

        # Preparar ruta de salida
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(base_dir, '..'))
        if output_dir:
            out_dir = os.path.abspath(output_dir)
        else:
            out_dir = os.path.join(project_root, 'files', 'exports')

        os.makedirs(out_dir, exist_ok=True)

        # Nombre de archivo por defecto
        safe_val = str(nombre_categoria).strip().lower().replace(' ', '_')
        safe_val = ''.join(ch for ch in safe_val if ch.isalnum() or ch in ('-', '_'))
        if not filename:
            filename = f"export_categoria_{col}_{safe_val}.csv"

        output_path = os.path.join(out_dir, filename)

        # Guardar CSV con codificación utf-8-sig para compatibilidad con Excel
        resultado.to_csv(output_path, index=include_index, encoding='utf-8-sig')

        return os.path.abspath(output_path)