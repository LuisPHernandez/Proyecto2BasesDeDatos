import { createContext, useMemo, useState } from 'react'

interface AuthUser {
    username: string
    nombre: string
}

interface AuthContextValue {
    user: AuthUser | null
    isAuthenticated: boolean
    login: (username: string, password: string) => boolean
    logout: () => void
}

const STORAGE_KEY = 'tienda-auth-user'

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<AuthUser | null>(() => {
        const savedUser = localStorage.getItem(STORAGE_KEY)
        return savedUser ? JSON.parse(savedUser) : null
    })

    const login = (username: string, password: string) => {
        if (username.trim() !== 'admin' || password !== 'admin123') {
            return false
        }

        const nextUser = {
            username: 'admin',
            nombre: 'Administrador'
        }

        setUser(nextUser)
        localStorage.setItem(STORAGE_KEY, JSON.stringify(nextUser))
        return true
    }

    const logout = () => {
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
