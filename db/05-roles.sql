CREATE ROLE rol_admin;
CREATE ROLE rol_gerente;
CREATE ROLE rol_vendedor;
CREATE ROLE rol_bodeguero;
CREATE ROLE rol_auditor;

-- El usuario de conexion de la app (creado por Docker) puede asumir los roles definidos
GRANT rol_admin TO proy3;
GRANT rol_gerente TO proy3;
GRANT rol_vendedor TO proy3;
GRANT rol_bodeguero TO proy3;
GRANT rol_auditor TO proy3;

-- Quitar todos los permisos por defecto (PUBLIC = todos los roles/usuarios)
REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL PROCEDURES IN SCHEMA public FROM PUBLIC;

-- Todos los roles necesitan poder resolver objetos dentro del schema
GRANT USAGE ON SCHEMA public TO rol_admin;
GRANT USAGE ON SCHEMA public TO rol_gerente;
GRANT USAGE ON SCHEMA public TO rol_vendedor;
GRANT USAGE ON SCHEMA public TO rol_bodeguero;
GRANT USAGE ON SCHEMA public TO rol_auditor;

-- Admin tiene todos los permisos
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO rol_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO rol_admin;

-- Gerente tiene lectura amplia en tablas y vistas
GRANT SELECT ON proveedor, categoria, producto, empleado, cliente, venta, detalle_venta TO rol_gerente;
GRANT SELECT ON venta_detallada TO rol_gerente;

-- Vendedor consulta productos con sus proveedores y categorias y registra ventas/clientes
GRANT SELECT ON producto TO rol_vendedor;
GRANT UPDATE (unidades_disponibles) ON producto TO rol_vendedor;
GRANT SELECT ON proveedor TO rol_vendedor;
GRANT SELECT ON categoria TO rol_vendedor;
GRANT SELECT, INSERT ON cliente TO rol_vendedor;
GRANT SELECT, INSERT ON venta TO rol_vendedor;
GRANT SELECT, INSERT ON detalle_venta TO rol_vendedor;
GRANT SELECT ON empleado TO rol_vendedor;
GRANT SELECT ON venta_detallada TO rol_vendedor;
GRANT USAGE, SELECT ON SEQUENCE cliente_id_cliente_seq TO rol_vendedor;
GRANT USAGE, SELECT ON SEQUENCE venta_id_venta_seq TO rol_vendedor;

-- Bodeguero gestiona inventario y categorias
GRANT SELECT ON proveedor TO rol_bodeguero;
GRANT SELECT, INSERT, UPDATE ON categoria TO rol_bodeguero;
GRANT SELECT, INSERT, UPDATE ON producto TO rol_bodeguero;
GRANT SELECT ON venta, detalle_venta TO rol_bodeguero;
GRANT USAGE, SELECT ON SEQUENCE categoria_id_categoria_seq TO rol_bodeguero;
GRANT USAGE, SELECT ON SEQUENCE producto_id_producto_seq TO rol_bodeguero;

-- Auditor solo tiene lectura
GRANT SELECT ON proveedor, categoria, producto, empleado, cliente, venta, detalle_venta TO rol_auditor;
GRANT SELECT ON venta_detallada TO rol_auditor;

-- Para el login de aplicacion todos los roles pueden validar usuarios.
GRANT SELECT ON usuario_app TO rol_admin;
GRANT SELECT ON usuario_app TO rol_gerente;
GRANT SELECT ON usuario_app TO rol_vendedor;
GRANT SELECT ON usuario_app TO rol_bodeguero;
GRANT SELECT ON usuario_app TO rol_auditor;