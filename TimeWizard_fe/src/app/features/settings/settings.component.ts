import { Component, inject, Renderer2 } from '@angular/core';
import { ThemeService } from '../../Core/services/theme.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.scss'
})
export class SettingsComponent {
  renderer = inject(Renderer2);
  themeService = inject(ThemeService);
  selectedLanguage = 'es';
  notificationsEnabled = true;
  fontSize = 'medium';

  get currentTheme() {
    return this.themeService.getCurrentTheme();
  }

  toggleTheme() {
    this.themeService.toggleTheme();
  }

  resetSettings() {
    this.selectedLanguage = 'es';
    this.notificationsEnabled = true;
    this.fontSize = 'medium';
  }

}
