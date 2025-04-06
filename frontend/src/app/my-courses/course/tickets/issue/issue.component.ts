import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { myCoursesInstructorGuard } from 'src/app/my-courses/my-courses.guard';

@Component({
  selector: 'app-issue',
  standalone: true,
  imports: [],
  templateUrl: './issue.component.html',
  styleUrl: './issue.component.css'
})
export class IssueComponent {
  public static Route = {
    path: 'tickets',
    title: 'Course',
    component: IssueComponent,
    canActivate: [myCoursesInstructorGuard]
  };

  constructor(private route: ActivatedRoute) {}
}
