import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { SpinnerComponent } from '../../../../shared/components/spinner/spinner.component';
import { IterationService } from '../../services/iteration.service';
import { EstimateApiService } from '../../../../Core/services/estimate-api.service';
import { IPrediction } from '../../../../Core/models/prediction.interface';
import { ChartModule } from 'primeng/chart';

@Component({
  selector: 'app-estimate-effort',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink, CommonModule, SpinnerComponent, FormsModule, ChartModule],
  templateUrl: './estimate-effort.component.html',
  styleUrl: './estimate-effort.component.scss'
})
export class EstimateEffortComponent {
  router = inject(Router);
  iterationService = inject(IterationService);
  seniorities = [
    { id: 1, seniority: 'Junior' },
    { id: 2, seniority: 'Semi senior' },
    { id: 3, seniority: 'Senior' }
  ];
  frontendLanguage = [
    { id: 1, language: 'React' },
    { id: 2, language: 'Angular' },
    { id: 3, language: 'JavaScript' },
    { id: 4, language: 'React Native' },//0 0 0 0
  ];
  backendLanguage = [
    { id: 1, language: 'Node' },
    { id: 2, language: '.Net' },
    { id: 3, language: 'Java' },
    { id: 4, language: 'Python' },// 0 0 0 0
  ];
  calculateEffortForm = new FormGroup({
    seniorityFrontend: new FormControl('', Validators.required),
    seniorityBackend: new FormControl('', Validators.required),
    frontendLanguage: new FormControl('', Validators.required),
    backendLanguage: new FormControl('', Validators.required),
    // requirementDescription: new FormControl('', [Validators.minLength(10), Validators.maxLength(80), Validators.required]),
    complexity: new FormControl('', [Validators.required, Validators.min(1), Validators.max(32)]),
  });
  isLoading = false;
  estimateApiService = inject(EstimateApiService);
  prediction?: IPrediction;
  selectedOption: string | null = null;
  showMessageToSelectModel: boolean = false;

  data: any;
  options: any;

  calculateEffort() {
    if (!this.selectedOption) {
      this.showMessageToSelectModel = true;
      setTimeout(() => {
        this.showMessageToSelectModel = false;
      }, 3000);
      return;
    };

    this.isLoading = true
    setTimeout(() => {
      this.isLoading = false;
      const data = {
        "s_frontend": this.calculateEffortForm.value.seniorityFrontend,
        "s_backend": this.calculateEffortForm.value.seniorityBackend,
        "lf_react": this.checkLanguageSelected('React'),
        "lf_angular": this.checkLanguageSelected('Angular'),
        "lf_javascript": this.checkLanguageSelected('JavaScript'),
        "lb_node": this.checkLanguageSelected('Node'),
        "lb_dotnet": this.checkLanguageSelected('.Net'),
        "lb_java": this.checkLanguageSelected('Java'),
        "Complexity_value": this.calculateEffortForm.value.complexity
      };

      if (this.selectedOption == '2') {
        this.estimateWithXGB(data);
      } else {
        this.estimateWithRLM(data);
      }

    }, 1000)
  }

  estimateWithXGB(data: any) {
    this.estimateApiService.estimateWithXGB(data).subscribe({
      next: res => {
        this.prediction = res.predictions;
      },
      error: error => {
        console.log(error);
      },
      complete: () => {
        this.initializeChart();
      }
    });
  }

  estimateWithRLM(data: any) {
    this.estimateApiService.estimateWithRLM(data).subscribe({
      next: res => {
        this.prediction = res.predictions;
      },
      error: error => {
        console.log(error);
      },
      complete: () => {
        this.initializeChart();
      }
    });
  }

  checkLanguageSelected(language: string): number {
    return (this.calculateEffortForm.value.frontendLanguage == language || this.calculateEffortForm.value.backendLanguage == language) ? 1 : 0;
  }


  resetForm() {
    this.prediction = undefined;
    this.calculateEffortForm.reset();
  }

  resetPrediction() {
    this.prediction = undefined;
  }


  initializeChart(){
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color-primary');
    const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

    this.data = {
      labels: ['Diseño', 'Frontend', 'Backend', 'QA'],
      datasets: [
        {
          label: 'Horas estimadas',
          backgroundColor: [
            '#42A5F5', '#66BB6A', '#FFA726', '#AB47BC'
          ],
          data: [this.prediction?.t_design, this.prediction?.t_frontend, this.prediction?.t_backend, this.prediction?.t_qa]
        }
      ]
    };

    this.options = {
      plugins: {
        legend: {
          labels: {
            color: textColor
          }
        },
        title:{
          display:true,
          text: 'Horas estimadas por area',
          color: textColor,
          font: {
            size: 18
          }
        },
      },     
      scales: {
        x: {
          ticks: {
            color: textColorSecondary
          },
          // grid: {
          //   color: surfaceBorder
          // }
        },
        y: {
          ticks: {
            color: textColorSecondary
          },
          grid: {
            color: surfaceBorder
          }
        }
      }
    };
  }

}
