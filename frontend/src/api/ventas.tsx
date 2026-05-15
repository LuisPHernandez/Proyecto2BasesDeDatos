import type { VentaCreateInput, VentaSummary } from "../types"

const BASE = '/api/ventas/'

export async function getVentas(fecha_inicio: Date, fecha_fin: Date) {
    const res = await fetch(
        `${BASE}?fecha_inicio=${fecha_inicio.toISOString()}&fecha_fin=${fecha_fin.toISOString()}`
    )
    if (!res.ok) throw new Error('Error al obtener ventas')
    return res.json()
}

export async function getVentaById(id: number) {
    const res = await fetch(`${BASE}${id}`)
    if (!res.ok) throw new Error('Error al obtener venta')
    return res.json()
}

export async function getVentaProductosById(id: number) {
    const res = await fetch(`${BASE}${id}/productos`)
    if (!res.ok) throw new Error('Error al obtener productos de la venta')
    return res.json()
}

export async function createVenta(data: VentaCreateInput): Promise<VentaSummary> {
    const res = await fetch(BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail ?? 'Error al crear venta')
    }
    return res.json()
}

export async function deleteVenta(id: number) {
    const res = await fetch(`${BASE}${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Error al eliminar venta')
}