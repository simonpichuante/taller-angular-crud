import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Departamento, DepartamentoForm } from '../../models/departamento.model';
import { mensajeError } from '../../services/api/mensaje-error';
import { DepartamentoService } from '../../services/api/departamento.service';
import { LogService } from '../../services/sistema/log.service';
import { AlertaService } from '../../services/ui/alerta.service';

@Component({
  selector: 'app-departamentos',
  imports: [FormsModule],
  templateUrl: './departamentos.html',
})
export class Departamentos implements OnInit {
  private servicio = inject(DepartamentoService);
  private alerta = inject(AlertaService);
  private log = inject(LogService);

  lista = signal<Departamento[]>([]);
  buscar = signal('');
  editandoId = signal<number | null>(null);
  form: DepartamentoForm = { nombre: '', descripcion: '' };

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
        this.alerta.exito('Departamento guardado correctamente.');
        this.log.info(`Departamento guardado: ${this.form.nombre}`);
        this.limpiar();
        this.cargar();
      },
      error: (error: HttpErrorResponse) => this.alerta.error(mensajeError(error)),
    });
  }

  editar(item: Departamento): void {
    this.form = { nombre: item.nombre, descripcion: item.descripcion };
    this.editandoId.set(item.id);
  }

  eliminar(item: Departamento): void {
    if (!confirm(`¿Eliminar "${item.nombre}"?`)) {
      return;
    }
    this.servicio.eliminar(item.id).subscribe({
      next: () => {
        this.alerta.exito('Departamento eliminado.');
        this.log.info(`Departamento eliminado: ${item.nombre}`);
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
