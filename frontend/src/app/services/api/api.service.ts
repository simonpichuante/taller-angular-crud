import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, finalize, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { LogService } from '../sistema/log.service';
import { CargaService } from '../ui/carga.service';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private carga = inject(CargaService);
  private log = inject(LogService);
  private url = environment.apiUrl;

  get<T>(ruta: string, params: Record<string, string> = {}): Observable<T> {
    return this.ejecutar(`GET ${ruta}`, this.http.get<T>(this.url + ruta, { params }));
  }

  post<T>(ruta: string, datos: unknown): Observable<T> {
    return this.ejecutar(`POST ${ruta}`, this.http.post<T>(this.url + ruta, datos));
  }

  put<T>(ruta: string, datos: unknown): Observable<T> {
    return this.ejecutar(`PUT ${ruta}`, this.http.put<T>(this.url + ruta, datos));
  }

  delete<T>(ruta: string): Observable<T> {
    return this.ejecutar(`DELETE ${ruta}`, this.http.delete<T>(this.url + ruta));
  }

  private ejecutar<T>(descripcion: string, peticion: Observable<T>): Observable<T> {
    this.carga.mostrar();
    return peticion.pipe(
      tap({
        next: () => this.log.info(`${descripcion}: correcto`),
        error: (error) => this.log.error(`${descripcion}: error ${error.status}`),
      }),
      finalize(() => this.carga.ocultar()),
    );
  }
}
