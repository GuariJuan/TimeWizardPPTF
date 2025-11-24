import { Component } from '@angular/core';
import { LineChartComponent } from "./components/line-chat/line-chart.component";
import { PieChartComponent } from './components/pie-chart/pie-chart.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [ LineChartComponent, PieChartComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {
// [x: string]: string;
title = "Evolución de Horas Facturadas por Mes";
title2 = "Tendencia de Requerimientos Entregados";
title3 = "Distribución de Proyectos por Tecnología";
title4 = "Participación por Tipo de Servicio";
labels:string[] = ['Angular', 'React', '.NET'];
labels2 = ['Desarrollo', 'Mantenimiento', 'Consultoría'];
}
