CREATE VIEW venta_detallada AS
SELECT 
    v.id_venta,
    v.fecha,
    v.total,
    e.nombre AS nombre_empleado,
    c.email AS email_cliente,
    c.nombre AS nombre_cliente
FROM venta v
JOIN empleado e ON v.id_empleado = e.id_empleado
JOIN cliente c ON v.id_cliente = c.id_cliente;