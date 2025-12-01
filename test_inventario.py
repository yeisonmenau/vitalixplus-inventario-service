import pytest
import pandas as pd
import os
import tempfile
from service.inventario_service import InventarioService


class TestInventarioService:
    """Pruebas unitarias básicas para InventarioService."""

    @pytest.fixture
    def servicio(self):
        """Fixture: crea una instancia del servicio."""
        return InventarioService()

    def test_cargar_excel_exitoso(self, servicio):
        """Verifica que el Excel se carga correctamente."""
        assert servicio.df is not None, "DataFrame no se cargó"
        assert len(servicio.df) > 0, "DataFrame vacío"

    def test_columnas_disponibles(self, servicio):
        """Verifica que se retorna la lista de columnas."""
        columnas = servicio.columnas_disponibles()
        assert isinstance(columnas, list), "columnas_disponibles debe retornar una lista"
        assert len(columnas) > 0, "No hay columnas disponibles"

    def test_listar_todo(self, servicio):
        """Verifica que listar_todo retorna registros."""
        resultado = servicio.listar_todo()
        assert isinstance(resultado, list), "listar_todo debe retornar una lista"
        assert len(resultado) > 0, "No hay registros para listar"

    def test_buscar_por_id_existe(self, servicio):
        """Verifica búsqueda por ID (si existe al menos un registro)."""
        # Obtener el primer ID del DataFrame para probar
        if servicio.df is not None:
            col_id = servicio._buscar_columna(['codigo', 'código', 'code', 'id'])
            if col_id:
                primer_id = servicio.df[col_id].iloc[0]
                resultado = servicio.buscar_por_id(int(primer_id))
                assert isinstance(resultado, list), "buscar_por_id debe retornar una lista"
                assert len(resultado) > 0, f"No se encontró registro con ID {primer_id}"

    def test_buscar_por_nombre_existe(self, servicio):
        """Verifica búsqueda por nombre."""
        if servicio.df is not None:
            col_desc = servicio._buscar_columna(['descripcion', 'descripción', 'nombre'])
            if col_desc:
                primer_nombre = str(servicio.df[col_desc].iloc[0])[:3]  # Primeras 3 caracteres
                resultado = servicio.buscar_por_nombre(primer_nombre)
                assert isinstance(resultado, list), "buscar_por_nombre debe retornar una lista"

    def test_helper_buscar_columna(self, servicio):
        """Verifica que el helper _buscar_columna detecta columnas."""
        # Probar con candidatos comunes
        col = servicio._buscar_columna(['codigo', 'código', 'code'])
        # No falla si no la encuentra, simplemente retorna None
        assert col is None or isinstance(col, str), "_buscar_columna debe retornar str o None"

    def test_exportar_por_categoria_en_memoria(self, servicio):
        """Verifica exportación en stream (en memoria)."""
        if servicio.df is not None:
            col_cat = servicio._buscar_columna(['categoria', 'categoría', 'tipo'])
            if col_cat:
                primer_categoria = servicio.df[col_cat].iloc[0]
                try:
                    buffer = servicio.exportar_por_categoria_stream(primer_categoria)
                    contenido = buffer.getvalue()
                    assert isinstance(contenido, str), "Buffer debe contener string"
                    assert len(contenido) > 0, "CSV vacío"
                    assert "," in contenido, "CSV debe tener columnas separadas por comas"
                except KeyError:
                    # Si no encuentra columna de categoría, skip
                    pytest.skip("No hay columna de categoría detectada")

    def test_exportar_por_categoria_a_disco(self, servicio):
        """Verifica exportación con guardar a disco."""
        if servicio.df is not None:
            col_cat = servicio._buscar_columna(['categoria', 'categoría', 'tipo'])
            if col_cat:
                primer_categoria = servicio.df[col_cat].iloc[0]
                with tempfile.TemporaryDirectory() as tmpdir:
                    try:
                        ruta = servicio.exportar_por_categoria(
                            primer_categoria,
                            output_dir=tmpdir
                        )
                        assert os.path.exists(ruta), f"Archivo CSV no fue creado en {ruta}"
                        assert ruta.endswith('.csv'), "Archivo debe tener extensión .csv"
                    except KeyError:
                        pytest.skip("No hay columna de categoría detectada")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
