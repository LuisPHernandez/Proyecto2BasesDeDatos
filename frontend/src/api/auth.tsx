import { AUTH_STORAGE_KEY, getSessionToken } from "./client"

const BASE = "/api/auth"

export interface AuthUser {
    id_usuario: number
    username: string
    nombre: string
    rol: string
    session_token: string
}

export async function loginRequest(username: string, password: string): Promise<AuthUser> {
    const res = await fetch(`${BASE}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    })

    if (!res.ok) {
        const data = await res.json().catch(() => null)
        throw new Error(data?.detail ?? "Usuario o contraseña incorrectos")
    }

    return res.json()
}

export async function logoutRequest() {
    const token = getSessionToken()

    await fetch(`${BASE}/logout`, {
        method: "POST",
        headers: token ? { "X-Session-Token": token } : {},
    })

    localStorage.removeItem(AUTH_STORAGE_KEY)
}
