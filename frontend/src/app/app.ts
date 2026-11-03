import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Alertas } from './components/alertas/alertas';
import { Carga } from './components/carga/carga';
import { Menu } from './components/menu/menu';
import { CargaService } from './services/ui/carga.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Menu, Alertas, Carga],
  templateUrl: './app.html',
})
export class App {
  carga = inject(CargaService);
}
