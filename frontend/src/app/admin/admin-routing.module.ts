import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminComponent } from './admin.component';
import { AdminRoleDetailsComponent } from './roles/details/admin-role-details.component';
import { AdminRolesListComponent } from './roles/list/admin-roles-list.component';
import { AdminUsersListComponent } from './users/list/admin-users-list.component';
import { AdminReservationComponent } from './admin-reservation/admin-reservation.component';

const routes: Routes = [
  { path: '', component: AdminComponent, children: [
    AdminUsersListComponent.Route,
    AdminRolesListComponent.Route,
    AdminRoleDetailsComponent.Route,
    AdminReservationComponent.Route,
  ]},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
