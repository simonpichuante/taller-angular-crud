import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Cargo, CargoForm } from '../../models/cargo.model';
import { ApiService } from './api.service';

@Injectable({ providedIn: 'root' })
export class CargoService {
  private api = inject(ApiService);

  listar(): Observable<Cargo[]> {
    return this.api.get<Cargo[]>('/cargos');
  }

  crear(datos: CargoForm): Observable<Cargo> {
    return this.api.post<Cargo>('/cargos', datos);
  }

  actualizar(id: number, datos: CargoForm): Observable<Cargo> {
    return this.api.put<Cargo>(`/cargos/${id}`, datos);
  }

  eliminar(id: number): Observable<void> {
    return this.api.delete<void>(`/cargos/${id}`);
  }
}
