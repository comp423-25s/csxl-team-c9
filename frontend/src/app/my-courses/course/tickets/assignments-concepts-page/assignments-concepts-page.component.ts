import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { myCoursesInstructorGuard } from 'src/app/my-courses/my-courses.guard';

@Component({
  selector: 'app-assignments-concepts-page',
  standalone: true,
  imports: [],
  templateUrl: './assignments-concepts-page.component.html',
  styleUrl: './assignments-concepts-page.component.css'
})
export class AssignmentsConceptsPageComponent {
  public static Route = {
    path: 'tickets',
    title: 'Course',
    component: AssignmentsConceptsPageComponent,
    canActivate: [myCoursesInstructorGuard]
  };

  constructor(private route: ActivatedRoute) {}
}
