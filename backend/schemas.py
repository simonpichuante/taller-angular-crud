from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class DepartamentoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: str = ''


class DepartamentoCreate(DepartamentoBase):
    pass


class DepartamentoUpdate(DepartamentoBase):
    pass


class Departamento(DepartamentoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CargoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: str = ''


class CargoCreate(CargoBase):
    pass


class CargoUpdate(CargoBase):
    pass


class Cargo(CargoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Region(BaseModel):
    id: int
    numero_romano: str
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class Provincia(BaseModel):
    id: int
    nombre: str
    region_id: int

    model_config = ConfigDict(from_attributes=True)


class Comuna(BaseModel):
    id: int
    nombre: str
    provincia_id: int
    provincia: str
    region_id: int
    region: str

    model_config = ConfigDict(from_attributes=True)


class EmpleadoBase(BaseModel):
    rut: str = Field(..., min_length=5, max_length=20)
    nombres: str = Field(..., min_length=1, max_length=120)
    apellidos: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    telefono: str = ''
    direccion: str = ''
    fecha_ingreso: date
    sueldo: Optional[float] = None
    activo: bool = True
    comuna_id: Optional[int] = None
    cargo_id: Optional[int] = None
    departamento_id: Optional[int] = None


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(EmpleadoBase):
    pass


class Empleado(EmpleadoBase):
    id: int
    comuna: str = ''
    provincia: str = ''
    region: str = ''
    cargo: str = ''
    departamento: str = ''

    model_config = ConfigDict(from_attributes=True)
