import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Empleado, EmpleadoForm } from '../../models/empleado.model';
import { ApiService } from './api.service';

@Injectable({ providedIn: 'root' })
export class EmpleadoService {
  private api = inject(ApiService);

  listar(buscar = ''): Observable<Empleado[]> {
    return this.api.get<Empleado[]>('/empleados', { buscar });
  }

  crear(datos: EmpleadoForm): Observable<Empleado> {
    return this.api.post<Empleado>('/empleados', datos);
  }

  actualizar(id: number, datos: EmpleadoForm): Observable<Empleado> {
    return this.api.put<Empleado>(`/empleados/${id}`, datos);
  }

  eliminar(id: number): Observable<void> {
    return this.api.delete<void>(`/empleados/${id}`);
  }
}
