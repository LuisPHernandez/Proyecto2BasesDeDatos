import { useState } from 'react'
import type { CategoriaBase } from '../../types'
import modalStyles from '../Modal/Modal.module.css'
import Modal from './Modal'

interface Props {
    onClose: () => void
    onCrear: (data: CategoriaBase) => Promise<void>
}

function CrearCategoriaModal({ onClose, onCrear }: Props) {
    const [form, setForm] = useState<CategoriaBase>({ nombre: '' })
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)

    const handleSubmit = async () => {
        if (!form.nombre.trim()) {
            setError('El nombre de la categoría es requerido')
            return
        }
        if (form.nombre.trim().length > 30) {
            setError('El nombre de la categoría no puede exceder los 30 caracteres')
            return
        }
        if (form.nombre.trim().length < 2) {
            setError('El nombre de la categoría debe tener al menos 2 caracteres')
            return
        }

        setLoading(true)
        try {
            await onCrear(form)
            onClose()
        } catch (e) {
            setError(e instanceof Error ? e.message : 'Ocurri� un error')
        } finally {
            setLoading(false)
        }
    }

    return (
        <Modal titulo="Nueva categoría" onClose={onClose}>
            <div className={modalStyles.field}>
                <label>Nombre</label>
                <input
                    value={form.nombre}
                    onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))}
                    placeholder="Nombre de la categoría"
                />
            </div>

            {error && <p style={{ color: '#dc2626', fontSize: '0.85rem', margin: 0 }}>{error}</p>}

            <div className={modalStyles.actions}>
                <button className={modalStyles.cancelButton} onClick={onClose}>Cancelar</button>
                <button className={modalStyles.submitButton} onClick={handleSubmit} disabled={loading}>
                    {loading ? 'Creando...' : 'Crear categoría'}
                </button>
            </div>
        </Modal>
    )
}

export default CrearCategoriaModal