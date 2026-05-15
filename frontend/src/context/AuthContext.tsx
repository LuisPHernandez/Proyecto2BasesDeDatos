import { createContext, useContext, useEffect, useMemo, useState } from 'react'

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
    const [user, setUser] = useState<AuthUser | null>(null)

    useEffect(() => {
        const savedUser = localStorage.getItem(STORAGE_KEY)
        if (savedUser) {
            setUser(JSON.parse(savedUser))
        }
    }, [])

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

function useAuth() {
    const context = useContext(AuthContext)

    if (!context) {
        throw new Error('useAuth debe usarse dentro de AuthProvider')
    }

    return context
}

export { AuthProvider, useAuth }

