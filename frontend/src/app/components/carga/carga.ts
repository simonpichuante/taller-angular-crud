import { Component, inject } from '@angular/core';
import { CargaService } from '../../services/ui/carga.service';

@Component({
  selector: 'app-carga',
  templateUrl: './carga.html',
  styleUrl: './carga.css',
})
export class Carga {
  servicio = inject(CargaService);
}
