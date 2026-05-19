from sqlalchemy import Column, Integer, Text, Numeric, ForeignKey, TIMESTAMP  # pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship  # pyrefly: ignore [missing-import]
from database import Base

class Proveedor(Base):
    __tablename__ = "proveedor"

    id_proveedor = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)

    productos = relationship("Producto", back_populates="proveedor")

class Categoria(Base):
    __tablename__ = "categoria"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)

    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = "producto"

    id_producto = Column(Integer, primary_key=True, index=True)
    id_proveedor = Column(Integer, ForeignKey("proveedor.id_proveedor", ondelete="CASCADE"), nullable=False)
    nombre = Column(Text, nullable=False, unique=True)
    unidades_disponibles = Column(Integer, nullable=False)
    precio_venta = Column(Numeric(10, 2), nullable=False)
    precio_compra = Column(Numeric(10, 2), nullable=False)
    id_categoria = Column(Integer, ForeignKey("categoria.id_categoria", ondelete="CASCADE"), nullable=False)

    proveedor = relationship("Proveedor", back_populates="productos")
    categoria = relationship("Categoria", back_populates="productos")
    detalles = relationship("DetalleVenta", back_populates="producto")

class Empleado(Base):
    __tablename__ = "empleado"

    id_empleado = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)

    ventas = relationship("Venta", back_populates="empleado")

class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)

    ventas = relationship("Venta", back_populates="cliente")

class Venta(Base):
    __tablename__ = "venta"

    id_venta = Column(Integer, primary_key=True, index=True)
    id_empleado = Column(Integer, ForeignKey("empleado.id_empleado", ondelete="CASCADE"), nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente", ondelete="CASCADE"), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    empleado = relationship("Empleado", back_populates="ventas")
    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = "detalle_venta"

    id_venta = Column(Integer, ForeignKey("venta.id_venta", ondelete="CASCADE"), primary_key=True)
    id_producto = Column(Integer, ForeignKey("producto.id_producto", ondelete="CASCADE"), primary_key=True)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    cantidad = Column(Integer, nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")

class UsuarioApp(Base):
    __tablename__ = "usuario_app"

    id_usuario = Column(Integer, primary_key=True, index=True)
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    nombre = Column(Text, nullable=False)
    rol = Column(Text, nullable=False)
