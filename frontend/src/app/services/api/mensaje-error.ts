import { HttpErrorResponse } from '@angular/common/http';

export function mensajeError(error: HttpErrorResponse): string {
  const detalle = error.error?.detail;
  if (error.status === 0) {
    return 'No se pudo conectar con la API. Revisa que esté encendida.';
  }
  if (typeof detalle === 'string') {
    return detalle;
  }
  if (Array.isArray(detalle)) {
    return detalle[0].msg.replace('Value error, ', '');
  }
  return 'Ocurrió un error en el servidor.';
}
