from __future__ import annotations

from datetime import date
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, or_, select, text
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
    try:
        from .database import SessionLocal
        from .territorio_data import TERRITORIO_DPA
    except ImportError:
        from database import SessionLocal
        from territorio_data import TERRITORIO_DPA

    db = SessionLocal()
    try:
        sincronizar_secuencias_postgres(db)

        region_data = [
            (1, 'I', 'Tarapacá'),
            (2, 'II', 'Antofagasta'),
            (3, 'III', 'Atacama'),
            (4, 'IV', 'Coquimbo'),
            (5, 'V', 'Valparaíso'),
            (6, 'VI', 'Libertador General Bernardo O’Higgins'),
            (7, 'VII', 'Maule'),
            (8, 'VIII', 'Biobío'),
            (9, 'IX', 'La Araucanía'),
            (10, 'X', 'Los Lagos'),
            (11, 'XI', 'Aysén'),
            (12, 'XII', 'Magallanes y Antártica Chilena'),
            (13, 'XIII', 'Metropolitana de Santiago'),
            (14, 'XIV', 'Los Ríos'),
            (15, 'XV', 'Arica y Parinacota'),
            (16, 'XVI', 'Ñuble'),
        ]
        region_ids = set(db.execute(select(RegionModel.id)).scalars())
        db.add_all(
            RegionModel(id=region_id, numero_romano=numero_romano, nombre=nombre)
            for region_id, numero_romano, nombre in region_data
            if region_id not in region_ids
        )
        db.flush()

        provincias_por_clave = {
            (provincia.region_id, provincia.nombre): provincia
            for provincia in db.execute(select(ProvinciaModel)).scalars()
        }
        for region_id, provincias in TERRITORIO_DPA.items():
            for nombre, _ in provincias:
                clave = (region_id, nombre)
                if clave not in provincias_por_clave:
                    provincia = ProvinciaModel(nombre=nombre, region_id=region_id)
                    db.add(provincia)
                    provincias_por_clave[clave] = provincia
        db.flush()

        comunas_existentes = {
            (comuna.provincia_id, comuna.nombre)
            for comuna in db.execute(select(ComunaModel)).scalars()
        }
        comunas_nuevas = []
        for region_id, provincias in TERRITORIO_DPA.items():
            for nombre_provincia, nombres_comunas in provincias:
                provincia = provincias_por_clave[(region_id, nombre_provincia)]
                for nombre_comuna in nombres_comunas:
                    clave = (provincia.id, nombre_comuna)
                    if clave not in comunas_existentes:
                        comunas_nuevas.append(
                            ComunaModel(nombre=nombre_comuna, provincia_id=provincia.id)
                        )
                        comunas_existentes.add(clave)
        db.add_all(comunas_nuevas)
        db.flush()

        departamentos = {
            departamento.nombre
            for departamento in db.execute(select(DepartamentoModel)).scalars()
        }
        departamento_data = [
            ('Tecnología', 'Equipo de software'),
            ('Recursos Humanos', 'Gestión de personas'),
            ('Administración', 'Soporte financiero y administrativo'),
        ]
        db.add_all(
            DepartamentoModel(nombre=nombre, descripcion=descripcion)
            for nombre, descripcion in departamento_data
            if nombre not in departamentos
        )

        cargos = {cargo.nombre for cargo in db.execute(select(CargoModel)).scalars()}
        cargo_data = [
            ('Desarrollador', 'Desarrollo de software'),
            ('Analista', 'Análisis de negocio'),
            ('Administrador', 'Administración de procesos'),
        ]
        db.add_all(
            CargoModel(nombre=nombre, descripcion=descripcion)
            for nombre, descripcion in cargo_data
            if nombre not in cargos
        )
        db.flush()

        if db.execute(select(EmpleadoModel.id)).first() is None:
            provincia_santiago = provincias_por_clave[(13, 'Santiago')]
            comuna_santiago = db.execute(
                select(ComunaModel).where(
                    ComunaModel.provincia_id == provincia_santiago.id,
                    ComunaModel.nombre == 'Santiago',
                )
            ).scalar_one()
            departamento_id = db.execute(
                select(DepartamentoModel.id).where(DepartamentoModel.nombre == 'Tecnología')
            ).scalar_one()
            cargo_id = db.execute(
                select(CargoModel.id).where(CargoModel.nombre == 'Desarrollador')
            ).scalar_one()
            db.add(
                EmpleadoModel(
                    rut='12345678-5',
                    nombres='Ana',
                    apellidos='García',
                    email='ana@empresa.cl',
                    telefono='+56912345678',
                    direccion='Av. Principal 123',
                    fecha_ingreso=date(2024, 1, 10),
                    sueldo=1500000,
                    activo=True,
                    comuna_id=comuna_santiago.id,
                    cargo_id=cargo_id,
                    departamento_id=departamento_id,
                )
            )

        db.commit()
        sincronizar_secuencias_postgres(db)
        db.commit()
    finally:
        db.close()


def sincronizar_secuencias_postgres(db: Session) -> None:
    """Alinea los SERIAL con los IDs existentes, incluidas las filas semilla."""
    if db.get_bind().dialect.name != 'postgresql':
        return

    tablas = ('regiones', 'provincias', 'comunas', 'departamentos', 'cargos', 'empleados')
    for tabla in tablas:
        db.execute(
            text(
                f"""SELECT setval(
                    pg_get_serial_sequence('{tabla}', 'id'),
                    COALESCE(MAX(id), 1),
                    MAX(id) IS NOT NULL
                ) FROM {tabla}"""
            )
        )


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
