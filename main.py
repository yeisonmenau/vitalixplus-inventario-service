from fastapi import FastAPI
from controller.inventario_controller import router as inventario_router

app = FastAPI()

# Registrar rutas
app.include_router(inventario_router)

@app.get("/")
def root():
    return {"message": "microservicio funcionando correctamente 🎉"}