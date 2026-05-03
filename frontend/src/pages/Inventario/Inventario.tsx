import { useEffect, useState } from 'react'
import { getLowStockIds, getProductos } from '../../api/productos'
import type { ProductoDetailed } from '../../types'
import styles from './Inventario.module.css'

function Inventario() {
    const [productos, setProductos] = useState<ProductoDetailed[]>([])
    const [lowStockIds, setLowStockIds] = useState<number[]>([])
    const [lowStockFilter, setLowStockFilter] = useState(false)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const load = async () => {
            try {
                const [data, ids] = await Promise.all([
                    getProductos(),
                    getLowStockIds()
                ])
                setProductos(data)
                setLowStockIds(ids)
            } catch (e: any) {
                setError(e.message)
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [])

    if (loading) return <p>Cargando...</p>
    if (error) return <p>Error: {error}</p>

    const productosMostrados = lowStockFilter
        ? productos.filter(p => lowStockIds.includes(p.id_producto))
        : productos

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1>Inventario</h1>
                <button
                    className={styles.filterButton}
                    onClick={() => setLowStockFilter(!lowStockFilter)}
                >
                    {lowStockFilter ? 'Mostrar todos los productos' : 'Mostrar solo los productos con stock bajo'}
                </button>
            </div>

            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Categoría</th>
                        <th>Proveedor</th>
                        <th>Precio compra</th>
                        <th>Precio venta</th>
                        <th>Unidades disponibles</th>
                    </tr>
                </thead>
                <tbody>
                    {productosMostrados.map(p => (
                        <tr key={p.id_producto}>
                            <td>{p.id_producto}</td>
                            <td>{p.nombre}</td>
                            <td>{p.categoria}</td>
                            <td>{p.proveedor}</td>
                            <td>{p.precio_compra}</td>
                            <td>{p.precio_venta}</td>
                            <td>
                                {p.unidades_disponibles}
                                {lowStockIds.includes(p.id_producto) && (
                                    <span className={styles.lowStock}> ⚠ Stock bajo</span>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default Inventario