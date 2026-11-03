import { ErrorHandler, Injectable, inject } from '@angular/core';
import { AlertaService } from '../ui/alerta.service';
import { LogService } from './log.service';

@Injectable()
export class ErrorGlobalService implements ErrorHandler {
  private log = inject(LogService);
  private alerta = inject(AlertaService);

  handleError(error: Error): void {
    this.log.error(`Error no controlado: ${error.message}`);
    this.alerta.error('Ocurrió un error inesperado.');
  }
}
