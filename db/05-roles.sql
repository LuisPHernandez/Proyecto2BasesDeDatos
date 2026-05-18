CREATE ROLE rol_admin;
CREATE ROLE rol_gerente;
CREATE ROLE rol_vendedor;
CREATE ROLE rol_bodeguero;
CREATE ROLE rol_auditor;

REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;

-- Permisos del admin
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO rol_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO rol_admin;

-- Permisos del gerente
GRANT SELECT ON proveedor, categoria, producto, empleado, cliente, venta, detalle_venta TO rol_gerente;

-- Permisos del vendedor
GRANT SELECT (id_producto, nombre, unidades_disponibles, precio_venta, id_categoria) ON producto TO rol_vendedor;
GRANT SELECT, INSERT ON cliente, venta, detalle_venta TO rol_vendedor;
GRANT USAGE ON SEQUENCE cliente_id_cliente_seq TO rol_vendedor;
GRANT USAGE ON SEQUENCE venta_id_venta_seq TO rol_vendedor;
GRANT USAGE ON SEQUENCE detalle_venta_id_detalle_venta_seq TO rol_vendedor;

-- Permisos del bodeguero
GRANT SELECT, INSERT, UPDATE ON producto, categoria TO rol_bodeguero;
GRANT SELECT ON proveedor, venta, detalle_venta TO rol_bodeguero;
GRANT USAGE ON SEQUENCE producto_id_producto_seq TO rol_bodeguero;
GRANT USAGE ON SEQUENCE categoria_id_categoria_seq TO rol_bodeguero;

-- Permisos del auditor
GRANT SELECT ON proveedor, categoria, producto, empleado, cliente, venta, detalle_venta TO rol_auditor;
GRANT SELECT ON venta_detallada TO rol_auditor;