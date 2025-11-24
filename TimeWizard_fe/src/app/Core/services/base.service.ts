import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class BaseService {
  private _http = inject(HttpClient);

  get http(): HttpClient {
    return this._http;
  }

  get url(): string {
    return environment.API_URL;
  }

}
