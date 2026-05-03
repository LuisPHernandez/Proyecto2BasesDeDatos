import { useEffect, useState } from 'react'
import { deleteProducto, getLowStockIds, getProductos, updateProducto } from '../../api/productos'
import ActionsMenu from '../../components/ActionsMenu/ActionsMenu'
import ConfirmModal from '../../components/ConfirmModal/ConfirmModal'
import StockBadge from '../../components/StockBadge/StockBadge'
import type { Producto, ProductoDetailed } from '../../types'
import styles from './Inventario.module.css'

function Inventario() {
    const [productos, setProductos] = useState<ProductoDetailed[]>([])
    const [lowStockIds, setLowStockIds] = useState<number[]>([])
    const [lowStockFilter, setLowStockFilter] = useState(false)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [editandoId, setEditandoId] = useState<number | null>(null)
    const [editForm, setEditForm] = useState<Partial<Producto>>({})
    const [confirmarId, setConfirmarId] = useState<number | null>(null)

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

    const handleEditar = (p: Producto) => {
        setEditandoId(p.id_producto)
        setEditForm({ nombre: p.nombre, precio_compra: p.precio_compra, precio_venta: p.precio_venta, unidades_disponibles: p.unidades_disponibles, id_categoria: p.id_categoria, id_proveedor: p.id_proveedor })
    }

    const handleGuardar = async (p: Producto) => {
        await updateProducto(p.id_producto, { ...p, ...editForm })
        setProductos(prev => prev.map(x => x.id_producto === p.id_producto ? { ...x, ...editForm } : x))
        setEditandoId(null)
    }

    const handleEliminar = async () => {
        if (!confirmarId) return

        try {
            await deleteProducto(confirmarId)

            setProductos(prev =>
                prev.filter(p => p.id_producto !== confirmarId)
            )
        } catch (e: any) {
            setError(e.message)
        } finally {
            setConfirmarId(null)
        }
    }

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
                <button className={styles.createButton}>
                    + Nuevo producto
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
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {productosMostrados.map(p => (
                        <tr key={p.id_producto}>
                            {editandoId === p.id_producto ? (
                                <>
                                    <td>{p.id_producto}</td>
                                    <td>
                                        <input
                                            className={styles.inlineInput}
                                            value={editForm.nombre ?? ''}
                                            onChange={e => setEditForm(f => ({ ...f, nombre: e.target.value }))}
                                        />
                                    </td>
                                    <td>{p.categoria}</td>
                                    <td>{p.proveedor}</td>
                                    <td>
                                        <input
                                            className={styles.inlineInput}
                                            type="number"
                                            value={editForm.precio_compra ?? ''}
                                            onChange={e => setEditForm(f => ({ ...f, precio_compra: +e.target.value }))}
                                        />
                                    </td>
                                    <td>
                                        <input
                                            className={styles.inlineInput}
                                            type="number"
                                            value={editForm.precio_venta ?? ''}
                                            onChange={e => setEditForm(f => ({ ...f, precio_venta: +e.target.value }))}
                                        />
                                    </td>
                                    <td>
                                        <input
                                            className={styles.inlineInput}
                                            type="number"
                                            value={editForm.unidades_disponibles ?? ''}
                                            onChange={e => setEditForm(f => ({ ...f, unidades_disponibles: +e.target.value }))}
                                        />
                                        <StockBadge show={lowStockIds.includes(p.id_producto)} />
                                    </td>
                                    <td>
                                        <button className={styles.saveButton} onClick={() => handleGuardar(p)}>Guardar</button>
                                        <button className={styles.cancelButton} onClick={() => setEditandoId(null)}>Cancelar</button>
                                    </td>
                                </>
                            ) : (
                                <>
                                    <td>{p.id_producto}</td>
                                    <td>{p.nombre}</td>
                                    <td>{p.categoria}</td>
                                    <td>{p.proveedor}</td>
                                    <td>{p.precio_compra}</td>
                                    <td>{p.precio_venta}</td>
                                    <td>
                                        {p.unidades_disponibles}
                                        <StockBadge show={lowStockIds.includes(p.id_producto)} />
                                    </td>
                                    <td>
                                        <ActionsMenu
                                            onEditar={() => handleEditar(p)}
                                            onEliminar={() => setConfirmarId(p.id_producto)}
                                        />
                                    </td>
                                </>
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>

            {confirmarId && (
                <ConfirmModal
                    mensaje={`¿Eliminar "${productos.find(p => p.id_producto === confirmarId)?.nombre}"?\n\nATENCION: Esta accion eliminara todos los detalles de venta en los que aparezca este producto.`}
                    onConfirm={handleEliminar}
                    onCancel={() => setConfirmarId(null)}
                />
            )}
        </div>
    )
}

export default Inventario