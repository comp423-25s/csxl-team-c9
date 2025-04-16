from pydantic import BaseModel


class OpenAITestResponse(BaseModel):
    """Response model for OpenAI test endpoint."""

    new_category: bool
    category: str
