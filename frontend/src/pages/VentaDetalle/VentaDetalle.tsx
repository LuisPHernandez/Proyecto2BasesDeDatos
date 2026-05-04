import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { deleteVenta, getVentaById, getVentaProductosById } from '../../api/ventas'
import ConfirmModal from '../../components/ConfirmModal/ConfirmModal'
import type { VentaProducto, VentaSummary } from '../../types'
import styles from './VentaDetalle.module.css'

function VentaDetalle() {
    const { id } = useParams()
    const navigate = useNavigate()

    const [venta, setVenta] = useState<VentaSummary | null>(null)
    const [productos, setProductos] = useState<VentaProducto[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [confirmar, setConfirmar] = useState(false)

    useEffect(() => {
        if (!id) return
        const load = async () => {
            try {
                const [ventaData, productosData] = await Promise.all([
                    getVentaById(+id),
                    getVentaProductosById(+id)
                ])
                setVenta(ventaData)
                setProductos(productosData)
            } catch (e: any) {
                setError(e.message)
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [id])

    const handleEliminar = async () => {
        if (!id) return
        await deleteVenta(+id)
        navigate('/ventas')
    }

    const formatFecha = (fecha: string | Date) =>
        new Date(fecha).toLocaleString('es-GT', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })

    const formatMoneda = (n: number) => `Q${n.toFixed(2)}`

    if (loading) return <p>Cargando...</p>
    if (error) return <p>Error: {error}</p>
    if (!venta) return <p>Venta no encontrada.</p>

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <button className={styles.backButton} onClick={() => navigate('/ventas')}>
                    ← Volver a ventas
                </button>
                <button className={styles.deleteButton} onClick={() => setConfirmar(true)}>
                    Eliminar venta
                </button>
            </div>

            <div className={styles.card}>
                <p className={styles.cardTitle}>Información de la venta</p>
                <div className={styles.infoGrid}>
                    <div className={styles.infoItem}>
                        <label>ID</label>
                        <span>#{venta.id_venta}</span>
                    </div>
                    <div className={styles.infoItem}>
                        <label>Empleado</label>
                        <span>{venta.nombre_empleado}</span>
                    </div>
                    <div className={styles.infoItem}>
                        <label>Cliente</label>
                        <span>{venta.nombre_cliente}</span>
                    </div>
                    <div className={styles.infoItem}>
                        <label>Email</label>
                        <span>{venta.email_cliente}</span>
                    </div>
                    <div className={styles.infoItem}>
                        <label>Fecha</label>
                        <span>{formatFecha(venta.fecha)}</span>
                    </div>
                    <div className={styles.infoItem}>
                        <label>Total</label>
                        <span>{formatMoneda(venta.total)}</span>
                    </div>
                </div>
            </div>

            <div className={styles.card}>
                <p className={styles.cardTitle}>Productos</p>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th>Precio unitario</th>
                            <th>Cantidad</th>
                            <th>Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        {productos.map(p => (
                            <tr key={p.id_producto}>
                                <td>{p.nombre_producto}</td>
                                <td>{formatMoneda(p.precio_unitario)}</td>
                                <td>{p.cantidad}</td>
                                <td>{formatMoneda(p.precio_unitario * p.cantidad)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div className={styles.total}>
                    Total: {formatMoneda(venta.total)}
                </div>
            </div>

            {confirmar && (
                <ConfirmModal
                    mensaje={`Eliminar venta #${venta.id_venta}?\n\nTambien se borraran todos los detalles de producto asociados a esta venta.`}
                    onConfirm={handleEliminar}
                    onCancel={() => setConfirmar(false)}
                />
            )}
        </div>
    )
}

export default VentaDetalle
