from __future__ import annotations

from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Region(Base):
    __tablename__ = 'regiones'

    id = Column(Integer, primary_key=True, index=True)
    numero_romano = Column(String(10), nullable=False)
    nombre = Column(String(80), nullable=False, unique=True)

    provincias = relationship('Provincia', back_populates='region')


class Provincia(Base):
    __tablename__ = 'provincias'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    region_id = Column(Integer, ForeignKey('regiones.id'), nullable=False)

    region = relationship('Region', back_populates='provincias')
    comunas = relationship('Comuna', back_populates='provincia')


class Comuna(Base):
    __tablename__ = 'comunas'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    provincia_id = Column(Integer, ForeignKey('provincias.id'), nullable=False)

    provincia = relationship('Provincia', back_populates='comunas')
    empleados = relationship('Empleado', back_populates='comuna')


class Departamento(Base):
    __tablename__ = 'departamentos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, default='')

    empleados = relationship('Empleado', back_populates='departamento')


class Cargo(Base):
    __tablename__ = 'cargos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, default='')

    empleados = relationship('Empleado', back_populates='cargo')


class Empleado(Base):
    __tablename__ = 'empleados'

    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(120), nullable=False)
    apellidos = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    telefono = Column(String(30), default='')
    direccion = Column(String(255), default='')
    fecha_ingreso = Column(Date, nullable=False)
    sueldo = Column(Float, nullable=False)
    activo = Column(Boolean, default=True)
    comuna_id = Column(Integer, ForeignKey('comunas.id'), nullable=False)
    cargo_id = Column(Integer, ForeignKey('cargos.id'), nullable=False)
    departamento_id = Column(Integer, ForeignKey('departamentos.id'), nullable=False)

    comuna = relationship('Comuna', back_populates='empleados')
    cargo = relationship('Cargo', back_populates='empleados')
    departamento = relationship('Departamento', back_populates='empleados')
