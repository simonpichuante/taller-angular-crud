from __future__ import annotations

from datetime import date
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

try:
    from .database import get_db, init_db
    from .models import Cargo as CargoModel, Comuna as ComunaModel, Departamento as DepartamentoModel, Empleado as EmpleadoModel, Provincia as ProvinciaModel, Region as RegionModel
    from .schemas import (
        Cargo as CargoSchema,
        CargoCreate,
        CargoUpdate,
        Comuna as ComunaSchema,
        Departamento as DepartamentoSchema,
        DepartamentoCreate,
        DepartamentoUpdate,
        Empleado as EmpleadoSchema,
        EmpleadoCreate,
        EmpleadoUpdate,
        Provincia as ProvinciaSchema,
        Region as RegionSchema,
    )
except ImportError:
    from database import get_db, init_db
    from models import Cargo as CargoModel, Comuna as ComunaModel, Departamento as DepartamentoModel, Empleado as EmpleadoModel, Provincia as ProvinciaModel, Region as RegionModel
    from schemas import (
        Cargo as CargoSchema,
        CargoCreate,
        CargoUpdate,
        Comuna as ComunaSchema,
        Departamento as DepartamentoSchema,
        DepartamentoCreate,
        DepartamentoUpdate,
        Empleado as EmpleadoSchema,
        EmpleadoCreate,
        EmpleadoUpdate,
        Provincia as ProvinciaSchema,
        Region as RegionSchema,
    )

