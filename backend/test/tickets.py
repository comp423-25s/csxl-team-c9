"""Testing the services for the tickets folder."""

from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import pytest
from models import AssignmentConcept  # no work why
from entities.office_hours.issue_entity import IssueEntity
from entities.office_hours.ticket_entity import OfficeHoursTicketEntity
from services.office_hours.office_hours import OfficeHoursService
from entities.office_hours.ticket_category_entity import TicketCategoryEntity
from main import app


@pytest.fixture
def mock_oh_service():
    mock_service = MagicMock(OfficeHoursService)
    app.dependency_overrides[OfficeHoursService] = (
        lambda: mock_service
    )  # override dependency injection in OHS
    yield mock_service  # return to test
    app.dependency_overrides = {}  # Reset after test


@pytest.fixture
def mock_session():
    """Fixture to mock the SQLAlchemy session."""
    mock_session = MagicMock()
    return mock_session


# Tests Below


def test_get_all_assignments_concepts(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    # Mock TicketCategoryEntity
    mock_category = MagicMock(TicketCategoryEntity)
    mock_category.id = 1
    mock_category.course_site_id = 123
    mock_category.category = "ASSIGNMENT_HELP"
    mock_category.to_model.return_value = AssignmentConcept(
        id=1,
        num_issues=1,  # This would be derived based on the number of related issues in the database
        category="ASSIGNMENT_HELP",
        course_site_id=1001,  # Simulating the course_site_id associated with this category
    )

    # Mock the database query to return mock_category
    mock_session.query.return_value.filter.return_value.all.return_value = [
        mock_category
    ]

    # Mock IssueEntity query
    mock_session.query.return_value.filter.return_value.all.return_value = []

    # Set mock session to the service
    mock_oh_service._session = mock_session

    # Test method
    result = mock_oh_service.get_all_assignments_concepts(123)

    assert "assignments" in result
    assert len(result["assignments"]) == 1
    assert result["assignments"][0]["category"] == "ASSIGNMENT_HELP"


# Test for `get_all_issues`
def test_get_all_issues(mock_oh_service: OfficeHoursService, mock_session: MagicMock):
    # Mock IssueEntity
    mock_issue = MagicMock(IssueEntity)
    mock_issue.id = 1
    mock_issue.ticket_category_id = "asg123"
    mock_issue.to_model.return_value = {"id": 1, "num_tickets": 0}

    # Mock the database query to return mock_issue
    mock_session.query.return_value.filter.return_value.all.return_value = [mock_issue]

    # Mock OfficeHoursTicketEntity query
    mock_session.query.return_value.filter.return_value.all.return_value = []

    # Set mock session to the service
    mock_oh_service._session = mock_session

    # Test method
    result = mock_oh_service.get_all_issues("asg123")

    assert "issues" in result
    assert len(result["issues"]) == 1
    assert result["issues"][0]["id"] == 1


# Test for `get_all_tickets_by_issue`
def test_get_all_tickets_by_issue(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    # Mock OfficeHoursTicketEntity
    mock_ticket = MagicMock(OfficeHoursTicketEntity)
    mock_ticket.id = 1
    mock_ticket.issue_id = "issue123"
    mock_ticket.to_model.return_value = {"id": 1, "status": "open"}

    # Mock the database query to return mock_ticket
    mock_session.query.return_value.filter.return_value.all.return_value = [mock_ticket]

    # Set mock session to the service
    mock_oh_service._session = mock_session

    # Test method
    result = mock_oh_service.get_all_tickets_by_issue("issue123")

    assert "tickets" in result
    assert len(result["tickets"]) == 1
    assert result["tickets"][0]["id"] == 1


# Test when no categories found for `get_all_assignments_concepts`
def test_get_all_assignments_concepts_empty(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    # Mock empty data from database
    mock_session.query.return_value.filter.return_value.all.return_value = []

    # Set mock session to the service
    mock_oh_service._session = mock_session

    # Test method
    result = mock_oh_service.get_all_assignments_concepts(123)

    assert result["assignments"] == []
    assert result["concepts"] == []


# Test when no issues found for `get_all_issues`
def test_get_all_issues_empty(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    # Mock empty data from database
    mock_session.query.return_value.filter.return_value.all.return_value = []

    # Set mock session to the service
    mock_oh_service._session = mock_session

    # Test method
    result = mock_oh_service.get_all_issues("asg123")

    assert result["issues"] == []


# Test when no tickets found for `get_all_tickets_by_issue`
def test_get_all_tickets_by_issue_empty(
    mock_oh_service: OfficeHoursService, mock_session: MagicMock
):
    # Mock empty data from database
    mock_session.query.return_value.filter.return_value.all.return_value = []

    # Set mock session to the service
    mock_oh_service._session = mock_session

    # Test method
    result = mock_oh_service.get_all_tickets_by_issue("issue123")
    assert result["tickets"] == []
