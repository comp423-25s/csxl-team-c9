import { HttpClient } from '@angular/common/http';
import { Component, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { myCoursesInstructorGuard } from 'src/app/my-courses/my-courses.guard';
import { Ticket, TicketWrapper } from 'src/app/my-courses/my-courses.model';

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

  courseSiteId: string;

  constructor(
    private route: ActivatedRoute,
    private client: HttpClient
  ) {
    this.courseSiteId = this.route.parent!.snapshot.params['course_site_id'];
  }

  tickets = signal<Ticket[]>([]);

  ngOnInit() {
    this.getAllAssignmentsConcepts().subscribe((data: TicketWrapper) => {
      console.log(data);
      this.tickets.set(data.tickets);
    });
  }

  getAllAssignmentsConcepts(): Observable<TicketWrapper> {
    return this.client.get<TicketWrapper>(
      `/api/office-hours/issues/${this.courseSiteId}`
    );
  }

  IsOpen: { [key: number]: boolean } = {};

  OpenTicket(ticketId: number): void {
    //added for toggling opening ticket
    this.IsOpen[ticketId] = !this.IsOpen[ticketId];
  }

  isDetailsVisible(ticketId: number): boolean {
    return this.IsOpen[ticketId] ?? false; // is it open
  }
}
