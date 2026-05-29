export const AUTH_STORAGE_KEY = 'tienda-auth-user'

interface StoredAuthUser {
    session_token?: string
}

export function getSessionToken() {
    const savedUser = localStorage.getItem(AUTH_STORAGE_KEY)

    if (!savedUser) {
        return null
    }

    try {
        const user = JSON.parse(savedUser) as StoredAuthUser
        return user.session_token ?? null
    } catch {
        return null
    }
}

export function authHeaders(headers?: HeadersInit): HeadersInit {
    const token = getSessionToken()

    return {
        ...(headers ?? {}),
        ...(token ? { 'X-Session-Token': token } : {}),
    }
}

export function apiFetch(input: RequestInfo | URL, init?: RequestInit) {
    return fetch(input, {
        ...init,
        headers: authHeaders(init?.headers),
    })
}
