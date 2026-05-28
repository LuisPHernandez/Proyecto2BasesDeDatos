CREATE OR REPLACE FUNCTION sp_crear_venta(
    p_id_cliente INT,
    p_id_empleado INT,
    p_fecha TIMESTAMP,
    p_total NUMERIC,
    OUT p_id_venta_creada INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO venta (
        id_cliente,
        id_empleado,
        fecha,
        total
    )
    VALUES (
        p_id_cliente,
        p_id_empleado,
        p_fecha,
        p_total
    )
    RETURNING id_venta INTO p_id_venta_creada;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al crear venta: %', SQLERRM;
END;
$$;


CREATE OR REPLACE PROCEDURE sp_insertar_detalle_venta(
    p_id_venta INT,
    p_id_producto INT,
    p_cantidad INT,
    p_precio_unitario NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_stock_actual INT;
BEGIN
    SELECT unidades_disponibles
    INTO v_stock_actual
    FROM producto
    WHERE id_producto = p_id_producto
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Producto no encontrado';
    END IF;

    IF p_cantidad <= 0 THEN
        RAISE EXCEPTION 'La cantidad debe ser mayor a 0';
    END IF;

    IF v_stock_actual < p_cantidad THEN
        RAISE EXCEPTION 'Stock insuficiente para producto %', p_id_producto;
    END IF;

    INSERT INTO detalle_venta (
        id_venta,
        id_producto,
        precio_unitario,
        cantidad
    )
    VALUES (
        p_id_venta,
        p_id_producto,
        p_precio_unitario,
        p_cantidad
    );

    UPDATE producto
    SET unidades_disponibles = unidades_disponibles - p_cantidad
    WHERE id_producto = p_id_producto;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al insertar detalle de venta: %', SQLERRM;
END;
$$;


CREATE OR REPLACE FUNCTION sp_crear_producto(
    p_id_proveedor INT,
    p_nombre TEXT,
    p_unidades_disponibles INT,
    p_precio_venta NUMERIC,
    p_precio_compra NUMERIC,
    p_id_categoria INT,
    OUT p_id_producto_creado INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_unidades_disponibles < 0 THEN
        RAISE EXCEPTION 'El stock no puede ser negativo';
    END IF;

    INSERT INTO producto (
        id_proveedor,
        nombre,
        unidades_disponibles,
        precio_venta,
        precio_compra,
        id_categoria
    )
    VALUES (
        p_id_proveedor,
        p_nombre,
        p_unidades_disponibles,
        p_precio_venta,
        p_precio_compra,
        p_id_categoria
    )
    RETURNING id_producto INTO p_id_producto_creado;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al crear producto: %', SQLERRM;
END;
$$;


CREATE OR REPLACE PROCEDURE sp_actualizar_stock(
    p_id_producto INT,
    p_nuevas_unidades INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_nuevas_unidades < 0 THEN
        RAISE EXCEPTION 'El stock no puede ser negativo';
    END IF;

    UPDATE producto
    SET unidades_disponibles = p_nuevas_unidades
    WHERE id_producto = p_id_producto;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Producto no encontrado';
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE sp_eliminar_venta(
    p_id_venta INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM venta
    WHERE id_venta = p_id_venta;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Venta no encontrada';
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al eliminar venta: %', SQLERRM;
END;
$$;