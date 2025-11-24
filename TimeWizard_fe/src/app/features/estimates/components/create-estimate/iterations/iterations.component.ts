import { Component, inject } from '@angular/core';
import { IterationService } from '../../../services/iteration.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { EstimateApiService } from '../../../../../Core/services/estimate-api.service';

@Component({
  selector: 'app-iterations',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule,],
  templateUrl: './iterations.component.html',
  styleUrl: './iterations.component.scss'
})
export class IterationsComponent {
  router = inject(Router);
  iterationService = inject(IterationService);
  estimateApiService = inject(EstimateApiService);
  currentIteration = 1;
  promptForImprovement = ""

  ngOnInit() {
    if (this.iterationService.iterations.length == 0) {
      this.router.navigate(['/create-estimate']);
    }
  }

  selectIteration(idx: number) {
    this.currentIteration = idx;
  }

  addImprovement(){
    this.estimateApiService.addImprovement(this.iterationService.iterations[this.currentIteration - 1], this.promptForImprovement).
    subscribe({
      next: res => {
        this.resetPrompt();
        this.addIteration(res.newEstimate);
      },
      error: error => {
        console.log(error);
      },
      complete: () => {
      }
    });
  }

  resetPrompt(){
    this.promptForImprovement = "";
  }

  addIteration(iteration: string) {
    const count = this.iterationService.count();
    this.iterationService.addIteration(iteration);
    this.currentIteration ++;
  }

  updateIterations(iterations: string[]) {
    this.iterationService.iterations = iterations;
  }

  finish() {
    console.log(this.iterationService.iterations[this.currentIteration - 1]);
    
  }

}
