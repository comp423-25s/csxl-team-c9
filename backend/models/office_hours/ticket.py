from pydantic import BaseModel
from datetime import datetime
from typing import Literal

from .ticket_type import TicketType
from .ticket_state import TicketState

__authors__ = [
    "Ajay Gandecha",
    "Sadie Amato",
    "Bailey DeSouza",
    "Meghan Sun",
    "Maddy Andrews",
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class NewOfficeHoursTicket(BaseModel):
    """
    Pydantic model to represent a new ticket.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    description: str
    type: TicketType
    office_hours_id: int
    assignment_concept_name: str | None = None


class OfficeHoursTicket(NewOfficeHoursTicket):
    """
    Pydantic model to represent an `OfficeHoursTicket`.

    This model is based on the `OfficeHoursTicketEntity` model, which defines the shape
    of the `OfficeHoursTicket` database in the PostgreSQL database.
    """

    id: int
    state: TicketState = TicketState.QUEUED
    created_at: datetime = datetime.now()
    called_at: datetime | None
    closed_at: datetime | None
    have_concerns: bool = False
    caller_notes: str = ""
    caller_id: int | None
    issue_id: int | None = None


class AssignmentConcept(BaseModel):
    """
    Pydantic model to represent an `AssignmentConcepts`.

    This model stores the data for an assignment or concept
    """
    id: int
    name: str
    category: Literal[TicketType.ASSIGNMENT_HELP, TicketType.CONCEPTUAL_HELP]
    course_site_id: int


class Issue(BaseModel):
    """
    Pydantic model to represent an `AssignmentIssue`.

    This model stores the data for an assignments issues.
    """
    id: int
    name: str
    ticket_category_id: int