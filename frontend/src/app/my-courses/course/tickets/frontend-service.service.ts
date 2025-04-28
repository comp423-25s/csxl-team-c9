import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AssignmentsConcepts } from 'src/app/my-courses/my-courses.model';
import { TicketWrapper } from 'src/app/my-courses/my-courses.model';
import { IssueWrapper } from 'src/app/my-courses/my-courses.model';

@Injectable({
  providedIn: 'root'
})
export class FrontendServiceService {
  constructor(private client: HttpClient) {}

  getAllAssignmentsConcepts(
    courseSiteId: string
  ): Observable<AssignmentsConcepts> {
    return this.client.get<AssignmentsConcepts>(
      `/api/office-hours/assignments-concepts/${courseSiteId}`
    );
  }

  getAllIssues(issue_id: string): Observable<TicketWrapper> {
    return this.client.get<TicketWrapper>(
      `/api/office-hours/issues/${issue_id}`
    );
  }

  getAllTickets(ticket_category_id: string): Observable<IssueWrapper> {
    return this.client.get<IssueWrapper>(
      `/api/office-hours/assignments/${ticket_category_id}`
    );
  }
}
