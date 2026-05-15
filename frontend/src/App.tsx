import { BrowserRouter, Route, Routes } from "react-router-dom"
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
          <Route index element={<Home />} />
          <Route path="inventario" element={<Inventario />} />
          <Route path="proveedores" element={<Proveedores />} />
          <Route path="categorias" element={<Categorias />} />
          <Route path="ventas" element={<Ventas />} />
          <Route path="ventas/:id" element={<VentaDetalle />} />
          <Route path="clientes" element={<Clientes />} />
          <Route path="empleados" element={<Empleados />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
