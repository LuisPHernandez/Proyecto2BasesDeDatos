# Proyecto 2 - Tienda: inventario y ventas

Aplicacion web para gestionar el inventario y las ventas de una tienda. El sistema incluye frontend, backend y base de datos relacional en PostgreSQL, levantados con Docker Compose.

Servidor remoto con el frontend: http://34.51.81.158/proyecto2/
Servidor remoto con el backend: http://34.51.81.158:8867/

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
DB_USER=proy3
DB_PASSWORD=secret
```

2. Levantar todos los servicios:

```bash
docker compose up --build
```

3. Abrir la aplicacion web:

```text
http://localhost:5173/proyecto2/
```

4. Servicios disponibles:

- Frontend: `http://localhost:5173/proyecto2/`
- Backend/API: `http://localhost:8867/`
- Documentacion de FastAPI: `http://localhost:8867/docs`
- PostgreSQL expuesto localmente en el puerto `5555`

Para reiniciar desde cero la base de datos con los scripts iniciales:

```bash
docker compose down -v
docker compose up --build
```

## Autenticación simulada

El proyecto incluye una autenticación simulada en el frontend para demostrar el manejo de sesión global con React Context.

Esta autenticación no valida usuarios contra la base de datos ni contra el backend. Su objetivo es mostrar el flujo de login/logout, protección de rutas y estado de sesión compartido en la aplicación.

Credenciales de acceso:

```text
Usuario: admin
Contraseña: admin123
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

## Esquema de roles

Se definen 5 roles en PostgreSQL mediante `CREATE ROLE` con permisos
granulares por tabla asignados con `GRANT` y `REVOKE`.

| Rol | Descripción |
|---|---|
| `rol_admin` | Control total sobre todas las tablas y sequences |
| `rol_gerente` | Lectura total, incluyendo `precio_compra` y reportes |
| `rol_vendedor` | Crea ventas; ve productos sin `precio_compra` |
| `rol_bodeguero` | Gestiona productos y categorías; no accede a datos financieros |
| `rol_auditor` | Solo lectura sobre todas las tablas; no puede modificar nada |

### Permisos por tabla

| Tabla | rol_admin | rol_gerente | rol_vendedor | rol_bodeguero | rol_auditor |
|---|---|---|---|---|---|
| `proveedor` | ALL | SELECT | — | SELECT | SELECT |
| `categoria` | ALL | SELECT | — | SELECT, INSERT, UPDATE | SELECT |
| `producto` | ALL | SELECT | SELECT* | SELECT, INSERT, UPDATE | SELECT |
| `empleado` | ALL | SELECT | — | — | SELECT |
| `cliente` | ALL | SELECT | SELECT | — | SELECT |
| `venta` | ALL | SELECT | SELECT, INSERT | SELECT | SELECT |
| `detalle_venta` | ALL | SELECT | SELECT, INSERT | SELECT | SELECT |
| `venta_detallada` (VIEW) | ALL | SELECT | — | — | SELECT |

> \* `rol_vendedor` tiene acceso a columna-nivel en `producto`:
> puede ver `id_producto`, `nombre`, `unidades_disponibles`,
> `precio_venta` e `id_categoria`, pero **no** `precio_compra`.