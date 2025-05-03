"""
APIs for academics for office hour tickets.
"""

from ...models.office_hours.ticket_type import TicketType
from typing import Annotated, Literal
from datetime import datetime
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...database import db_session
from ...models.user import User
from ...models.academics.section_member import RosterRole
from ...models.academics.my_courses import (
    OfficeHourTicketOverview,
)
from ...models.office_hours.ticket import (
    TicketState,
    NewOfficeHoursTicket,
    OfficeHoursTicket,
)

from ...models.office_hours.ticket import Issue
from ...entities.office_hours.issue_entity import IssueEntity

from ..openai import OpenAIService, openai_client 
from ...models.openai_test_response import OpenAITestResponse

from ...entities.academics.section_entity import SectionEntity
from ...entities.office_hours import (
    CourseSiteEntity,
    OfficeHoursEntity,
    OfficeHoursTicketEntity,
)

from ...entities.office_hours.ticket_category_entity import TicketCategoryEntity

from ...entities.academics.section_member_entity import SectionMemberEntity
from ..exceptions import CoursePermissionException, ResourceNotFoundException
from ...entities.office_hours import user_created_tickets_table

__authors__ = ["Ajay Gandecha",
               "Simon Felt",
               "Daniel Ramsgard"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OfficeHourTicketService:
    """
    Service that performs all of the actions for office hour tickets.
    """

    def query_gpt(self, office_hours_ticket: OfficeHoursTicket) -> int:
        # get all issues that share the assignment id
        all_issues: list[IssueEntity] = self._session.query(IssueEntity).filter(IssueEntity.ticket_category_id == office_hours_ticket.ticket_category_id).all()

        # find the ticket_category
        ticket_category: int = self._session.query(TicketCategoryEntity).filter(TicketCategoryEntity.id == office_hours_ticket.ticket_category_id).one()

        # make requets to OpenAI API for new Issue or existing selection
        response: OpenAITestResponse = self._openai_svc.prompt(
            f"""
                Your task is to classify office hour tickets based on the specific problem the student needed help with. Each ticket is related to a broader context — for example, a course topic or assignment — but your job is to focus on the underlying conceptual issue, not just surface-level overlap.

                Context for this ticket: "{ticket_category}"

                Choose the best-fit category from this list:
                ({', '.join(issue.to_model().name for issue in all_issues)})

                When selecting a category:

                Prioritize conceptual similarity — this means the root problem or type of confusion should match, not just the subject or tool involved.

                Do not group tickets simply because they involve the same technology or topic. For example:

                "Docker not running due to daemon error" and "confusing Dockerfile syntax" should be separate — one is a runtime issue, the other is a configuration/syntax issue.

                "Resolving merge conflicts" and "merging divergent branches" share a conceptual focus on handling Git divergence and should be grouped.

                But "creating a Git branch" is setup-related and conceptually distinct — it should not be grouped with conflict resolution.

                If the issue does not clearly fit an existing category, create a new one. Be conservative: when in doubt, make a new category.

                Any new category must:

                Be 1–5 words long

                Be more specific than a general topic (e.g., use “Dockerfile syntax confusion” instead of “Docker Issues”)

                Be general enough that multiple similar tickets could use it

                Respond with:

                A boolean indicating whether a new category was created

                The best-fit category (either an existing one or your newly created one)

                Only use the ticket content and provided context — do not make unstated assumptions.
            """
            ,
            f"""
                Ticket: ({office_hours_ticket.description})
            """
            , OpenAITestResponse)
        
        # if there is a new Issue then store it and return issue id else just return the existing issue id
        if response.new_category:
            issue = IssueEntity(name=response.category, ticket_category_id=office_hours_ticket.ticket_category_id)
            self._session.add(issue)
            self._session.commit()
            issue_id = issue.id
        else:
            issue = self._session.query(IssueEntity).filter_by(name=response.category).one_or_none()
            if not issue:
                issue = IssueEntity(name=response.category, ticket_category_id=office_hours_ticket.ticket_category_id)
                self._session.add(issue)
                self._session.commit()
                issue_id = issue.id
            else:
                issue_id = issue.id

        return issue_id


    def __init__(self, openai_svc: Annotated[OpenAIService, Depends()], session: Session = Depends(db_session)):
        """
        Initializes the database session.
        """
        self._session = session        
        self._openai_svc = openai_svc

    def _to_oh_ticket_overview(
        self, ticket: OfficeHoursTicketEntity
    ) -> OfficeHourTicketOverview:
        return OfficeHourTicketOverview(
            id=ticket.id,
            created_at=ticket.created_at,
            called_at=ticket.called_at,
            state=ticket.state.to_string(),
            type=ticket.type.to_string(),
            description=ticket.description,
            creators=[creator.user.to_public_model() for creator in ticket.creators],
            caller=(ticket.caller.user.to_public_model() if ticket.caller else None),
        )

    def call_ticket(self, user: User, ticket_id: int) -> OfficeHourTicketOverview:
        """
        Calls a ticket in an office hour queue.

        Returns:
            OfficeHourTicketOverview
        """
        # Attempt to access the ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, ticket_id)

        if not ticket_entity:
            raise ResourceNotFoundException(f"Ticket not found with ID: {ticket_id}")

        if ticket_entity.state == TicketState.CALLED:
            raise CoursePermissionException("This ticket was already called!")

        if ticket_entity.state != TicketState.QUEUED:
            raise CoursePermissionException(
                "Cannot call a ticket that is not in the queue."
            )

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == ticket_entity.office_hours_id)
        )

        user_members = self._session.scalars(user_member_query).unique().all()

        # If the user is not a member of the looked up course, throw an error
        if len(user_members) == 0 or RosterRole.STUDENT in [
            member.member_role for member in user_members
        ]:
            raise CoursePermissionException(
                "Not allowed to call if a ticket if you are not a UTA, GTA, or instructor for."
            )

        # Call the ticket
        ticket_entity.caller_id = user_members[0].id
        ticket_entity.called_at = datetime.now()
        ticket_entity.state = TicketState.CALLED

        # Save changes
        self._session.commit()

        # Return the changed ticket
        return self._to_oh_ticket_overview(ticket_entity)

    def cancel_ticket(self, user: User, ticket_id: int) -> OfficeHourTicketOverview:
        """
        Cancels a ticket in an office hour queue.

        Returns:
            OfficeHourTicketOverview
        """
        # Attempt to access the ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, ticket_id)

        if not ticket_entity:
            raise ResourceNotFoundException(f"Ticket not found with ID: {ticket_id}")

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == ticket_entity.office_hours_id)
        )

        user_members = self._session.scalars(user_member_query).unique().all()
        user_member = user_members[0] if len(user_members) > 0 else None

        # If the user is not a member of the looked up course, throw an error
        if not user_member or (
            user_member.member_role == RosterRole.STUDENT
            and user_member.id not in [creator.id for creator in ticket_entity.creators]
        ):
            raise CoursePermissionException(
                "Not allowed to cancel if a ticket if you are not a UTA, GTA, or instructor for it, or you did not open it."
            )

        # Cancel the ticket
        ticket_entity.state = TicketState.CANCELED

        # Save changes
        self._session.commit()

        # Return the changed ticket
        return self._to_oh_ticket_overview(ticket_entity)

    def close_ticket(self, user: User, ticket_id: int) -> OfficeHourTicketOverview:
        """
        Closes a ticket in an office hour queue.

        Returns:
            OfficeHourTicketOverview
        """
        # Attempt to access the ticket
        ticket_entity = self._session.get(OfficeHoursTicketEntity, ticket_id)

        if not ticket_entity:
            raise ResourceNotFoundException(f"Ticket not found with ID: {ticket_id}")

        if ticket_entity.state != TicketState.CALLED:
            raise CoursePermissionException(
                "Cannot close a ticket that has not been called."
            )
        
        # query the AI to get selection and set the issue id
        issue_id: int = self.query_gpt(ticket_entity.to_model())
        ticket_entity.issue_id = issue_id

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id == user.id)
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == ticket_entity.office_hours_id)
        )

        user_members = self._session.scalars(user_member_query).unique().all()

        # If the user is not a member of the looked up course, throw an error
        if len(user_members) == 0 or RosterRole.STUDENT in [
            member.member_role for member in user_members
        ]:
            raise CoursePermissionException(
                "Not allowed to call if a ticket if you are not a UTA, GTA, or instructor for."
            )

        # Close the ticket
        ticket_entity.closed_at = datetime.now()
        ticket_entity.state = TicketState.CLOSED        

        # Save changes
        self._session.commit()

        # Return the changed ticket
        return self._to_oh_ticket_overview(ticket_entity)
    
    def _create_or_store_assignment_concept(self, assignment_concept_name: str, category: TicketType, course_site_id: int):        
        # attempt to find the concept or assignment based on name
        new_item = self._session.query(TicketCategoryEntity).filter(TicketCategoryEntity.name == assignment_concept_name).one_or_none()

        # store if doesn't exist yet and return the id
        if not new_item:
            ticket_cat = TicketCategoryEntity(name=assignment_concept_name, category=category, course_site_id=course_site_id)
            self._session.add(ticket_cat)
            self._session.commit()
            id_to_ret = ticket_cat.id
        else:
            id_to_ret = new_item.id

        return id_to_ret

    def create_ticket(
        self, user: User, ticket: NewOfficeHoursTicket, course_id: int
    ) -> OfficeHourTicketOverview:
        """
        Creates a new office hours ticket.

        Args:
            subject (User): A valid User model representing the currently logged-in user.
            ticket (OfficeHoursTicket): OfficeHoursTicket object to add to the table.

        Returns:
            OfficeHoursTicketDetails: The newly created OfficeHoursTicket object.

        Raises:
            PermissionError: If the logged-in user is not a section member student.

        """
        # initially create a concept or assignment
        ticket_category_id_ret = self._create_or_store_assignment_concept(ticket.assignment_concept_name, ticket.type, course_id)


        # Find the IDs of the creators of the ticket
        creator_ids = [user.id]
        # TODO: Reimplement group tickets
        # list(set([creator.id for creator in oh_ticket_draft.creators] + [user.id]))

        # Create query off of the member query for just the members matching
        # with the current user (used to determine permissions)
        user_member_query = (
            select(SectionMemberEntity)
            .where(SectionMemberEntity.user_id.in_(creator_ids))
            .join(SectionEntity)
            .join(CourseSiteEntity)
            .join(OfficeHoursEntity)
            .where(OfficeHoursEntity.id == ticket.office_hours_id)
        )

        user_members = self._session.scalars(user_member_query).unique().all()

        user_member_ids = [user_member.user_id for user_member in user_members]

        for creator_id in creator_ids:
            if creator_id not in user_member_ids:
                raise CoursePermissionException(
                    "Not allowed to create a ticket if you are not in the course."
                )

        for user_member in user_members:
            # If the user is not a member of the looked up course, throw an error
            if not user_member or user_member.member_role != RosterRole.STUDENT:
                raise CoursePermissionException(
                    "Not allowed to create a ticket if you are not a student."
                )

        # Check if the user already has a ticket in a queue
        queued_query = (
            select(OfficeHoursTicketEntity)
            .join(OfficeHoursEntity)
            .join(user_created_tickets_table)
            .join(SectionMemberEntity)
            .where(OfficeHoursEntity.id == ticket.office_hours_id)
            .where(OfficeHoursTicketEntity.state == TicketState.QUEUED)
            .where(SectionMemberEntity.user_id == user.id)
        )
        queued_tickets_entities = self._session.scalars(queued_query).all()

        if len(queued_tickets_entities) > 0:
            raise CoursePermissionException(
                "You cannot create multiple tickets at once."
            )

        # Create entity
        ticket.ticket_category_id = ticket_category_id_ret
        oh_ticket_entity = OfficeHoursTicketEntity.from_new_model(ticket)        

        # Add new object to table and commit changes
        self._session.add(oh_ticket_entity)

        # Commit so can get ticket id
        self._session.commit()

        # Now, Associate ticket with Creators
        for section_member_entity in user_members:
            self._session.execute(
                user_created_tickets_table.insert().values(
                    {
                        "ticket_id": oh_ticket_entity.id,
                        "member_id": section_member_entity.id,
                    }
                )
            )

        self._session.commit()

        # Return details model
        return self._to_oh_ticket_overview(oh_ticket_entity)
