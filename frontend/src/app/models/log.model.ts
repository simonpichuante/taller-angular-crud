export interface Log {
  fecha: Date;
  nivel: 'info' | 'advertencia' | 'error';
  mensaje: string;
}
