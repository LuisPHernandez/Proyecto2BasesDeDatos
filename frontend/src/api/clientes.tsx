import type { ClienteBase } from "../types"

const BASE = '/api/clientes/'

export async function getClientes() {
    const res = await fetch(BASE)
    if (!res.ok) throw new Error('Error al obtener clientes')
    return res.json()
}

export async function createCliente(data: ClienteBase) {
    const res = await fetch(BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error('Error al crear cliente')
    return res.json()
}

export async function updateCliente(id: number, data: ClienteBase) {
    const res = await fetch(`${BASE}${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error('Error al actualizar cliente')
    return res.json()
}

export async function deleteCliente(id: number) {
    const res = await fetch(`${BASE}${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Error al eliminar cliente')
}