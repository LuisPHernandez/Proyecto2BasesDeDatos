import { useState } from 'react'
import type { ProveedorBase } from '../../types'
import modalStyles from '../Modal/Modal.module.css'
import Modal from './Modal'

interface Props {
    onClose: () => void
    onCrear: (data: ProveedorBase) => Promise<void>
}

function CrearProveedorModal({ onClose, onCrear }: Props) {
    const [form, setForm] = useState<ProveedorBase>({ nombre: '', email: '' })
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)

    const handleSubmit = async () => {
        if (!form.nombre.trim() || !form.email.trim()) {
            setError('Todos los campos son requeridos')
            return
        }
        if (form.nombre.length > 30) {
            setError('El nombre del proveedor no puede exceder los 30 caracteres')
            return
        }
        if (form.nombre.length < 2) {
            setError('El nombre del proveedor debe tener al menos 2 caracteres')
            return
        }
        if (form.email.length > 30) {
            setError('El email del proveedor no puede exceder los 30 caracteres')
            return
        }
        if (form.email.length < 3) {
            setError('El email del proveedor debe tener al menos 3 caracteres')
            return
        }
        if (!form.email.includes('@')) {
            setError('El email del proveedor debe contener un @')
            return
        }
        if (form.email.trim().includes(' ')) {
            setError('El email del proveedor no puede contener espacios')
            return
        }

        setLoading(true)
        try {
            await onCrear(form)
            onClose()
        } catch (e: any) {
            setError(e.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <Modal titulo="Nuevo proveedor" onClose={onClose}>
            <div className={modalStyles.field}>
                <label>Nombre</label>
                <input
                    value={form.nombre}
                    onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))}
                    placeholder="Nombre del proveedor"
                />
            </div>
            <div className={modalStyles.field}>
                <label>Email</label>
                <input
                    type="email"
                    value={form.email}
                    onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
                    placeholder="correo@ejemplo.com"
                />
            </div>

            {error && <p style={{ color: '#dc2626', fontSize: '0.85rem', margin: 0 }}>{error}</p>}

            <div className={modalStyles.actions}>
                <button className={modalStyles.cancelButton} onClick={onClose}>Cancelar</button>
                <button className={modalStyles.submitButton} onClick={handleSubmit} disabled={loading}>
                    {loading ? 'Creando...' : 'Crear proveedor'}
                </button>
            </div>
        </Modal>
    )
}

export default CrearProveedorModal