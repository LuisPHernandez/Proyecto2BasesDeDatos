import type { ProveedorBase } from "../types"

const BASE = '/api/proveedores/'

export async function getProveedores() {
    const res = await fetch(BASE)
    if (!res.ok) throw new Error('Error al obtener proveedores')
    return res.json()
}

export async function createProveedor(data: ProveedorBase) {
    const res = await fetch(BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error('Error al crear proveedor')
    return res.json()
}

export async function updateProveedor(id: number, data: ProveedorBase) {
    const res = await fetch(`${BASE}${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error('Error al actualizar proveedor')
    return res.json()
}

export async function deleteProveedor(id: number) {
    const res = await fetch(`${BASE}${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Error al eliminar proveedor')
}