import { Injectable, ɵsetCurrentInjector } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError, map, tap, pipe, OperatorFunction, Subscriber, from } from 'rxjs';
import { Equipment } from './Equipment'


@Injectable({
    providedIn: 'root'
  })

export class EquipmentService{
    constructor(private http: HttpClient) {}
    
    sortByAvailable() {
        return this.http.get<Equipment[]>("/api/equipment/status/?status=1");
    }

    sortByUnavailable() {
        return this.http.get<Equipment[]>("/api/equipment/status/?status=0");
    }

    listEquipment() {
        return this.http.get<Equipment[]>("/api/equipment");
    }

    addEquipment(id: number, name: string, type: string, notes: string) {
        let newEquipment: Equipment = {
            "id": id,
            "name": name,
            "type": type,
            "status": 1,
            "notes":notes 
        };
        return this.http.post<Equipment>("/api/equipment", newEquipment);
    }

    updateEquipment(id: number, name: string, type: string, notes: string) {
        let newEquipment: Equipment = {
            "id": id,
            "name": name,
            "type": type,
            "status": 1,
            "notes":notes 
        };
        return this.http.put<Equipment>("/api/equipment", newEquipment);
    }

    deleteEquipment(equipment_id: number){
        return this.http.delete<void>("/api/equipment?equipment_id=" + equipment_id);
    }

}