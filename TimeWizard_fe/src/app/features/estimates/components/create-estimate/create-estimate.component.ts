import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { SpinnerComponent } from '../../../../shared/components/spinner/spinner.component';
import * as XLSX from 'xlsx';
import { EstimateApiService } from '../../../../Core/services/estimate-api.service';
import { EstimatesService } from '../../services/estimates.service';
import { FormattedData, InputData } from '../../../../Core/models/formated-data.interface';
import { Predictions } from '../../../../Core/models/estimates.interface';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-create-estimate',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink, CommonModule, SpinnerComponent],
  templateUrl: './create-estimate.component.html',
  styleUrl: './create-estimate.component.scss'
})
export class CreateEstimateComponent {
  fileUploadForm: FormGroup;
  selectedFile: File | null = null;
  isLoading = false;
  previewHeaders: string[] = [];
  previewData: any[] = [];
  estimateApiService = inject(EstimateApiService);
  estimateService = inject(EstimatesService);
  rowCount = 0;

  constructor(private fb: FormBuilder, private router: Router) {
    this.fileUploadForm = this.fb.group({});
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      console.log('Archivo seleccionado:', this.selectedFile.name);
      this.previewData = []; // Reset preview
    }
  }

  uploadFile(): void {
    if (!this.selectedFile) {
      console.error('No se ha seleccionado ningún archivo');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e: any) => {
      const data = new Uint8Array(e.target.result);
      const workbook = XLSX.read(data, { type: 'array' });
      const sheetName = workbook.SheetNames[0]; // Tomar la primera hoja
      const sheet = workbook.Sheets[sheetName];
      // Convertir el archivo en JSON
      var jsonData: any[] = XLSX.utils.sheet_to_json(sheet);
      this.rowCount = jsonData.length;
      // Mapear los datos al formato esperado
      const formattedData: FormattedData = {
        inputs: jsonData
          .map(row => this.mapRowToInputData(row))
          .sort((a, b) => a.Complexity_value - b.Complexity_value) // Ordenar por Complexity_value
      };

      jsonData = jsonData.sort((a, b) => (Number(a['Complexity_value']) || 0) - (Number(b['Complexity_value']) || 0));
      this.estimateService.originalData = jsonData.map(row => this.mapRowToPrediction(row));
      this.estimateService.complexities = jsonData.map(row => Number(row['Complexity_value']) || 0);
      this.sendEstimates(formattedData);
    };

    reader.readAsArrayBuffer(this.selectedFile);
  }

  private sendEstimates(formattedData: FormattedData): void {
    this.isLoading = true;

  const rlm$ = this.estimateApiService.estimateAllWithRLM(formattedData);
  const xgb$ = this.estimateApiService.estimateAllWithXGB(formattedData);

  forkJoin([rlm$, xgb$]).subscribe({
    next: ([resRLM, resXGB]) => {
      this.estimateService.estimatesRLM = resRLM.batch_predictions.map(batchPrediction => batchPrediction.predictions);
      this.estimateService.estimatesXGB = resXGB.batch_predictions.map(batchPrediction => batchPrediction.predictions);

      // Ahora que ambas respuestas están listas, navegamos
      this.navigateWithDelay();
    },
    error: error => this.handleError(error)
  });
  }


  private handleError(error: any): void {
    console.error('Error en la estimación:', error);
    this.isLoading = false;
  }

  private navigateWithDelay(): void {
    setTimeout(() => {
      this.router.navigate(['/home/show-estimates']);
      this.isLoading = false;
    }, 1000);
  }


  private mapRowToInputData(row: any): InputData {
    return {
      s_frontend: Number(row['s_frontend']) || 0,
      s_backend: Number(row['s_backend']) || 0,
      lf_react: Number(row['lf_react']) || 0,
      lf_angular: Number(row['lf_angular']) || 0,
      lf_javascript: Number(row['lf_javascript']) || 0,
      lb_node: Number(row['lb_node']) || 0,
      lb_dotnet: Number(row['lb_dotnet']) || 0,
      lb_java: Number(row['lb_java']) || 0,
      Complexity_value: Number(row['Complexity_value']) || 0
    };
  }
  
  private mapRowToPrediction(row: any): Predictions {
    return {
      t_design: Number(row['t_design']) || 0,
      t_frontend: Number(row['t_frontend']) || 0,
      t_backend: Number(row['t_backend']) || 0,
      t_qa: Number(row['t_qa']) || 0
    };
  }

  getAllEstimatesWithRLM(formattedData: any) {
    this.estimateApiService.estimateAllWithRLM(formattedData).subscribe({
      next: res => {
      },
      error: error => {
        console.log(error);
      },
      complete: () => {
        this.isLoading = false;
      }
    });
  }

  getAllEstimatesWithXGB(formattedData: any) {
    this.estimateApiService.estimateAllWithXGB(formattedData).subscribe({
      next: res => {

      },
      error: error => {
        console.log(error);
        this.isLoading = false;
      },
      complete: () => {
        this.isLoading = false;
      }
    });
  }

  previewFile(): void {
    if (!this.selectedFile) return;
    const reader = new FileReader();
    reader.onload = (e: any) => {
      const data = new Uint8Array(e.target.result);
      const workbook = XLSX.read(data, { type: 'array' });
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });

      if (jsonData.length > 0) {
        this.previewHeaders = jsonData[0] as string[];
        this.previewData = jsonData.slice(1, 11); // Tomar las primeras 10 filas
      }
    };
    reader.readAsArrayBuffer(this.selectedFile);
  }

}
