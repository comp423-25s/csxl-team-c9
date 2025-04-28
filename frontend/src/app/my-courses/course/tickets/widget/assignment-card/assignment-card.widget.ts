import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { AssignmentsConcepts } from 'src/app/my-courses/my-courses.model';
//import { CourseSiteOverview } from '../../my-courses.model';

@Component({
  selector: 'app-assignment-card',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, CommonModule],
  templateUrl: './assignment-card.widget.html',
  styleUrl: './assignment-card.widget.scss'
})
export class AssignmentCardWidget {
  /** Term for the course */
  @Input() name!: string;
  /** The course to show */
  @Input() numTickets!: number;
  @Input() assignmentID!: number;

  @Output() viewClicked = new EventEmitter<void>(); // no need to send any data

  onView() {
    console.log('Button clicked!');
    this.viewClicked.emit();
  }
}
