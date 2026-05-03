import styles from './ConfirmModal.module.css'

interface Props {
    mensaje: string
    onConfirm: () => void
    onCancel: () => void
}

function ConfirmModal({ mensaje, onConfirm, onCancel }: Props) {
    return (
        <div className={styles.overlay}>
            <div className={styles.modal}>
                <p className={styles.text}>{mensaje}</p>

                <div className={styles.actions}>
                    <button
                        className={styles.cancel}
                        onClick={onCancel}
                    >
                        Cancelar
                    </button>

                    <button
                        className={styles.confirm}
                        onClick={onConfirm}
                    >
                        Confirmar
                    </button>
                </div>
            </div>
        </div>
    )
}

export default ConfirmModal