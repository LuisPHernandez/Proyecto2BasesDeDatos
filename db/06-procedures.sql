CREATE OR REPLACE PROCEDURE registrar_venta(
    IN p_id_empleado INT,
    IN p_id_cliente INT,
    IN p_id_producto INT,
    IN p_cantidad INT,
    OUT p_id_venta INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_stock INT;
    v_precio DECIMAL(10,2);
BEGIN
    SELECT unidades_disponibles, precio_venta
    INTO v_stock, v_precio
    FROM producto
    WHERE id_producto = p_id_producto;

    IF v_stock IS NULL THEN
        RAISE EXCEPTION 'Producto no existe';
    END IF;

    IF v_stock < p_cantidad THEN
        RAISE EXCEPTION 'Stock insuficiente';
    END IF;

    INSERT INTO venta(id_empleado, id_cliente, fecha, total)
    VALUES (p_id_empleado, p_id_cliente, NOW(), v_precio * p_cantidad)
    RETURNING id_venta INTO p_id_venta;

    INSERT INTO detalle_venta(id_venta, id_producto, precio_unitario, cantidad)
    VALUES (p_id_venta, p_id_producto, v_precio, p_cantidad);

    UPDATE producto
    SET unidades_disponibles = unidades_disponibles - p_cantidad
    WHERE id_producto = p_id_producto;

EXCEPTION
    WHEN OTHERS THEN
        RAISE;
END;
$$;