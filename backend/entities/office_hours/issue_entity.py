"""Definition of SQLAlchemy table-backed object mapping entity for Office Hour tickets."""

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ...models.office_hours.ticket import Issue


from ..entity_base import EntityBase
from typing import Self

__authors__ = [
    "Simon Augustus Felt (GoValuate)",
    "Daniel William Ramsgard (GoValuate)"
]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class IssueEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `OfficeHoursTicket` table"""

    # Name for the events table in the PostgreSQL database
    __tablename__ = "issue"

    # Unique id for OfficeHoursTicket
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Name of issue
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Assignment id that issue is mapped to
    ticket_category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ticket_category.id"),  # <- foreign key reference
        nullable=True
    )

    # Number of tickets
    # num_tickets: Mapped[int] = mapped_column(Integer, nullable=False) -> this is derived

    @classmethod
    def from_model(cls, model: Issue) -> Self:
        """
        Class method that converts an `OfficeHoursTicket` model into a `OfficeHoursTicketEntity`

        Parameters:
            - model (OfficeHoursTicket): Model to convert into an entity
        Returns:
            OfficeHoursTicketEntity: Entity created from model
        """
        return cls(
            id=model.id,
            name=model.name,
            ticket_category_id=model.ticket_category_id
        )

    def to_model(self) -> Issue:
        """
        Converts a `OfficeHoursTicketEntity` object into a `OfficeHoursTicket` model object

        Returns:
            OfficeHoursTicket: `OfficeHoursTicket` object from the entity
        """
        return Issue(
            id=self.id,
            name=self.name,
            ticket_category_id=self.ticket_category_id
        )
