import { Injectable } from '@angular/core';
import { FormattedData } from '../../../Core/models/formated-data.interface';
import { Predictions } from '../../../Core/models/estimates.interface';

@Injectable({
  providedIn: 'root'
})
export class EstimatesService {
  originalData?:Predictions[];
  estimatesRLM?:Predictions[];
  estimatesXGB?:Predictions[];
  complexities?: number[];

  getComplexities(): string[]{
    return this.complexities?.map(c => c.toString()) || [];
  }

  getOriginalDataQA(){
    return this.originalData?.map(c => c.t_qa) || [];
  }


  getOriginalDataBK(){
    return this.originalData?.map(c => c.t_backend) || [];
  }

  getOriginalDataFR(){
    return this.originalData?.map(c => c.t_frontend) || [];
  }

  getOriginalDataDS(){
    return this.originalData?.map(c => c.t_design) || [];
  }

  getEstimatesRLMQA(){
    return this.estimatesRLM?.map(c => c.t_qa) || [];
  }

  getEstimatesRLMBK(){
    return this.estimatesRLM?.map(c => c.t_backend) || [];
  }

  getEstimatesRLMFR(){
    return this.estimatesRLM?.map(c => c.t_frontend) || [];  
  }

  getEstimatesRLMDS(){
    return this.estimatesRLM?.map(c => c.t_design) || [];
  }


  getEstimatesXGBQA(){
    return this.estimatesXGB?.map(c => c.t_qa) || [];
  }

  getEstimatesXGBBK(){
    return this.estimatesXGB?.map(c => c.t_backend) || [];
  }

  getEstimatesXGBFR(){
    return this.estimatesXGB?.map(c => c.t_frontend) || [];
  }

  getEstimatesXGBDS(){
    return this.estimatesXGB?.map(c => c.t_design) || [];
  }


}
