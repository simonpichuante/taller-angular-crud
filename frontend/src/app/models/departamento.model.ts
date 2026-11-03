export interface DepartamentoForm {
  nombre: string;
  descripcion: string;
}

export interface Departamento extends DepartamentoForm {
  id: number;
}
