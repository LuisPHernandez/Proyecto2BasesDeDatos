import { useEffect, useState } from 'react'
import { createCliente, deleteCliente, getActiveIds, getClientes, updateCliente } from '../../api/clientes'
import ActionsMenu from '../../components/ActionsMenu/ActionsMenu'
import ConfirmModal from '../../components/ConfirmModal/ConfirmModal'
import CrearClienteModal from '../../components/Modal/CrearClienteModal'
import type { Cliente, ClienteBase } from '../../types'
import styles from './Clientes.module.css'

function Clientes() {
    const [clientes, setClientes] = useState<Cliente[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [activeIds, setActiveIds] = useState<number[]>([])
    const [activeFilter, setActiveFilter] = useState(false)
    const [editandoId, setEditandoId] = useState<number | null>(null)
    const [editForm, setEditForm] = useState<ClienteBase>({ nombre: '', email: '' })
    const [confirmarId, setConfirmarId] = useState<number | null>(null)
    const [mostrarCrear, setMostrarCrear] = useState(false)

    useEffect(() => {
        const load = async () => {
            try {
                const [data, ids] = await Promise.all([
                    getClientes(),
                    getActiveIds()
                ])
                setClientes(data)
                setActiveIds(ids)
            } catch (e: any) {
                setError(e.message)
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [])

    const handleCrear = async (data: ClienteBase) => {
        const nuevo = await createCliente(data)
        setClientes(prev => [...prev, nuevo])
    }

    const handleEditar = (c: Cliente) => {
        setEditandoId(c.id_cliente)
        setEditForm({ nombre: c.nombre, email: c.email })
    }

    const handleGuardar = async (c: Cliente) => {
        await updateCliente(c.id_cliente, editForm)
        setClientes(prev =>
            prev.map(x => x.id_cliente === c.id_cliente ? { ...x, ...editForm } : x)
        )
        setEditandoId(null)
    }

    const handleEliminar = async () => {
        if (!confirmarId) return
        try {
            await deleteCliente(confirmarId)
            setClientes(prev => prev.filter(c => c.id_cliente !== confirmarId))
        } catch (e: any) {
            setError(e.message)
        } finally {
            setConfirmarId(null)
        }
    }

    if (loading) return <p>Cargando...</p>
    if (error) return <p>Error: {error}</p>

    const clientesMostrados = activeFilter
        ? clientes.filter(c => activeIds.includes(c.id_cliente))
        : clientes

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1>Clientes</h1>
                <button
                    className={styles.filterButton}
                    onClick={() => setActiveFilter(!activeFilter)}
                >
                    {activeFilter ? 'Mostrar todos los clientes' : 'Mostrar solo los clientes activos'}
                </button>
                <button className={styles.createButton} onClick={() => setMostrarCrear(true)}>
                    + Nuevo cliente
                </button>
            </div>

            {activeFilter && (
                <h2>Mostrando solo clientes que hayan realizado alguna compra en el últmo mes</h2>
            )}

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
                    {clientesMostrados.map(c => (
                        <tr key={c.id_cliente}>
                            {editandoId === c.id_cliente ? (
                                <>
                                    <td>{c.id_cliente}</td>
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
                                        <button className={styles.saveButton} onClick={() => handleGuardar(c)}>Guardar</button>
                                        <button className={styles.cancelButton} onClick={() => setEditandoId(null)}>Cancelar</button>
                                    </td>
                                </>
                            ) : (
                                <>
                                    <td>{c.id_cliente}</td>
                                    <td>{c.nombre}</td>
                                    <td>{c.email}</td>
                                    <td>
                                        <ActionsMenu
                                            onEditar={() => handleEditar(c)}
                                            onEliminar={() => setConfirmarId(c.id_cliente)}
                                        />
                                    </td>
                                </>
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>

            {mostrarCrear && (
                <CrearClienteModal
                    onClose={() => setMostrarCrear(false)}
                    onCrear={handleCrear}
                />
            )}

            {confirmarId && (
                <ConfirmModal
                    mensaje={`Eliminar "${clientes.find(c => c.id_cliente === confirmarId)?.nombre}"?\n\nTambien se borraran todas las ventas de este cliente y todos los detalles asociados a esas ventas.`}
                    onConfirm={handleEliminar}
                    onCancel={() => setConfirmarId(null)}
                />
            )}
        </div>
    )
}

export default Clientes
