from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import productos, ventas, proveedores, categorias, empleados, clientes

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
app.include_router(categorias.router, prefix="/api/categorias", tags=["categorias"])
app.include_router(empleados.router, prefix="/api/empleados", tags=["empleados"])
app.include_router(clientes.router, prefix="/api/clientes", tags=["clientes"])
