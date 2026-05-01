CREATE DATABASE proyecto2;

CREATE TABLE proveedor (
    id_proveedor INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE producto (
    id_producto INTEGER PRIMARY KEY,
    id_proveedor INTEGER NOT NULL,
    nombre TEXT NOT NULL UNIQUE,
    unidades_disponibles INTEGER NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    precio_compra DECIMAL(10,2) NOT NULL,
    id_categoria INTEGER NOT NULL,

    CONSTRAINT fk_producto_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedor(id_proveedor),
    
    CONSTRAINT fk_producto_categoria
        FOREIGN KEY (id_categoria)
        REFERENCES categoria(id_categoria)
);

CREATE TABLE categoria (
    id_categoria INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE empleado (
    id_empleado INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE cliente (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE venta (
    id_venta INTEGER PRIMARY KEY,
    id_empleado INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    fecha DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_venta_empleado
        FOREIGN KEY (id_empleado)
        REFERENCES empleado(id_empleado),

    CONSTRAINT fk_venta_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES cliente(id_cliente)
);

CREATE TABLE detalle_venta (
    id_venta INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    cantidad INTEGER NOT NULL,

    PRIMARY KEY (id_venta, id_producto),

    CONSTRAINT fk_detalle_venta_venta
        FOREIGN KEY (id_venta)
        REFERENCES venta(id_venta),

    CONSTRAINT fk_detalle_venta_producto
        FOREIGN KEY (id_producto)
        REFERENCES producto(id_producto)
);