from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import productos, ventas, proveedores

# Inicialización de la aplicación FastAPI
app = FastAPI(title="Tienda API")

# Configuración de CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers
app.include_router(productos.router, prefix="/api/productos", tags=["productos"])
app.include_router(proveedores.router, prefix="/api/proveedores", tags=["proveedores"])
app.include_router(ventas.router,    prefix="/api/ventas",    tags=["ventas"])