app = FastAPI(title='Control de Empleados API', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:4200', 'http://127.0.0.1:4200'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
def startup_event() -> None:
    init_db()
    seed_base_data()


def seed_base_data() -> None:
    from database import SessionLocal

    db = SessionLocal()
    try:
        regions = db.execute(select(RegionModel)).scalars().all()
        if not regions:
            data = [
                RegionModel(id=1, numero_romano='I', nombre='Tarapacá'),
                RegionModel(id=2, numero_romano='II', nombre='Antofagasta'),
                RegionModel(id=3, numero_romano='III', nombre='Atacama'),
                RegionModel(id=4, numero_romano='IV', nombre='Coquimbo'),
                RegionModel(id=5, numero_romano='V', nombre='Valparaíso'),
                RegionModel(id=6, numero_romano='VI', nombre='Libertador General Bernardo O’Higgins'),
                RegionModel(id=7, numero_romano='VII', nombre='Maule'),
                RegionModel(id=8, numero_romano='VIII', nombre='Biobío'),
                RegionModel(id=9, numero_romano='IX', nombre='La Araucanía'),
                RegionModel(id=10, numero_romano='X', nombre='Los Lagos'),
                RegionModel(id=11, numero_romano='XI', nombre='Aysén'),
                RegionModel(id=12, numero_romano='XII', nombre='Magallanes y Antártica Chilena'),
                RegionModel(id=13, numero_romano='XIII', nombre='Metropolitana de Santiago'),
                RegionModel(id=14, numero_romano='XIV', nombre='Los Ríos'),
                RegionModel(id=15, numero_romano='XV', nombre='Arica y Parinacota'),
                RegionModel(id=16, numero_romano='XVI', nombre='Ñuble'),
            ]
            db.add_all(data)

        provinces = db.execute(select(ProvinciaModel)).scalars().all()
        if not provinces:
            db.add_all(
                [
                    ProvinciaModel(id=1, nombre='Iquique', region_id=1),
                    ProvinciaModel(id=2, nombre='Antofagasta', region_id=2),
                    ProvinciaModel(id=3, nombre='Santiago', region_id=13),
                    ProvinciaModel(id=4, nombre='Concepción', region_id=8),
                    ProvinciaModel(id=5, nombre='Valdivia', region_id=14),
                ]
            )

        communes = db.execute(select(ComunaModel)).scalars().all()
        if not communes:
            db.add_all(
                [
                    ComunaModel(id=1, nombre='Iquique', provincia_id=1),
                    ComunaModel(id=2, nombre='Antofagasta', provincia_id=2),
                    ComunaModel(id=3, nombre='Santiago', provincia_id=3),
                    ComunaModel(id=4, nombre='Concepción', provincia_id=4),
                    ComunaModel(id=5, nombre='Valdivia', provincia_id=5),
                ]
            )

        if db.execute(select(DepartamentoModel.id)).first() is None:
            db.add_all([
                DepartamentoModel(id=1, nombre='Tecnología', descripcion='Equipo de software'),
                DepartamentoModel(id=2, nombre='Recursos Humanos', descripcion='Gestión de personas'),
                DepartamentoModel(id=3, nombre='Administración', descripcion='Soporte financiero y administrativo'),
            ])

        if db.execute(select(CargoModel.id)).first() is None:
            db.add_all([
                CargoModel(id=1, nombre='Desarrollador', descripcion='Desarrollo de software'),
                CargoModel(id=2, nombre='Analista', descripcion='Análisis de negocio'),
                CargoModel(id=3, nombre='Administrador', descripcion='Administración de procesos'),
            ])

        if db.execute(select(EmpleadoModel.id)).first() is None:
            db.add(
                EmpleadoModel(
                    id=1,
                    rut='12345678-5',
                    nombres='Ana',
                    apellidos='García',
                    email='ana@empresa.cl',
                    telefono='+56912345678',
                    direccion='Av. Principal 123',
                    fecha_ingreso=date(2024, 1, 10),
                    sueldo=1500000,
                    activo=True,
                    comuna_id=3,
                    cargo_id=1,
                    departamento_id=1,
                )
            )

        db.commit()
    finally:
        db.close()


@app.get('/regiones', response_model=List[RegionSchema])
def listar_regiones(db: Session = Depends(get_db)):
    query = select(RegionModel).order_by(RegionModel.id)
    return db.execute(query).scalars().all()


@app.get('/regiones/{region_id}/provincias', response_model=List[ProvinciaSchema])
def listar_provincias(region_id: int, db: Session = Depends(get_db)):
    query = select(ProvinciaModel).where(ProvinciaModel.region_id == region_id).order_by(ProvinciaModel.id)
    return db.execute(query).scalars().all()


@app.get('/provincias/{provincia_id}/comunas', response_model=List[ComunaSchema])
def listar_comunas(provincia_id: int, db: Session = Depends(get_db)):
    query = (
        select(ComunaModel, ProvinciaModel, RegionModel)
        .join(ProvinciaModel, ProvinciaModel.id == ComunaModel.provincia_id)
        .join(RegionModel, RegionModel.id == ProvinciaModel.region_id)
        .where(ProvinciaModel.id == provincia_id)
        .order_by(ComunaModel.id)
    )
    rows = db.execute(query).all()
    return [
        ComunaSchema(
            id=comuna.id,
            nombre=comuna.nombre,
            provincia_id=comuna.provincia_id,
            provincia=provincia.nombre,
            region_id=region.id,
            region=region.nombre,
        )
        for comuna, provincia, region in rows
    ]


@app.get('/comunas/{comuna_id}', response_model=ComunaSchema)
def detalle_comuna(comuna_id: int, db: Session = Depends(get_db)):
    row = (
        db.execute(
            select(ComunaModel, ProvinciaModel, RegionModel)
            .join(ProvinciaModel, ProvinciaModel.id == ComunaModel.provincia_id)
            .join(RegionModel, RegionModel.id == ProvinciaModel.region_id)
            .where(ComunaModel.id == comuna_id)
        )
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail='Comuna no encontrada')
    comuna, provincia, region = row
    return ComunaSchema(
        id=comuna.id,
        nombre=comuna.nombre,
        provincia_id=provincia.id,
        provincia=provincia.nombre,
        region_id=region.id,
        region=region.nombre,
    )


@app.get('/departamentos', response_model=List[DepartamentoSchema])
def listar_departamentos(db: Session = Depends(get_db)):
    return db.execute(select(DepartamentoModel).order_by(DepartamentoModel.id)).scalars().all()


@app.post('/departamentos', response_model=DepartamentoSchema, status_code=status.HTTP_201_CREATED)
def crear_departamento(datos: DepartamentoCreate, db: Session = Depends(get_db)):
    registro = DepartamentoModel(**datos.model_dump())
    db.add(registro)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='Ya existe un registro con ese nombre')
    db.refresh(registro)
    return registro


