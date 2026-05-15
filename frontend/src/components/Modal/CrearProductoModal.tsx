import { useEffect, useState } from 'react'
import { getCategorias } from '../../api/categorias'
import { getProveedores } from '../../api/proveedores'
import type { Categoria, ProductoBase, ProductoDetailed, Proveedor } from '../../types'
import modalStyles from '../Modal/Modal.module.css'
import Modal from './Modal'

interface Props {
    onClose: () => void
    onCrear: (data: ProductoBase) => Promise<ProductoDetailed>
}

function CrearProductoModal({ onClose, onCrear }: Props) {
    const [proveedores, setProveedores] = useState<Proveedor[]>([])
    const [categorias, setCategorias] = useState<Categoria[]>([])
    const [loadingData, setLoadingData] = useState(true)
    const [form, setForm] = useState<ProductoBase>({
        nombre: '',
        precio_compra: 0,
        precio_venta: 0,
        unidades_disponibles: 0,
        id_categoria: 0,
        id_proveedor: 0
    })
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        const load = async () => {
            try {
                const [proveedoresData, categoriasData] = await Promise.all([
                    getProveedores(),
                    getCategorias()
                ])
                setProveedores(proveedoresData)
                setCategorias(categoriasData)
            } catch (e) {
                setError(e instanceof Error ? e.message : 'Ocurrió un error')
            } finally {
                setLoadingData(false)
            }
        }

        load()
    }, [])

    const handleSubmit = async () => {
        if (!form.nombre.trim()) {
            setError('Ingresa el nombre del producto')
            return
        }
        if (form.nombre.length > 30) {
            setError('El nombre del producto no puede exceder los 30 caracteres')
            return
        }
        if (form.nombre.length < 2) {
            setError('El nombre del producto debe tener al menos 2 caracteres')
            return
        }
        if (!form.id_proveedor || !form.id_categoria) {
            setError('Selecciona proveedor y categoria')
            return
        }
        if (form.precio_compra < 0 || form.precio_venta < 0 || form.unidades_disponibles < 0) {
            setError('Los precios y unidades no pueden ser negativos')
            return
        }
        if (form.precio_compra > form.precio_venta) {
            setError('El precio de compra no puede ser mayor al precio de venta')
            return
        }
        if (form.unidades_disponibles % 1 !== 0) {
            setError('Las unidades disponibles deben ser numeros enteros')
            return
        }

        setLoading(true)
        setError(null)
        try {
            await onCrear(form)
            onClose()
        } catch (e) {
            setError(e instanceof Error ? e.message : 'Ocurrió un error')
        } finally {
            setLoading(false)
        }
    }

    return (
        <Modal titulo="Nuevo producto" onClose={onClose}>
            {loadingData ? (
                <p>Cargando datos...</p>
            ) : (
                <>
                    <div className={modalStyles.field}>
                        <label>Nombre</label>
                        <input
                            value={form.nombre}
                            onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))}
                            placeholder="Nombre del producto"
                        />
                    </div>

                    <div className={modalStyles.field}>
                        <label>Proveedor</label>
                        <select
                            value={form.id_proveedor || ''}
                            onChange={e => setForm(f => ({ ...f, id_proveedor: +e.target.value }))}
                        >
                            <option value="">Seleccionar...</option>
                            {proveedores.map(proveedor => (
                                <option key={proveedor.id_proveedor} value={proveedor.id_proveedor}>
                                    {proveedor.nombre}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className={modalStyles.field}>
                        <label>Categoria</label>
                        <select
                            value={form.id_categoria || ''}
                            onChange={e => setForm(f => ({ ...f, id_categoria: +e.target.value }))}
                        >
                            <option value="">Seleccionar...</option>
                            {categorias.map(categoria => (
                                <option key={categoria.id_categoria} value={categoria.id_categoria}>
                                    {categoria.nombre}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className={modalStyles.field}>
                        <label>Precio compra</label>
                        <input
                            type="number"
                            min={0}
                            step="0.01"
                            value={form.precio_compra}
                            onChange={e => setForm(f => ({ ...f, precio_compra: +e.target.value }))}
                        />
                    </div>

                    <div className={modalStyles.field}>
                        <label>Precio venta</label>
                        <input
                            type="number"
                            min={0}
                            step="0.01"
                            value={form.precio_venta}
                            onChange={e => setForm(f => ({ ...f, precio_venta: +e.target.value }))}
                        />
                    </div>

                    <div className={modalStyles.field}>
                        <label>Unidades disponibles</label>
                        <input
                            type="number"
                            min={0}
                            value={form.unidades_disponibles}
                            onChange={e => setForm(f => ({ ...f, unidades_disponibles: +e.target.value }))}
                        />
                    </div>

                    {error && <p style={{ color: '#dc2626', fontSize: '0.85rem', margin: 0 }}>{error}</p>}

                    <div className={modalStyles.actions}>
                        <button className={modalStyles.cancelButton} onClick={onClose}>Cancelar</button>
                        <button className={modalStyles.submitButton} onClick={handleSubmit} disabled={loading}>
                            {loading ? 'Creando...' : 'Crear producto'}
                        </button>
                    </div>
                </>
            )}
        </Modal>
    )
}

export default CrearProductoModal
