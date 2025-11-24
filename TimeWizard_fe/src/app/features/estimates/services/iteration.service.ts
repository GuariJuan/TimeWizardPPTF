import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class IterationService {
  iterations: string[] = [];
  count = signal(0);

  addIteration(iteration: string) {
    this.iterations.push(iteration);
    this.count.set(this.iterations.length);
  }

}
