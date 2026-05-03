import type { ProductoBase } from "../types"

const BASE = '/api/productos/'

export async function getProductos() {
    const res = await fetch(BASE)
    if (!res.ok) throw new Error('Error al obtener productos')
    return res.json()
}

export async function getLowStockIds() {
    const res = await fetch(`${BASE}low-stock`)
    if (!res.ok) throw new Error('Error al obtener productos con bajo stock')
    return res.json()
}

export async function getProductoById(id: number) {
    const res = await fetch(`${BASE}${id}`)
    if (!res.ok) throw new Error('Error al obtener producto')
    return res.json()
}

export async function createProducto(data: ProductoBase) {
    const res = await fetch(BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error('Error al crear producto')
    return res.json()
}

export async function updateProducto(id: number, data: ProductoBase) {
    const res = await fetch(`${BASE}${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error('Error al actualizar producto')
    return res.json()
}

export async function deleteProducto(id: number) {
    const res = await fetch(`${BASE}/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Error al eliminar producto')
    return res.json()
}