import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { myCoursesInstructorGuard } from 'src/app/my-courses/my-courses.guard';

@Component({
  selector: 'app-group',
  standalone: true,
  imports: [],
  templateUrl: './group.component.html',
  styleUrl: './group.component.css'
})
export class GroupComponent {
  public static Route = {
    path: 'ticket-group',
    title: 'Course',
    component: GroupComponent,
    canActivate: [myCoursesInstructorGuard]
  };

  constructor(private route: ActivatedRoute) {}
}
