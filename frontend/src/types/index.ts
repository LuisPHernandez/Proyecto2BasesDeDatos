export interface ProductoBase {
    id_proveedor: number
    nombre: string
    unidades_disponibles: number
    precio_venta: number
    precio_compra: number
    id_categoria: number
}

export interface Producto extends ProductoBase {
    id_producto: number
}

export interface ProductoDetailed extends Producto {
    proveedor: string
    categoria: string
}
