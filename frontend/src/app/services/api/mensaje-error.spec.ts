import { HttpErrorResponse } from '@angular/common/http';
import { describe, expect, it } from 'vitest';
import { mensajeError } from './mensaje-error';

describe('mensajeError', () => {
  it('usa el mensaje que envía la API', () => {
    const error = { status: 409, error: { detail: 'Ya existe un registro con ese nombre' } } as HttpErrorResponse;
    expect(mensajeError(error)).toBe('Ya existe un registro con ese nombre');
  });

  it('limpia los errores de validación', () => {
    const error = {
      status: 422,
      error: { detail: [{ msg: 'Value error, el campo es obligatorio.' }] },
    } as HttpErrorResponse;
    expect(mensajeError(error)).toBe('el campo es obligatorio.');
  });

  it('avisa cuando la API no responde', () => {
    const error = { status: 0, error: null } as HttpErrorResponse;
    expect(mensajeError(error)).toBe('No se pudo conectar con la API. Revisa que esté encendida.');
  });
});
