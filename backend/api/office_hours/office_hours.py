
"""Office Hours API

APIs handling office hours.
"""

from fastapi import APIRouter, Depends

from ...models.office_hours.office_hours_details import PrimaryOfficeHoursDetails

from ...models.office_hours.office_hours_recurrence_pattern import (
    NewOfficeHoursRecurrencePattern,
)
from ...services.office_hours.office_hours_recurrence import (
    OfficeHoursRecurrenceService,
)
from ..authentication import registered_user
from ...services.office_hours.office_hours import OfficeHoursService
from ...models.user import User
from ...models.office_hours.office_hours import OfficeHours, NewOfficeHours, MoveTicket
from ...models.academics.my_courses import (
    OfficeHourQueueOverview,
    OfficeHourEventRoleOverview,
    OfficeHourGetHelpOverview,
)

__authors__ = ["Ajay Gandecha", "Simon Felt", "Daniel Ramsgard"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/office-hours")


@api.get("/assignments-concepts/{course_id}", tags=["Office Hours"])
def get_all_issues(
    course_id: int,
    oh_event_svc: OfficeHoursService = Depends()):
    """
    Gets all of the assignment and concepts associated with a course.
    """
    return oh_event_svc.get_all_assignments_concepts(course_id)


@api.get("/assignments/{assignment_id}", tags=["Office Hours"])
def get_all_issues(
    assignment_id: str, 
    oh_event_svc: OfficeHoursService = Depends()):
    """
    Gets all of the issues associated with specific assignemnt.
    """
    return oh_event_svc.get_all_issues(assignment_id)


@api.get("/issues/{issue_id}", tags=["Office Hours"])
def get_all_tickets(
    issue_id: str, 
    oh_event_svc: OfficeHoursService = Depends()):
    """
    Gets all tickets associated with specific issue.
    """
    return oh_event_svc.get_all_tickets_by_issue(issue_id)


@api.post("/issues/move", tags=["Office Hours"])
def get_all_tickets(
    moveTicket: MoveTicket,
    oh_event_svc: OfficeHoursService = Depends()):
    """
    Moves ticket to new issue
    """
    return oh_event_svc.move_ticket(moveTicket)


@api.delete("/issues/{issue_id}", tags=["Office Hours"])
def get_all_tickets(
    issue_id: str,
    oh_event_svc: OfficeHoursService = Depends()):
    """
    Deletes specific issue forever.
    """
    return oh_event_svc.delete_ticket(issue_id)


@api.get("/{id}/queue", tags=["Office Hours"])
def get_office_hours_queue(
    id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> OfficeHourQueueOverview:
    """
    Gets the queue overview for an office hour event.

    Returns:
        OfficeHourQueueOverview
    """
    return oh_event_svc.get_office_hour_queue(subject, id)


@api.get("/{id}/role", tags=["Office Hours"])
def get_office_hours_role(
    id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> OfficeHourEventRoleOverview:
    """
    Gets a user's role for a given office hour event.

    Returns:
        OfficeHourEventRoleOverview
    """
    return oh_event_svc.get_oh_event_role(subject, id)


@api.get("/{id}/get-help", tags=["Office Hours"])
def get_office_hours_help(
    id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> OfficeHourGetHelpOverview:
    """
    Gets information about getting help in office hours.

    Returns:
        OfficeHourGetHelpOverview
    """
    return oh_event_svc.get_office_hour_get_help_overview(subject, id)


@api.post("/{site_id}", tags=["Office Hours"])
def create_office_hours(
    site_id: int,
    oh: NewOfficeHours,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> OfficeHours:
    """
    Creates new office hours.

    Returns:
        OfficeHours
    """
    return oh_event_svc.create(subject, site_id, oh)


@api.post("/{site_id}/recurring", tags=["Office Hours"])
def create_recurring_office_hours(
    site_id: int,
    oh: NewOfficeHours,
    recur: NewOfficeHoursRecurrencePattern,
    subject: User = Depends(registered_user),
    oh_event_recurrence_svc: OfficeHoursRecurrenceService = Depends(),
) -> list[OfficeHours]:
    """
    Creates new office hours events based on a recurrence pattern.

    Returns:
        list[OfficeHours]
    """
    return oh_event_recurrence_svc.create_recurring(subject, site_id, oh, recur)


@api.put("/{site_id}", tags=["Office Hours"])
def update_office_hours(
    site_id: int,
    oh: OfficeHours,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> OfficeHours:
    """
    Updates new office hours.

    Returns:
        OfficeHours
    """
    return oh_event_svc.update(subject, site_id, oh)


@api.put("/{site_id}/recurring", tags=["Office Hours"])
def update_recurring_office_hours(
    site_id: int,
    oh: OfficeHours,
    recur: NewOfficeHoursRecurrencePattern,
    subject: User = Depends(registered_user),
    oh_event_recurrence_svc: OfficeHoursRecurrenceService = Depends(),
) -> list[OfficeHours]:
    """
    Updates an existing office hours event and future events in the recurrence pattern.
    """
    return oh_event_recurrence_svc.update_recurring(subject, site_id, oh, recur)


@api.delete("/{site_id}/{oh_id}", tags=["Office Hours"])
def delete_office_hours(
    site_id: int,
    oh_id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
):
    """
    Deletes office hours.
    """
    oh_event_svc.delete(subject, site_id, oh_id)


@api.delete("/{site_id}/{oh_id}/recurring", tags=["Office Hours"])
def delete_recurring_office_hours(
    site_id: int,
    oh_id: int,
    subject: User = Depends(registered_user),
    oh_event_recurrence_svc: OfficeHoursRecurrenceService = Depends(),
):
    """
    Deletes an existing office hours event and future events in the recurrence pattern.
    """
    oh_event_recurrence_svc.delete_recurring(subject, site_id, oh_id)


@api.get("/{site_id}/{oh_id}", tags=["Office Hours"])
def get_office_hours(
    site_id: int,
    oh_id: int,
    subject: User = Depends(registered_user),
    oh_event_svc: OfficeHoursService = Depends(),
) -> PrimaryOfficeHoursDetails:
    """
    Gets office hours.
    """
    return oh_event_svc.get(subject, site_id, oh_id)
