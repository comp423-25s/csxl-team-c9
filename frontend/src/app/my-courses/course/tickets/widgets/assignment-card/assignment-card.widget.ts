import { Component, Input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
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
}
