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

### Buscar por categoría
```
GET /inventario/categoria/{categoria}
```
Busca productos que pertenezcan a una categoría específica.

**Parámetros:**
- `categoria` (string): Nombre de la categoría (insensible a mayúsculas/minúsculas)

**Ejemplo:**
```
GET /inventario/categoria/suplementos
```

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
