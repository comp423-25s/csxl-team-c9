import { Component } from '@angular/core';

@Component({
  selector: 'app-assignment-card',
  standalone: true,
  imports: [],
  templateUrl: './assignment-card.widget.html',
  styleUrl: './assignment-card.widget.css'
})
export class AssignmentCardWidget {
  /** Term for the course */
  //@Input() termId!: string;
  /** The course to show */
  //@Input() course!: CourseSiteOverview;
}
