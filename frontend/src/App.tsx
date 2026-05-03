import { BrowserRouter, Route, Routes } from "react-router-dom"
import Navbar from "./components/Navbar/Navbar"
import Home from "./pages/Home/Home"
import Inventario from "./pages/Inventario/Inventario"
import Proveedores from "./pages/Proveedores"
import VentaDetalle from "./pages/VentaDetalle/VentaDetalle"
import Ventas from "./pages/Ventas/Ventas"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navbar />} >
          <Route index element={<Home />} />
          <Route path="inventario" element={<Inventario />} />
          <Route path="ventas" element={<Ventas />} />
          <Route path="ventas/:id" element={<VentaDetalle />} />
          <Route path="proveedores" element={<Proveedores />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App