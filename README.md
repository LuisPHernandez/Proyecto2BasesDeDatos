# Proyecto 3 - Tienda: inventario, ventas y seguridad en base de datos

Aplicacion web para gestionar el inventario y las ventas de una tienda. El sistema incluye frontend, backend, base de datos PostgreSQL, autenticacion con sesiones, roles del DBMS, stored procedures y ORM.

## Tecnologias

- Frontend: React, TypeScript y Vite.
- Backend: FastAPI y SQLAlchemy ORM.
- Base de datos: PostgreSQL 16.
- Infraestructura: Docker Compose.

## Como levantar el proyecto desde cero

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

Servicios disponibles:

- Frontend: `http://localhost:5173/proyecto2/`
- Backend/API: `http://localhost:8867/`
- Documentacion de FastAPI: `http://localhost:8867/docs`
- PostgreSQL local: puerto `5555`

Para reiniciar la base de datos desde cero y volver a ejecutar los scripts iniciales:

```bash
docker compose down -v
docker compose up --build
```

## Credenciales de prueba

La autenticacion se realiza contra la tabla `usuario_app` en PostgreSQL. Cada usuario tiene un rol de aplicacion que corresponde a un rol definido en el DBMS.

| Usuario | Contrasena | Rol |
|---|---|---|
| `admin` | `admin123` | `rol_admin` |
| `gerente` | `gerente123` | `rol_gerente` |
| `vendedor` | `vendedor123` | `rol_vendedor` |
| `bodeguero` | `bodeguero123` | `rol_bodeguero` |
| `auditor` | `auditor123` | `rol_auditor` |

Al iniciar sesion, el backend genera un token de sesion. Las requests protegidas envian ese token al backend y el backend determina el rol real del usuario. El frontend no decide el rol de base de datos.

## Seguridad y roles del DBMS

Se definen exactamente 5 roles en PostgreSQL mediante `CREATE ROLE`. El usuario de conexion `proy3` puede asumir esos roles con `SET ROLE`, y el backend selecciona el rol segun la sesion autenticada.

| Rol | Responsabilidad |
|---|---|
| `rol_admin` | Administracion general del sistema. |
| `rol_gerente` | Consulta amplia de datos, ventas y reportes. |
| `rol_vendedor` | Registro de clientes, ventas y detalles de venta. |
| `rol_bodeguero` | Gestion de productos, categorias e inventario. |
| `rol_auditor` | Consulta de informacion sin modificaciones. |

### Permisos por tabla o vista

| Objeto | rol_admin | rol_gerente | rol_vendedor | rol_bodeguero | rol_auditor |
|---|---|---|---|---|---|
| `proveedor` | ALL | SELECT | - | SELECT | SELECT |
| `categoria` | ALL | SELECT | - | SELECT, INSERT, UPDATE | SELECT |
| `producto` | ALL | SELECT | SELECT, UPDATE `unidades_disponibles` | SELECT, INSERT, UPDATE | SELECT |
| `empleado` | ALL | SELECT | SELECT | - | SELECT |
| `cliente` | ALL | SELECT | SELECT, INSERT | - | SELECT |
| `venta` | ALL | SELECT | SELECT, INSERT | SELECT | SELECT |
| `detalle_venta` | ALL | SELECT | SELECT, INSERT | SELECT | SELECT |
| `venta_detallada` | ALL | SELECT | SELECT | - | SELECT |
| `usuario_app` | SELECT | SELECT | SELECT | SELECT | SELECT |

`rol_vendedor` tiene permiso de lectura sobre `producto`, incluyendo `precio_compra`, segun la configuracion actual del proyecto.

## Proteccion de rutas y vistas

El frontend protege rutas segun el rol del usuario autenticado. Los enlaces visibles en la barra de navegacion tambien se filtran por rol.

| Vista | Roles permitidos |
|---|---|
| Home | Todos los roles |
| Inventario | Todos los roles |
| Proveedores | `rol_admin`, `rol_gerente`, `rol_bodeguero`, `rol_auditor` |
| Categorias | `rol_admin`, `rol_gerente`, `rol_bodeguero`, `rol_auditor` |
| Ventas | `rol_admin`, `rol_gerente`, `rol_vendedor`, `rol_auditor` |
| Clientes | `rol_admin`, `rol_gerente`, `rol_vendedor`, `rol_auditor` |
| Empleados | `rol_admin`, `rol_gerente`, `rol_auditor` |

## Stored procedures

Las operaciones criticas se implementan como stored procedures en PostgreSQL y se invocan desde el backend.

| Stored procedure | Uso | Roles con EXECUTE |
|---|---|---|
| `sp_crear_venta` | Crea el encabezado de una venta. | `rol_admin`, `rol_vendedor` |
| `sp_insertar_detalle_venta` | Inserta detalle de venta y descuenta stock. | `rol_admin`, `rol_vendedor` |
| `sp_crear_producto` | Crea un producto. | `rol_admin`, `rol_bodeguero` |
| `sp_actualizar_stock` | Actualiza unidades disponibles de un producto. | `rol_admin`, `rol_bodeguero` |
| `sp_eliminar_venta` | Elimina una venta. | `rol_admin` |

`sp_crear_venta` y `sp_crear_producto` usan parametros de salida (`OUT`) para devolver el identificador creado. Los procedures manejan errores con validaciones y excepciones donde corresponde.

`sp_eliminar_venta` incluye control transaccional explicito con `COMMIT` y `ROLLBACK`. Debido a que PostgreSQL solo permite terminar transacciones dentro de un procedure cuando se llama fuera de una transaccion activa, el backend lo ejecuta con una conexion dedicada en modo `AUTOCOMMIT`.

## ORM

El backend usa SQLAlchemy ORM para modelos y operaciones CRUD. Las consultas avanzadas, vistas, reportes y llamadas a stored procedures usan SQL explicito cuando corresponde.

Ejemplos de uso de ORM:

- CRUD de clientes.
- CRUD de categorias.
- CRUD de empleados.
- CRUD de proveedores.
- Consultas de productos y ventas con modelos relacionados.

## Estructura del proyecto

```text
.
+-- backend/
|   +-- main.py
|   +-- database.py
|   +-- models.py
|   +-- routers/
|   +-- services/
|   +-- repositories/
+-- db/
|   +-- 01-ddl.sql
|   +-- 02-indexes.sql
|   +-- 03-views.sql
|   +-- 04-data.sql
|   +-- 05-roles.sql
|   +-- 06-stored-procedures.sql
+-- frontend/
|   +-- src/
|   |   +-- api/
|   |   +-- auth/
|   |   +-- components/
|   |   +-- context/
|   |   +-- pages/
|   +-- vite.config.ts
+-- docker-compose.yml
+-- .env.example
+-- README.md
```

## Dominio del sistema

La tienda maneja productos agrupados en categorias. Los productos son comprados a proveedores. Los clientes realizan compras atendidas por empleados. Cada venta puede incluir varios productos, por lo que se registra una tabla de detalle de venta con cantidad y precio unitario. El sistema controla stock disponible, registra ventas y permite consultar reportes segun los permisos del usuario autenticado.
