import { Navigate } from 'react-router-dom'
import { type AppRole, canAccess } from '../../auth/permissions'
import { useAuth } from '../../context/useAuth'

interface Props {
    children: React.ReactNode
    roles?: AppRole[]
}

function ProtectedRoute({ children, roles }: Props) {
    const { isAuthenticated, user } = useAuth()

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />
    }

    if (roles && !canAccess(user?.rol, roles)) {
        return <Navigate to="/" replace />
    }

    return children
}

export default ProtectedRoute