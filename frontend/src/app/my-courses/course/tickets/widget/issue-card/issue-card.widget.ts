import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { AssignmentsConcepts } from 'src/app/my-courses/my-courses.model';
//import { CourseSiteOverview } from '../../my-courses.model';

@Component({
  selector: 'app-issue-card',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, CommonModule],
  templateUrl: './issue-card.widget.html',
  styleUrl: './issue-card.widget.scss'
})
export class IssueCardWidget {
  /** Term for the course */
  @Input() name!: string;
  /** The course to show */
  @Input() numTickets!: number;
  @Input() issueID!: number;

  @Output() viewClicked = new EventEmitter<number>();

  onView() {
    console.log('Button clicked!');
    this.viewClicked.emit(this.issueID);
  }
}
