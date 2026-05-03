import { NavLink, Outlet } from "react-router-dom"
import styles from './Navbar.module.css'

const links = [
    { to: "/", label: "Home" },
    { to: "/inventario", label: "Inventario" },
    { to: "/ventas", label: "Ventas" },
    { to: "/proveedores", label: "Proveedores" }
]

function Navbar() {
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
                            >{link.label}</NavLink>
                        </li>
                    ))}
                </ul>
            </nav>
            <main className={styles.mainContent}>
                <Outlet />
            </main>
        </div>
    )
}

export default Navbar