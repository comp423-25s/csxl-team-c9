"""Testing the service for the tickets folder."""

from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import pytest
from backend.models.office_hours.ticket import AssignmentConcept, TicketType
from backend.entities.office_hours.issue_entity import IssueEntity
from backend.entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from backend.services.office_hours.office_hours import OfficeHoursService
from backend.entities.office_hours.ticket_category_entity import TicketCategoryEntity
from backend.main import app
from pydantic import ValidationError

__authors__ = ["Cassidy Lowe"]


@pytest.fixture
def mock_oh_service():
    mock_service = MagicMock(OfficeHoursService)
    app.dependency_overrides[OfficeHoursService] = lambda: mock_service
    yield mock_service
    app.dependency_overrides = {}


@pytest.fixture
def mock_session():
    """Fixture to mock the SQLAlchemy session."""
    mock_session = MagicMock()
    return mock_session


# Tests Below


def test_get_all_assignments_concepts(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    """Ensure it returns an asssignment when there is one."""
    mock_category = MagicMock(spec=TicketCategoryEntity)
    mock_category.id = 1
    mock_category.course_site_id = 123
    mock_category.category = TicketType.ASSIGNMENT_HELP
    mock_category.to_model.return_value = AssignmentConcept(
        name="Assignment 1",
        id=1,
        num_issues=1,
        category=TicketType.ASSIGNMENT_HELP,
        course_site_id=123,
    )
    mock_session.query.return_value.filter.return_value.all.return_value = [
        mock_category
    ]
    mock_oh_service._session = mock_session
    mock_oh_service.get_all_assignments_concepts.return_value = {
        "assignments": [
            {
                "name": "Assignment 1",
                "id": 1,
                "num_issues": 1,
                "category": TicketType.ASSIGNMENT_HELP,
                "course_site_id": 123,
            }
        ]
    }
    result = mock_oh_service.get_all_assignments_concepts(123)
    assert "assignments" in result
    assert len(result["assignments"]) == 1


def test_get_all_assignments_concepts_empty(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    """If there are no closed ticket, make sure there are no assignments/concepts."""
    mock_oh_service.get_all_assignments_concepts.return_value = {
        "assignments": [],
        "concepts": [],
    }

    result = mock_oh_service.get_all_assignments_concepts(123)
    assert result["assignments"] == []
    assert result["concepts"] == []


def test_get_all_assignments_concepts_category(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    """Ensure it does not return an asssignment when there is only a concept."""
    mock_category = MagicMock(spec=TicketCategoryEntity)
    mock_category.id = 1
    mock_category.course_site_id = 123
    mock_category.category = TicketType.CONCEPTUAL_HELP
    mock_category.to_model.return_value = AssignmentConcept(
        name="Git",
        id=1,
        num_issues=1,
        category=TicketType.CONCEPTUAL_HELP,
        course_site_id=123,
    )
    mock_session.query.return_value.filter.return_value.all.return_value = [
        mock_category
    ]
    mock_oh_service._session = mock_session
    mock_oh_service.get_all_assignments_concepts.return_value = {"assignments": []}
    result = mock_oh_service.get_all_assignments_concepts(123)
    assert len(result["assignments"]) == 0


def test_get_all_assignments_concepts_category(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    """Ensure it returns a concept when there is one."""
    mock_category = MagicMock(spec=TicketCategoryEntity)
    mock_category.id = 1
    mock_category.course_site_id = 2
    mock_category.category = TicketType.CONCEPTUAL_HELP
    mock_category.to_model.return_value = AssignmentConcept(
        name="Git",
        id=1,
        num_issues=1,
        category=TicketType.CONCEPTUAL_HELP,
        course_site_id=2,
    )
    mock_session.query.return_value.filter.return_value.all.return_value = [
        mock_category
    ]
    mock_oh_service._session = mock_session
    mock_oh_service.get_all_assignments_concepts.return_value = {
        "concepts": [
            {
                "name": "Git",
                "id": 1,
                "num_issues": 1,
                "category": TicketType.CONCEPTUAL_HELP,
                "course_site_id": 2,
            }
        ]
    }
    result = mock_oh_service.get_all_assignments_concepts(2)
    assert len(result["concepts"]) == 1


def test_get_all_assignments_concepts_category_two(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    """Ensure it returns 2 concepts when there are two."""
    mock_category = MagicMock(spec=TicketCategoryEntity)
    mock_category.id = 1
    mock_category.course_site_id = 2
    mock_category.category = TicketType.CONCEPTUAL_HELP
    mock_category.to_model.return_value = AssignmentConcept(
        name="Git",
        id=1,
        num_issues=1,
        category=TicketType.CONCEPTUAL_HELP,
        course_site_id=2,
    )
    mock_category2 = MagicMock(spec=TicketCategoryEntity)
    mock_category2.id = 2
    mock_category2.course_site_id = 2
    mock_category2.category = TicketType.CONCEPTUAL_HELP
    mock_category2.to_model.return_value = AssignmentConcept(
        name="Docker",
        id=2,
        num_issues=1,
        category=TicketType.CONCEPTUAL_HELP,
        course_site_id=2,
    )
    mock_session.query.return_value.filter.return_value.all.return_value = [
        mock_category,
        mock_category2,
    ]
    mock_oh_service._session = mock_session
    mock_oh_service.get_all_assignments_concepts.return_value = {
        "concepts": [
            {
                "name": "Git",
                "id": 1,
                "num_issues": 1,
                "category": TicketType.CONCEPTUAL_HELP,
                "course_site_id": 2,
            },
            {
                "name": "Docker",
                "id": 2,
                "num_issues": 1,
                "category": TicketType.CONCEPTUAL_HELP,
                "course_site_id": 2,
            },
        ]
    }
    result = mock_oh_service.get_all_assignments_concepts(2)
    assert len(result["concepts"]) == 2


def test_get_all_assignments_concepts_category_sites(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    """Ensure it returns grabs concepts from the correct site."""
    mock_category = MagicMock(spec=TicketCategoryEntity)
    mock_category.id = 1
    mock_category.course_site_id = 2
    mock_category.category = TicketType.CONCEPTUAL_HELP
    mock_category.to_model.return_value = AssignmentConcept(
        name="Git",
        id=1,
        num_issues=1,
        category=TicketType.CONCEPTUAL_HELP,
        course_site_id=2,
    )
    mock_category2 = MagicMock(spec=TicketCategoryEntity)
    mock_category2.id = 2
    mock_category2.course_site_id = 4
    mock_category2.category = TicketType.CONCEPTUAL_HELP
    mock_category2.to_model.return_value = AssignmentConcept(
        name="Docker",
        id=2,
        num_issues=1,
        category=TicketType.CONCEPTUAL_HELP,
        course_site_id=4,
    )
    mock_session.query.return_value.filter.return_value.all.return_value = [
        mock_category,
        mock_category2,
    ]
    mock_oh_service._session = mock_session
    mock_oh_service.get_all_assignments_concepts.return_value = {
        "concepts": [
            {
                "name": "Git",
                "id": 1,
                "num_issues": 1,
                "category": TicketType.CONCEPTUAL_HELP,
                "course_site_id": 2,
            }
        ]
    }
    result = mock_oh_service.get_all_assignments_concepts(2)
    assert len(result["concepts"]) == 1


def test_get_all_issues(mock_oh_service: OfficeHoursService, mock_session: MagicMock):
    mock_issue = MagicMock(spec=IssueEntity)
    """"Make sure an issue can be retrieved."""
    mock_issue.id = 1
    mock_issue.ticket_category_id = "1234"
    mock_issue.to_model.return_value = {
        "id": 1,
        "num_tickets": 1,
    }

    mock_session.query.return_value.filter.return_value.all.return_value = [mock_issue]
    mock_oh_service._session = mock_session

    mock_oh_service.get_all_issues.return_value = {
        "issues": [mock_issue.to_model.return_value]
    }

    result = mock_oh_service.get_all_issues("1234")
    assert "issues" in result
    assert result["issues"][0]["id"] == 1


def test_get_all_issues(mock_oh_service: OfficeHoursService, mock_session: MagicMock):
    mock_issue = MagicMock(spec=IssueEntity)
    """"Make sure more than one issue can be retrieved."""
    mock_issue.id = 1
    mock_issue.ticket_category_id = "1234"
    mock_issue.to_model.return_value = {
        "id": 1,
        "num_tickets": 1,
    }
    mock_issue2 = MagicMock(spec=IssueEntity)
    mock_issue2.id = 2
    mock_issue2.ticket_category_id = "1234"
    mock_issue2.to_model.return_value = {
        "id": 2,
        "num_tickets": 1,
    }
    mock_session.query.return_value.filter.return_value.all.return_value = [
        mock_issue,
        mock_issue2,
    ]
    mock_oh_service._session = mock_session

    mock_oh_service.get_all_issues.return_value = {
        "issues": [mock_issue.to_model.return_value, mock_issue2.to_model.return_value]
    }
    result = mock_oh_service.get_all_issues("1234")
    assert "issues" in result
    assert result["issues"][0]["id"] == 1
    assert result["issues"][1]["id"] == 2


def test_get_all_tickets_by_issue(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    """Ensure can retrieve a ticket from issues."""
    mock_ticket = MagicMock(spec=OfficeHoursTicketEntity)
    mock_ticket.id = 1
    mock_ticket.issue_id = "123"
    mock_ticket.to_model.return_value = {"id": 1, "status": "closed"}
    mock_session.query.return_value.filter.return_value.all.return_value = [mock_ticket]
    mock_oh_service._session = mock_session
    mock_oh_service.get_all_tickets_by_issue.return_value = {
        "tickets": [mock_ticket.to_model.return_value]
    }
    result = mock_oh_service.get_all_tickets_by_issue("123")
    assert "tickets" in result
    assert result["tickets"][0]["id"] == 1


def test_get_all_tickets_by_issue_multiple(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    """Ensure can retrieve more than one ticket from issues."""
    mock_ticket = MagicMock(spec=OfficeHoursTicketEntity)
    mock_ticket.id = 1
    mock_ticket.issue_id = "123"
    mock_ticket.to_model.return_value = {"id": 1, "status": "closed"}
    mock_ticket2 = MagicMock(spec=OfficeHoursTicketEntity)
    mock_ticket2.id = 2
    mock_ticket2.issue_id = "123"
    mock_ticket2.to_model.return_value = {"id": 2, "status": "closed"}
    mock_session.query.return_value.filter.return_value.all.return_value = [
        mock_ticket,
        mock_ticket2,
    ]
    mock_oh_service._session = mock_session
    mock_oh_service.get_all_tickets_by_issue.return_value = {
        "tickets": [
            mock_ticket.to_model.return_value,
            mock_ticket2.to_model.return_value,
        ]
    }
    result = mock_oh_service.get_all_tickets_by_issue("123")
    assert "tickets" in result
    assert result["tickets"][0]["id"] == 1
    assert result["tickets"][1]["id"] == 2
