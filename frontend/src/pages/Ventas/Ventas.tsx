import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createVenta, deleteVenta, getVentas } from '../../api/ventas'
import ActionsMenu from '../../components/ActionsMenu/ActionsMenu'
import ConfirmModal from '../../components/ConfirmModal/ConfirmModal'
import CrearVentaModal from '../../components/CrearVentaModal/CrearVentaModal'
import type { VentaCreateInput, VentaSummary } from '../../types'
import { getRango, type RangoFecha } from '../../utils/fechas'
import styles from './Ventas.module.css'

const RANGOS: { label: string, value: RangoFecha }[] = [
    { label: 'Última semana', value: '1s' },
    { label: 'Últimas 2 semanas', value: '2s' },
    { label: 'Último mes', value: '1m' },
]

function Ventas() {
    const navigate = useNavigate()
    const [ventas, setVentas] = useState<VentaSummary[]>([])
    const [rango, setRango] = useState<RangoFecha>('1s')
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [confirmarId, setConfirmarId] = useState<number | null>(null)
    const [mostrarCrear, setMostrarCrear] = useState(false)

    useEffect(() => {
        const load = async () => {
            setLoading(true)
            try {
                const { inicio, fin } = getRango(rango)
                const data = await getVentas(inicio, fin)
                setVentas(data)
            } catch (e: any) {
                setError(e.message)
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [rango])

    const handleCrear = async (data: VentaCreateInput) => {
        const nueva = await createVenta(data)
        setVentas(prev => [nueva, ...prev])
        return nueva
    }

    const handleEliminar = async () => {
        if (!confirmarId) return
        await deleteVenta(confirmarId)
        setVentas(prev => prev.filter(v => v.id_venta !== confirmarId))
        setConfirmarId(null)
    }

    const formatFecha = (fecha: string | Date) =>
        new Date(fecha).toLocaleString('es-GT', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })

    const formatTotal = (total: number) =>
        `Q${total.toFixed(2)}`

    if (error) return <p>Error: {error}</p>
    if (loading) return <p>Cargando...</p>

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1>Ventas recientes</h1>
                <div className={styles.filterGroup}>
                    {RANGOS.map(r => (
                        <button
                            key={r.value}
                            onClick={() => setRango(r.value)}
                            className={`${styles.filterButton} ${rango === r.value ? styles.filterButtonActive : ''}`}
                        >
                            {r.label}
                        </button>
                    ))}
                    <button className={styles.createButton} onClick={() => setMostrarCrear(true)}>
                        + Nueva venta
                    </button>
                </div>
            </div>

            {ventas.length === 0 ? (
                <p className={styles.empty}>No hay ventas en este período.</p>
            ) : (
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Empleado</th>
                            <th>Cliente</th>
                            <th>Fecha</th>
                            <th>Total</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {ventas.map(v => (
                            <tr
                                key={v.id_venta}
                                onClick={() => navigate(`/ventas/${v.id_venta}`)}
                            >
                                <td>{v.id_venta}</td>
                                <td>{v.nombre_empleado}</td>
                                <td>{v.email_cliente}</td>
                                <td>{formatFecha(v.fecha)}</td>
                                <td>{formatTotal(v.total)}</td>
                                <td onClick={e => e.stopPropagation()}>
                                    <ActionsMenu
                                        onEliminar={() => setConfirmarId(v.id_venta)}
                                    />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}

            {mostrarCrear && (
                <CrearVentaModal
                    onClose={() => setMostrarCrear(false)}
                    onCrear={handleCrear}
                />
            )}

            {confirmarId && (
                <ConfirmModal
                    mensaje={`¿Eliminar venta #${confirmarId}?\n\nATENCION: Esta accion eliminara todos los detalles de venta asociados a esta venta.`}
                    onConfirm={handleEliminar}
                    onCancel={() => setConfirmarId(null)}
                />
            )}
        </div>
    )
}

export default Ventas