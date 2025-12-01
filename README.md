# Microservicio de Inventario Vitalix Plus

API REST desarrollada con FastAPI para la gestión y consulta de inventario a partir de archivos Excel.

## 📋 Descripción

Este microservicio permite consultar el inventario de productos Vitalix Plus mediante endpoints REST. Los datos se cargan desde un archivo Excel y se exponen a través de una API simple y eficiente.

## 🚀 Características

- Consulta completa del inventario
- Búsqueda de productos por código
- Búsqueda de productos por nombre (coincidencia parcial)
- Carga automática de datos desde Excel
- API documentada automáticamente con Swagger

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno para Python
- **Pandas**: Procesamiento y análisis de datos
- **Python 3.x**: Lenguaje de programación

## 📦 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/yeisonmenau/vitalixplus-inventario-service.git
cd vitalixplus-inventario-service
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r dependencias.txt
```

4. Asegurarse de que el archivo Excel esté en la ruta correcta:
```
files/data/inventario_vitalix_plus.xlsx
```

## ▶️ Ejecución

Iniciar el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

## 📚 Documentación de la API

Una vez iniciado el servidor, acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints

### Raíz
```
GET /
```
Verifica que el microservicio esté funcionando.

**Respuesta:**
```json
{
  "message": "microservicio funcionando correctamente 🎉"
}
```

### Listar todo el inventario
```
GET /inventario/
```
Retorna todos los productos del inventario.

### Buscar por código
```
GET /inventario/codigo/{item_id}
```
Busca un producto específico por su código.

**Parámetros:**
- `item_id` (int): Código del producto

**Ejemplo:**
```
GET /inventario/codigo/101
```

### Buscar por nombre
```
GET /inventario/nombre/{nombre}
```
Busca productos cuya descripción contenga el texto especificado (búsqueda insensible a mayúsculas).

**Parámetros:**
- `nombre` (string): Texto a buscar en la descripción

**Ejemplo:**
```
GET /inventario/nombre/vitamina
```

### Exportar por categoría (con almacenamiento en disco)
```
GET /inventario/exportar/categoria/{valor}
```
Exporta los registros de una categoría a un archivo CSV (se guarda en `files/exports/` y se devuelve como descarga).

**Parámetros:**
- `valor` (ruta): valor de la categoría a filtrar.
- `columna` (query, opcional): nombre de la columna de categoría. Si no se proporciona, el sistema intenta detectarla automáticamente entre: `categoría`, `categoria`, `category`, `tipo`, `clase`, `categoria_producto`.

**Ejemplos:**
```
GET /inventario/exportar/categoria/vitaminas
GET /inventario/exportar/categoria/bebidas?columna=tipo
```

**Respuesta:**
- Archivo CSV descargable (Content-Type: `text/csv`).
- También se guarda en `files/exports/export_categoria_{columna}_{valor}.csv`.

### Exportar por categoría (en memoria, sin disco)
```
GET /inventario/exportar/categoria/{valor}/stream
```
Exporta los registros de una categoría directamente como stream (en memoria, sin escribir en disco).

**Parámetros:**
- `valor` (ruta): valor de la categoría a filtrar.
- `columna` (query, opcional): nombre de la columna de categoría.

**Ejemplos:**
```
GET /inventario/exportar/categoria/vitaminas/stream
GET /inventario/exportar/categoria/bebidas/stream?columna=tipo
```

**Respuesta:**
- Archivo CSV descargable (Content-Type: `text/csv`).
- NO se guarda en servidor (más eficiente para archivos grandes).

---

## 🧪 Pruebas

Ejecutar tests unitarios:
```bash
pip install pytest
pytest test_inventario.py -v
```

Tests incluidos:
- Carga de archivo Excel
- Listado de columnas
- Búsqueda por ID
- Búsqueda por nombre
- Helper de detección de columnas
- Exportación en stream
- Exportación a disco

---

## 🛠️ Características principales

- ✅ **Detección inteligente de columnas**: Detecta automáticamente nombres de columnas con/sin acentos, espacios, variantes (`código` / `codigo`, etc.).
- ✅ **Búsquedas tolerantes**: Soporta búsqueda case-insensitive por nombre e ID.
- ✅ **Exportación flexible**: Dos opciones de exportación — en disco (guarda archivo) o por stream (descarga directa en memoria).
- ✅ **Logging automático**: Registra cargas de archivos, exportaciones y errores.
- ✅ **Manejo de errores robusto**: HTTPException con status codes apropiados (400 para entrada inválida, 500 para errores del servidor).
- ✅ **Documentación automática**: Swagger disponible en `/docs` y ReDoc en `/redoc`.

---

## 📝 Ejemplo de uso completo (Python + requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Listar todo
response = requests.get(f"{BASE_URL}/inventario/")
todos = response.json()
print(f"Total productos: {len(todos)}")

# 2. Buscar por código
response = requests.get(f"{BASE_URL}/inventario/codigo/101")
producto = response.json()
print(f"Producto: {producto}")

# 3. Buscar por nombre
response = requests.get(f"{BASE_URL}/inventario/nombre/vitamina")
resultados = response.json()
print(f"Encontrados: {len(resultados)} productos con 'vitamina'")

# 4. Exportar por categoría (a disco)
response = requests.get(f"{BASE_URL}/inventario/exportar/categoria/bebidas")
with open("bebidas.csv", "wb") as f:
    f.write(response.content)
print("CSV descargado: bebidas.csv")

# 5. Exportar por categoría (stream, sin disco)
response = requests.get(f"{BASE_URL}/inventario/exportar/categoria/vitaminas/stream")
with open("vitaminas.csv", "wb") as f:
    f.write(response.content)
print("CSV descargado (stream): vitaminas.csv")
```

---

## 🔄 Flujo de trabajo (Git)

Rama actual: `feature/ExportCSV`

Cambios implementados:
1. Método `exportar_por_categoria` — exportación a disco con detección automática de categoría.
2. Endpoint `GET /inventario/exportar/categoria/{valor}` — descarga CSV desde disco.
3. Helper `_buscar_columna` — detección robusta de nombres de columnas.
4. Actualización de `buscar_por_id` / `buscar_por_nombre` — búsquedas tolerantes.
5. Método `exportar_por_categoria_stream` — exportación en memoria.
6. Endpoint `GET /inventario/exportar/categoria/{valor}/stream` — descarga CSV desde stream.
7. Tests unitarios (`test_inventario.py`) — validación de funcionalidad.
8. Logging mejorado — registro de operaciones y errores.

## 📁 Estructura del Proyecto

```
.
├── main.py                          # Punto de entrada de la aplicación
├── controller/
│   └── inventario_controller.py     # Controlador con rutas REST
├── service/
│   └── inventario_service.py        # Lógica de negocio y acceso a datos
├── files/
│   └── data/
│       └── inventario_vitalix_plus.xlsx  # Archivo de datos
├── .gitignore                       # Archivos ignorados por Git
└── README.md                        # Este archivo
