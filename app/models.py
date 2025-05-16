import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


class PostListItem(BaseModel):
    id: str
    title: str


class PostIn(BaseModel):
    """
    Modell för indata när man skapar ett inlägg.
    """

    title: str = Field(..., min_length=1, max_length=200)
    image_url: str = Field(None, description="URL till inläggets bild")
    image_text: str = Field(..., min_length=1)


class PostOut(PostIn):
    """
    Modell för utskrift/serialisering av ett inlägg.
    Ärver title, image_text, image_url från PostIn.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unikt ID (UUID4)")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Tidpunkt då inlägget skapades (UTC)",
    )

    model_config = ConfigDict(
        from_attributes=True,
    )
