import { useEffect, useState } from 'react'
import { getCategorias } from '../../api/categorias'
import { createProducto, deleteProducto, getLowStockIds, getProductos, getTopMes, updateProducto } from '../../api/productos'
import { getProveedores } from '../../api/proveedores'
import ActionsMenu from '../../components/ActionsMenu/ActionsMenu'
import ConfirmModal from '../../components/ConfirmModal/ConfirmModal'
import CrearProductoModal from '../../components/Modal/CrearProductoModal'
import StockBadge from '../../components/StockBadge/StockBadge'
import type { Producto, ProductoBase, ProductoDetailed, ProductoTop } from '../../types'
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
    const [mostrarCrearModal, setMostrarCrearModal] = useState(false)
    const [topMes, setTopMes] = useState<ProductoTop[]>([])

    useEffect(() => {
        const load = async () => {
            try {
                const [data, ids, top] = await Promise.all([
                    getProductos(),
                    getLowStockIds(),
                    getTopMes()
                ])
                setProductos(data)
                setLowStockIds(ids)
                setTopMes(top)
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

    const handleCrear = async (data: ProductoBase) => {
        const [producto, proveedores, categorias] = await Promise.all([
            createProducto(data),
            getProveedores(),
            getCategorias()
        ])

        const nuevoProducto: ProductoDetailed = {
            ...producto,
            proveedor: proveedores.find(p => p.id_proveedor === producto.id_proveedor)?.nombre ?? '',
            categoria: categorias.find(c => c.id_categoria === producto.id_categoria)?.nombre ?? ''
        }

        setProductos(prev => [...prev, nuevoProducto])
        return nuevoProducto
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
                <button className={styles.createButton} onClick={() => setMostrarCrearModal(true)}>
                    + Nuevo producto
                </button>
            </div>

            {topMes.length > 0 && (
                <div className={styles.topMes}>
                    <p className={styles.topMesTitle}>Top 5 más vendidos este mes</p>
                    <div className={styles.topMesGrid}>
                        <div className={styles.topMesHeader}>
                            <span>Pos.</span>
                            <span>Producto</span>
                            <span>Unidades</span>
                            <span>Ingresos</span>
                        </div>
                        {topMes.map((p, i) => (
                            <div key={p.id_producto} className={styles.topMesCard}>
                                <span className={styles.topMesRank}>#{i + 1}</span>
                                <span className={styles.topMesNombre}>{p.nombre}</span>
                                <span className={styles.topMesUnidades}>{p.unidades_vendidas} uds.</span>
                                <span className={styles.topMesIngresos}>Q{p.ingresos.toFixed(2)}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

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

            {mostrarCrearModal && (
                <CrearProductoModal
                    onClose={() => setMostrarCrearModal(false)}
                    onCrear={handleCrear}
                />
            )}

            {confirmarId && (
                <ConfirmModal
                    mensaje={`Eliminar "${productos.find(p => p.id_producto === confirmarId)?.nombre}"?\n\nTambien se borraran todos los detalles de venta donde aparezca este producto. Las ventas quedaran registradas, pero sin este producto en su detalle.`}
                    onConfirm={handleEliminar}
                    onCancel={() => setConfirmarId(null)}
                />
            )}
        </div>
    )
}

export default Inventario
