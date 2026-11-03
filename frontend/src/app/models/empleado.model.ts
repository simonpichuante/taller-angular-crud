export interface EmpleadoForm {
  rut: string;
  nombres: string;
  apellidos: string;
  email: string;
  telefono: string;
  direccion: string;
  fecha_ingreso: string;
  sueldo: number | null;
  activo: boolean;
  comuna_id: number | null;
  cargo_id: number | null;
  departamento_id: number | null;
}

export interface Empleado extends EmpleadoForm {
  id: number;
  comuna: string;
  provincia: string;
  region: string;
  cargo: string;
  departamento: string;
}
