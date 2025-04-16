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
    path: 'issues',
    title: 'Course',
    component: IssueComponent,
    canActivate: [myCoursesInstructorGuard]
  };

  issues = signal<Issue[]>([]);

  ngOnInit() {
    this.getAllAssignmentsConcepts().subscribe((data: IssueWrapper) => {
      console.log(data);
      this.issues.set(data.issues);
    });
  }

  navigateToTickets(): void {
    this.router.navigate([`/course/${this.courseSiteId}/issues/${issue_id}`]);
  }

  courseSiteId: string;

  constructor(
    private route: ActivatedRoute,
    private client: HttpClient,
    private router: Router
  ) {
    this.courseSiteId = this.route.parent!.snapshot.params['course_site_id'];
  }

  getAllAssignmentsConcepts(): Observable<IssueWrapper> {
    return this.client.get<IssueWrapper>(
      `/api/office-hours/assignments/${this.courseSiteId}`
    );
  }
}
