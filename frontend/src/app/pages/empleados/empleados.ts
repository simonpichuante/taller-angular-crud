import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Cargo } from '../../models/cargo.model';
import { Departamento } from '../../models/departamento.model';
import { Empleado, EmpleadoForm } from '../../models/empleado.model';
import { Comuna, Provincia, Region } from '../../models/territorio.model';
import { CargoService } from '../../services/api/cargo.service';
import { DepartamentoService } from '../../services/api/departamento.service';
import { EmpleadoService } from '../../services/api/empleado.service';
import { mensajeError } from '../../services/api/mensaje-error';
import { TerritorioService } from '../../services/api/territorio.service';
import { LogService } from '../../services/sistema/log.service';
import { AlertaService } from '../../services/ui/alerta.service';

@Component({
  selector: 'app-empleados',
  imports: [FormsModule],
  templateUrl: './empleados.html',
})
export class Empleados implements OnInit {
  private empleadoService = inject(EmpleadoService);
  private departamentoService = inject(DepartamentoService);
  private cargoService = inject(CargoService);
  private territorio = inject(TerritorioService);
  private alerta = inject(AlertaService);
  private log = inject(LogService);

  empleados = signal<Empleado[]>([]);
  departamentos = signal<Departamento[]>([]);
  cargos = signal<Cargo[]>([]);
  regiones = signal<Region[]>([]);
  provincias = signal<Provincia[]>([]);
  comunas = signal<Comuna[]>([]);
  editandoId = signal<number | null>(null);
  buscar = '';
  form: EmpleadoForm = this.formVacio();
  regionId: number | null = null;
  provinciaId: number | null = null;

  mostrarError = (error: HttpErrorResponse) => this.alerta.error(mensajeError(error));

  ngOnInit(): void {
    this.cargar();
    this.departamentoService.listar().subscribe({ next: (datos) => this.departamentos.set(datos), error: this.mostrarError });
    this.cargoService.listar().subscribe({ next: (datos) => this.cargos.set(datos), error: this.mostrarError });
    this.territorio.regiones().subscribe({ next: (datos) => this.regiones.set(datos), error: this.mostrarError });
  }

  cargar(): void {
    this.empleadoService.listar(this.buscar).subscribe({
      next: (datos) => this.empleados.set(datos),
      error: this.mostrarError,
    });
  }

  cambiarRegion(id: number | null): void {
    this.regionId = id;
    this.provinciaId = null;
    this.form.comuna_id = null;
    this.provincias.set([]);
    this.comunas.set([]);
    if (id) {
      this.territorio.provincias(id).subscribe({ next: (datos) => this.provincias.set(datos), error: this.mostrarError });
    }
  }

  cambiarProvincia(id: number | null): void {
    this.provinciaId = id;
    this.form.comuna_id = null;
    this.comunas.set([]);
    if (id) {
      this.territorio.comunas(id).subscribe({ next: (datos) => this.comunas.set(datos), error: this.mostrarError });
    }
  }

  guardar(): void {
    const id = this.editandoId();
    const peticion = id ? this.empleadoService.actualizar(id, this.form) : this.empleadoService.crear(this.form);
    peticion.subscribe({
      next: () => {
        this.alerta.exito('Empleado guardado correctamente.');
        this.log.info(`Empleado guardado: ${this.form.nombres} ${this.form.apellidos}`);
        this.limpiar();
        this.cargar();
      },
      error: this.mostrarError,
    });
  }

  editar(empleado: Empleado): void {
    this.form = {
      rut: empleado.rut,
      nombres: empleado.nombres,
      apellidos: empleado.apellidos,
      email: empleado.email,
      telefono: empleado.telefono,
      direccion: empleado.direccion,
      fecha_ingreso: empleado.fecha_ingreso,
      sueldo: empleado.sueldo,
      activo: empleado.activo,
      comuna_id: empleado.comuna_id,
      cargo_id: empleado.cargo_id,
      departamento_id: empleado.departamento_id,
    };
    this.editandoId.set(empleado.id);
    if (empleado.comuna_id === null) {
      return;
    }
    this.territorio.comuna(empleado.comuna_id).subscribe({
      next: (comuna) => {
        this.regionId = comuna.region_id;
        this.provinciaId = comuna.provincia_id;
        this.territorio.provincias(comuna.region_id).subscribe({ next: (datos) => this.provincias.set(datos), error: this.mostrarError });
        this.territorio.comunas(comuna.provincia_id).subscribe({ next: (datos) => this.comunas.set(datos), error: this.mostrarError });
      },
      error: this.mostrarError,
    });
  }

  eliminar(empleado: Empleado): void {
    if (!confirm(`¿Eliminar a ${empleado.nombres} ${empleado.apellidos}?`)) {
      return;
    }
    this.empleadoService.eliminar(empleado.id).subscribe({
      next: () => {
        this.alerta.exito('Empleado eliminado.');
        this.log.info(`Empleado eliminado: ${empleado.nombres} ${empleado.apellidos}`);
        this.cargar();
      },
      error: this.mostrarError,
    });
  }

  limpiar(): void {
    this.form = this.formVacio();
    this.editandoId.set(null);
    this.regionId = null;
    this.provinciaId = null;
    this.provincias.set([]);
    this.comunas.set([]);
  }

  private formVacio(): EmpleadoForm {
    return {
      rut: '',
      nombres: '',
      apellidos: '',
      email: '',
      telefono: '',
      direccion: '',
      fecha_ingreso: '',
      sueldo: null,
      activo: true,
      comuna_id: null,
      cargo_id: null,
      departamento_id: null,
    };
  }
}
