import { Component } from '@angular/core';
import { courseSitePageGuard } from '../../office-hours/office-hours.guard';

@Component({
  selector: 'app-assignments-concepts-page',
  standalone: true,
  imports: [],
  templateUrl: './assignments-concepts-page.component.html',
  styleUrl: './assignments-concepts-page.component.css'
})
export class AssignmentsConceptsPageComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'assignment-concepts-page',
    title: 'Assignments Concepts Page Component',
    component: AssignmentsConceptsPageComponent,
    canActivate: [courseSitePageGuard(['UTA', 'GTA', 'Instructor'])],
    resolve: {}
  };
}
