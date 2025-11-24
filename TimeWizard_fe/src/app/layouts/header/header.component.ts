import { Component, inject } from '@angular/core';
import { Router, RouterLink } from "@angular/router";

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  route = inject(Router);
  userName = this.capitalizeFirstLetter((JSON.parse(localStorage.getItem('userName') || '""') as string));
  blank = `assets/media/avatars/blank.png`;
  avatars = [
    '300-25.jpg',
    '300-26.jpg',
    '300-27.jpg',
    '300-28.jpg',
    '300-29.jpg',
    '300-30.jpg',
    'blank.png',
  ];
  randomAvatar = this.avatars[Math.floor(Math.random() * this.avatars.length)];
  avatarUrl = `assets/media/avatars/${this.randomAvatar}`;


  private capitalizeFirstLetter(nombre: string): string {
    return nombre.charAt(0).toUpperCase() + nombre.slice(1).toLowerCase();
  }
  
  redirectToHome(){
    console.log("asda");
    
    this.route.navigate(['/home'])
  }

}
