// ---------------------------- Productos ---------------------------- 
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

export interface ProductoTop {
    id_producto: number
    nombre: string
    unidades_vendidas: number
    ingresos: number
}

// ---------------------------- Ventas ---------------------------- 
export interface VentaBase {
    id_cliente: number
    id_empleado: number
    fecha: Date
    total: number
}

export interface Venta extends VentaBase {
    id_venta: number
}

export interface VentaSummary {
    id_venta: number
    nombre_empleado: string
    email_cliente: string
    nombre_cliente: string
    fecha: Date
    total: number
}

export interface VentaProducto {
    id_producto: number
    nombre_producto: string
    precio_unitario: number
    cantidad: number
}

export interface DetalleVentaInput {
    id_producto: number
    cantidad: number
    precio_unitario: number
}

export interface VentaCreateInput {
    id_cliente: number
    id_empleado: number
    fecha: string
    productos: DetalleVentaInput[]
}

// ---------------------------- Proveedores ----------------------------

export interface ProveedorBase {
    nombre: string
    email: string
}

export interface Proveedor extends ProveedorBase {
    id_proveedor: number
}

// ---------------------------- Clientes ----------------------------

export interface ClienteBase {
    nombre: string
    email: string
}

export interface Cliente extends ClienteBase {
    id_cliente: number
}

// ---------------------------- Empleados ----------------------------

export interface EmpleadoBase {
    nombre: string
}

export interface Empleado extends EmpleadoBase {
    id_empleado: number
}

export interface EmpleadoSales extends Empleado {
    ventas: number
    ingresos: number
}

// ---------------------------- Categorias ----------------------------

export interface CategoriaBase {
    nombre: string
}

export interface Categoria extends CategoriaBase {
    id_categoria: number
}

export interface CategoriaIncome extends Categoria {
    ingresos: number
}