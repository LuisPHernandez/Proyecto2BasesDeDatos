# Proyecto 2 - Tienda: inventario y ventas

Aplicacion web para gestionar el inventario y las ventas de una tienda. El sistema incluye frontend, backend y base de datos relacional en PostgreSQL, levantados con Docker Compose.

## Tecnologias

- Frontend: React, TypeScript y Vite.
- Backend: FastAPI y psycopg2.
- Base de datos: PostgreSQL 16.
- Infraestructura: Docker Compose.

## Como levantar el proyecto

1. Crear el archivo `.env` en la raiz del proyecto usando `.env.example` como base:

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=tienda
DB_USER=proy2
DB_PASSWORD=secret
```

2. Levantar todos los servicios:

```bash
docker compose up --build
```

3. Abrir la aplicacion web:

```text
http://localhost:5173
```

4. Servicios disponibles:

- Frontend: `http://localhost:5173`
- Backend/API: `http://localhost:8000`
- Documentacion de FastAPI: `http://localhost:8000/docs`
- PostgreSQL expuesto localmente en el puerto `5555`

Para reiniciar desde cero la base de datos con los scripts iniciales:

```bash
docker compose down -v
docker compose up --build
```

## Estructura del proyecto

```text
.
+-- backend/
|   +-- main.py
|   +-- database.py
|   +-- routers/
|   +-- services/
|   +-- repositories/
+-- db/
|   +-- 01-ddl.sql
|   +-- 02-indexes.sql
|   +-- 03-views.sql
|   +-- 04-data.sql
+-- frontend/
|   +-- src/
|   |   +-- api/
|   |   +-- components/
|   |   +-- pages/
|   +-- vite.config.ts
+-- docker-compose.yml
+-- .env.example
+-- README.md
```

## Dominio del sistema

La tienda maneja productos agrupados en categorias. Los productos son comprados a proveedores. Los clientes realizan compras atendidas por empleados. Cada venta puede incluir varios productos, por lo que se registra una tabla de detalle de venta con cantidad y precio unitario.

## Funcionalidades implementadas

### Inventario

- Lista productos con proveedor y categoria.
- Permite crear, editar y eliminar productos.
- Permite elegir proveedor y categoria existentes al crear productos.
- Muestra productos con stock bajo.
- Muestra top 5 productos mas vendidos del mes.

Archivos principales:

- UI: `frontend/src/pages/Inventario/Inventario.tsx`
- Modal de creacion: `frontend/src/components/Modal/CrearProductoModal.tsx`
- API frontend: `frontend/src/api/productos.tsx`
- Backend: `backend/routers/productos.py`, `backend/services/productos.py`, `backend/repositories/productos.py`

### Ventas

- Lista ventas por rango de fechas.
- Permite crear ventas con varios productos.
- Calcula total y descuenta stock dentro de una transaccion explicita.
- Permite ver el detalle de productos vendidos.
- Permite eliminar ventas.

Archivos principales:

- UI: `frontend/src/pages/Ventas/Ventas.tsx`, `frontend/src/pages/VentaDetalle/VentaDetalle.tsx`
- Modal de creacion: `frontend/src/components/CrearVentaModal/CrearVentaModal.tsx`
- API frontend: `frontend/src/api/ventas.tsx`
- Backend: `backend/routers/ventas.py`, `backend/services/ventas.py`, `backend/repositories/ventas.py`

### Empleados

- Lista empleados con total de ventas e ingresos generados.
- Permite crear, editar y eliminar empleados.
- Exporta el reporte de empleados a CSV desde la UI.

Archivos principales:

- UI y exportacion CSV: `frontend/src/pages/Empleados/Empleados.tsx`
- API frontend: `frontend/src/api/empleados.tsx`
- Backend: `backend/routers/empleados.py`, `backend/services/empleados.py`, `backend/repositories/empleados.py`

### Clientes, proveedores y categorias

- CRUD de clientes.
- CRUD de proveedores.
- CRUD de categorias.
- Reporte de categorias por ingresos.
- Indicador de clientes activos.

Archivos principales:

- Clientes: `frontend/src/pages/Clientes/Clientes.tsx`, `backend/repositories/clientes.py`
- Proveedores: `frontend/src/pages/Proveedores/Proveedores.tsx`, `backend/repositories/proveedores.py`
- Categorias: `frontend/src/pages/Categorias/Categorias.tsx`, `backend/repositories/categorias.py`

## Consultas SQL destacadas

Las consultas se ejecutan desde la aplicacion web mediante endpoints del backend. No se usa ORM; el SQL esta escrito explicitamente en `backend/repositories/`.

### JOIN entre multiples tablas visibles en UI

1. Inventario con producto, proveedor y categoria:
   - Archivo: `backend/repositories/productos.py`
   - Pantalla: `frontend/src/pages/Inventario/Inventario.tsx`

2. Ventas con empleado y cliente:
   - Archivo: `backend/repositories/ventas.py`
   - Pantallas: `frontend/src/pages/Ventas/Ventas.tsx` y `frontend/src/pages/VentaDetalle/VentaDetalle.tsx`

3. Categorias con productos y detalle de venta:
   - Archivo: `backend/repositories/categorias.py`
   - Pantalla: `frontend/src/pages/Categorias/Categorias.tsx`

### Subqueries visibles en UI

1. Productos con stock bajo vendidos al menos una vez:
   - Archivo: `backend/repositories/productos.py`
   - Consulta usa `IN (SELECT ...)`
   - Pantalla: `frontend/src/pages/Inventario/Inventario.tsx`

2. Clientes activos durante el ultimo mes:
   - Archivo: `backend/repositories/clientes.py`
   - Consulta usa `IN (SELECT DISTINCT ...)`
   - Pantalla: `frontend/src/pages/Clientes/Clientes.tsx`

### GROUP BY, HAVING y agregaciones visibles en UI

1. Empleados con ventas e ingresos:
   - Archivo: `backend/repositories/empleados.py`
   - Usa `COUNT`, `SUM`, `GROUP BY` y `HAVING`
   - Pantalla: `frontend/src/pages/Empleados/Empleados.tsx`

2. Categorias con ingresos:
   - Archivo: `backend/repositories/categorias.py`
   - Usa `SUM`, `GROUP BY` y `HAVING`
   - Pantalla: `frontend/src/pages/Categorias/Categorias.tsx`

### CTE visible en UI

- Top 5 productos mas vendidos del mes:
  - Archivo: `backend/repositories/productos.py`
  - Usa `WITH ventas_mes AS (...)`
  - Pantalla: `frontend/src/pages/Inventario/Inventario.tsx`

### VIEW usada por backend para alimentar la UI

- View: `venta_detallada`
- Definicion: `db/03-views.sql`
- Uso: `backend/repositories/ventas.py`
- Pantalla: `frontend/src/pages/Ventas/Ventas.tsx`

### Transaccion explicita con ROLLBACK

- Creacion de ventas:
  - Archivo: `backend/repositories/ventas.py`
  - Usa `BEGIN`, `COMMIT` y `ROLLBACK`
  - Inserta la venta, inserta sus detalles, descuenta stock y revierte si ocurre un error o si el stock queda negativo.

## Notas de datos iniciales

Los datos de prueba estan en `db/04-data.sql`. El script inserta datos para proveedores, categorias, productos, empleados, clientes, ventas y detalles de venta, y luego ajusta el inventario con base en las unidades vendidas.