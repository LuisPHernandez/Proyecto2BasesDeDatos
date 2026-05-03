import { useEffect, useState } from 'react'
import { getClientes } from '../../api/clientes'
import { getEmpleados } from '../../api/empleados'
import { getProductos } from '../../api/productos'
import type { Cliente, DetalleVentaInput, Empleado, ProductoDetailed, VentaCreateInput, VentaSummary } from '../../types'
import Modal from '../Modal/Modal'
import styles from './CrearVentaModal.module.css'

interface ItemForm extends DetalleVentaInput {
    nombre_producto: string
}

interface Props {
    onClose: () => void
    onCrear: (data: VentaCreateInput) => Promise<VentaSummary>
}

function CrearVentaModal({ onClose, onCrear }: Props) {
    const [clientes, setClientes] = useState<Cliente[]>([])
    const [empleados, setEmpleados] = useState<Empleado[]>([])
    const [productos, setProductos] = useState<ProductoDetailed[]>([])
    const [loadingData, setLoadingData] = useState(true)

    const [idCliente, setIdCliente] = useState<number | ''>('')
    const [idEmpleado, setIdEmpleado] = useState<number | ''>('')
    const [fecha, setFecha] = useState<string>(() => {
        const now = new Date()
        return new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 16)
    })

    const [idProductoSel, setIdProductoSel] = useState<number | ''>('')
    const [cantidadSel, setCantidadSel] = useState<number>(1)

    const [items, setItems] = useState<ItemForm[]>([])
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        const load = async () => {
            try {
                const [c, e, p] = await Promise.all([getClientes(), getEmpleados(), getProductos()])
                setClientes(c)
                setEmpleados(e)
                setProductos(p)
            } finally {
                setLoadingData(false)
            }
        }
        load()
    }, [])

    const productoSeleccionado = productos.find(p => p.id_producto === idProductoSel)

    const handleAgregarProducto = () => {
        if (!productoSeleccionado || cantidadSel <= 0) return

        const existe = items.find(i => i.id_producto === productoSeleccionado.id_producto)
        if (existe) {
            setItems(prev => prev.map(i =>
                i.id_producto === productoSeleccionado.id_producto
                    ? { ...i, cantidad: i.cantidad + cantidadSel }
                    : i
            ))
        } else {
            setItems(prev => [...prev, {
                id_producto: productoSeleccionado.id_producto,
                nombre_producto: productoSeleccionado.nombre,
                precio_unitario: productoSeleccionado.precio_venta,
                cantidad: cantidadSel
            }])
        }

        setIdProductoSel('')
        setCantidadSel(1)
    }

    const handleRemoverItem = (id_producto: number) => {
        setItems(prev => prev.filter(i => i.id_producto !== id_producto))
    }

    const total = items.reduce((acc, i) => acc + i.precio_unitario * i.cantidad, 0)

    const handleSubmit = async () => {
        if (idCliente === '' || idEmpleado === '') {
            setError('Selecciona cliente y empleado')
            return
        }
        if (items.length === 0) {
            setError('Agrega al menos un producto')
            return
        }
        setLoading(true)
        setError(null)
        try {
            await onCrear({
                id_cliente: idCliente,
                id_empleado: idEmpleado,
                fecha: new Date(fecha).toISOString(),
                productos: items.map(({ id_producto, cantidad, precio_unitario }) => ({
                    id_producto, cantidad, precio_unitario
                }))
            })
            onClose()
        } catch (e: any) {
            setError(e.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <Modal titulo="Nueva venta" onClose={onClose}>
            {loadingData ? (
                <p>Cargando datos...</p>
            ) : (
                <div className={styles.body}>
                    <div className={styles.section}>
                        <p className={styles.sectionTitle}>Información general</p>
                        <div className={styles.grid2}>
                            <div className={styles.field}>
                                <label>Cliente</label>
                                <select
                                    value={idCliente}
                                    onChange={e => setIdCliente(+e.target.value)}
                                >
                                    <option value="">Seleccionar...</option>
                                    {clientes.map(c => (
                                        <option key={c.id_cliente} value={c.id_cliente}>
                                            {c.nombre}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div className={styles.field}>
                                <label>Empleado</label>
                                <select
                                    value={idEmpleado}
                                    onChange={e => setIdEmpleado(+e.target.value)}
                                >
                                    <option value="">Seleccionar...</option>
                                    {empleados.map(e => (
                                        <option key={e.id_empleado} value={e.id_empleado}>
                                            {e.nombre}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>
                        <div className={styles.field}>
                            <label>Fecha y hora</label>
                            <input
                                type="datetime-local"
                                value={fecha}
                                onChange={e => setFecha(e.target.value)}
                            />
                        </div>
                    </div>

                    <hr className={styles.divider} />

                    <div className={styles.section}>
                        <p className={styles.sectionTitle}>Productos</p>
                        <div className={styles.addProductRow}>
                            <div className={styles.field}>
                                <label>Producto</label>
                                <select
                                    value={idProductoSel}
                                    onChange={e => setIdProductoSel(+e.target.value)}
                                >
                                    <option value="">Seleccionar...</option>
                                    {productos.map(p => (
                                        <option key={p.id_producto} value={p.id_producto}>
                                            {p.nombre} — Q{p.precio_venta.toFixed(2)}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div className={styles.field}>
                                <label>Cantidad</label>
                                <input
                                    type="number"
                                    min={1}
                                    value={cantidadSel}
                                    onChange={e => setCantidadSel(+e.target.value)}
                                />
                            </div>
                            <button
                                className={styles.addBtn}
                                onClick={handleAgregarProducto}
                                disabled={idProductoSel === '' || cantidadSel <= 0}
                            >
                                + Agregar
                            </button>
                        </div>

                        {items.length > 0 && (
                            <>
                                <table className={styles.itemsTable}>
                                    <thead>
                                        <tr>
                                            <th>Producto</th>
                                            <th>Precio unit.</th>
                                            <th>Cant.</th>
                                            <th>Subtotal</th>
                                            <th></th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {items.map(i => (
                                            <tr key={i.id_producto}>
                                                <td>{i.nombre_producto}</td>
                                                <td>Q{i.precio_unitario.toFixed(2)}</td>
                                                <td>{i.cantidad}</td>
                                                <td>Q{(i.precio_unitario * i.cantidad).toFixed(2)}</td>
                                                <td>
                                                    <button
                                                        className={styles.removeBtn}
                                                        onClick={() => handleRemoverItem(i.id_producto)}
                                                    >
                                                        ✕
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                                <p className={styles.total}>Total: Q{total.toFixed(2)}</p>
                            </>
                        )}
                    </div>

                    {error && <p className={styles.error}>{error}</p>}

                    <div className={styles.actions}>
                        <button className={styles.cancelBtn} onClick={onClose}>Cancelar</button>
                        <button className={styles.submitBtn} onClick={handleSubmit} disabled={loading}>
                            {loading ? 'Creando...' : 'Crear venta'}
                        </button>
                    </div>
                </div>
            )}
        </Modal>
    )
}

export default CrearVentaModal