import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { MainLayoutComponent } from './layouts/main-layout/main-layout.component';
import { NotFoundComponent } from './pages/not-found/not-found.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';

export const routes: Routes = [
    {
        path: '',
        component: LoginComponent
    },
    {
        path: 'home',
        component: MainLayoutComponent,
        children: [
            {
                path: '',
                component: DashboardComponent
            },
            {
                path: 'estimates',
                loadComponent: () => import('./features/estimates/estimates.component').
                    then(c => c.EstimatesComponent)
            },
            {
                path: 'settings',
                loadComponent: () => import('./features/settings/settings.component')
                    .then(c => c.SettingsComponent)
            },
            {
                path: 'create-estimate',
                loadComponent: () => import('./features/estimates/components/create-estimate/create-estimate.component')
                    .then(c => c.CreateEstimateComponent)
            },
            {
                path: 'estimate-effort',
                loadComponent: () => import('./features/estimates/components/estimate-effort/estimate-effort.component')
                    .then(c => c.EstimateEffortComponent)
            },
            {
                path: 'iterations',
                loadComponent: () => import('./features/estimates/components/create-estimate/iterations/iterations.component')
                    .then(c => c.IterationsComponent)
            },
            {
                path: 'view-estimate/:id',
                loadComponent: () => import('./features/estimates/components/view-estimate/view-estimate.component')
                    .then(c => c.ViewEstimateComponent)
            },
            {
                path: 'show-estimates',
                loadComponent: () => import('./features/estimates/components/show-estimates/show-estimates.component')
                    .then(c => c.ShowEstimatesComponent)
            },
        ]
    },
    {
        path: '**',
        component: NotFoundComponent
    }
];