@app.put('/departamentos/{departamento_id}', response_model=DepartamentoSchema)
def actualizar_departamento(departamento_id: int, datos: DepartamentoUpdate, db: Session = Depends(get_db)):
    registro = db.get(DepartamentoModel, departamento_id)
    if registro is None:
        raise HTTPException(status_code=404, detail='Departamento no encontrado')
    for campo, valor in datos.model_dump().items():
        setattr(registro, campo, valor)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='Ya existe un registro con ese nombre')
    db.refresh(registro)
    return registro


@app.delete('/departamentos/{departamento_id}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_departamento(departamento_id: int, db: Session = Depends(get_db)):
    departamento = db.get(DepartamentoModel, departamento_id)
    if departamento is None:
        raise HTTPException(status_code=404, detail='Departamento no encontrado')
    if departamento.empleados:
        raise HTTPException(status_code=409, detail='El registro tiene empleados asociados')
    db.delete(departamento)
    db.commit()


@app.get('/cargos', response_model=List[CargoSchema])
def listar_cargos(db: Session = Depends(get_db)):
    return db.execute(select(CargoModel).order_by(CargoModel.id)).scalars().all()


@app.post('/cargos', response_model=CargoSchema, status_code=status.HTTP_201_CREATED)
def crear_cargo(datos: CargoCreate, db: Session = Depends(get_db)):
    registro = CargoModel(**datos.model_dump())
    db.add(registro)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='Ya existe un registro con ese nombre')
    db.refresh(registro)
    return registro


@app.put('/cargos/{cargo_id}', response_model=CargoSchema)
def actualizar_cargo(cargo_id: int, datos: CargoUpdate, db: Session = Depends(get_db)):
    registro = db.get(CargoModel, cargo_id)
    if registro is None:
        raise HTTPException(status_code=404, detail='Cargo no encontrado')
    for campo, valor in datos.model_dump().items():
        setattr(registro, campo, valor)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='Ya existe un registro con ese nombre')
    db.refresh(registro)
    return registro


