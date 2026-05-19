import { createContext, useMemo, useState } from 'react'
import { loginRequest, logoutRequest } from '../api/auth'

interface AuthUser {
    id_usuario: number
    username: string
    nombre: string
    rol: string
}

interface AuthContextValue {
    user: AuthUser | null
    isAuthenticated: boolean
    login: (username: string, password: string) => Promise<boolean>
    logout: () => void
}

const STORAGE_KEY = 'tienda-auth-user'

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<AuthUser | null>(() => {
        const savedUser = localStorage.getItem(STORAGE_KEY)
        return savedUser ? JSON.parse(savedUser) : null
    })

    const login = async (username: string, password: string) => {
        try {
            const nextUser = await loginRequest(username, password)

            setUser(nextUser)
            localStorage.setItem(STORAGE_KEY, JSON.stringify(nextUser))

            return true
        } catch {
            return false
        }
    }

    const logout = () => {
        logoutRequest().catch(() => { })
        setUser(null)
        localStorage.removeItem(STORAGE_KEY)
    }

    const value = useMemo(
        () => ({
            user,
            isAuthenticated: Boolean(user),
            login,
            logout
        }),
        [user]
    )

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}

export { AuthContext, AuthProvider }

