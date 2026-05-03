import styles from './Modal.module.css'

interface Props {
    titulo: string
    onClose: () => void
    children: React.ReactNode
}

function Modal({ titulo, onClose, children }: Props) {
    return (
        <div className={styles.overlay} onClick={onClose}>
            <div className={styles.modal} onClick={e => e.stopPropagation()}>
                <div className={styles.modalHeader}>
                    <h2>{titulo}</h2>
                    <button className={styles.closeButton} onClick={onClose}>✕</button>
                </div>
                {children}
            </div>
        </div>
    )
}

export default Modal