import { Injectable, computed, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class CargaService {
  private peticiones = signal(0);
  activa = computed(() => this.peticiones() > 0);

  mostrar(): void {
    this.peticiones.update((n) => n + 1);
  }

  ocultar(): void {
    this.peticiones.update((n) => n - 1);
  }
}
