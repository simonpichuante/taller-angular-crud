export interface Alerta {
  id: number;
  tipo: 'exito' | 'error' | 'advertencia' | 'info';
  mensaje: string;
}
