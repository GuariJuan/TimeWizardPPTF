import { Component } from '@angular/core';
import { EstimatesTableComponent } from "./components/estimates-table/estimates-table.component";
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-estimates',
  standalone: true,
  imports: [EstimatesTableComponent, RouterLink],
  templateUrl: './estimates.component.html',
  styleUrl: './estimates.component.scss'
})
export class EstimatesComponent {

}
