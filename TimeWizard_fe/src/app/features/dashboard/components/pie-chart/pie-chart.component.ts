import { Component, Input } from '@angular/core';
import { ChartModule } from 'primeng/chart';

@Component({
    selector: 'app-pie-chart',
    standalone: true,
    imports: [ChartModule],
    templateUrl: './pie-chart.component.html',
    styleUrl: './pie-chart.component.scss'
})
export class PieChartComponent {
    data: any;
    options: any;
    @Input() title = "Grafico de Linea";
    @Input() label:string[] = ['Api', 'Movil', 'Web'];

    ngOnInit() {
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--text-color-primary');

        this.data = {
            labels: this.label,
            datasets: [
                {
                    data: this.generateRandomData(this.label.length),
                    backgroundColor: this.generateRandomColors(this.label.length),
                    borderColor: '#ffffffcc',
                }
            ]
        };

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
                },
                tooltip: {
                    callbacks: {
                        label: function (context:any) {
                          const dataset = context.dataset.data;
                          const total = dataset.reduce((acc:any, value:any) => acc + value, 0);
                          const currentValue = context.raw;
                          const percentage = ((currentValue / total) * 100).toFixed(0);
                          return ` (${percentage}%)`;
                        }
                    }
                }
            },
        };
    }
    
    private randomColor(): string {
        const color = Math.floor(Math.random() * 16777215).toString(16);
        return `#${color.padStart(6, '0')}`;
    }

    private generateRandomColors(count: number): string[] {
        return Array.from({ length: count }, () => this.randomColor());
    }

    private generateRandomData(count: number): number[] {
    const minPercent = 10; // mínimo 10%
    const minTotal = minPercent * count;

    // Si el mínimo supera 100, no tiene sentido
    if (minTotal > 100) {
        throw new Error("El mínimo por sector es demasiado alto para la cantidad de labels.");
    }

    // Paso 1: generar valores base aleatorios
    let values = Array.from({ length: count }, () => Math.random());

    // Paso 2: normalizarlos para que sumen el restante
    const remaining = 100 - minTotal;
    const sum = values.reduce((a, b) => a + b, 0);

    values = values.map(v => (v / sum) * remaining);

    // Paso 3: sumar el mínimo a cada uno
    return values.map(v => Math.round(v + minPercent));
}

}
