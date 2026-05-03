import { useEffect, useRef, useState } from 'react';
import ActionsMenuIcon from "../../assets/ActionsMenuIcon.svg?react";
import styles from './ActionsMenu.module.css';

interface Props {
    onEditar?: () => void
    onEliminar: () => void
}

function ActionsMenu({ onEditar, onEliminar }: Props) {
    const [open, setOpen] = useState(false)
    const ref = useRef<HTMLDivElement>(null)

    useEffect(() => {
        const handler = (e: MouseEvent) => {
            if (ref.current && !ref.current.contains(e.target as Node)) {
                setOpen(false)
            }
        }
        document.addEventListener('mousedown', handler)
        return () => document.removeEventListener('mousedown', handler)
    }, [])

    return (
        <div ref={ref} className={styles.container}>
            <button
                className={styles.trigger}
                onClick={() => setOpen(!open)}
            >
                <ActionsMenuIcon />
            </button>

            {open && (
                <div className={styles.menu}>
                    {onEditar && (
                        <button
                            className={styles.item}
                            onClick={() => { onEditar?.(); setOpen(false) }}
                        >
                            Editar
                        </button>
                    )}

                    <button
                        className={`${styles.item} ${styles.delete}`}
                        onClick={() => { onEliminar(); setOpen(false) }}
                    >
                        Eliminar
                    </button>
                </div>
            )}
        </div>
    )
}

export default ActionsMenu