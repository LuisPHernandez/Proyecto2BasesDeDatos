export type RangoFecha = '1s' | '2s' | '1m'

export function getRango(rango: RangoFecha): { inicio: Date, fin: Date } {
    const fin = new Date()
    const inicio = new Date()
    if (rango === '1s') inicio.setDate(fin.getDate() - 7)
    if (rango === '2s') inicio.setDate(fin.getDate() - 14)
    if (rango === '1m') inicio.setMonth(fin.getMonth() - 1)
    return { inicio, fin }
}