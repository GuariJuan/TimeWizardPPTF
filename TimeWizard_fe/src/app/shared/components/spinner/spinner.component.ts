import { CommonModule } from '@angular/common';
import { Component, Input, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-spinner',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './spinner.component.html',
  styleUrl: './spinner.component.scss'
})
export class SpinnerComponent {
  @Input() isLoading = false;
  @Input() messages: string[] = []; // Lista de mensajes opcionales
  @Input() rowCount = 1500;
  currentMessage = '';
  private messageIndex = 0;
  private intervalId: any;
  private charIndex = 0;
  private typingSpeed = 120; 

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['isLoading']) {
      if (this.isLoading) {
        this.startMessageRotation();
      } else {
        this.stopMessageRotation();
      }
    }
  }

  private startMessageRotation(): void {
    if (this.messages.length > 0) {
      // this.currentMessage = this.messages[this.messageIndex];
      // this.intervalId = setInterval(() => {
      //   // this.messageIndex = (this.messageIndex + 1) % this.messages.length;
      //   this.currentMessage = this.messages[this.messageIndex];
      //   this.messageIndex = this.messageIndex < this.messages.length - 1 ? this.messageIndex + 1 : this.messages.length - 1;
      // }, this.rowCount * 3 < 1000 ? 1500 : this.rowCount * 3); 
      this.messageIndex = 0;
      this.typeMessage();
    }
  }


  private typeMessage(): void {
    this.charIndex = 0;
    this.currentMessage = '';

    this.intervalId = setInterval(() => {
      const fullMessage = this.messages[this.messageIndex];

      if (this.charIndex < fullMessage.length) {
        this.currentMessage += fullMessage[this.charIndex];
        this.charIndex++;
      } else {
        clearInterval(this.intervalId);
        setTimeout(() => {
          this.messageIndex = this.messageIndex < this.messages.length - 1 ? this.messageIndex + 1 : this.messages.length - 1;
          this.typeMessage(); // Inicia el próximo mensaje
        }, this.rowCount * 4 ); // Pausa antes de escribir el siguiente mensaje
      }
    }, this.typingSpeed);
  }

  private stopMessageRotation(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      this.currentMessage = ''; 
    }
  }

  ngOnDestroy(): void {
    this.stopMessageRotation(); // Limpia el intervalo si el componente se destruye
  }

}
