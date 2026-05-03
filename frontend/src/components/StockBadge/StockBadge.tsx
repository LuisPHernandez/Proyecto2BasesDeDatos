import WarningIcon from '../../assets/WarningIcon.svg?react'
import styles from './StockBadge.module.css'

interface Props {
    show: boolean
}

function StockBadge({ show }: Props) {
    if (!show) return null
    return (
        <span className={styles.badge}>
            <WarningIcon />
        </span>
    )
}

export default StockBadge