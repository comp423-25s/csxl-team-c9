import { HttpClient } from '@angular/common/http';
import { Component, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { myCoursesInstructorGuard } from 'src/app/my-courses/my-courses.guard';
import {
  AssignmentConcept,
  AssignmentsConcepts
} from 'src/app/my-courses/my-courses.model';
import { Router } from '@angular/router';
import { AssignmentCardWidget } from 'src/app/my-courses/course/tickets/widgets/assignment-card/assignment-card.widget';
//import { AssignmentCardComponent } from '../widgets/assignment-card/assignment-card.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-assignments-concepts-page',
  standalone: true,
  imports: [AssignmentCardWidget, CommonModule],
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

  ngOnInit() {
    this.getAllAssignmentsConcepts().subscribe((data: AssignmentsConcepts) => {
      console.log(data);
      this.assnConcepts.set(data);
    });
  }
  courseSiteId: string;

  navigateToIssues(): void {
    console.log('MFOOFMFMF');
    this.router.navigate([`/course/${this.courseSiteId}/issues`]);
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
      `/api/office-hours/assignments-concepts`
    );
  }
}
