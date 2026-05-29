import { createContext, useMemo, useState } from 'react'
import { loginRequest, logoutRequest, type AuthUser } from '../api/auth'
import { AUTH_STORAGE_KEY } from '../api/client'

interface AuthContextValue {
    user: AuthUser | null
    isAuthenticated: boolean
    login: (username: string, password: string) => Promise<boolean>
    logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<AuthUser | null>(() => {
        const savedUser = localStorage.getItem(AUTH_STORAGE_KEY)
        return savedUser ? JSON.parse(savedUser) : null
    })

    const login = async (username: string, password: string) => {
        try {
            const nextUser = await loginRequest(username, password)

            setUser(nextUser)
            localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(nextUser))

            return true
        } catch {
            return false
        }
    }

    const logout = () => {
        logoutRequest().catch(() => { })
        setUser(null)
        localStorage.removeItem(AUTH_STORAGE_KEY)
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
