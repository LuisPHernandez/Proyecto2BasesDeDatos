export async function apiErrorMessage(res: Response, fallback: string) {
    try {
        const data = await res.json()
        return data?.detail ?? fallback
    } catch {
        return fallback
    }
}