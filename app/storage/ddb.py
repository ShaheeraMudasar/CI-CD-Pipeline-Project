from datetime import datetime, timezone
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from app.env import feature_ddb_enabled, get_aws_credentials
from app.models import PostIn, PostListItem, PostOut

TABLE_NAME = "DevOps1_Posts"


class DynamoClient:
    """
    DynamoDB klient för att interagera med blogginlägg.
    """

    def __init__(self):
        self._dynamodb = boto3.resource("dynamodb", **get_aws_credentials())
        self._table = self._dynamodb.Table(TABLE_NAME)

    def list_posts(self) -> list[PostListItem]:
        """
        Returnerar lista med alla inlägg.
        """
        response = self._table.scan()
        items = response.get("Items", [])
        # Sortera items på created_at i stigande ordning (äldst först)
        items_sorted = sorted(items, key=lambda x: x.get("created_at", ""))
        posts = []
        for item in items_sorted:
            posts.append(PostListItem(id=item["id"], title=item["title"]))
        return posts

    def get_post(self, post_id: str) -> Optional[PostOut]:
        """
        Hämta ett inlägg via dess ID.
        """
        try:
            response = self._table.get_item(Key={"id": post_id})
        except ClientError:
            return None
        item = response.get("Item")
        if not item:
            return None
        return PostOut(
            id=item["id"],
            title=item["title"],
            image_url=item.get("image_url"),
            image_text=item.get("image_text"),
            created_at=datetime.fromisoformat(item["created_at"]),
        )

    def create_post(self, post: PostIn) -> str:
        """
        Skapa ett nytt inlägg i DynamoDB.
        """
        now = datetime.now(timezone.utc)
        post_id = now.strftime("%Y%m%d%H%M%S%f")  # exempel: 20250520153045012345
        now_iso = now.isoformat()  # exempel: 2025-05-21T14:33:07.123456+00:00
        item = {
            "id": post_id,
            "title": post.title,
            "image_url": post.image_url,
            "image_text": post.image_text,
            "created_at": now_iso,
        }
        self._table.put_item(Item=item)
        return post_id

    def delete_post(self, post_id: str) -> bool:
        """
        Ta bort ett inlägg via dess ID.
        """
        try:
            response = self._table.delete_item(
                Key={"id": post_id},
                ConditionExpression="attribute_exists(id)",
            )
            _ = response  # 👈 This tells the linter: "I know it's unused — on purpose"
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return False
            raise


# en enda instans som återanvänds
_dynamo_client = None


def get_dynamo_client() -> DynamoClient:
    """
    Returnerar DynamoClient-instans. Om mock är aktiverat, returnera mock-klienten.
    """
    if feature_ddb_enabled():
        global _dynamo_client
        if _dynamo_client is None:
            _dynamo_client = DynamoClient()
        return _dynamo_client
    from app.storage.ddb_mock import get_mock_dynamo_client

    return get_mock_dynamo_client()
