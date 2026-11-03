import { Injectable, signal } from '@angular/core';
import { Alerta } from '../../models/alerta.model';

@Injectable({ providedIn: 'root' })
export class AlertaService {
  alertas = signal<Alerta[]>([]);
  private siguienteId = 1;

  exito(mensaje: string): void {
    this.mostrar('exito', mensaje);
  }

  error(mensaje: string): void {
    this.mostrar('error', mensaje);
  }

  advertencia(mensaje: string): void {
    this.mostrar('advertencia', mensaje);
  }

  info(mensaje: string): void {
    this.mostrar('info', mensaje);
  }

  cerrar(id: number): void {
    this.alertas.update((lista) => lista.filter((alerta) => alerta.id !== id));
  }

  private mostrar(tipo: Alerta['tipo'], mensaje: string): void {
    if (this.alertas().some((alerta) => alerta.mensaje === mensaje)) {
      return;
    }
    const id = this.siguienteId++;
    this.alertas.update((lista) => [...lista, { id, tipo, mensaje }]);
    setTimeout(() => this.cerrar(id), 5000);
  }
}
