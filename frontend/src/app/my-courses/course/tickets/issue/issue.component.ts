import { HttpClient } from '@angular/common/http';
import { Component, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { myCoursesInstructorGuard } from 'src/app/my-courses/my-courses.guard';
import { Issue } from 'src/app/my-courses/my-courses.model';

@Component({
  selector: 'app-issue',
  standalone: true,
  imports: [],
  templateUrl: './issue.component.html',
  styleUrl: './issue.component.css'
})
export class IssueComponent {
  public static Route = {
    path: 'issue',
    title: 'Course',
    component: IssueComponent,
    canActivate: [myCoursesInstructorGuard]
  };

  issues = signal<Issue[]>([]);

  ngOnInit() {
    this.getAllAssignmentsConcepts().subscribe((data: Issue[]) => {
      console.log(data);
      this.issues.set(data);
    });
  }

  courseSiteId: string;

  constructor(
    private route: ActivatedRoute,
    private client: HttpClient
  ) {
    this.courseSiteId = this.route.parent!.snapshot.params['course_site_id'];
  }

  getAllAssignmentsConcepts(): Observable<Issue[]> {
    return this.client.get<Issue[]>(`/api/office-hours/assignments/1`);
  }
}
