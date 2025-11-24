import { Component, inject, model } from '@angular/core';
import { Estimate } from '../../../../Core/models/estimate.interface';
import { FormsModule, NgModel, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-estimates-table',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule, RouterLink],
  templateUrl: './estimates-table.component.html',
  styleUrl: './estimates-table.component.scss'
})
export class EstimatesTableComponent {
  searchValue = model<string>('');
  page: number = 0;
  pageSize: number = 3; //elementos por pagina
  estimates: Estimate[] = [];
  currentPage = 1;
  pageElements: Estimate[] = [];
  numberPages: number[] = [];
  listFilter: Estimate[] = [];
  projectsTypes = [
    { name: 'Desarrollo Web' },
    { name: 'Aplicación Movil' },
    { name: 'API Backend' }
  ];



  ngOnInit() {
    this.getEstimates();
  }

  nextPage() {
    this.currentPage++;
    this.page += this.pageSize;
    this.setElementsToPage(this.page);
  }

  selectPage(page: number) {
    this.currentPage = page;
    this.page = (page - 1) * this.pageSize;
    this.setElementsToPage(this.page);
  }

  prevPage() {
    this.currentPage--;
    if (this.page > 0)
      this.page -= this.pageSize;
    this.setElementsToPage(this.page);
  }

  changePageSize(pageSize: number) {
    this.pageSize = pageSize;
    this.page = 0;
    this.currentPage = 1;
    this.setElementsToPage(this.page);
    this.calculateNumberPages();
  }

  getEstimates() {
    this.estimates = [
      {
        id: 1,
        name: 'Landing Page Corporativa',
        description: 'Estimación para una landing page institucional con diseño responsive y formulario de contacto.',
        created_at: this.getRandomDate(),
        updated_at: new Date(),
        type: 'Desarrollo Web'
      },
      {
        id: 2,
        name: 'Panel de Administración E-commerce',
        description: 'Estimación de desarrollo para un panel de administración de productos, usuarios y pedidos.',
        created_at: this.getRandomDate(),
        updated_at: new Date(),
        type: 'Desarrollo Web'
      },
      {
        id: 3,
        name: 'App de Reservas Médicas',
        description: 'Estimación para una app móvil que permita a pacientes agendar turnos y recibir recordatorios.',
        created_at: this.getRandomDate(),
        updated_at: new Date(),
        type: 'Aplicación Movil'
      },
      {
        id: 4,
        name: 'App de Delivery de Comida',
        description: 'Estimación de una app con geolocalización, catálogo, y sistema de pedidos en tiempo real.',
        created_at: this.getRandomDate(),
        updated_at: new Date(),
        type: 'Aplicación Movil'
      },
      {
        id: 5,
        name: 'API para Gestión de Inventario',
        description: 'Estimación de un backend RESTful con endpoints para altas, bajas y reportes de stock.',
        created_at: this.getRandomDate(),
        updated_at: new Date(),
        type: 'API Backend'
      },
      {
        id: 6,
        name: 'Microservicio de Autenticación',
        description: 'Estimación de un microservicio para login, registro y manejo de tokens JWT.',
        created_at: this.getRandomDate(),
        updated_at: new Date(),
        type: 'API Backend'
      },
      {
        id: 7,
        name: 'Dashboard de Métricas en Tiempo Real',
        description: 'Estimación para el desarrollo de un dashboard con gráficos interactivos y actualizaciones vía WebSocket.',
        created_at: this.getRandomDate(),
        updated_at: new Date(),
        type: 'Desarrollo Web'
      },
      {
        id: 8,
        name: 'App de Finanzas Personales',
        description: 'Estimación de una app móvil que permite registrar gastos, generar alertas y visualizar reportes.',
        created_at: this.getRandomDate(),
        updated_at: new Date(),
        type: 'Aplicación Movil'
      }
    ];    
    this.listFilter = this.estimates;
    this.calculateNumberPages();
    this.setElementsToPage(this.page);
  }

  setElementsToPage(page: number) {
    this.pageElements = this.listFilter.slice(page, page + this.pageSize);
  }

  calculateNumberPages() {
    this.numberPages = [];
    const count = Math.ceil(this.listFilter.length / this.pageSize);
    for (let i = 0; i < count; i++) {
      this.numberPages.push(i);
    };

    if (this.numberPages.length === 1) {
      this.selectPage(1);
    }
  }

  onInputChange(event: Event) {
    const inputValue = (event.target as HTMLInputElement).value;
    if (inputValue) {
      this.listFilter = this.estimates.filter((estimate) => {
        return estimate.name?.toLowerCase().includes(inputValue.toLowerCase());
      });
    } else {
      this.listFilter = this.estimates
    }
    this.page = 0;
    this.currentPage = 1;
    this.calculateNumberPages();
    this.setElementsToPage(this.page);
    this.resetSearch('searchType');
  }

  resetSearch(idHtml: string) {
    const inputValue = document.getElementById(idHtml) as HTMLInputElement;
    if (inputValue) {      
      inputValue.value = '';
    }
  }


  changeType(event: Event) {
    const inputValue = (event.target as HTMLInputElement).value;
    if (inputValue) {
      this.listFilter = this.estimates.filter((estimate) => {
        return estimate.type?.toLowerCase().includes(inputValue.toLowerCase());
      });
    } else {
      this.listFilter = this.estimates
    }
    this.page = 0;
    this.currentPage = 1;
    this.calculateNumberPages();
    this.setElementsToPage(this.page);
    this.resetSearch('searchByName');
  }

  getRandomDate() {
    const randomDays = Math.floor(Math.random() * 30) + 1;
    const today = new Date();
    today.setDate(today.getDate() - randomDays);
    return today;
  }



}
