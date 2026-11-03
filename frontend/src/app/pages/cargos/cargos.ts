import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Cargo, CargoForm } from '../../models/cargo.model';
import { mensajeError } from '../../services/api/mensaje-error';
import { CargoService } from '../../services/api/cargo.service';
import { LogService } from '../../services/sistema/log.service';
import { AlertaService } from '../../services/ui/alerta.service';

@Component({
  selector: 'app-cargos',
  imports: [FormsModule],
  templateUrl: './cargos.html',
})
export class Cargos implements OnInit {
  private servicio = inject(CargoService);
  private alerta = inject(AlertaService);
  private log = inject(LogService);

  lista = signal<Cargo[]>([]);
  buscar = signal('');
  editandoId = signal<number | null>(null);
  form: CargoForm = { nombre: '', descripcion: '' };

  filtrados = computed(() => {
    const texto = this.buscar().toLowerCase();
    return this.lista().filter((item) => item.nombre.toLowerCase().includes(texto));
  });

  ngOnInit(): void {
    this.cargar();
  }

  cargar(): void {
    this.servicio.listar().subscribe({
      next: (datos) => this.lista.set(datos),
      error: (error: HttpErrorResponse) => this.alerta.error(mensajeError(error)),
    });
  }

  guardar(): void {
    const id = this.editandoId();
    const peticion = id ? this.servicio.actualizar(id, this.form) : this.servicio.crear(this.form);
    peticion.subscribe({
      next: () => {
        this.alerta.exito('Cargo guardado correctamente.');
        this.log.info(`Cargo guardado: ${this.form.nombre}`);
        this.limpiar();
        this.cargar();
      },
      error: (error: HttpErrorResponse) => this.alerta.error(mensajeError(error)),
    });
  }

  editar(item: Cargo): void {
    this.form = { nombre: item.nombre, descripcion: item.descripcion };
    this.editandoId.set(item.id);
  }

  eliminar(item: Cargo): void {
    if (!confirm(`¿Eliminar "${item.nombre}"?`)) {
      return;
    }
    this.servicio.eliminar(item.id).subscribe({
      next: () => {
        this.alerta.exito('Cargo eliminado.');
        this.log.info(`Cargo eliminado: ${item.nombre}`);
        this.cargar();
      },
      error: (error: HttpErrorResponse) => this.alerta.error(mensajeError(error)),
    });
  }

  limpiar(): void {
    this.form = { nombre: '', descripcion: '' };
    this.editandoId.set(null);
  }
}
