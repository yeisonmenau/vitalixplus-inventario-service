import pandas as pd
import os
import unicodedata

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
            col = self._buscar_columna(['codigo', 'código', 'code', 'id', 'item_id', 'codigo_producto'])
            if not col:
                raise KeyError("No se encontró una columna de 'código' en el archivo Excel.")
            
            # Comparar tolerante: convertir a string y comparar
            resultado = self.df[self.df[col].astype(str).str.strip() == str(valor_id).strip()]
            return resultado.to_dict(orient="records")
        return []

    def buscar_por_nombre(self, nombre: str):
        if self.df is not None:
            col = self._buscar_columna(['descripcion', 'descripción', 'nombre', 'name', 'producto', 'nombre_producto'])
            if not col:
                raise KeyError("No se encontró una columna de 'descripción' en el archivo Excel.")

            resultado = self.df[self.df[col].astype(str).str.contains(nombre, case=False, na=False)]
            return resultado.to_dict(orient="records")
        return []
    
    def columnas_disponibles(self):
        if self.df is not None:
            return self.df.columns.tolist()
        return []

    def _buscar_columna(self, candidatos):
        """Helper privado: busca columna en candidatos (variantes de nombres con/sin acentos, espacios, etc.).
        
        Parámetros:
        - candidatos: lista de nombres posibles (en cualquier formato).
        
        Retorna:
        - Nombre exacto de la columna en self.df si existe, o None si no.
        """
        if self.df is None:
            return None
        
        cols_disponibles = self.df.columns.tolist()
        
        def normalizar(s):
            """Normaliza string: quita acentos, espacios a guiones bajos, minusculas."""
            s = str(s).strip().lower()
            # Quitar acentos (ñ -> n, á -> a, etc.)
            s = ''.join(c for c in unicodedata.normalize('NFD', s) 
                       if unicodedata.category(c) != 'Mn')
            # Reemplazar espacios y guiones con guion bajo
            s = s.replace(' ', '_').replace('-', '_')
            return s
        
        # Normalizar candidatos
        candidatos_norm = {normalizar(c): c for c in candidatos}
        
        # Buscar en columnas del df
        for col in cols_disponibles:
            if normalizar(col) in candidatos_norm:
                return col
        
        return None

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
        """
        if self.df is None:
            raise ValueError("No hay datos cargados para exportar.")

        # Determinar columna de categoría
        if columna_categoria:
            # Si el usuario especificó columna, intentar normalizarla
            col = self._buscar_columna([columna_categoria])
            if not col:
                raise KeyError(f"La columna especificada '{columna_categoria}' no existe en el DataFrame.")
        else:
            # Intentar detectar columna de categoría automáticamente
            col = self._buscar_columna(['categoria', 'categoría', 'category', 'tipo', 'clase', 'categoria_producto'])
            if not col:
                raise KeyError("No se encontró una columna de categoría conocida. Por favor, especifica 'columna_categoria'.")

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