//ANGULAR
import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';

// PRIMENG
import { PrimeNGConfig } from 'primeng/api';
import { ToastModule } from 'primeng/toast';
import { MessagesModule } from 'primeng/messages';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ButtonModule, ToastModule, MessagesModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'TimeWizard_fe';
  primeConfig = inject(PrimeNGConfig);
  

  ngOnInit(): void {
    this.primeConfig.ripple = false;
    this,this.primeConfig.setTranslation({
      accept: 'Aceptar',
      reject: 'Cancelar',
      choose: 'Seleccionar',
      upload: 'Subir',
      lt: 'Anterior',
      lte: 'Anterior o igual',
      gt : 'Siguiente',
      gte: 'Siguiente o igual',
      dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
      dayNamesShort: ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'],
      dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
      monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
      monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
    });
    this.primeConfig.zIndex = {
      modal: 1100,
      overlay: 1000,
      menu: 100,
      tooltip: 1100
    };
  }
}
