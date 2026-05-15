import { NavLink, Outlet, useNavigate } from "react-router-dom"
import { useAuth } from "../../context/useAuth"
import styles from './Navbar.module.css'

const links = [
    { to: "/", label: "Home" },
    { to: "/inventario", label: "Inventario" },
    { to: "/proveedores", label: "Proveedores" },
    { to: "/categorias", label: "Categorias" },
    { to: "/ventas", label: "Ventas" },
    { to: "/clientes", label: "Clientes" },
    { to: "/empleados", label: "Empleados" }
]

function Navbar() {
    const { user, logout } = useAuth()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        navigate('/login')
    }

    return (
        <div>
            <nav className={styles.navbar}>
                <ul className={styles.navList}>
                    {links.map(link => (
                        <li key={link.to} className={styles.navItem}>
                            <NavLink
                                to={link.to}
                                end={link.to === '/'}
                                className={({ isActive }) =>
                                    `${styles.navLink} ${isActive ? styles.activeLink : styles.inactiveLink}`
                                }
                            >
                                {link.label}
                            </NavLink>
                        </li>
                    ))}
                </ul>

                <div className={styles.session}>
                    <span>Sesión: {user?.nombre}</span>
                    <button className={styles.logoutButton} onClick={handleLogout}>
                        Cerrar sesión
                    </button>
                </div>
            </nav>

            <main className={styles.mainContent}>
                <Outlet />
            </main>
        </div>
    )
}

export default Navbar
