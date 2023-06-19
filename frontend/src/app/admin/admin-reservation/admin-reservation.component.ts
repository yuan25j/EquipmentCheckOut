import { Component } from '@angular/core';
import { MatTable } from '@angular/material/table'
import { Reservation } from '../../Reservation';
import { Equipment } from '../../Equipment';
import { User } from '../../User';
import { ReservationService } from '../../reservation.service';
import { ProfileService, Profile } from '../../profile/profile.service';
import { permissionGuard } from 'src/app/permission.guard';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-admin-reservation',
  templateUrl: './admin-reservation.component.html',
  styleUrls: ['./admin-reservation.component.css']
})
export class AdminReservationComponent {
  columnsToDisplay = ['type', 'equipment', 'notes', 'pid', 'delete_button'];
  reservationsList: Reservation[] = [];

  public static Route = {
    path: 'reservations',
    component: AdminReservationComponent,
    title: 'Reservations',
    canActivate: [permissionGuard('user.list', 'user/')],
    
  }

  constructor(
    private reservationService: ReservationService,
    private profileService: ProfileService,
    private router: Router,

  ) {
    this.updateList();
  }
  
  updateList() {
    this.profileService.profile$.subscribe(
      (profile: Profile | undefined) => {
        if (profile === undefined)
          return;
        this.reservationService.listReservation().subscribe((reservations: Reservation[]) => {
          this.reservationsList = reservations;
        })
    });
  }

  deleteReservation(reservationId: number): void {
    this.reservationService.deleteReservation(reservationId).subscribe(() => {
      this.updateList();
    });
  }

  onClick(user: Profile) {
    this.router.navigate(['admin', 'users', user.id]);
  }

}
