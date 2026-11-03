export interface CargoForm {
  nombre: string;
  descripcion: string;
}

export interface Cargo extends CargoForm {
  id: number;
}
