import { BrowserRouter, Route, Routes } from "react-router-dom"
import { routeRoles } from "./auth/permissions"
import Navbar from "./components/Navbar/Navbar"
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute"
import Categorias from "./pages/Categorias/Categorias"
import Clientes from "./pages/Clientes/Clientes"
import Empleados from "./pages/Empleados/Empleados"
import Home from "./pages/Home/Home"
import Inventario from "./pages/Inventario/Inventario"
import Login from "./pages/Login/Login"
import Proveedores from "./pages/Proveedores/Proveedores"
import VentaDetalle from "./pages/VentaDetalle/VentaDetalle"
import Ventas from "./pages/Ventas/Ventas"

function App() {
  return (
    <BrowserRouter basename="/proyecto2">
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Navbar />
            </ProtectedRoute>
          }
        >
          <Route index element={<ProtectedRoute><Home /></ProtectedRoute>} />

          <Route
            path="inventario"
            element={<ProtectedRoute roles={routeRoles.inventario}><Inventario /></ProtectedRoute>}
          />

          <Route
            path="proveedores"
            element={<ProtectedRoute roles={routeRoles.proveedores}><Proveedores /></ProtectedRoute>}
          />

          <Route
            path="categorias"
            element={<ProtectedRoute roles={routeRoles.categorias}><Categorias /></ProtectedRoute>}
          />

          <Route
            path="ventas"
            element={<ProtectedRoute roles={routeRoles.ventas}><Ventas /></ProtectedRoute>}
          />

          <Route
            path="ventas/:id"
            element={<ProtectedRoute roles={routeRoles.ventas}><VentaDetalle /></ProtectedRoute>}
          />

          <Route
            path="clientes"
            element={<ProtectedRoute roles={routeRoles.clientes}><Clientes /></ProtectedRoute>}
          />

          <Route
            path="empleados"
            element={<ProtectedRoute roles={routeRoles.empleados}><Empleados /></ProtectedRoute>}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
