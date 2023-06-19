import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppTitleStrategy } from './app-title.strategy';
import { GateComponent } from './gate/gate.component';
import { HomeComponent } from './home/home.component';
import { EquipmentComponent } from './equipment/equipment.component';
import { ReservationsComponent } from './reservations/reservations.component';
import { ProfileEditorComponent } from './profile/profile-editor/profile-editor.component';
import { UpdateEquipmentFormComponent } from './update-equipment-form/update-equipment-form.component';


const routes: Routes = [
  HomeComponent.Route,
  ProfileEditorComponent.Route,
  GateComponent.Route,
  { path: 'admin', title: 'Admin', loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule) },
  { path: 'equipment', title: 'Equipment', component: EquipmentComponent },
  { path: 'reservations', title: 'Reservations', component: ReservationsComponent },
  { path: 'equipment/edit', title: 'Edit Equipment', component: UpdateEquipmentFormComponent},
  { path: 'equipment/add', title: 'Add Equipment', component: UpdateEquipmentFormComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled',
    anchorScrolling: 'enabled'
  })],
  exports: [RouterModule],
  providers: [AppTitleStrategy.Provider]
})
export class AppRoutingModule {}