import { Component } from '@angular/core';
import { officeHourPageGuard } from '../../office-hours/office-hours.guard';

@Component({
  selector: 'app-group',
  standalone: true,
  imports: [],
  templateUrl: './group.component.html',
  styleUrl: './group.component.css'
})
export class GroupComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    //path: 'office-hours/:event_id/queue',
    title: 'Groups',
    component: GroupComponent,
    canActivate: [officeHourPageGuard(['UTA', 'GTA', 'Instructor'])]
  };
}
