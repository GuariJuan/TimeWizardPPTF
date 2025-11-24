import { Component, inject } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { SpinnerComponent } from '../../shared/components/spinner/spinner.component';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterLink, SpinnerComponent],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {
  router = inject(Router);
  isLoading = false;
  logout() {
    this.isLoading = true;
    
    setTimeout(() => {
      this.isLoading = false;
      this.router.navigate(['']);
    }, 1500);
    
  }
}
