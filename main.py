from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.inventario_controller import router as inventario_router
from controller.imagen_controller import router as imagen_router

app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://192.168.80.10:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Registrar rutas
app.include_router(inventario_router)
app.include_router(imagen_router)

@app.get("/")
def root():
    return {"message": "microservicio funcionando correctamente 🎉"}


