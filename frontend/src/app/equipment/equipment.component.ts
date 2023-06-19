import { Component } from '@angular/core';
import { MatTable } from '@angular/material/table'
import { Equipment } from '../Equipment';
import { EquipmentService } from '../equipment.service';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { UpdateEquipmentFormService } from '../update-equipment-form.service';
import { ReservationService } from '../reservation.service';
import { Reservation } from '../Reservation';
import { Profile, ProfileService } from '../profile/profile.service';
import { PermissionService } from '../permission.service';
import { User } from '../User';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Dialog } from '@angular/cdk/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatSlideToggleChange } from '@angular/material/slide-toggle'

@Component({
  selector: 'app-equipment',
  templateUrl: './equipment.component.html',
  styleUrls: ['./equipment.component.css']
})
export class EquipmentComponent {
  columnsToDisplay = ['name', 'type', 'status', 'notes', 'reserve_button', 'edit_button', 'delete_button'];
  equipmentList: Equipment[] = [];
  canEditEquipment: boolean = false;
  canDeleteEquipment: boolean = false;
  filterByStatus: boolean = false;

  constructor(
    private equipmentService: EquipmentService,
    private editEquipmentFormService: UpdateEquipmentFormService,
    private reservationService: ReservationService,
    private profileService: ProfileService,
    private permissionService: PermissionService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    this.updateList();
    this.permissionService.check("equipment.update", "*").subscribe((perm: boolean) => {this.canEditEquipment = perm});
    this.permissionService.check("equipment.delete", "*").subscribe((perm: boolean) => {this.canDeleteEquipment = perm});
  }

  updateList() {
    if (this.filterByStatus)
      this.equipmentService.sortByAvailable().subscribe((data: Equipment[]) => {this.equipmentList = data});
    else
      this.equipmentService.listEquipment().subscribe((data: Equipment[]) => {this.equipmentList = data});
  }

  editEquipment(equipment: Equipment): void {
    this.editEquipmentFormService.setEquipment(equipment);
    this.router.navigate(['/equipment/edit']);
  }

  deleteEquipment(equipmentId: number) {
    this.equipmentService.deleteEquipment(equipmentId).subscribe(() => {
      this.updateList();
    });
  }

  reserveEquipment(equipment: Equipment): void {
    this.profileService.profile$.subscribe((profile: Profile | undefined) => {
      if (profile == null) {
        this.snackBar.open("Invalid profile", "", { duration: 2000 });
        return;
      }

      let createReservation = (profile: Profile | null) => {
        if (profile == null) {
          this.snackBar.open("Invalid profile", "", { duration: 2000 });
          return;
        }
        let user = profile? {id: profile.id, first_name: profile.first_name?? "", last_name: profile.last_name?? "", pid: profile.pid} : undefined;
        this.reservationService.createReservation(equipment.type, user?? {id: null, pid: 0, first_name: "", last_name: ""}, equipment, equipment.notes).subscribe(
          () => {this.updateList();}
        );
      };
      if (profile.id == null) {
        this.profileService.put(profile).subscribe((profile) => {
          createReservation(profile);
        });
      } else {
        createReservation(profile);
      }
    });
  }

  statusToString(status: number): string {
    switch (status) {
      case 0:
        return "Unavailable"
      case 1:
        return "Available"
      default:
        return "Unknown"
    }
  }

  toggleStatusFilter(event: MatSlideToggleChange) {
    this.filterByStatus = event.checked;
    this.updateList();
  }
}
