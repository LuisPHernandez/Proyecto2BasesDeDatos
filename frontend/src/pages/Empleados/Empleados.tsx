import { useEffect, useState } from 'react'
import { createEmpleado, deleteEmpleado, getEmpleados, updateEmpleado } from '../../api/empleados'
import ActionsMenu from '../../components/ActionsMenu/ActionsMenu'
import ConfirmModal from '../../components/ConfirmModal/ConfirmModal'
import CrearEmpleadoModal from '../../components/Modal/CrearEmpleadoModal'
import type { Empleado, EmpleadoBase } from '../../types'
import styles from './Empleados.module.css'

function Empleados() {
    const [empleados, setEmpleados] = useState<Empleado[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [editandoId, setEditandoId] = useState<number | null>(null)
    const [editForm, setEditForm] = useState<EmpleadoBase>({ nombre: '' })
    const [confirmarId, setConfirmarId] = useState<number | null>(null)
    const [mostrarCrear, setMostrarCrear] = useState(false)

    useEffect(() => {
        const load = async () => {
            try {
                const data = await getEmpleados()
                setEmpleados(data)
            } catch (e: any) {
                setError(e.message)
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [])

    const handleCrear = async (data: EmpleadoBase) => {
        const nuevo = await createEmpleado(data)
        setEmpleados(prev => [...prev, nuevo])
    }

    const handleEditar = (p: Empleado) => {
        setEditandoId(p.id_empleado)
        setEditForm({ nombre: p.nombre })
    }

    const handleGuardar = async (p: Empleado) => {
        await updateEmpleado(p.id_empleado, editForm)
        setEmpleados(prev =>
            prev.map(x => x.id_empleado === p.id_empleado ? { ...x, ...editForm } : x)
        )
        setEditandoId(null)
    }

    const handleEliminar = async () => {
        if (!confirmarId) return
        try {
            await deleteEmpleado(confirmarId)
            setEmpleados(prev => prev.filter(p => p.id_empleado !== confirmarId))
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
                <h1>Empleados</h1>
                <button className={styles.createButton} onClick={() => setMostrarCrear(true)}>
                    + Nuevo empleado
                </button>
            </div>

            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {empleados.map(p => (
                        <tr key={p.id_empleado}>
                            {editandoId === p.id_empleado ? (
                                <>
                                    <td>{p.id_empleado}</td>
                                    <td>
                                        <input
                                            className={styles.inlineInput}
                                            value={editForm.nombre}
                                            onChange={e => setEditForm(f => ({ ...f, nombre: e.target.value }))}
                                        />
                                    </td>
                                    <td>
                                        <button className={styles.saveButton} onClick={() => handleGuardar(p)}>Guardar</button>
                                        <button className={styles.cancelButton} onClick={() => setEditandoId(null)}>Cancelar</button>
                                    </td>
                                </>
                            ) : (
                                <>
                                    <td>{p.id_empleado}</td>
                                    <td>{p.nombre}</td>
                                    <td>
                                        <ActionsMenu
                                            onEditar={() => handleEditar(p)}
                                            onEliminar={() => setConfirmarId(p.id_empleado)}
                                        />
                                    </td>
                                </>
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>

            {mostrarCrear && (
                <CrearEmpleadoModal
                    onClose={() => setMostrarCrear(false)}
                    onCrear={handleCrear}
                />
            )}

            {confirmarId && (
                <ConfirmModal
                    mensaje={`¿Eliminar "${empleados.find(p => p.id_empleado === confirmarId)?.nombre}"?`}
                    onConfirm={handleEliminar}
                    onCancel={() => setConfirmarId(null)}
                />
            )}
        </div>
    )
}

export default Empleados