import { Component, inject, Inject } from '@angular/core';
import { LineChartCompareComponent } from "./components/line-chart-compare/line-chart-compare.component";
import { EstimatesService } from '../../services/estimates.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-show-estimates',
  standalone: true,
  imports: [LineChartCompareComponent],
  templateUrl: './show-estimates.component.html',
  styleUrl: './show-estimates.component.scss'
})
export class ShowEstimatesComponent {
  router = inject(Router);
  estimateService = inject(EstimatesService);
  ejeX = this.estimateService.getComplexities();
  


  titleQA = "Comparativa: RLM vs Horas Reales vs XGB (QA)";
  seriesRLMQA = this.estimateService.getEstimatesRLMQA();
  seriesHorasRealesQA = this.estimateService.getOriginalDataQA();
  seriesXGBQA = this.estimateService.getEstimatesXGBQA(); 

  titleBK = "Comparativa: RLM vs Horas Reales vs XGB (Backend)";
  seriesRLMBK = this.estimateService.getEstimatesRLMBK();
  seriesHorasRealesBK = this.estimateService.getOriginalDataBK();
  seriesXGBBK = this.estimateService.getEstimatesXGBBK();

  titleFR = "Comparativa: RLM vs Horas Reales vs XGB (Frontend)";
  seriesRLMFR = this.estimateService.getEstimatesRLMFR();
  seriesHorasRealesFR = this.estimateService.getOriginalDataFR();
  seriesXGBFR = this.estimateService.getEstimatesXGBFR();

  titleDS = "Comparativa: RLM vs Horas Reales vs XGB (Diseño)";
  seriesRLMDS = this.estimateService.getEstimatesRLMDS();
  seriesHorasRealesDS = this.estimateService.getOriginalDataDS();
  seriesXGBDS = this.estimateService.getEstimatesXGBDS();

  ngOnInit(): void {
    if(this.ejeX.length == 0) this.router.navigate(['estimates']);
  }

}
