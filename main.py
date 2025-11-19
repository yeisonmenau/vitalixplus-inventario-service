from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.inventario_controller import router as inventario_router
from controller.imagen_controller import router as imagen_router

app = FastAPI()

# Registrar rutas
app.include_router(inventario_router)
app.include_router(imagen_router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "microservicio funcionando correctamente 🎉"}


