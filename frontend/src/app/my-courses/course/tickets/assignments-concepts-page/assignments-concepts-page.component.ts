import { HttpClient } from '@angular/common/http';
import { Component, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { myCoursesInstructorGuard } from 'src/app/my-courses/my-courses.guard';
import {
  AssignmentConcept,
  AssignmentsConcepts
} from 'src/app/my-courses/my-courses.model';
import { AssignmentCardWidget } from 'src/app/my-courses/course/tickets/widget/assignment-card/assignment-card.widget';
import { Router } from '@angular/router';
import { consumerPollProducersForChange } from '@angular/core/primitives/signals';

@Component({
  selector: 'app-assignments-concepts-page',
  standalone: true,
  imports: [AssignmentCardWidget],
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

  assnConcepts = signal<AssignmentsConcepts>({
    assignments: [],
    concepts: []
  });

  length = signal<number>(0);

  ngOnInit() {
    this.getAllAssignmentsConcepts().subscribe((data: AssignmentsConcepts) => {
      console.log(data);
      this.assnConcepts.set(data);
      this.length.set(data.concepts.length);
    });
  }
  courseSiteId: string;

  navigateToIssues(ticket_category_id: number): void {
    this.router.navigate([
      `/course/${this.courseSiteId}/ticket_categories/${ticket_category_id}/issues`
    ]);
  }

  constructor(
    private route: ActivatedRoute,
    private client: HttpClient,
    private router: Router
  ) {
    this.courseSiteId = this.route.parent!.snapshot.params['course_site_id'];
  }

  getAllAssignmentsConcepts(): Observable<AssignmentsConcepts> {
    return this.client.get<AssignmentsConcepts>(
      `/api/office-hours/assignments-concepts/${this.courseSiteId}`
    );
  }
}
