import { provideHttpClient } from '@angular/common/http';
import { ApplicationConfig, ErrorHandler, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { ErrorGlobalService } from './services/sistema/error-global.service';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    { provide: ErrorHandler, useClass: ErrorGlobalService },
    provideRouter(routes),
    provideHttpClient(),
  ],
};
