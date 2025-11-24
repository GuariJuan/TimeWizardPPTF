import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private currentTheme = 'dark';
    toggleTheme() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-bs-theme', this.currentTheme);
    }

    getCurrentTheme() {
        return this.currentTheme;
    }
}
