import { Component, inject, Input } from '@angular/core';
import { ChartModule } from 'primeng/chart';

@Component({
    selector: 'app-line-chat',
    standalone: true,
    imports: [ChartModule],
    templateUrl: './line-chart.component.html',
    styleUrl: './line-chart.component.scss'
})
export class LineChartComponent {
    data: any;
    options: any;
    @Input() title = "Grafico de Linea";

    ngOnInit() {
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--text-color-primary');
        const DATA_COUNT = 12;
        const NUMBER_CFG = {count: DATA_COUNT, min: 0, max: 100};

        this.data = {
            labels: this.months({count: 12}),
            datasets: [
                {
                    label: 'Datos 2024',
                    data: this.numbers(NUMBER_CFG),
                    // borderColor: 'red',
                    // backgroundColor:'red',
                },
                {
                    label: 'Datos 2025',
                    data: this.numbers(NUMBER_CFG),
                    // borderColor: 'green',
                    // backgroundColor:'green',
                },
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
                }
            },
            
        };
    }


    numbers(config: {count: number, min: number, max: number}) {
        const {count, min, max} = config;
        return Array.from({length: count}, () => Math.floor(Math.random() * (max - min + 1)) + min);
    }

    months(config: { count: number }) {
        const monthNames = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"];
        const today = new Date();
        return Array.from({ length: config.count }, (_, i) => {
            const monthIndex = (today.getMonth() - i + 12) % 12;
            return monthNames[monthIndex];
        }).reverse();
    }
    
}