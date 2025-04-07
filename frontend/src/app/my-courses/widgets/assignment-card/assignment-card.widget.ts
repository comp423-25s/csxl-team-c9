import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-assignment-card',
  standalone: true,
  imports: [MatCardModule, MatButtonModule],
  templateUrl: './assignment-card.widget.html',
  styleUrl: './assignment-card.widget.css'
})
export class AssignmentCardWidget {
  /** Term for the course */
  //@Input() termId!: string;
  /** The course to show */
  //@Input() course!: CourseSiteOverview;
}
