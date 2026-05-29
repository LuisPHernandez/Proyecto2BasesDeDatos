import { apiFetch } from "./client"
import type { ProductoBase, ProductoTop } from "../types"
import { apiErrorMessage } from "./errors"

const BASE = '/api/productos/'

export async function getProductos() {
    const res = await apiFetch(BASE)
    if (!res.ok) throw new Error('Error al obtener productos')
    return res.json()
}

export async function getLowStockIds() {
    const res = await apiFetch(`${BASE}low-stock`)
    if (!res.ok) throw new Error('Error al obtener productos con bajo stock')
    return res.json()
}

export async function getProductoById(id: number) {
    const res = await apiFetch(`${BASE}${id}`)
    if (!res.ok) throw new Error('Error al obtener producto')
    return res.json()
}

export async function getTopMes(): Promise<ProductoTop[]> {
    const res = await apiFetch(`${BASE}top-mes`)
    if (!res.ok) throw new Error('Error al obtener top productos')
    return res.json()
}

export async function createProducto(data: ProductoBase) {
    const res = await apiFetch(BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error(await apiErrorMessage(res, 'Error al crear producto'))
    return res.json()
}

export async function updateProducto(id: number, data: ProductoBase) {
    const res = await apiFetch(`${BASE}${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error(await apiErrorMessage(res, 'Error al actualizar producto'))
    return res.json()
}

export async function deleteProducto(id: number) {
    const res = await apiFetch(`${BASE}${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error(await apiErrorMessage(res, 'Error al eliminar producto'))
}