@app.delete('/cargos/{cargo_id}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cargo(cargo_id: int, db: Session = Depends(get_db)):
    cargo = db.get(CargoModel, cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail='Cargo no encontrado')
    if cargo.empleados:
        raise HTTPException(status_code=409, detail='El registro tiene empleados asociados')
    db.delete(cargo)
    db.commit()


@app.get('/empleados', response_model=List[EmpleadoSchema])
def listar_empleados(
    buscar: str = Query('', alias='buscar'),
    db: Session = Depends(get_db),
):
    query = (
        select(
            EmpleadoModel,
            ComunaModel.nombre.label('comuna_nombre'),
            ProvinciaModel.nombre.label('provincia_nombre'),
            RegionModel.nombre.label('region_nombre'),
            CargoModel.nombre.label('cargo_nombre'),
            DepartamentoModel.nombre.label('departamento_nombre'),
        )
        .join(ComunaModel, ComunaModel.id == EmpleadoModel.comuna_id)
        .join(ProvinciaModel, ProvinciaModel.id == ComunaModel.provincia_id)
        .join(RegionModel, RegionModel.id == ProvinciaModel.region_id)
        .join(CargoModel, CargoModel.id == EmpleadoModel.cargo_id)
        .join(DepartamentoModel, DepartamentoModel.id == EmpleadoModel.departamento_id)
    )
    if buscar:
        termino = f'%{buscar.lower()}%'
        query = query.where(
            or_(
                func.lower(EmpleadoModel.nombres).like(termino),
                func.lower(EmpleadoModel.apellidos).like(termino),
                func.lower(EmpleadoModel.rut).like(termino),
            )
        )
    rows = db.execute(query).all()
    resultado: List[EmpleadoSchema] = []
    for empleado, comuna_nombre, provincia_nombre, region_nombre, cargo_nombre, departamento_nombre in rows:
        resultado.append(
            EmpleadoSchema(
                id=empleado.id,
                rut=empleado.rut,
                nombres=empleado.nombres,
                apellidos=empleado.apellidos,
                email=empleado.email,
                telefono=empleado.telefono,
                direccion=empleado.direccion,
                fecha_ingreso=empleado.fecha_ingreso,
                sueldo=empleado.sueldo,
                activo=empleado.activo,
                comuna_id=empleado.comuna_id,
                cargo_id=empleado.cargo_id,
                departamento_id=empleado.departamento_id,
                comuna=comuna_nombre,
                provincia=provincia_nombre,
                region=region_nombre,
                cargo=cargo_nombre,
                departamento=departamento_nombre,
            )
        )
    return resultado


@app.post('/empleados', response_model=EmpleadoSchema, status_code=status.HTTP_201_CREATED)
def crear_empleado(datos: EmpleadoCreate, db: Session = Depends(get_db)):
    if datos.comuna_id is None or datos.cargo_id is None or datos.departamento_id is None:
        raise HTTPException(status_code=400, detail='Debe elegir comuna, cargo y departamento')
    registro = EmpleadoModel(**datos.model_dump())
    db.add(registro)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='Ya existe un registro con ese RUT o email')
    db.refresh(registro)
    return formatear_empleado(db, registro)


@app.put('/empleados/{empleado_id}', response_model=EmpleadoSchema)
def actualizar_empleado(empleado_id: int, datos: EmpleadoUpdate, db: Session = Depends(get_db)):
    registro = db.get(EmpleadoModel, empleado_id)
    if registro is None:
        raise HTTPException(status_code=404, detail='Empleado no encontrado')
    for campo, valor in datos.model_dump().items():
        setattr(registro, campo, valor)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='Ya existe un registro con ese RUT o email')
    return formatear_empleado(db, registro)


@app.delete('/empleados/{empleado_id}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_empleado(empleado_id: int, db: Session = Depends(get_db)):
    registro = db.get(EmpleadoModel, empleado_id)
    if registro is None:
        raise HTTPException(status_code=404, detail='Empleado no encontrado')
    db.delete(registro)
    db.commit()


def formatear_empleado(db: Session, empleado: EmpleadoModel) -> EmpleadoSchema:
    comuna = db.get(ComunaModel, empleado.comuna_id)
    provincia = db.get(ProvinciaModel, comuna.provincia_id) if comuna else None
    region = db.get(RegionModel, provincia.region_id) if provincia else None
    cargo = db.get(CargoModel, empleado.cargo_id)
    departamento = db.get(DepartamentoModel, empleado.departamento_id)
    return EmpleadoSchema(
        id=empleado.id,
        rut=empleado.rut,
        nombres=empleado.nombres,
        apellidos=empleado.apellidos,
        email=empleado.email,
        telefono=empleado.telefono,
        direccion=empleado.direccion,
        fecha_ingreso=empleado.fecha_ingreso,
        sueldo=empleado.sueldo,
        activo=empleado.activo,
        comuna_id=empleado.comuna_id,
        cargo_id=empleado.cargo_id,
        departamento_id=empleado.departamento_id,
        comuna=comuna.nombre if comuna else '',
        provincia=provincia.nombre if provincia else '',
        region=region.nombre if region else '',
        cargo=cargo.nombre if cargo else '',
        departamento=departamento.nombre if departamento else '',
    )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
