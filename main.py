from fastapi import FastAPI
from controller.inventario_controller import router as inventario_router
from controller.imagen_controller import router as imagen_router

app = FastAPI()

# Registrar rutas
app.include_router(inventario_router)
app.include_router(imagen_router)

@app.get("/")
def root():
    return {"message": "microservicio funcionando correctamente 🎉"}


