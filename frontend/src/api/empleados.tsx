import type { EmpleadoBase } from "../types"

const BASE = '/api/empleados/'

export async function getEmpleados() {
    const res = await fetch(BASE)
    if (!res.ok) throw new Error('Error al obtener empleados')
    return res.json()
}

export async function createEmpleado(data: EmpleadoBase) {
    const res = await fetch(BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error('Error al crear empleado')
    return res.json()
}

export async function updateEmpleado(id: number, data: EmpleadoBase) {
    const res = await fetch(`${BASE}${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error('Error al actualizar empleado')
    return res.json()
}

export async function deleteEmpleado(id: number) {
    const res = await fetch(`${BASE}${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Error al eliminar empleado')
}