import { useEffect, useState } from 'react'
import { createEmpleado, deleteEmpleado, getEmpleados, updateEmpleado } from '../../api/empleados'
import ActionsMenu from '../../components/ActionsMenu/ActionsMenu'
import ConfirmModal from '../../components/ConfirmModal/ConfirmModal'
import CrearEmpleadoModal from '../../components/Modal/CrearEmpleadoModal'
import type { Empleado, EmpleadoBase, EmpleadoSales } from '../../types'
import styles from './Empleados.module.css'

function Empleados() {
    const [empleados, setEmpleados] = useState<EmpleadoSales[]>([])
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

    const escapeCsv = (value: string | number) => {
        const text = String(value)
        return `"${text.replace(/"/g, '""')}"`
    }

    const handleExportarCsv = () => {
        const headers = ['ID', 'Nombre', 'Total de ventas', 'Ingresos generados']
        const rows = empleados.map(e => [
            e.id_empleado,
            e.nombre,
            e.ventas,
            e.ingresos
        ])
        const csv = [headers, ...rows]
            .map(row => row.map(escapeCsv).join(','))
            .join('\r\n')
        const blob = new Blob([`\uFEFF${csv}`], { type: 'text/csv;charset=utf-8;' })
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')

        link.href = url
        link.download = 'reporte-empleados-ingresos.csv'
        document.body.appendChild(link)
        link.click()
        link.remove()
        URL.revokeObjectURL(url)
    }

    if (loading) return <p>Cargando...</p>
    if (error) return <p>Error: {error}</p>

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1>Empleados con más ventas</h1>
                <div className={styles.actions}>
                    <button
                        className={styles.exportButton}
                        onClick={handleExportarCsv}
                        disabled={empleados.length === 0}
                    >
                        Exportar CSV
                    </button>
                    <button className={styles.createButton} onClick={() => setMostrarCrear(true)}>
                        + Nuevo empleado
                    </button>
                </div>
            </div>

            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Total de ventas</th>
                        <th>Ingresos generados</th>
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
                                    <td>{p.ventas}</td>
                                    <td>{p.ingresos}</td>
                                    <td>
                                        <button className={styles.saveButton} onClick={() => handleGuardar(p)}>Guardar</button>
                                        <button className={styles.cancelButton} onClick={() => setEditandoId(null)}>Cancelar</button>
                                    </td>
                                </>
                            ) : (
                                <>
                                    <td>{p.id_empleado}</td>
                                    <td>{p.nombre}</td>
                                    <td>{p.ventas}</td>
                                    <td>{p.ingresos}</td>
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
                    mensaje={`Eliminar "${empleados.find(p => p.id_empleado === confirmarId)?.nombre}"?\n\nTambien se borraran todas las ventas atendidas por este empleado y todos los detalles asociados a esas ventas.`}
                    onConfirm={handleEliminar}
                    onCancel={() => setConfirmarId(null)}
                />
            )}
        </div>
    )
}

export default Empleados
