import { useState } from 'react'
import type { EmpleadoBase } from '../../types'
import modalStyles from '../Modal/Modal.module.css'
import Modal from './Modal'

interface Props {
    onClose: () => void
    onCrear: (data: EmpleadoBase) => Promise<void>
}

function CrearEmpleadoModal({ onClose, onCrear }: Props) {
    const [form, setForm] = useState<EmpleadoBase>({ nombre: '' })
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)

    const handleSubmit = async () => {
        if (!form.nombre.trim()) {
            setError('El campo de nombre es requerido')
            return
        }
        if (form.nombre.length > 30) {
            setError('El nombre del empleado no puede exceder los 30 caracteres')
            return
        }
        if (form.nombre.length < 2) {
            setError('El nombre del empleado debe tener al menos 2 caracteres')
            return
        }
        setLoading(true)
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
        <Modal titulo="Nuevo empleado" onClose={onClose}>
            <div className={modalStyles.field}>
                <label>Nombre</label>
                <input
                    value={form.nombre}
                    onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))}
                    placeholder="Nombre del empleado"
                />
            </div>

            {error && <p style={{ color: '#dc2626', fontSize: '0.85rem', margin: 0 }}>{error}</p>}

            <div className={modalStyles.actions}>
                <button className={modalStyles.cancelButton} onClick={onClose}>Cancelar</button>
                <button className={modalStyles.submitButton} onClick={handleSubmit} disabled={loading}>
                    {loading ? 'Creando...' : 'Crear empleado'}
                </button>
            </div>
        </Modal>
    )
}

export default CrearEmpleadoModal