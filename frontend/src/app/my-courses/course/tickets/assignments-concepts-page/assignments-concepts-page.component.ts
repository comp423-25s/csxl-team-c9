import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { myCoursesInstructorGuard } from 'src/app/my-courses/my-courses.guard';
import { AssignmentsConcepts } from 'src/app/my-courses/my-courses.model';

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

  courseSiteId: string;

  constructor(
    private route: ActivatedRoute,
    private client: HttpClient
  ) {
    this.courseSiteId = this.route.parent!.snapshot.params['course_site_id'];
  }

  getAllAssignmentsConcepts(): Observable<AssignmentsConcepts> {
    return this.client.get<AssignmentsConcepts>(
      `/api/office-hours/assignments-concepts`
    );
  }
}
