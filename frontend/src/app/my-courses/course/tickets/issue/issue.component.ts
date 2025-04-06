import { Component } from '@angular/core';
import { officeHourPageGuard } from '../../office-hours/office-hours.guard';

@Component({
  selector: 'app-issue',
  standalone: true,
  imports: [],
  templateUrl: './issue.component.html',
  styleUrl: './issue.component.css'
})
export class IssueComponent {
  public static Route = {
    //path: 'office-hours/:event_id/queue',
    title: 'Issue',
    component: IssueComponent,
    canActivate: [officeHourPageGuard(['UTA', 'GTA', 'Instructor'])]
  };
}
