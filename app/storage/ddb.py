from typing import Optional

from app.env import feature_ddb_enabled
from app.models import PostIn, PostListItem, PostOut

WIP_IMAGE_URL = "https://www.pngkey.com/png/full/862-8620381_work-in-progress-sign.png"


class DynamoClient:
    """
    Mockad klient för att interagera med blogginlägg via en in-memory databas.
    """

    def __init__(self):
        self._posts = {
            "1": PostOut(
                id="1", title="Mockad post 1", image_url=WIP_IMAGE_URL, image_text="Bild 1"
            ),
            "2": PostOut(
                id="2", title="Mockad post 2", image_url=WIP_IMAGE_URL, image_text="Bild 2"
            ),
        }
        self._nextPostId = 3

    async def list_posts(self) -> list[PostOut]:
        """
        Returnerar lista med alla inlägg.
        """
        if not feature_ddb_enabled():
            return [PostListItem(id=post.id, title=post.title) for post in self._posts.values()]

        raise NotImplementedError

    async def get_post(self, post_id: str) -> Optional[PostOut]:
        """
        Hämta ett inlägg via dess ID.
        """
        if not feature_ddb_enabled():
            return self._posts.get(post_id)

        raise NotImplementedError

    async def create_post(self, post: PostIn) -> str:
        """
        Skapa ett nytt inlägg (mockat: lägg till i in-memory databas).
        """
        if not feature_ddb_enabled():
            new_id = str(self._nextPostId)
            self._nextPostId += 1
            self._posts[new_id] = PostOut(id=new_id, **post.dict())
            return new_id

        raise NotImplementedError

    async def delete_post(self, post_id: str) -> bool:
        """
        Ta bort ett inlägg via dess ID.
        """
        if not feature_ddb_enabled():
            return self._posts.pop(post_id, None) is not None

        raise NotImplementedError


# Skapa EN instans här, direkt i modulen
_dynamo_client = DynamoClient()


def get_dynamo_client() -> DynamoClient:
    """
    Returnerar alltid samma DynamoClient-instans, så att state bevaras
    över flera anrop.
    """
    return _dynamo_client
