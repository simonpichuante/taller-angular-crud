import { Routes } from '@angular/router';
import { Cargos } from './pages/cargos/cargos';
import { Departamentos } from './pages/departamentos/departamentos';
import { Empleados } from './pages/empleados/empleados';
import { Logs } from './pages/logs/logs';

export const routes: Routes = [
  { path: '', redirectTo: 'empleados', pathMatch: 'full' },
  { path: 'empleados', component: Empleados },
  { path: 'departamentos', component: Departamentos },
  { path: 'cargos', component: Cargos },
  { path: 'logs', component: Logs },
];
