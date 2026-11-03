import { DatePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { LogService } from '../../services/sistema/log.service';

@Component({
  selector: 'app-logs',
  imports: [DatePipe],
  templateUrl: './logs.html',
})
export class Logs {
  servicio = inject(LogService);
}
