import { Component } from '@angular/core';
import { courseSitePageGuard } from '../../office-hours/office-hours.guard';

@Component({
  selector: 'app-issue',
  standalone: true,
  imports: [],
  templateUrl: './issue.component.html',
  styleUrl: './issue.component.css'
})
export class IssueComponent {
  public static Route = {
    path: 'issue/:event_id/edit',
    title: 'Issue Component',
    component: IssueComponent,
    canActivate: [courseSitePageGuard(['UTA', 'GTA', 'Instructor'])],
    resolve: {}
  };
}
