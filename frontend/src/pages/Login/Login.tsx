import { type SyntheticEvent, useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/useAuth'
import styles from './Login.module.css'

function Login() {
    const { isAuthenticated, login } = useAuth()
    const navigate = useNavigate()
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState<string | null>(null)

    if (isAuthenticated) {
        return <Navigate to="/" replace />
    }

    const handleSubmit = (e: SyntheticEvent<HTMLFormElement>) => {
        e.preventDefault()

        const ok = login(username, password)

        if (!ok) {
            setError('Usuario o contraseña incorrectos')
            return
        }

        navigate('/')
    }

    return (
        <main className={styles.page}>
            <section className={styles.card}>
                <h1 className={styles.title}>Iniciar sesión</h1>
                <p className={styles.subtitle}>Sistema de inventario y ventas</p>

                <form className={styles.form} onSubmit={handleSubmit}>
                    <label className={styles.field}>
                        Usuario
                        <input
                            value={username}
                            onChange={e => setUsername(e.target.value)}
                            autoComplete="username"
                        />
                    </label>

                    <label className={styles.field}>
                        Contraseña
                        <input
                            type="password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            autoComplete="current-password"
                        />
                    </label>

                    {error && <p className={styles.error}>{error}</p>}

                    <button className={styles.button} type="submit">
                        Entrar
                    </button>
                </form>

                <p className={styles.help}>Usuario: admin | Contraseña: admin123</p>
            </section>
        </main>
    )
}

export default Login
