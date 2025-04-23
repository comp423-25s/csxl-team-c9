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
    path: 'issues/:issue_id',
    title: 'Course',
    component: GroupComponent,
    canActivate: [myCoursesInstructorGuard]
  };

  issue_id: string;

  constructor(
    private route: ActivatedRoute,
    private client: HttpClient
  ) {
    this.issue_id = this.route.parent!.snapshot.params['issue_id'];
  }

  tickets = signal<Ticket[]>([]);

  ngOnInit() {
    this.route.paramMap.subscribe((params) => {
      this.issue_id = params.get('issue_id')!;
      this.getAllAssignmentsConcepts().subscribe((data: TicketWrapper) => {
        console.log(data);
        this.tickets.set(data.tickets);
      });
    });
  }

  getAllAssignmentsConcepts(): Observable<TicketWrapper> {
    return this.client.get<TicketWrapper>(
      `/api/office-hours/issues/${this.issue_id}`
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
