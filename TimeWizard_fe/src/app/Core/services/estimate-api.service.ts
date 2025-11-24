import { Injectable } from '@angular/core';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { IPredictions } from '../models/prediction.interface';
import { IEstimates } from '../models/estimates.interface';

@Injectable({
  providedIn: 'root'
})
export class EstimateApiService extends BaseService {

  addImprovement(estimate: string, infoToAdd: string): Observable<any> {
    const body = { estimate: estimate, infoToAdd: infoToAdd }; 
    return this.http.post(`${this.url}/Estimate`, body);
  }

  estimateWithRLM(data: any): Observable<IPredictions> {
    return this.http.post(`${this.url}/predict-all/`, data) as Observable<IPredictions>;
  }


  estimateWithXGB(data: any): Observable<IPredictions> {
    return this.http.post(`${this.url}/predict-all-xgb/`, data) as Observable<IPredictions>;
  }

  estimateAllWithRLM(data: any): Observable<IEstimates> {
    return this.http.post(`${this.url}/predict-all-batch/`, data) as Observable<IEstimates>;
  }

  estimateAllWithXGB(data: any): Observable<IEstimates> {
    return this.http.post<IEstimates>(`${this.url}/predict-all-batch-xgb/`, data);
  }

}
