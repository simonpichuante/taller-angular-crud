export interface Region {
  id: number;
  numero_romano: string;
  nombre: string;
}

export interface Provincia {
  id: number;
  nombre: string;
  region_id: number;
}

export interface Comuna {
  id: number;
  nombre: string;
  provincia_id: number;
  provincia: string;
  region_id: number;
  region: string;
}
