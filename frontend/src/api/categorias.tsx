import type { CategoriaBase, CategoriaIncome } from "../types"

const BASE = '/api/categorias/'

export async function getCategorias() {
    const res = await fetch(BASE)
    if (!res.ok) throw new Error('Error al obtener categorias')
    return res.json()
}

export async function getCategoriasWithIncome(): Promise<CategoriaIncome[]> {
    const res = await fetch(`${BASE}ingresos`)
    if (!res.ok) throw new Error('Error al obtener categorias con sus ingresos')
    return res.json()
}

export async function createCategoria(data: CategoriaBase) {
    const res = await fetch(BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error('Error al crear categoria')
    return res.json()
}

export async function updateCategoria(id: number, data: CategoriaBase) {
    const res = await fetch(`${BASE}${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error('Error al actualizar categoria')
    return res.json()
}

export async function deleteCategoria(id: number) {
    const res = await fetch(`${BASE}${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Error al eliminar categoria')
}