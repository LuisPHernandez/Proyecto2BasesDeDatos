import { useEffect, useState } from 'react'
import { createProveedor, deleteProveedor, getProveedores, updateProveedor } from '../../api/proveedores'
import ActionsMenu from '../../components/ActionsMenu/ActionsMenu'
import ConfirmModal from '../../components/ConfirmModal/ConfirmModal'
import CrearProveedorModal from '../../components/Modal/CrearProveedorModal'
import type { Proveedor, ProveedorBase } from '../../types'
import styles from './Proveedores.module.css'

function Proveedores() {
    const [proveedores, setProveedores] = useState<Proveedor[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [editandoId, setEditandoId] = useState<number | null>(null)
    const [editForm, setEditForm] = useState<ProveedorBase>({ nombre: '', email: '' })
    const [confirmarId, setConfirmarId] = useState<number | null>(null)
    const [mostrarCrear, setMostrarCrear] = useState(false)

    useEffect(() => {
        const load = async () => {
            try {
                const data = await getProveedores()
                setProveedores(data)
            } catch (e: any) {
                setError(e.message)
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [])

    const handleCrear = async (data: ProveedorBase) => {
        const nuevo = await createProveedor(data)
        setProveedores(prev => [...prev, nuevo])
    }

    const handleEditar = (p: Proveedor) => {
        setEditandoId(p.id_proveedor)
        setEditForm({ nombre: p.nombre, email: p.email })
    }

    const handleGuardar = async (p: Proveedor) => {
        await updateProveedor(p.id_proveedor, editForm)
        setProveedores(prev =>
            prev.map(x => x.id_proveedor === p.id_proveedor ? { ...x, ...editForm } : x)
        )
        setEditandoId(null)
    }

    const handleEliminar = async () => {
        if (!confirmarId) return
        try {
            await deleteProveedor(confirmarId)
            setProveedores(prev => prev.filter(p => p.id_proveedor !== confirmarId))
        } catch (e: any) {
            setError(e.message)
        } finally {
            setConfirmarId(null)
        }
    }

    if (loading) return <p>Cargando...</p>
    if (error) return <p>Error: {error}</p>

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1>Proveedores</h1>
                <button className={styles.createButton} onClick={() => setMostrarCrear(true)}>
                    + Nuevo proveedor
                </button>
            </div>

            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Email</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {proveedores.map(p => (
                        <tr key={p.id_proveedor}>
                            {editandoId === p.id_proveedor ? (
                                <>
                                    <td>{p.id_proveedor}</td>
                                    <td>
                                        <input
                                            className={styles.inlineInput}
                                            value={editForm.nombre}
                                            onChange={e => setEditForm(f => ({ ...f, nombre: e.target.value }))}
                                        />
                                    </td>
                                    <td>
                                        <input
                                            className={styles.inlineInput}
                                            value={editForm.email}
                                            onChange={e => setEditForm(f => ({ ...f, email: e.target.value }))}
                                        />
                                    </td>
                                    <td>
                                        <button className={styles.saveButton} onClick={() => handleGuardar(p)}>Guardar</button>
                                        <button className={styles.cancelButton} onClick={() => setEditandoId(null)}>Cancelar</button>
                                    </td>
                                </>
                            ) : (
                                <>
                                    <td>{p.id_proveedor}</td>
                                    <td>{p.nombre}</td>
                                    <td>{p.email}</td>
                                    <td>
                                        <ActionsMenu
                                            onEditar={() => handleEditar(p)}
                                            onEliminar={() => setConfirmarId(p.id_proveedor)}
                                        />
                                    </td>
                                </>
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>

            {mostrarCrear && (
                <CrearProveedorModal
                    onClose={() => setMostrarCrear(false)}
                    onCrear={handleCrear}
                />
            )}

            {confirmarId && (
                <ConfirmModal
                    mensaje={`¿Eliminar "${proveedores.find(p => p.id_proveedor === confirmarId)?.nombre}"?`}
                    onConfirm={handleEliminar}
                    onCancel={() => setConfirmarId(null)}
                />
            )}
        </div>
    )
}

export default Proveedores