import { Component, inject } from '@angular/core';
import { AlertaService } from '../../services/ui/alerta.service';

@Component({
  selector: 'app-alertas',
  templateUrl: './alertas.html',
  styleUrl: './alertas.css',
})
export class Alertas {
  servicio = inject(AlertaService);
}
