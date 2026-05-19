import { NavLink, Outlet, useNavigate } from "react-router-dom"
import { canAccess, routeRoles, type AppRole } from "../../auth/permissions"
import { useAuth } from "../../context/useAuth"
import styles from './Navbar.module.css'

const links: { to: string; label: string; roles: AppRole[] }[] = [
    { to: "/", label: "Home", roles: routeRoles.home },
    { to: "/inventario", label: "Inventario", roles: routeRoles.inventario },
    { to: "/proveedores", label: "Proveedores", roles: routeRoles.proveedores },
    { to: "/categorias", label: "Categorias", roles: routeRoles.categorias },
    { to: "/ventas", label: "Ventas", roles: routeRoles.ventas },
    { to: "/clientes", label: "Clientes", roles: routeRoles.clientes },
    { to: "/empleados", label: "Empleados", roles: routeRoles.empleados }
]

function Navbar() {
    const { user, logout } = useAuth()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        navigate('/login')
    }

    const visibleLinks = links.filter(link => canAccess(user?.rol, link.roles))

    return (
        <div>
            <nav className={styles.navbar}>
                <ul className={styles.navList}>
                    {visibleLinks.map(link => (
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
                    <span>Sesión: {user?.nombre} ({user?.rol})</span>
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
