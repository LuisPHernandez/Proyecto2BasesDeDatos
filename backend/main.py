from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import productos, clientes, empleados, ventas, reportes

app = FastAPI(title="Tienda API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(productos.router, prefix="/api/productos", tags=["productos"])
app.include_router(clientes.router,  prefix="/api/clientes",  tags=["clientes"])
app.include_router(empleados.router, prefix="/api/empleados", tags=["empleados"])
app.include_router(ventas.router,    prefix="/api/ventas",    tags=["ventas"])
app.include_router(reportes.router,  prefix="/api/reportes",  tags=["reportes"])