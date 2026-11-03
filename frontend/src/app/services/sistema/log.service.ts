import { Injectable, signal } from '@angular/core';
import { Log } from '../../models/log.model';

@Injectable({ providedIn: 'root' })
export class LogService {
  logs = signal<Log[]>([]);

  info(mensaje: string): void {
    this.registrar('info', mensaje);
  }

  advertencia(mensaje: string): void {
    this.registrar('advertencia', mensaje);
  }

  error(mensaje: string): void {
    this.registrar('error', mensaje);
  }

  limpiar(): void {
    this.logs.set([]);
  }

  private registrar(nivel: Log['nivel'], mensaje: string): void {
    this.logs.update((lista) => [{ fecha: new Date(), nivel, mensaje }, ...lista].slice(0, 100));
    console.log(`[${nivel}] ${mensaje}`);
  }
}
