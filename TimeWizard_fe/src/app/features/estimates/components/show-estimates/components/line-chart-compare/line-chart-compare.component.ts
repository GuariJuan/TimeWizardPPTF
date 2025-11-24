import { Component, Input } from '@angular/core';
import { ChartModule } from 'primeng/chart';

@Component({
    selector: 'app-line-chart-compare',
    standalone: true,
    imports: [ChartModule],
    templateUrl: './line-chart-compare.component.html',
    styleUrl: './line-chart-compare.component.scss'
})
export class LineChartCompareComponent {
    @Input() title: string = '';
    @Input() labels: string[] = [];
    @Input() seriesRLM: number[] = [];
    @Input() seriesHorasReales: number[] = [];
    @Input() seriesXGB: number[] = [];

    data: any;
    options: any;

    ngOnInit() {
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--text-color-primary');

        // Configuración de las opciones del gráfico
        this.options = {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        usePointStyle: true,
                        color: textColor
                    }
                },
                title: {
                    display: true,
                    text: this.title,
                    color: textColor,
                    font: {
                        size: 20
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Complejidad',
                        color: textColor,
                        font: {
                            size: 16
                        }
                    },
                    ticks: {
                        color: textColor,
                        callback: (value: any, index: number) => {
                            return index % 5 === 0 ? this.labels[index] : '';
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Horas',
                        color: textColor,
                        font: {
                            size: 16
                        }
                    },
                    ticks: {
                        color: textColor
                    }
                }
            }
        };


        // Configuración de los datos del gráfico utilizando las etiquetas y series recibidas
        this.data = {
            labels: this.labels, // Etiquetas para el eje X
            datasets: [
                {
                    label: 'Predicciones con RLM',
                    data: this.seriesRLM,
                    borderColor: 'red',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    pointBackgroundColor: 'red',
                    pointBorderColor: 'darkred',
                    showLine: false
                },
                {
                    label: 'Horas reales',
                    data: this.seriesHorasReales,
                    borderColor: 'green',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    pointBackgroundColor: 'green',
                    pointBorderColor: 'darkgreen',
                    showLine: false
                },
                {
                    label: 'Predicciones con XGB',
                    data: this.seriesXGB,
                    borderColor: 'blue',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    pointBackgroundColor: 'blue',
                    pointBorderColor: 'darkblue',
                    showLine: false
                }
            ]
        };
    }


}
