import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Comuna, Provincia, Region } from '../../models/territorio.model';
import { ApiService } from './api.service';

@Injectable({ providedIn: 'root' })
export class TerritorioService {
  private api = inject(ApiService);

  regiones(): Observable<Region[]> {
    return this.api.get<Region[]>('/regiones');
  }

  provincias(regionId: number): Observable<Provincia[]> {
    return this.api.get<Provincia[]>(`/regiones/${regionId}/provincias`);
  }

  comunas(provinciaId: number): Observable<Comuna[]> {
    return this.api.get<Comuna[]>(`/provincias/${provinciaId}/comunas`);
  }

  comuna(id: number): Observable<Comuna> {
    return this.api.get<Comuna>(`/comunas/${id}`);
  }
}
