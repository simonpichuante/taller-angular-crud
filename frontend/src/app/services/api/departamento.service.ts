import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Departamento, DepartamentoForm } from '../../models/departamento.model';
import { ApiService } from './api.service';

@Injectable({ providedIn: 'root' })
export class DepartamentoService {
  private api = inject(ApiService);

  listar(): Observable<Departamento[]> {
    return this.api.get<Departamento[]>('/departamentos');
  }

  crear(datos: DepartamentoForm): Observable<Departamento> {
    return this.api.post<Departamento>('/departamentos', datos);
  }

  actualizar(id: number, datos: DepartamentoForm): Observable<Departamento> {
    return this.api.put<Departamento>(`/departamentos/${id}`, datos);
  }

  eliminar(id: number): Observable<void> {
    return this.api.delete<void>(`/departamentos/${id}`);
  }
}
