import { HttpClient } from '@angular/common/http';
import { Component, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { myCoursesInstructorGuard } from 'src/app/my-courses/my-courses.guard';
import { Issue, IssueWrapper } from 'src/app/my-courses/my-courses.model';

@Component({
  selector: 'app-issue',
  standalone: true,
  imports: [],
  templateUrl: './issue.component.html',
  styleUrl: './issue.component.css'
})
export class IssueComponent {
  public static Route = {
    path: 'ticket_categories/:ticket_category_id/issues',
    title: 'Course',
    component: IssueComponent,
    canActivate: [myCoursesInstructorGuard]
  };

  issues = signal<Issue[]>([]);

  ticket_category_id: string;

  ngOnInit() {
    this.route.paramMap.subscribe((params) => {
      this.ticket_category_id = params.get('ticket_category_id')!;
      this.getAllAssignmentsConcepts().subscribe((data: IssueWrapper) => {
        console.log(data);
        this.issues.set(data.issues);
      });
    });
  }

  navigateToTickets(issue_id: number): void {
    this.router.navigate([`/course/${this.courseSiteId}/issues/${issue_id}`]);
  }

  courseSiteId: string;

  constructor(
    private route: ActivatedRoute,
    private client: HttpClient,
    private router: Router
  ) {
    this.courseSiteId = this.route.parent!.snapshot.params['course_site_id'];
    this.ticket_category_id =
      this.route.parent!.snapshot.params['ticket_category_id'];
  }

  getAllAssignmentsConcepts(): Observable<IssueWrapper> {
    return this.client.get<IssueWrapper>(
      `/api/office-hours/assignments/${this.ticket_category_id}`
    );
  }
}
