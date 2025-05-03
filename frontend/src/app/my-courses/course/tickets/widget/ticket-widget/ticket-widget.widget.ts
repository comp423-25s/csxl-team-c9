/**
 * The Called Ticket Card widget defines the UI card for
 * a called ticket in an OH queue.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges,
  Type,
  WritableSignal,
  signal
} from '@angular/core';
import { OfficeHourTicketOverview, Ticket } from '../../../../my-courses.model';
import { MatCardModule } from '@angular/material/card';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { MatDividerModule } from '@angular/material/divider';
import { UserChipList } from 'src/app/shared/user-chip-list/user-chip-list.widget';

@Component({
  selector: 'app-ticket-widget',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, CommonModule, MatDividerModule],
  templateUrl: './ticket-widget.widget.html',
  styleUrls: ['./ticket-widget.widget.scss']
})
export class TicketWidget implements OnChanges {
  @Input() ticket!: Ticket;
  @Input() calledByUser: boolean = false;
  @Input() type!: string;
  @Input() description!: string;
  @Input() id!: number;
  @Input() state!: number;
  @Input() created!: string;
  @Input() called!: string;
  @Input() closed!: string | null;
  @Input() have_concerns!: boolean;
  @Input() caller_notes!: string;
  @Input() caller_id!: number;
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
    if (changes['calledByUser'] && changes['calledByUser'].currentValue) {
      this.expanded.set(true);
    }

    const raw = marked.parse(this.description || '') as string;
    this.description = DOMPurify.sanitize(raw);
  }
}
