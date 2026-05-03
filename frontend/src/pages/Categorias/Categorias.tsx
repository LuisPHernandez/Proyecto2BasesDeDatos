import { useEffect, useState } from 'react'
import { createCategoria, deleteCategoria, getCategorias, updateCategoria } from '../../api/categorias'
import ActionsMenu from '../../components/ActionsMenu/ActionsMenu'
import ConfirmModal from '../../components/ConfirmModal/ConfirmModal'
import CrearCategoriaModal from '../../components/Modal/CrearCategoriaModal'
import type { Categoria, CategoriaBase } from '../../types'
import styles from './Categorias.module.css'

function Categorias() {
    const [categorias, setCategorias] = useState<Categoria[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [editandoId, setEditandoId] = useState<number | null>(null)
    const [editForm, setEditForm] = useState<CategoriaBase>({ nombre: '' })
    const [confirmarId, setConfirmarId] = useState<number | null>(null)
    const [mostrarCrear, setMostrarCrear] = useState(false)

    useEffect(() => {
        const load = async () => {
            try {
                const data = await getCategorias()
                setCategorias(data)
            } catch (e: any) {
                setError(e.message)
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [])

    const handleCrear = async (data: CategoriaBase) => {
        const nuevo = await createCategoria(data)
        setCategorias(prev => [...prev, nuevo])
    }

    const handleEditar = (p: Categoria) => {
        setEditandoId(p.id_categoria)
        setEditForm({ nombre: p.nombre })
    }

    const handleGuardar = async (p: Categoria) => {
        await updateCategoria(p.id_categoria, editForm)
        setCategorias(prev =>
            prev.map(x => x.id_categoria === p.id_categoria ? { ...x, ...editForm } : x)
        )
        setEditandoId(null)
    }

    const handleEliminar = async () => {
        if (!confirmarId) return
        try {
            await deleteCategoria(confirmarId)
            setCategorias(prev => prev.filter(p => p.id_categoria !== confirmarId))
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
                <h1>Categorías de productos</h1>
                <button className={styles.createButton} onClick={() => setMostrarCrear(true)}>
                    + Nueva categoría
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
                    {categorias.map(p => (
                        <tr key={p.id_categoria}>
                            {editandoId === p.id_categoria ? (
                                <>
                                    <td>{p.id_categoria}</td>
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
                                    <td>{p.id_categoria}</td>
                                    <td>{p.nombre}</td>
                                    <td>
                                        <ActionsMenu
                                            onEditar={() => handleEditar(p)}
                                            onEliminar={() => setConfirmarId(p.id_categoria)}
                                        />
                                    </td>
                                </>
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>

            {mostrarCrear && (
                <CrearCategoriaModal
                    onClose={() => setMostrarCrear(false)}
                    onCrear={handleCrear}
                />
            )}

            {confirmarId && (
                <ConfirmModal
                    mensaje={`¿Eliminar "${categorias.find(p => p.id_categoria === confirmarId)?.nombre}"?`}
                    onConfirm={handleEliminar}
                    onCancel={() => setConfirmarId(null)}
                />
            )}
        </div>
    )
}

export default Categorias