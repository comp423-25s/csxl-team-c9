import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges,
  WritableSignal,
  signal
} from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { Ticket } from 'src/app/my-courses/my-courses.model';
//import { CourseSiteOverview } from '../../my-courses.model';

@Component({
  selector: 'app-ticket-card',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, CommonModule],
  templateUrl: './ticket-card.widget.html',
  styleUrl: './ticket-card.widget.scss'
})
export class TicketCardWidget implements OnChanges {
  @Input() ticket!: Ticket;
  @Output() closeButtonPressed = new EventEmitter<Ticket>();
  expanded: WritableSignal<boolean> = signal(false);

  constructor() {}

  toggleExpanded() {
    this.expanded.set(!this.expanded());
  }

  closeButtonEvent() {
    this.closeButtonPressed.emit(this.ticket);
  }

  ngOnChanges(changes: SimpleChanges): void {
    // If open the ticket the it is open
    this.expanded.set(true);
  }
}
