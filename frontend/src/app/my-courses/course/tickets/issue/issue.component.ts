import { HttpClient } from '@angular/common/http';
import { Component, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { FrontendServiceService } from '../frontend-service.service';
import { myCoursesInstructorGuard } from 'src/app/my-courses/my-courses.guard';
import { Issue, IssueWrapper } from 'src/app/my-courses/my-courses.model';
import { IssueCardWidget } from '../widget/issue-card/issue-card.widget';

@Component({
  selector: 'app-issue',
  standalone: true,
  imports: [IssueCardWidget],
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

  // need an issues list
  issues = signal<Issue[]>([]);

  ticket_category_id: string;

  // need an API request for getting the issues associated with current assignment or concept
  ngOnInit() {
    this.route.paramMap.subscribe((params) => {
      this.ticket_category_id = params.get('ticket_category_id')!;
      this.service
        .getAllTickets(this.ticket_category_id)
        .subscribe((data: IssueWrapper) => {
          console.log(data);
          this.issues.set(data.issues);
        });
    });
  }

  // changes active URL to navigate to hierarchical page
  navigateToTickets(issue_id: number): void {
    this.router.navigate([`/course/${this.courseSiteId}/issues/${issue_id}`]);
  }

  courseSiteId: string;

  constructor(
    private route: ActivatedRoute,
    private client: HttpClient,
    private router: Router,
    private service: FrontendServiceService
  ) {
    // get the ids from the URL
    this.courseSiteId = this.route.parent!.snapshot.params['course_site_id'];
    this.ticket_category_id =
      this.route.parent!.snapshot.params['ticket_category_id'];
  }
}
