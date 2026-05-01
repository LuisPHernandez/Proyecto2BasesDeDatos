-- Reportes por fecha
CREATE INDEX idx_venta_fecha
ON venta(fecha);

-- Análisis de productos más vendidos
CREATE INDEX idx_detalle_venta_producto
ON detalle_venta(id_producto);